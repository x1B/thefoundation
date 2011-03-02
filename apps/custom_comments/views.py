from django.contrib.comments.views import post_comment as _post


def post_comment(request):
    return _post(request)
