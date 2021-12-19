from django.shortcuts import render

# Create your views here.
from product.models import Item, Comment, Category, Manufacturer


def home_page(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/home_page.html',
        {'recent_items' : recent_items }
    )

def my_page(request):
    if request.user.is_authenticated:
        comment_list = Comment.objects.order_by('-pk')[:]
        user_email = request.user.email
    else:
        comment_list = None
        user_email = None
    return render(request, 'single_pages/my_page.html', {
        'comment_list': comment_list,
        'user_email': user_email
    })

def manufacturer_page(request):
    drink = Item.objects.filter(category='1').count()
    cake = Item.objects.filter(category='2').count()
    icecream = Item.objects.filter(category='3').count()
    bread = Item.objects.filter(category='4').count()
    cookie = Item.objects.filter(category='5').count()

    starbucks = Item.objects.filter(manufacturer='1').count()
    a_twosome_place = Item.objects.filter(manufacturer='2').count()
    baskin_robbins = Item.objects.filter(manufacturer='3').count()
    waffle_university = Item.objects.filter(manufacturer='4').count()
    paris_baguette = Item.objects.filter(manufacturer='5').count()

    return render(request, 'single_pages/manufacturer_page.html',{
        'drink_count': drink,
        'cake_count': cake,
        'icecream_count': icecream,
        'bread_count': bread,
        'cookie_count': cookie,

        'starbucks_count': starbucks,
        'a_twosome_place_count': a_twosome_place,
        'baskin_robbins_count': baskin_robbins,
        'waffle_university_count': waffle_university,
        'paris_baguette_count': paris_baguette,

        'manufacturer_list': Manufacturer.objects.all(),
    })