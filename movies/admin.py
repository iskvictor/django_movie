from re import I
from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("name", "url")
    list_display_links =("name",)


class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"

# @admin.register(Movie)
# class MovieAdmin(TranslationAdmin):
#     """Фильмы"""
#     list_display = ("title", "category", "url", "draft")
#     list_filter = ("category", "year")
#     search_fields = ("title", "category__name")
#     inlines = [MovieShotsInline, ReviewInline]
#     save_on_top = True
#     save_as = True
#     list_editable = ("draft",)
#     actions = ["publish", "unpublish"]
#     form = MovieAdminForm
#     readonly_fields = ("get_image",)
#     fieldsets = (
#         (None, {
#             "fields": (("title", "tagline"), )
#         }),
#         (None, {
#             "fields": ("description", ("poster", "get_image"))
#         }),
#         (None, {
#             "fields": (("year", "world_premiere", "country"), )
#         }),
#         ("Actors", {
#             "classes": ("collapse",),
#             "fields": (("actors", "directors", "genres", "category"), )
#         }),
#         (None, {
#             "fields": (("budget", "fees_in_usa", "fees_in_world"), )
#         }),
#         (None, {
#             "fields": (("url", "draft"), )
#         }),
#     )

#     def get_image(self, obj):
#         return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')
    

#     def unpublish(self, request, queryset):
#         """Снять с публикации"""
#         row_update = queryset.update(draft=True)
#         if row_update == 1:
#             message_bit = "1 запись была обновлена"
#         else:
#             message_bit = f"{row_update} записи были обновлены"
#         self.message_user(request, f"{message_bit}")

#     def publish(self, request, queryset):
#         """Публиковать"""
#         row_update = queryset.update(draft=False)
#         if row_update == 1:
#             message_bit = "1 запись была обновлена"
#         else:
#             message_bit = f"{row_update} записи были обновлены"
#         self.message_user(request, f"{message_bit}")

#     publish.short_description = "Опубликовать"
#     publish.allowed_permissions = ('change',)

#     unpublish.short_description = "Снять с публикации"
#     unpublish.allowed_permissions = ('change',)

#     get_image.short_description = "Постер")

class MovieResource(resources.ModelResource):
    # directors = fields.Field(column_name='directors', attribute='directors',
    #             widget=ManyToManyWidget(Actor, 'name'))
    # actors = fields.Field(column_name='actors', attribute='actors',
    #             widget=ManyToManyWidget(Actor, 'name'))
    # genres = fields.Field(column_name='genres', attribute='genres',
    #             widget=ManyToManyWidget(Genre, 'name'))
    # category = fields.Field(column_name='category', attribute='category',
    #             widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        model = Movie

@admin.register(Movie)
class MovieAdmin(ImportExportActionModelAdmin):
    resource_class = MovieResource
    list_display = ("title", "category", "url", "draft")
    inlines = [MovieShotsInline, ReviewInline]



@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    """Рейтинг"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"