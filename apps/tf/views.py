from tf.view_helpers import data_for_all, render


def start(request):
    """Display the start / overview page."""
    return render("meta_blogs.html", request, data_for_all(request))


def about(request):
    return render("meta_about.html", request, data_for_all(request))


def imprint(request):
    return render("meta_imprint.html", request, data_for_all(request))


def contact(request):
    return render("meta_contact.html", request, data_for_all(request))
