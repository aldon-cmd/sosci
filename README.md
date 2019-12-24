# project setup

install latest version of python  along with pip. add python to the path variable

install python 3.7.6. do not add python 3.7.6 to the path variable

pip install virtualenvwrapper-win

mkvirtualenv vsosci --python C:\Python37\python.exe

workon vsosci

cd sosci.git

pip install -r requirements.txt

python manage.py migrate

# custom migrations

0020_auto_20191221_1832.py . creates default product classes

0003_auto_20191117_1529.py .  creates user roles

0006_auto_20191223_2042.py . creates the default partner

# create and run empty migration

python manage.py makemigrations --empty app_name

python manage.py migrate

# build javascript libraries with webpack

cd sosci.git/livestream/twilio

npm run build

# steps for creating a page

Create a view class, and see examples in the views.py file, note there is 1 view.py file in each app/folder.
See line 149 of the views.py file in the catalogue app.

In the views.py file, set the template name to the name of the html file, under the folder in which it can be found. 

Create the template. 

Create the url that points to the class in the app.py file 

Copy the course_publish template, and make your modifications. 

