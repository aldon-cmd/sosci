# build sosci-live.js module

cd sosci.git/livestream/twilio

npm run build

# create and run data migration for custom_user app

python manage.py makemigrations --empty custom_user

python manage.py migrate

# Steps for creating a page

Create a view class, and see examples in the views.py file, note there is 1 view.py file in each app/folder.
See line 149 of the views.py file in the catalogue app.

In the views.py file, set the template name to the name of the html file, under the folder in which it can be found. 

Create the template. 

Create the url that points to the class in the app.py file 

Copy the course_publish template, and make your modifications. 

