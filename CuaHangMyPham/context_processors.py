from .models import Category, Brand, Cart

def menu(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return {'categories': categories, 'brands': brands}


def cart_item_count(request):
    total_items = 0
    if 'user' in request.session:
        user_id = request.session['user']
        total_items = Cart.objects.filter(user_id=user_id).count()
    return {'cart_item_count': total_items}