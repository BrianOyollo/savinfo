## Customer Orders API  (Savannah Informatics Technical Backend Challenge)

# Overview
This project is a simple API service that allows you to manage customers and their orders. It provides a RESTful interface to create, retrieve, update, and delete customer and order records. Additionally, it sends SMS alerts to customers when their orders are created using the Africa's Talking SMS gateway.*


## Tools and Technologies
-   **Django:** A high-level Python web framework for building secure and scalable APIs.
-   **DRF-SOCIAL-OAUTH2** Provides OAuth2 (and OpenID Connect)  support for Django applications.
-   **DRF (Django Rest Framework):** A powerful toolkit for building Web APIs.
-   **OpenAPI:** Automatically generated API documentation for easy exploration of endpoints


## API Documentation
View the API documentation at `https://4mx-astute-joule.circumeo-apps.net/api/docs/` to explore endpoints interactively.

## Installation
1. **Clone the repository:**
   ```
   git clone https://github.com/BrianOyollo/savinfo
   cd savinfo
   ```

2. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
	 ```
	  pip install -r requirements.txt
   ```
 4. **Create and add django secret key to .env**
	 ```
	python
	import secrets
	secrets.token_hex(32) # set the value generated as your secret key in settings.py file (SECRET_KEY) 
	 ```
4. **Setup PostgreSQL db:**
Set up your environment variables in a `.env` file or export them in your shell
	 ```
		POSTGRES_NAME=""
		POSTGRES_USER=""
		POSTGRES_PASSWORD=""
		POSTGRES_HOST=localhost
		POSTGRES_PORT=5432
   ```
5. **Run database migrations:**
	 ```
	  python manage.py migrate
   ```
6. **Create a superuser:**
	 ```
	  python manage.py createsuperuser
   ```
7. **Start the development server:**
	 ```
	  python manage.py runserver
   ```  

## Configuration
1. **Oauth2 Configuration**
-   Leave the client_id and client_secret fields unchanged 
-  Add your the client_id and client_secret your .env file
-   Set the user field to your superuser.
-   Leave the redirect_uris field blank.
-   Set the client_type field to confidential.
-   Set the authorization_grant_type field to ‘Resource owner password-based’.
-   Optionally, you can set the name field to a name of your choice.
  
 2. **Africa's Talking Credentials:**
 Ensure that the Africa's Talking API key, username and shortcode are configured in the .env file
	```
	SMS_API_USERNAME=
	SMS_API_KEY=
	SENDER_SHORTCODE=
	```
3. **OpenID Connect Integration**
	  1. Obtain _SOCIAL_AUTH_GOOGLE_OAUTH2_KEY_ and _SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET_ from [https://console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials)
	  [more info on how to create oauth key and secret](https://developers.google.com/identity/protocols/oauth2)
	  
	  3. Add the oauth key and secret to your .env file
			```
			SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
			SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
			```
 ## Testing
 ```
 pytest --ds=savinfo.settings
 ```	
 or with coverage
```
coverage run -m pytest --ds=savinfo.settings
```
