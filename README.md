# My Django Project

This Django project is a multi-tenancy application that allows managing different organizations and users within those
organizations. It is integrated with PostgreSQL for data persistence and uses Django Rest Framework (DRF) for creating
APIs.

## Features

- Connect to different PostgreSQL databases for different organizations dynamically.
- Automatically create new databases for new organizations.
- User management within organizations.
- RESTful APIs for retrieving users and organizations.

## Setup

### Requirements

- Python 3.6+
- PostgreSQL

### Installation

1. Clone the repository:
   ```sh
   git clone https://gitlab.com/sponix-team/spov-project/coretest.git
   ```


2. Change to the project directory:

   ```sh

   cd <project-directory>

   ```

3. Create and activate a virtual environment:
   ```sh

   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the requirements:
   ```sh
   pip install -r requirements.txt
   ```

5. Set up environment variables for database connection. You can do this by setting them in your environment or creating
   a `.env` file in the project root with the following variables:
   ```text
   CONSUL_HOST="your consul host"
   CONSUL_PORT=443
   CONSUL_TOKEN="consul token"
   DEBUG_MODE=true
   SECRET_KEY = "secret key"
   ```

6. Run migrations to create the database schema:
   ```sh
   python manage.py migrate
   ```


7. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

### APIs

1. **List Users within an Organization**

- Endpoint: `/list_users/`
- Method: `GET`
- Headers: `Authorization: JWT <token>`, `organization_id: <organization_id>`
- Response: List of users within the organization.

2. **Retrieve a User within an Organization**

- Endpoint: `/retrieve_user/<str:user_id>/`
- Method: `GET`
- Headers: `Authorization: JWT <token>`, `organization_id: <organization_id>`
- Response: User details along with organization info.

3. **Retrieve an Organization**

- Endpoint: `/retrieve_organization/`
- Method: `GET`
- Headers: `Authorization: JWT <token>`, `organization_id: <organization_id>`
- Response: Organization details.

4. **List All Organizations (Admin Only)**

- Endpoint: `/list_organizations/`
- Method: `GET`
- Headers: `Authorization: JWT <token>`
- Response: List of all organizations with users.

### Admin Interface

Django's built-in admin interface can be used to manage users and organizations. It can be accessed at `/admin`.

## Note

Ensure that your JWT Authentication is properly set up for handling organization_id in headers.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Author

[Sponix]