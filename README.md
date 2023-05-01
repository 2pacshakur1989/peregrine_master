Introduction : 

Welcome to Peregrine Falcon , a simple yet practical flight management mini app.
The app serves 4 types of users - Anonymous client , a registered customer , a registered airline and a registered admin. each user has different permissions that will be discussed later on in the file.






Technologies : 

The app is made up of DB, Backend server with an API interface , and a UI.

Database -> MySQL - a relational schema with the tables : Group , User , AirlineCompany , Customer , Flight , Ticket and Country.

Backend server -> Django web framework. (For detailed information regarding the version,  and the dependincies, please check the requirements.txt file).

User interface -> React JS. (For detailed information regarding the version,  and the dependincies, please check the package.json file in the React app folder)


Backend dependincies : 

        asgiref==3.5.2
        async-timeout==4.0.2
        certifi==2022.9.24
        cffi==1.15.1
        charset-normalizer==2.1.1
        cryptography==38.0.3
        defusedxml==0.7.1
        Django==4.1.3
        django-allauth==0.51.0
        django-mysql==4.7.1
        djangorestframework==3.14.0
        gunicorn==20.1.0
        idna==3.4
        mysql-connector-python==8.0.32
        node==1.2
        oauthlib==3.2.2
        odict==1.9.0
        packaging==21.3
        Pillow==9.3.0
        plumber==1.7
        protobuf==3.20.3
        pycparser==2.21
        pygame==2.1.2
        PyJWT==2.6.0
        pyparsing==3.0.9
        python3-openid==3.2.0
        pytz==2022.6
        redis==4.3.5
        requests==2.28.1
        requests-oauthlib==1.3.1
        six==1.16.0
        spotipy==2.21.0
        sqlparse==0.4.3
        urllib3==1.26.13
        whitenoise==6.2.0
        zope.component==5.1.0
        zope.deferredimport==4.4
        zope.deprecation==4.4.0
        zope.event==4.6
        zope.hookable==5.4
        zope.interface==5.5.2
        zope.lifecycleevent==4.4
        zope.proxy==5.0.0






App structure:



        Backend (Django) - the app is composed of different layers (implying the microservices principal of separating layers). 

        1 - The DAL (Data access layer), which its main function to implement basic CRUD (Create, read , update and delete) actions in the database through the Django models.py (which technically are the database).

        2 - The Facade layer - which is mainly the logic layer , and in addition, it is the layer that provides separation of permissions for different users.
        There are 5 facades (5 python modules) - facadebase , anonymousfacade , adminfacade , airlinefacade and customerfacade .all of the following facades -> anonymous,airline,customer and admin inherit from facadebase which has mostly generic get functions which are allowed for all users (including an anonymous user).
        Anonymous facade has 2 functions - Signup (add_customer) and login.
        Customer facade -> update profile , add ticket , remove ticket and view all tickets
        Airline facade -> update profile , add flight , edit flight , remove flight and get my flights.
        Admin facade -> view all customers/admins/airlines , add customer/admin/airline , remove customer/admin/airline.

        3 - The API interface (Django restframework). which is a RESTfull API , and made up of function based API views, for each model (Admin, AirlineCompany , Flight ...etc)
        Each model has: 
        GET,POST,PATCH/PUT,DELETE methods for necessary use.
        Its own serializer/s for validating input. The serializer has default validators and custom made validators.
        Url route basic route with additional parameters (depends on the request).
        the URLS : 

            Login/Logout :
                http://localhost:8000/api/login/    -   POST 
                http://localhost:8000/api/logout/    -   POST

            Flight :
                http://localhost:8000/api/flights/    -   GET,POST 
                http://localhost:8000/api/flights/?update=value   -   GET
                http://localhost:8000/api/flights/?id=value   -   PUT, DELETE
                http://localhost:8000/api/flights/?origin_country_id=value&destination_country_id=value&airline_company_id=value&departure_time=value&landing_time=value   -   GET

            Ticket :
                http://localhost:8000/api/tickets/    -   GET,POST 
                http://localhost:8000/api/flights/?id=value   -   GET, DELETE

            Customer :
                http://localhost:8000/api/customers/    -   GET,POST
                http://localhost:8000/api/customers/?id=value   -   GET, PATCH, DELETE
                http://localhost:8000/api/customers/?customer_id=value   -   GET
                http://localhost:8000/api/customers/?USER_id=value   -   GET

            Airline :
                http://localhost:8000/api/airlines/    -   GET,POST
                http://localhost:8000/api/airlines/?id=value   -   GET, PATCH, DELETE
                http://localhost:8000/api/customers/?customer_id=value   -   GET
                http://localhost:8000/api/customers/?user_id=value   -   GET

            Admin :
                http://localhost:8000/api/admins/    -   GET,POST
                http://localhost:8000/api/admins/?id=value   -   GET, DELETE

            Country :
                http://localhost:8000/api/countries/    -   GET
                http://localhost:8000/api/countries/?id=value   -   GET





        FrontEnd - React JS App. 

        "dependencies": 
            "@testing-library/jest-dom": "^5.16.5",
            "@testing-library/react": "^13.4.0",
            "@testing-library/user-event": "^13.5.0",
            "axios": "^1.3.4",
            "bootstrap": "^5.2.3",
            "helmet": "^6.1.5",
            "js-cookie": "^3.0.1",
            "jwt-decode": "^3.1.2",
            "moment": "^2.29.4",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-helmet": "^6.1.0",
            "react-helmet-async": "^1.3.0",
            "react-router-dom": "^6.10.0",
            "react-scripts": "5.0.1",
            "web-vitals": "^2.1.4"


        The app is hierarchy of components interacting with eachother, Making it a single page application that rednders differently according to the request.
        Components heirarchy:
        Index
        App
        General
        Navbar - The navbar renders components based on the request (onClick,onSubmit ..etc..).

        Components functionality - Landing page is the render of the General component, which has a Navbar rendered in.
        On that Navbar we'll see a 'Login', 'Signup', 'Flights' and 'About Us'. The 'Flights' and 'About Us' remain the same (always rendered - constant).
        The 'Flights' renders a flight search filter. upon a successfull search, the flight/s will be rendered with button 'add flight' as an option. The add ticket will always be displayed but it's active only for a customer.

        Upon signing up(if successfull), the page will display a temporary success message and refresh the page in order to login.
        Upon successfull login, The Navbar will set the Signup component to inactive, and will render the profile of the logged user.

        If it's a customer, 2 components will be rendered, Profile and Tickets.
        Profile -> renders an update profile form with the current data.
        Tickets -> renders the customer's ticket/s with an option to remove.

        If it's an airline, 2 components will be rendered, Profile and Flights
        Profile -> renders an update profile form with the current data.
        Flights -> renders the airline's flight/s with an option to 'Edit' remove.
        Upon clicking Edit an update form with the flight's current info will be rendered.

        If it's an admin, 3 components will be rendered, Admins , Airlines, Customers
        Admins -> renders 2 sub components , Dropdown list of the admins component and a form to add an admin.
        Customers -> renders 2 sub components, Dropdown list of customers component and a form to add a customer.
        Airlines -> renders 2 sub components, Dropdown list of airlines component and a form to add an airline.


Contact Info : 
    
    Name: Rawi Mousa
    Phone: 0544714325
    Email: rawi.mousa@gmail.com




LoginInfo : 

Admin : RawiMousa ,danny123
Password : Rawim1989

Airline : wizzair1989 , aircanada1989, airfrance1933 , lufthansa1989 , 
Password : Rawim1989

Customer : maxim123 , lorenzo123, jeff12345, julie123
Password : Rawim1989