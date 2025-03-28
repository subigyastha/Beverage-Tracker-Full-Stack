# Beverage Tracker

A Django-based web application for logging beverage entries, including categories, subcategories, additives, symptoms, and temperature details. Features dynamic subcategory selection, inline formsets for additives and symptoms, and an interactive temperature slider.

## Overview

This project allows users to:
- Record beverages with details like category (e.g., water, coffee), subcategory (e.g., plain water, espresso), quantity, and temperature.
- Add and manage additives (e.g., sugar, milk) and symptoms (e.g., headache, nausea) associated with each entry.
- Edit existing entries with persistent subcategory selection and formset management.

## Prerequisites

- **Python**: 3.8 or higher
- **Virtual Environment**: Recommended (e.g., `venv`)
- **Web Browser**: For accessing the app
- **Operating System**: Windows, macOS, or Linux

## Project Structure
```
beverage_tracker/
├── manage.py
├── tracker/             # Main Django app
│   ├── migrations/      # Database migrations
│   ├── static/          # Static files
│   │   └── js/
│   │       └── dynamic_subcategories.js
│   ├── templates/
│   │   └── beverage_entry_form.html
│   ├── init.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── beverage_tracker/    # Project settings
│   ├── init.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3           # Default SQLite database
├── requirements.txt     # Python dependencies
└── README.md            # This file

```







## Setup Instructions

### 1. Download or Copy the Project
- Obtain the project files (e.g., via download or manual copy) and place them in a directory, e.g., `beverage_tracker`.

### 2. Set Up a Virtual Environment
Create and activate a virtual environment to isolate dependencies:
- **Linux/macOS**:
  ```bash
  cd beverage_tracker
  python3 -m venv venv
  source venv/bin/activate
```
- **Windows**:

```cmd
cd beverage_tracker
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install required Python packages:
```
pip install -r requirements.txt
```

### 4. Configure the Database
The default setup uses SQLite. To use it:

Ensure settings.py has:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

```
Apply migrations:
```
python manage.py makemigrations
python manage.py migrate`
```

### 5. Collect Static Files
Gather static files (e.g., dynamic_subcategories.js):

```
python manage.py collectstatic
```

Ensure settings.py includes:

```
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "intake_tracker/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

### 6. Create a Superuser (Optional)
For admin access:

```
python manage.py createsuperuser
```
Follow prompts to set username, email, and password.

### 7. Run the Development Server
Start the app:
```
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.


### Features
- Beverage Logging: Track beverages with category, subcategory, quantity, unit, temperature, and notes.
- Dynamic Subcategories: JavaScript updates subcategory options based on category selection (see dynamic_subcategories.js).
- Additives & Symptoms: Add/remove via inline formsets with validation and deletion support.
- Temperature Slider: Interactive UI synced with a hidden select field.
- Edit Persistence: Subcategory values persist on edit using window.initialSubcategory.

### Usage
1. Create an Entry:
- Go to http://127.0.0.1:8000/ (adjust URL based on urls.py).
- Fill in beverage details, add additives/symptoms, and submit.
2. Edit an Entry:
- Navigate to /edit/<pk>/ (e.g., /edit/17/).
- Modify fields, add/remove additives or symptoms, and save.
3. Admin Interface:
- Visit /admin/ and log in with superuser credentials to manage entries.

### Development Notes
## Models
BeverageEntry: Core model with fields like category, subcategory, quantity, etc.
Additives: Linked to BeverageEntry with name and custom_additives.
Symptoms: Linked to BeverageEntry with symptoms, custom_symptoms, severity, and timing.
## Forms
BeverageEntryForm: Manages main entry fields with dynamic subcategory choices.
AdditiveFormSet & SymptomFormSet: Inline formsets with can_delete=True.
## Templates
beverage_entry_form.html: Main form with dynamic UI elements.
## Static Files
dynamic_subcategories.js: Handles subcategory updates and restoration.

### Troubleshooting
- Subcategory Reset:
Check window.initialSubcategory in <script> tag of beverage_entry_form.html.
Verify dynamic_subcategories.js is loaded (<script src="{% static 'js/dynamic_subcategories.js' %}"></script>).
- Formset Errors:
Inspect POST data in terminal logs for missing DELETE flags.
Ensure hidden fields (e.g., symptoms-0-DELETE) are rendered.
- Static Files Not Found:
Run collectstatic and check STATICFILES_DIRS and STATIC_ROOT in settings.py.
- Database Issues:
Re-run migrations or delete db.sqlite3 and start fresh if needed.


### Extending the Project
1. Add a Database:
For PostgreSQL, update DATABASES in settings.py and add psycopg2-binary to requirements.txt.
2. Enhance Features:
Add user authentication (django.contrib.auth).
Implement entry listing or analytics views.
3. Version Control:
To use Git:

git init
echo -e "venv/\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n*.db\n*.sqlite3\n*.log\n.env\nstaticfiles/" > .gitignore
git add .
git commit -m "Initial commit"


