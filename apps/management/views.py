import random

from django import forms
from django.contrib import auth
from django.http import HttpResponseRedirect

from tf.util import render, login_required, data_for_all, require_POST


class TextInput(forms.TextInput):
    def __init__(self):
        forms.TextInput.__init__(self, attrs = {"class": "text"})


class FileInput(forms.FileInput):
    def __init__(self):
        forms.FileInput.__init__(self, attrs = {"class": "text"})


def data_for_management(request):
    data = data_for_all(request)
    data.update({'gallery_form': GalleryUploadForm({'date': 'YYYY-mm-dd',
                                                    'show_form': False})})
    return data


def login(request):
    """Authenticate and log-in a user."""
    data = data_for_all(request)
    data.update({"show_login_form": True})
    return render("meta_blogs.html", request, data)


def login_submit(request):
    """Authenticate and log-in a user."""
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/manage/")
    return HttpResponseRedirect("/login/failed/")


def login_failed(request):
    """Re-display the login form, inform the user about the failure."""
    data = data_for_all(request)
    data.update({"login_failed": True, "show_login_form": True})
    return render("meta_blogs.html", request, data)


def logout(request):
    """Log out the current user."""
    auth.logout(request)
    return render("meta_logout.html", request, data_for_all(request))


@login_required
def manage(request):
    """Display an welcome/overview page to the logged-in user."""
    data = data_for_management(request)
    data.update({"welcome_phrase": random.choice(
       ["%s, motherfucker!",
         "rock on, %s!",
         "%s to the max!",
         "%s, hey dude!",
         "hax0r %s",
         "%s, you bastard!",
         "%s, mottafokka!"]) % data["current_user"].first_name})
    return render("meta_toolbox.html", request, data)


class GalleryUploadForm(forms.Form):
    """Form to upload zipped galleries."""
    title = forms.CharField(max_length = 120, widget = TextInput())
    description = forms.CharField(widget = TextInput())
    zip_file = forms.FileField(widget = FileInput(), label = "Zip Archive")
    date = forms.DateField(widget = TextInput(), input_formats = ['%Y-%m-%d'])


@login_required
def galleries(request):
    """List galleries."""
    return render("meta_manage_galleries.html",
                  request,
                  data_for_management(request))


@login_required
def galleries_new(request):
    """Show gallery upload form."""
    data = data_for_management(request)
    data.update({"show_new_gallery_form": True})
    return render("meta_manage_galleries.html", request, data)


@login_required
@require_POST
def galleries_submit(request):
    """Try to upload a new gallery."""
    # :TODO: check this -- file is not used?!
    if "zip_file" in request.FILES:
        file = request.FILES["zip_file"]
    return render("meta_manage_galleries.html",
                  request, data_for_management(request))


@login_required
def images(request):
    """List individual images."""
    return render("meta_manage_images.html",
                  request, data_for_management(request))

@login_required
def images_new(request):
    """Show gallery upload form."""
    return render("meta_manage_images.html",
                  request, data_for_management(request))

@login_required
def images_submit(request):
    """Try to upload a new gallery."""
    return render("meta_manage_images.html",
                  request, data_for_management(request))
