thefoundation.de
----------------

The personal [homepage](http://www.thefoundation.de) and blog of some friends. Probably not something useful for most people.

Also, pretty old (conceived 2006-2007). Here to receive a face-lift during our [geekweek](http://geekweek.thefoundation.de).


Article Author Information
--------------------------
- see ./support/documents/HELP


Developer Information
---------------------

- You need a working installation of Django 1.0 in your path.

- You also need the Python Imaging Library (PIL)

- You need SQLite, use settings_development or settings_testing
  
- To get started with some initial data, run:
  > ./tools/develop


Administrator Information
-------------------------

The following information applies to production and stage mode.

- The app runs as a FastCGI server, known as the 
  "thefoundation application" (or simply "TFA")
  see ./support/scripts/thefoundation

- Nginx is the http server in front of the TFA.
  See ./support/nginx.conf

- In production mode, PostgreSQL ist the database system to be used.
  Help on this can be found in ./support/configs/postgres

- The fastcgi server is managed using an init-style start/stop script
  like the one at at ./support/scripts/thefoundation

- Create directories ../logs and ../run

- The "setup" script will help you to create ./var and the necessary 
  subdirectories as well as some links from the read-only media-folder.

- Then, you must give (recursive) write-permissions on ./var to the fcgi 
  application. Currently, this is realized using a group "www" that the django 
  process and Nginx belong to.
  Also, give write permissions to ../run and ../logs

- TFA (production) and Nginx are started at system startup time.


More Information
----------------
- see ./support/documents/
