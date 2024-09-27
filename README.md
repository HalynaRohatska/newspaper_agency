# Newspaper Agency

A project for managing newspapers and editors, allowing tracking of publication topics and editor experience.

## Test User

To access the site as a test user, use the following credentials:

- **Username**: testredactor
- **Password**: plmokn951

This user has permissions to view the website and perform basic actions but does not have admin privileges.

## Models

The project contains three main models:
- **Topic**: The topic of a newspaper publication.
- **Redactor**: An editor who can have varying levels of experience.
- **Newspaper**: A newspaper publication that includes a title, content, publication date, topic, and is related to editors.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/newspaper_agency.git
    ```
2. Navigate to the project directory:
    ```bash
    cd newspaper_agency
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # for Mac/Linux
    venv\Scripts\activate      # for Windows
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Apply migrations:
    ```bash
    python manage.py migrate
    ```
6. Start the local server:
    ```bash
    python manage.py runserver
    ```

## Usage

### Creating Editors and Newspapers

1. Log in to the admin panel using a superuser account: [http://localhost:8000/admin](http://localhost:8000/admin)
2. Create topics, editors, and publications using the **Topic**, **Redactor**, and **Newspaper** models.

## Testing

Run tests:
```bash
python manage.py test

