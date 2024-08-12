from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import os
from google_auth_oauthlib.flow import Flow
from django.conf import settings

User = get_user_model()

def entry(request):
    # Handle the entry point for login and signup
    if request.method == 'POST':
        # User signup process
        if 'signup' in request.POST:
            # Collect user data from form
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Check if the email is already registered
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered!!")
                return redirect('entry')
            
            # Create a new user and save to the database
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            new_user.is_verified = False  # Mark the user as unverified initially
            
            # Prepare and send the activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            send_email_with_gmail_api(to_email=new_user.email, subject=mail_subject, message_text=message)
            
            messages.info(request, 'Please verify your email address to complete the registration')
            return redirect('entry')
        
        # User login process
        if 'signin' in request.POST:
            # Collect login credentials from form
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Authenticate user
            user = authenticate(email=email, password=password)
            if user is None:
                messages.info(request, "Incorrect login credentials!")
                return redirect('entry')
            else:
                # Log the user in and redirect to dashboard
                login(request, user)
                return redirect('dashboard')

    # Render login page for GET request
    return render(request, 'login.html')

def activate(request, uidb64, token):
    # Activate the user's account after verifying the email link
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return render(request, 'succ_reg.html')
    else:
        return HttpResponse('Activation link is invalid!')

def send_email_with_gmail_api(to_email, subject, message_text):
    """Send an email using the Gmail API."""
    # Load credentials from the token file
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])
    
    if not creds or not creds.valid:
        print("No valid credentials provided for Gmail API.")
        return
    
    service = build('gmail', 'v1', credentials=creds)
    
    # Create and send the email message
    message = MIMEText(message_text, 'html')
    message['to'] = to_email
    message['from'] = 'your_email@gmail.com'  # Replace with your actual email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    try:
        service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
    except Exception as error:
        print(f"An error occurred: {error}")

# OAuth2 flow for Google authentication and authorization to use Gmail for sending emails
def google_authenticate(request):
    # Initiate OAuth flow
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        redirect_uri=f'{settings.SITE_URL}/google_callback/'
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    request.session['state'] = state
    return redirect(authorization_url)

def google_callback(request):
    # Callback for Google OAuth flow
    state = request.session.get('state')
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        state=state,
        redirect_uri=f'{settings.SITE_URL}/google_callback/'
    )
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    credentials = flow.credentials
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())
    
    return HttpResponse('Google account successfully connected. You can now use the Gmail API to send emails.')
