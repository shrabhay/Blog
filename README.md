# Flask Blog Project
## Description
A simple and elegant blog application built using Flask, with features like user authentication, blog post creation, comment section, and rich text editing using CKEditor. This project demonstrates the use of several important Flask extensions like Flask-WTF, Flask-Login, Flask-SQLAlchemy, and Flask-CKEditor.

---

## Features
* **User Authentication**: Register, login, and manage user sessions.
* **Blog Post Creation**: Admin users can create, edit, and delete blog posts with titles, subtitles, and rich content.
* **Comment Section**: Allow users to comment on blog posts with rich-text formatting.
* **Responsive Design**: Uses Bootstrap for a mobile-first, responsive layout.
* **Rich Text Editor**: CKEditor is integrated for blog post content and comments.
* **SQLAlchemy ORM**: SQLite is used for the database, but the project can be easily extended to use other databases like MySQL or PostgreSQL.

---

## Tech Stack
* **Backend**: Python 3.x, Flask 2.x
* **Database**: SQLite (via Flask-SQLAlchemy)
* **Frontend**: HTML, CSS (Bootstrap 3/4), JavaScript
* **Authentication**: Flask-Login
* **Text Editing**: CKEditor 5
* **Form Handling**: Flask-WTF, WTForms
* **Environment Management**: Virtualenv

---

## Installation

### Prerequisites
1. **Python**: Ensure you have Python 3.x installed. You can check this by running:
    ```commandline
    python --version
    ```

2. **Pip**: Make sure pip (Python's package installer) is installed:
    ```commandline
    pip --version
    ```

### Clone the Repository
```commandline
git clone https://github.com/shrabhay/Blog.git
cd Blog
```

### Set Up a Virtual Environment
It is recommended to use a virtual environment to manage your project dependencies.

1. Create a virtual environment:
    ```commandline
    python -m venv venv
    ```

2. Activate the virtual environment:

   * On macOS/Linux:
   ```commandline
   source venv/bin/activate
   ```
   
   * On Windows:
   ```commandline
   .\venv\Scripts\activate
   ```

### Install Dependencies
Run the following command to install all required dependencies:
    ```commandline
    pip install -r requirements.txt
    ```

### Setting Up the Database
The application uses SQLite for database management, and Flask-SQLAlchemy handles the ORM.

Run the Flask app to initialize the database:
```commandline
flask run
```

This will automatically create the necessary SQLite database file (app.db) and tables.

### Configuration
To configure the application for your local environment, follow these steps:

1. Set Environment Variables:

   * `FLASK_APP`: Set to the application file, usually `app.py`.
   * `FLASK_ENV`: Set to `development` for local development or `production` for deployment.

2. Configure Secret Key: You may need to set a `SECRET_KEY` in your app to manage sessions and CSRF protection.

    In app.py, add:
    ```python
    app.config['SECRET_KEY'] = 'your-secret-key'
    ```

    It's recommended to use a random string for production.

### Running the Application
Once everything is set up, you can run the application:
```commandline
flask run
```

By default, the app will run on `http://127.0.0.1:5000/`.

### Access the Application
Visit `http://127.0.0.1:5000/` in your web browser to interact with the application.

* **Home Page**: Displays all published blog posts.
* **Login/Signup**: Users can register and log in to create posts and comment on them.
* **Post Creation**: Authenticated users can create new blog posts with rich content.
* **Commenting**: Users can comment on posts using a rich-text editor.

---

## Project Structure
Here’s a breakdown of the main project structure:
```text
flask-blog/
│
├── blog.py               # Main Flask application file
├── forms.py              # Forms for registration, login, post creation, and comments
├── requirements.txt      # List of project dependencies
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with common structure
│   ├── home.html         # Home page listing blog posts
│   ├── post.html         # Blog post detail page
│   ├── create_post.html  # Blog post creation form
│   └── login.html        # Login page
│   └── register.html     # Registration page
│   └── comment.html      # Comment submission form
│
├── static/               # Static files (CSS, JS, Images)
│   ├── css/              # CSS files
│   ├── js/               # JavaScript files
│   └── images/           # Images (e.g., blog post images)
│
├── instance/             # Configurations (for production settings)
├── venv/                 # Virtual environment
└── .gitignore            # Git ignore file
```

### Key Files:
* **`app.py`**: The main file that contains the Flask app setup, routes, and view functions.
* **`forms.py`**: Contains the form definitions for adding posts, registering users, and submitting comments.
* **`templates/`**: Directory for all HTML files using Jinja templating.
* **`static/`**: Contains static files such as stylesheets, JavaScript, and images.

---

## Deployment
For deployment, you can use services like Heroku, AWS, or DigitalOcean.

1. Heroku:

   * Install the Heroku CLI and log in.
   * Create a Procfile with the following content:
    ```text
    web: gunicorn app:app
    ```

    * Push your code to Heroku and deploy:
    ```commandline
    git push heroku master
    ```

2. Other Services:

   * You can deploy this app to any cloud provider with support for Python and Flask applications, such as AWS, Google Cloud, or DigitalOcean.

---

## Contributing
We welcome contributions to this project. If you'd like to improve or extend the functionality, feel free to fork the repository, create a new branch, and submit a pull request.

### Steps for Contributing:
1. Fork the repository.
2. Clone your fork locally:
    ```commandline
    git clone https://github.com/shrabhay/Blog.git
    ```

3. Create a new feature branch:
    ```commandline
    git checkout -b new-feature
    ```

4. Make your changes and commit them:
    ```commandline
    git commit -am 'Add new feature'
    ```

5. Push to your fork:
    ```commandline
    git push origin new-feature
    ```

6. Open a pull request.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgments
* Flask for providing the framework.
* Flask-SQLAlchemy for easy database integration.
* Flask-WTF for form handling and CSRF protection.
* Flask-Login for session management.
* CKEditor for rich text editing functionality.
* Bootstrap for responsive design.
