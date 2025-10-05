# Personal Expense Tracker

A comprehensive web-based expense tracking application built with Flask and SQLite. This application helps you manage your personal finances by tracking expenses, categorizing spending, and generating detailed reports.

## 🚀 Features

### Must-Have Features ✅
- **Add Expenses**: Record new expenses with amount, date, description, and category
- **View Expenses**: Browse all expenses with pagination and filtering
- **Update Expenses**: Edit existing expense details
- **Delete Expenses**: Remove expenses with confirmation
- **Data Persistence**: SQLite database for reliable data storage
- **Input Validation**: Comprehensive validation and error handling
- **Responsive UI**: Modern, mobile-friendly web interface

### Optional Features ✨
- **Category Management**: Create and manage custom expense categories
- **Monthly Recurring Expenses**: Toggle to mark expenses as monthly recurring
- **Advanced Dashboard**: Real-time statistics with dynamic filtering
- **Smart Filtering**: Multi-select category filtering and date range selection
- **PDF Export**: Download professional dashboard reports as PDF
- **Summary Reports**: Total spending, category breakdown, monthly summaries
- **Responsive Design**: Mobile-first design with Bootstrap 5
- **Real-time Updates**: Dynamic dashboard updates without page reload

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5.1.3, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.0.0
- **Dependencies**: Flask-SQLAlchemy, python-dateutil, reportlab (for PDF generation)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd PersonalExpenseTracker
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   Open your web browser and navigate to: `http://localhost:5000`

## 📖 How to Use

### Getting Started
1. **Initial Setup**: The application automatically creates default categories when first run
2. **Add Categories**: Create custom categories that match your spending patterns
3. **Add Expenses**: Start tracking your daily expenses with detailed information
4. **View Reports**: Analyze your spending patterns and trends

### Key Features Usage

#### Adding Expenses
- Navigate to "Add Expense" from the dashboard or sidebar
- Fill in amount, date, description, and select a category
- Real-time validation ensures data accuracy

#### Managing Categories
- Access "Categories" from the main navigation
- Create new categories with descriptions
- View expense counts per category
- Delete unused categories (only if no expenses exist)

#### Viewing Reports
- Dashboard provides overview statistics
- Reports page shows detailed breakdowns by category and month
- Export data for external analysis
- Print reports for offline reference

#### Advanced Dashboard Filtering
- **Date Filtering**: Toggle exact date or date range selection
- **Category Filtering**: Multi-select categories with checkboxes
- **Real-time Updates**: Dashboard statistics update dynamically
- **PDF Export**: Download filtered dashboard view as professional PDF report

#### Monthly Recurring Expenses
- Toggle expenses as "monthly recurring" or "one-time"
- Monthly expenses count toward monthly totals
- Visual indicators show expense type in listings
- Separate tracking for recurring vs. one-time expenses

## 🗂️ Project Structure

```
PersonalExpenseTracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation and footer
│   ├── index.html        # Dashboard page with advanced filtering
│   ├── expenses.html     # Expenses listing and filtering
│   ├── add_expense.html  # Add new expense form with monthly toggle
│   ├── edit_expense.html # Edit expense form
│   ├── reports.html      # Reports and analytics
│   ├── categories.html   # Category management
│   └── add_category.html # Add new category form
├── static/               # Static files (CSS, JS, images)
└── expenses.db          # SQLite database (created automatically)
```

## 🗄️ Database Schema

### Categories Table
- `id`: Primary key
- `name`: Category name (unique)
- `description`: Optional category description
- `created_at`: Timestamp of creation

### Expenses Table
- `id`: Primary key
- `amount`: Expense amount (decimal)
- `description`: Expense description
- `date`: Expense date
- `category_id`: Foreign key to categories
- `is_monthly`: Boolean flag for monthly recurring expenses
- `created_at`: Record creation timestamp
- `updated_at`: Last modification timestamp

## 🔧 API Endpoints

- `GET /`: Dashboard overview
- `GET /expenses`: List all expenses with pagination
- `POST /add_expense`: Create new expense
- `GET /edit_expense/<id>`: Edit expense form
- `POST /edit_expense/<id>`: Update expense
- `POST /delete_expense/<id>`: Delete expense
- `GET /reports`: View expense reports
- `GET /categories`: List all categories
- `POST /add_category`: Create new category
- `POST /delete_category/<id>`: Delete category
- `GET /download_dashboard_pdf`: Download PDF report of current dashboard view

## 🎨 Design Decisions

### User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Intuitive Navigation**: Clear menu structure with icons
- **Real-time Feedback**: Immediate validation and success/error messages
- **Progressive Enhancement**: Works without JavaScript, enhanced with it

### Technical Architecture
- **MVC Pattern**: Clear separation of concerns
- **Database ORM**: SQLAlchemy for type safety and migrations
- **RESTful API**: Consistent endpoint naming and HTTP methods
- **Error Handling**: Comprehensive error catching and user-friendly messages

### Security Considerations
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: ORM protects against SQL injection
- **XSS Protection**: Template auto-escaping prevents cross-site scripting
- **CSRF Protection**: Form-based CSRF tokens (can be enhanced)

## 📊 Sample Data & Usage

### Sample Categories
The application comes with pre-configured categories:
- Food & Dining
- Transportation
- Shopping
- Bills & Utilities
- Entertainment
- Healthcare
- Travel
- Education
- Other

### Sample Expense Entry
```
Amount: $25.50
Date: 2024-01-15
Description: Coffee and pastry at local café
Category: Food & Dining
```

### Sample Report Output
```
Total Spent: $1,234.56
Top Categories:
- Food & Dining: $456.78 (37.0%)
- Transportation: $234.56 (19.0%)
- Shopping: $198.76 (16.1%)
```

## 🚀 Deployment Options

### Local Development
- Run `python app.py` for development server
- Accessible at `http://localhost:5000`
- Auto-reloads on code changes

### Production Deployment
1. **Environment Variables**: Set `FLASK_ENV=production`
2. **Database**: Use PostgreSQL or MySQL for production
3. **Web Server**: Deploy with Gunicorn + Nginx
4. **Security**: Enable HTTPS and update secret keys

## 🔮 Future Enhancements

- **User Authentication**: Multi-user support with login/logout
- **Budget Management**: Set and track spending budgets
- **Recurring Expenses**: Handle monthly bills and subscriptions
- **Data Visualization**: Charts and graphs for better insights
- **Mobile App**: Native mobile application
- **Cloud Sync**: Backup and sync across devices
- **Receipt Upload**: Photo capture and storage
- **Expense Sharing**: Family or group expense tracking

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in app.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

2. **Database Errors**
   ```bash
   # Delete expenses.db and restart to recreate
   rm expenses.db
   python app.py
   ```

3. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   pip install -r requirements.txt
   ```

## 📝 License

This project is created for educational and portfolio purposes. Feel free to use and modify as needed.

## 👨‍💻 Author

**Built by Ashish Gupta**

Created as part of an internship application process, demonstrating full-stack development skills with Python, Flask, and modern web technologies. This project showcases advanced features including dynamic filtering, PDF generation, and responsive design.

---

**Note**: This application is designed to showcase technical skills and follows best practices for web development. It includes comprehensive error handling, input validation, responsive design, and a clean, maintainable codebase structure.
