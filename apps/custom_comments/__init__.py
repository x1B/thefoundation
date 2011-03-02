from django import forms
from django.dispatch import receiver

from django.contrib.comments.forms import CommentDetailsForm
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.comments.signals import comment_will_be_posted


class ArticleCommentModerator(CommentModerator):
    email_notification = False
    enable_field = 'public'
    auto_moderate_field = 'publication_date'
    moderate_after = 0


@receiver(comment_will_be_posted)
def handle_comment(sender, comment, **kwargs):
    comment.is_public = comment.user is not None


class CommentForm(CommentDetailsForm):
    email = forms.EmailField(label="Email address", required=False)

def get_form():
    return CommentForm