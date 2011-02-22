""" Newforms Admin configuration 
"""

from django.contrib import admin
from models import *


class BlogAdmin( admin.ModelAdmin ):
   list_display = ( "owner", "title", "sub_title" )


class TagAdmin( admin.ModelAdmin ):
   list_display = ( "name", "url_name" )
   prepopulated_fields = { "url_name": ["name"] }


class ArticleAdmin( admin.ModelAdmin ):
   prepopulated_fields = { "title_in_url": ["title"] }
   filter_horizontal = ( "tags", )
   list_display = ( "title", "author_name", "publication_date", "modified", "was_published", "public" )
   list_display_links = ( "publication_date", "title", )
   list_filter = ( "author", )
   list_per_page = 30
   search_fields = ( "title", "html_teaser", "html" )
   date_hierarchy = "publication_date"
   fieldsets = (
      ( "Basics", { "fields": ( "title", "title_in_url", ) } ),
      ( "Article", 
         { "description": "The teaser is displayed in the overview pages and above the article text.",
           "fields": ( "html_teaser", "html", ) } ),
      ( "More meta information", 
         { "fields": ( "tags", ),
           "classes": "collapse" } ),
      ( "Publication settings and information",
         { "description": "When saving to public for the first time, the publication date is set forever.",
           "fields": ( "public", ) } )
   )
   
   def formfield_for_dbfield(self, db_field, **kwargs):
       field = super( ArticleAdmin, self ).formfield_for_dbfield( db_field, **kwargs )
       if db_field.name == "html_teaser":
           field.widget.attrs[ 'rows' ] = 3
       if db_field.name == "html":
           field.widget.attrs[ 'rows' ] = 30
       return field


admin.site.register( Blog, BlogAdmin )
admin.site.register( Article, ArticleAdmin )
admin.site.register( Tag, TagAdmin )
