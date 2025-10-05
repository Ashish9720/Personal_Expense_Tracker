# Personal Expense Tracker - Short Documentation

**Built by Ashish Gupta**

## 📋 Assumptions

### User Requirements
- Users want to track personal expenses with basic categorization
- Need simple, intuitive interface without complex features
- Want to see spending patterns and totals quickly
- Prefer web-based application accessible from any device

### Technical Assumptions
- Single-user application (no authentication required)
- Local data storage is sufficient (SQLite database)
- Users have basic web browser knowledge
- Python 3.8+ environment available for running

### Data Assumptions
- Expenses are recorded in USD currency format
- Date format follows YYYY-MM-DD standard
- Categories are pre-defined but customizable
- Monthly recurring expenses need separate tracking

## 🎨 Design Decisions

### Architecture
- **Flask Web Framework**: Lightweight, flexible Python web framework
- **SQLite Database**: File-based database for easy deployment and backup
- **Bootstrap UI**: Responsive design that works on all devices
- **MVC Pattern**: Clean separation between data, logic, and presentation

### User Interface
- **Dashboard First**: Main page shows key statistics and recent expenses
- **Simple Navigation**: Clear menu structure with icons
- **Form Validation**: Real-time feedback for data entry
- **Filter Controls**: Easy-to-use toggles and dropdowns

### Data Management
- **Categories**: Pre-defined common categories with option to add custom ones
- **Expenses**: Required fields (amount, date, description, category) with optional monthly flag
- **Validation**: Server-side validation for data integrity
- **Backup**: SQLite file can be easily copied for backup

## 📊 Sample Inputs

### Adding an Expense
```
Amount: $25.50
Date: 2024-01-15
Description: Coffee and lunch at café
Category: Food & Dining
Monthly Recurring: No
```

### Adding a Category
```
Name: Gym Membership
Description: Monthly fitness center fees
```

### Date Filter Example
```
Date Toggle: ON
Date Range: 2024-01-01 to 2024-01-31
```

### Category Filter Example
```
Category Toggle: ON
Selected Categories: Food & Dining, Transportation
```

## 📈 Sample Outputs

### Dashboard Statistics
```
Total Spent: $1,234.56
This Month: $456.78
Total Expenses: 45
```

### Recent Expenses List
```
Date        Description           Category         Amount
2024-01-15  Coffee and lunch     Food & Dining    $25.50
2024-01-14  Bus fare             Transportation   $2.50
2024-01-13  Groceries            Food & Dining    $67.89
```

### Category Summary
```
Food & Dining:     $456.78 (37.0%)
Transportation:    $234.56 (19.0%)
Bills & Utilities: $198.76 (16.1%)
Entertainment:     $123.45 (10.0%)
Other:            $221.01 (17.9%)
```

### Monthly Summary
```
January 2024:   $456.78
December 2023:  $567.89
November 2023:  $432.10
```

## 🔧 Key Features

### Core Functionality
- ✅ Add, view, edit, delete expenses
- ✅ Category management
- ✅ Basic validation and error handling
- ✅ Data persistence with SQLite

### Advanced Features
- ✅ Monthly recurring expense tracking
- ✅ Dashboard with real-time statistics
- ✅ Advanced filtering (date range, multiple categories)
- ✅ PDF report generation
- ✅ Responsive design for mobile/desktop

### User Experience
- ✅ Intuitive navigation with icons
- ✅ Real-time form validation
- ✅ Professional styling with Bootstrap
- ✅ Clean, organized data presentation

## 📱 Interface Overview

### Dashboard
- Three main stat cards (Total Spent, This Month, Total Expenses)
- Recent expenses table with filtering options
- Quick actions for adding expenses and categories
- PDF download button for reports

### Expense Management
- Simple form with required fields
- Category dropdown selection
- Monthly recurring toggle switch
- Date picker for expense date

### Filtering System
- Date toggle with single date or date range options
- Category toggle with multi-select checkboxes
- Real-time updates without page refresh
- Clear visual indicators for active filters

## 🎯 Success Metrics

### User Experience
- Easy to add expenses (under 30 seconds)
- Clear visual feedback for all actions
- Responsive design works on all devices
- Intuitive navigation without training

### Technical Performance
- Fast page load times (< 2 seconds)
- Reliable data storage and retrieval
- Error handling for edge cases
- Clean, maintainable code structure

---

**This documentation provides a quick overview for understanding the application's purpose, design, and functionality without overwhelming technical details.**
