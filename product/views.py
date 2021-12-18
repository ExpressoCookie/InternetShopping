from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm

from .models import Item, Category, Manufacturer


class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count()
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_item_count'] = Item.objects.filter(manufacturer=None).count()
        return context

class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count()
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_item_count'] = Item.objects.filter(manufacturer=None).count()
        context['comment_form'] = CommentForm
        return context

def category_page(request, slug):
    # 다대일
    category = Category.objects.get(slug=slug)
    return render(request, 'product/item_list.html',
           {
               'item_list': Item.objects.filter(category=category),
               'categories': Category.objects.all(),
               'manufacturers': Manufacturer.objects.all(),
               'no_category_item_count': Item.objects.filter(category=None).count(),
               'no_manufacturer_item_count': Item.objects.filter(manufacturer=None).count(),
               'category': category
           })

def manufacturer_page(request, slug):
    manufacturer = Manufacturer.objects.get(slug=slug)
    return render(request, 'product/item_list.html',
           {
               'item_list': Item.objects.filter(manufacturer=manufacturer),
               'categories': Category.objects.all(),
               'manufacturers': Manufacturer.objects.all(),
               'no_category_item_count': Item.objects.filter(category=None).count(),
               'no_manufacturer_item_count': Item.objects.filter(manufacturer=None).count(),
               'manufacturer': manufacturer
           })

class ItemCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['title', 'content', 'image', 'price', 'manufacturer', 'category', 'kcal', 'gram', 'note']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # 로그인한 유저이면 create product 가능하게...
            return super(ItemCreate, self).form_valid(form)
        else:
            return redirect('/product/')

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['title', 'content', 'image', 'price', 'manufacturer', 'category', 'kcal', 'gram', 'note']
    template_name = 'product/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied

class ItemSearch(ItemList) :
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Item.objects.filter(
            Q(title__contains=q) | Q(content__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q}({self.get_queryset().count()})'

        return context