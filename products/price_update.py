import time
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware
from .models import Products, PriceUpdate, TrackingStatus
from .utils import flipkart_scrapper, ebay_scrapper
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_most_recent_update_date():
    # Attempt to find the most recent price update from the database
    last_update = PriceUpdate.objects.all().order_by('-dates').first()
    if last_update:
        # If an update exists, return the date of the last update
        return last_update.dates
    else:
        # If there's no update, return a date far in the past to ensure a new update is processed
        return make_aware(datetime.now() - timedelta(days=365)).date()
    
# Function to send email using Gmail API
def send_email_notification(email_address, product_name, old_price, new_price):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEMultipart()
        message['to'] = email_address
        message['subject'] = 'Price Drop Alert!'
        body = f"""
        Hi there,

        Great news! The price of {product_name} has dropped by more than 25%.
        Previous Price: {old_price}
        New Price: {new_price}

        Check it out on the website now!
        """
        message.attach(MIMEText(body, 'plain'))
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw_message}
        send_message = service.users().messages().send(userId='me', body=message_body).execute()
        print(f"Email sent to {email_address}: {send_message}")
    except HttpError as error:
        print(f'An error occurred: {error}')

def update_all_products():
    while True:  # Start an infinite loop to continuously check for price updates
        # Check the tracking status to see if updates should be processed
        tracking_status = TrackingStatus.objects.first()  # Assumes a single tracking status entry
        if not tracking_status or not tracking_status.is_tracking:
            # Exit loop if tracking is not enabled or not configured
            print("Tracking stopped or not configured. Exiting the loop.")
            break

        # Tracking is active; proceed with updating prices
        current_date = now().date()
        last_checked_date = get_most_recent_update_date()
        # Log the date checking process
        print(f"Current Date: {current_date}, Last Checked Date: {last_checked_date}")

        if current_date > last_checked_date:
            # Only proceed if the current date is after the last checked date
            products = Products.objects.all()
            for product in products:
                # Determine which scraper to use based on the product's URL
                if "flipkart" in product.product_url:
                    scrape_data = flipkart_scrapper(product.product_url)
                elif "ebay" in product.product_url:
                    scrape_data = ebay_scrapper(product.product_url)
                else:
                    # Skip if no suitable scraper is found
                    print(f"No suitable scraper found for {product.product_url}")
                    continue

                # If scraping is successful and a price is found, update the product's price
                if scrape_data and 'price' in scrape_data and scrape_data['price'] is not None:
                    PriceUpdate.objects.create(
                        product=product,
                        dates=current_date,
                        price=scrape_data['price']
                        
                    )
                    print(f"Updated price for {product.product_name} to {scrape_data['price']}")
                    
                else:
                    # Log failure if scraping didn't return a price
                    print(f"Failed to fetch price for {product.product_name}")
                
                try:
                    # Try to get the previous price update for the product
                    previous_update = PriceUpdate.objects.filter(product=product).order_by('-dates').exclude(dates=current_date).first()
                    if previous_update:
                        price_drop_percentage = ((previous_update.price - scrape_data['price']) / previous_update.price) * 100
                        if price_drop_percentage >= 25:
                            # If the price dropped by 25% or more, send an email notification
                            for user in product.user.all():
                                send_email_notification(user.email, product.product_name, previous_update.price, scrape_data['price'])
                                print(f"Email sent to {user.email} about a price drop in {product.product_name}")
                except Exception as e:
                    print(f"Error checking price drop or sending email for {product.product_name}: {str(e)}")

            print("All products updated. Waiting for the next day to check again.")
        else:
            # If the current date hasn't changed since the last check, wait for 4 hours before trying again
            print("No date change detected. Next check in 4 hours.")
        
        time.sleep(14400)  # Sleep for 4 hours (14400 seconds) before the next iteration
