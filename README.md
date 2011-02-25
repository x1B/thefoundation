thefoundation.de
----------------

The personal [homepage](http://www.thefoundation.de) and blog of some friends. Probably not something that is useful to most people.

Also, pretty old (conceived 2006-2007). Here to receive a facelift during our [geekweek](http://geekweek.thefoundation.de).


Article Author Information
--------------------------

* Articles are written in HTML.

* To embed a gallery: <gallery slug="{gallery_slug}">{title}</gallery>

* To embed a youtube video: <youtube id="{youtube_id}">{title}</youtube>


Setup
-----

Obtain the requirements (virtual

    pip install -r requirements/production.txt

Execute the "../tools/rebuild_styles_and_scripts" tool from the main folder to regenerate compressed and concatenated script files. The tool builds one  script file for general pages (blog articles, archive views...) and one for  gallery pages.

In your settings file, you can use the "DEBUG_JS" or "DEBUG_CSS" flag to get individual, uncompressed js-files instead of the compressed archives. This helps to quickly test changes and to fix bugs.


Administrator Information
-------------------------

The following information applies to production and stage mode.

- The app runs as a FastCGI server, known as the
  "thefoundation application" (or simply "TFA")
  see ./lib/configs/scripts/thefoundation

- Nginx is the http server in front of the TFA.
  See ./lib/configs/nginx.conf

- Run ./tools/setup to create necessary directories and links.

- Give (recursive) write-permissions on ../var to the user running the fcgi
  server. Also, give write permissions to ../run and ../logs
