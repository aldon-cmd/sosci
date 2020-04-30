# project setup

Before mounting the containers, you must create the postgres volume manually:

docker volume create --name=pgdata

cd .

docker-compose up -d

ssh into postgres container and run python manage.py migrate

navigate to localhost:80

cd docker-jitsi-meet

docker-compose up -d

navigate to https://localhost:8443

# update docker image

docker-compose build 

docker-compose up -d 

# reset database

docker-compose down

docker-compose up -d

# custom migrations

catalogue/migrations/0020_auto_20191221_1832.py . creates default product classes

custom_user/migrations/0003_auto_20191117_1529.py .  creates user roles

partner/migrations/0006_auto_20191223_2042.py . creates the default partner

core/migrations/0001_initial.py . sets the domain of the website

# create and run empty migration

python manage.py makemigrations --empty app_name

python manage.py migrate

# build javascript libraries with webpack

cd sosci.git/livestream/twilio

npm run dev-build

# steps for creating a page

Create a view class, and see examples in the views.py file, note there is 1 view.py file in each app/folder.
See line 149 of the views.py file in the catalogue app.

In the views.py file, set the template name to the name of the html file, under the folder in which it can be found. 

Create the template. 

Create the url that points to the class in the app.py file 

Copy the course_publish template, and make your modifications. 

# Bank transfer process

-Client transfer instructions
Select email

Account/Beneficiary Name: Nesberry Technologies Limited
Account Number: 1002270222
Bank: CIBC FirstCaribbean
Branch: 1 King Street, Kingston
Account Type: Chequing

Note: When transferring funds within Jamaica, Bank/Branch code and Swift number are not required


- Client input fields
Name on account - Rafer Johnson
Bank - FGB (dropdown)
Transaction reference number - 12345678
Transaction date/time - March 15, 2020, 12:05pm
Transfer amount: $12,500

Submit button