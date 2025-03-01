# TrackIt - E-commerce Price Tracker

TrackIt is a web application designed to empower consumers with transparent price information across e-commerce platforms. It tracks product prices from major e-commerce sites, helping users verify discount claims, compare prices in real-time, and make informed purchasing decisions.

## 🚀 Features

- **Price Tracking**: Monitor historical price trends of products from Flipkart and eBay
- **Price Comparison**: Compare prices of the same product across different e-commerce platforms in real-time
- **Deal Verification**: Verify the authenticity of discount claims during sales periods
- **Personalized Tracking List**: Add products to your personal tracking list with a centralized view
- **Notification System**: Receive alerts when prices drop below a set threshold
- **Ethical Web Scraping**: Gather real-time price data without compromising target websites
- **User Accounts**: Create and manage your account with email verification

## 💻 Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Web Scraping**: BeautifulSoup4
- **Email Notifications**: Google's Gmail API

## 📋 Prerequisites

- Python 3.x
- Django
- BeautifulSoup4
- Requests
- Other dependencies listed in requirements.txt

## 🔧 Installation

1. Clone the repository:
   ```
   git clone https://github.com/atuldeswal/TrackIt.git
   cd TrackIt
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (Admin):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## 🔑 Usage

1. **Register an Account**: Create a new account with your email address
2. **Add Products**: Copy product URLs from Flipkart or eBay and add them to your tracking list
3. **View Price History**: Monitor price changes over time with visual representation
4. **Set Price Alerts**: Configure notifications for when prices drop below your desired threshold
5. **Compare Prices**: See prices across different platforms to find the best deal

## 🏗️ Project Structure

Based on the provided file structure:

```
trackit/
├── accounts/                # User authentication and management
│   ├── __pycache__/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── manager.py
│   ├── models.py
│   ├── tests.py
│   ├── tokens.py
│   └── views.py
├── products/               # Product tracking functionality
│   ├── __pycache__/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── price_update.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── static/                 # Static files (CSS, JS, images)
│   ├── assets/
│   ├── js/
│   └── staticfiles/
├── templates/              # HTML templates
│   ├── admin/
│   ├── acc_active_email.html
│   ├── dashboard.html
│   ├── login.html
│   └── succ_reg.html
└── trackit/                # Main project configuration
    ├── __pycache__/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🛡️ Security Features

- Secure user authentication and authorization
- Password hashing
- Email verification for account creation
- Protection against common web vulnerabilities

## 🔄 Automated Price Updates

TrackIt includes a background process that regularly checks for price changes across all tracked products. The system automatically updates the database and sends notifications to users when significant price drops are detected.

## 🌐 Supported E-commerce Platforms

- Flipkart
- eBay

*Additional platforms planned for future updates*

## 👨‍💻 Developer Information

This project was developed as part my MCA final semester project.

## 🔮 Future Enhancements

- Support for additional e-commerce platforms (Amazon, Walmart, etc.)
- Mobile application development
- Advanced analytics and price prediction
- Browser extension for one-click tracking
- Social sharing features for great deals

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

For any questions or suggestions, please reach out to [hunnydeswal2@gmail.com](mailto:hunnydeswal2@gmail.com)
