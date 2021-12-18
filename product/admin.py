from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from product.models import Item, Category, Manufacturer, Comment

# Register your models here.

admin.site.register(Item, MarkdownxModelAdmin)
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(Category, CategoryAdmin)

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('manufacturer_name',)}

admin.site.register(Manufacturer, ManufacturerAdmin)