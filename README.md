# Finance Tracker - Django Web Application

A comprehensive Personal Finance Management system built with **Django**. This application allows users to track their income, manage expenses, set budgets, and view financial reports through an intuitive web interface.

## 🚀 Features

- **User Authentication**: Secure signup and login system for individual financial tracking.
- **Income Management**: Log and categorize various sources of income.
- **Expense Tracking**: Record daily expenses and monitor spending habits.
- **Budgeting**: Set monthly budgets for different categories and track adherence.
- **Financial Reports**: Visual summaries and lists of financial activities.
- **Admin Dashboard**: Specialized management interface for system administrators to oversee users and categories.
- **Responsive Design**: Modern UI built with Bootstrap for a seamless experience across desktop and mobile.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (Default)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap, Font Awesome
- **Icons & Graphics**: Custom static assets and SVG icons

## 📂 Project Structure

```text
.
├── manage.py           # Django command-line utility
├── myproject/          # Core project configuration (settings, urls)
├── user/               # Main application (models, views, templates, static)
├── admin_app/          # Admin-specific functionalities
├── income/             # Income management module
├── expense/            # Expense tracking module
├── budget/             # Budgeting and planning module
├── income_tracking/    # Specialized tracking services
└── static/             # Global CSS, JS, and Image assets
```

## 🏃 Getting Started

### 1. Prerequisites
- Python 3.x
- pip (Python package manager)

### 2. Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yovyshh/FINANCE-TRACKER.git
   cd FINANCE-TRACKER
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Django**:
   ```bash
   pip install django
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000` in your browser.



---
*Developed by Vaishnav T. Prakash*
