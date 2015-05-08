# Displayer

## Basic Description

Displayer (a System for Democratizing Interactive Public Screens) is made as a final capstone project at NYUAD in 2015 by Oleg Grishin (under the mentorship of Jay Chen and Azza Abouzied). Displayer is a system for making displayal of media on public screens easy through using mainly web-based interface for both user- and display-facing interfaces.

## Dependencies
Displayer uses Django on the backend (version 1.8 was used during the development process)
There are many other dependencies, like jQuery and Bootstrap, but they are directly referenced in the code and present in the repository, so there is no need to use tools like Bower for setting project up.

## Basic Setup
To start the Displayer server you will need to have Django installed. In addition, you will have to install a bridge between Django and the database of your choice. Please find more at https://docs.djangoproject.com/en/1.8/ref/databases/
You will need to modify 'settings.py' in 'displayer' folder to match your database settings.

## Sample data
You can use 'json.dump' to get simple set up and understand how the database schema is set up. Please use 'python manage.py loaddata json.dump' to load the data into your database. The actual files will not be copied to 'media' folder, so you will have to either manually change the database, or add the files that much the file names in the database.

## Help
Please contact me at og402@nyu.edu if you have any questions regarding development and general set up of the project.