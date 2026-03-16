# Finance Tracker - Comprehensive Personal Finance Management System

This project is a feature-rich Personal Finance Management system built with **Django**. It enables users to track income, manage expenses, set budgets, handle recurring transactions, and view detailed financial reports.

## 🚀 Key Features

- **User Authentication & Profiles**: Secure signup, login, and profile management with profile images.
- **Income Management**: Log various income sources with categorization.
- **Expense Tracking**: Record daily expenses and monitor spending habits.
- **Advanced Budgeting**: Set monthly budgets for specific categories with real-time tracking of remaining balances.
- **Recurring Transactions**: Manage automated recurring income or expenses (e.g., subscriptions, rent).
- **Tax Slab Management**: Define and track tax slabs for financial planning.
- **Financial Reports**: 
  - **Personal Reports**: Detailed breakdown of individual spending and earnings.
  - **Common Reports**: Aggregated views for broader financial insights.
- **Responsive UI**: Modern, intuitive interface built with Bootstrap, Font Awesome, and custom CSS/JS.
- **Admin Dashboard**: Specialized management interface for system administrators.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap, jQuery, Owl Carousel, Lightbox
- **Icons & Graphics**: Font Awesome, Custom static assets

## 📂 Project Structure

```text
.
├── manage.py           # Django command-line utility
├── moneymap/           # Core project configuration (settings, urls)
├── user_app/           # Main user authentication and profile module
├── income/             # Income management module
├── expense/            # Expense tracking module
├── budget/             # Budgeting and planning module
├── category/           # Category and subcategory management
├── recurring/          # Recurring transactions module
├── taxslab/            # Tax planning and slab management
├── media/              # User-uploaded content (e.g., profile images)
└── static/             # Global CSS, JS, and Image assets
```

## 🏃 Getting Started

### 1. Prerequisites
- Python 3.12+
- Django 5.0+

### 2. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yovyshh/FINANCE-TRACKER.git
   cd FINANCE-TRACKER
   ```

2. **Install Dependencies**:
   ```bash
   pip install django requests
   ```

3. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000`.

---
*Note: This project was migrated from the `moneymap_30_01_25` development branch.*
*Developed by Vaishnav T. Prakash*
