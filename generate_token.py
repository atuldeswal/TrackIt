from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope: Modify according to your needs
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8000)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    print("Gmail service created successfully with your credentials")

if __name__ == '__main__':
    main()
