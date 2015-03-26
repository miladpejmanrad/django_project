Here's the menu module I started fiddling with to get some Django experience. You'll need to make sure you add it to your Django project's settings.py under INSTALLED_APPS.

Additionally, you'll need to add URL patterns to your project's urls.py if you want to see anything outside of the admin area. The one I'm using for this module is:

url(r'^menu/', include('menu.urls')),

Ping me if you have questions or need help!
