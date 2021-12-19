from django.contrib.auth.models import User
from django.db import models
from markdown import markdown
from markdownx.models import MarkdownxField

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return f'/product/category/{self.slug}'

    class Meta:
        # admin 페이지에 모델 자동으로 뒤에 s 붙는거를 다음 문자열로 바꿔라...
        verbose_name_plural = 'Categories'

class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=30, null=True)

    manufacturer_image = models.ImageField(upload_to='product/images/manufacturer/', blank=True)

    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.manufacturer_name

    def get_absolute_url(self):
        return f'/product/manufacturer/{self.slug}'

class Item(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    image = models.ImageField(upload_to='product/images/Item/', blank=True)
    price = models.IntegerField()

    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    kcal = models.CharField(max_length=30, null=True, blank=True)
    gram = models.CharField(max_length=30, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/product/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.item.get_absolute_url()}#comment-{self.pk}'


    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/401/5c35620aec71444b/svg/{self.author.username}/'