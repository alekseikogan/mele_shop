from django.urls import reverse

from cart.cart import Cart
from django.shortcuts import render, redirect

from .form import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # очистить корзину
            order_created.delay(order.id)  # пишет письмо
            request.session['order_id'] = order.id  # сохранить номер заказа
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})
    
from easy_thumbnails.files import get_thumbnailer
from shop.models import Product

product = Product.objects.first()
thumbnailer = get_thumbnailer(product.image)
im = thumbnailer.get_thumbnail({'size': (300, 300), 'crop': True})
print(im.url)

