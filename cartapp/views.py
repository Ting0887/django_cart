from django.contrib.auth.hashers import check_password
from django.core import paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render,HttpResponse,get_object_or_404
from django.core.paginator import Paginator,Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from cartapp import models,send_email_user, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.forms import modelformset_factory
import pandas as pd

orderlist = []

# 首頁
def index(request):
    if 'cartlist' in request.session:
        cartlist = request.session['cartlist']

    productall = models.ProductModel.objects.all()    
    print(productall)
    # all products do pagination
    paginator = Paginator(productall,16)
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {"products":products}
    return render(request,"index.html",context)

def search_product(request):
    search = request.GET.get('q')
    print('search keyword:',search)
    search_result = []
    
    search_result = models.ProductModel.objects.filter(prod_name__icontains=search)
    if not search_result.exists():
        message = "此商品不存在"
        return render(request, 'index.html', {'message': message})
    else:
        # all products do pagination
        paginator = Paginator(search_result,16)
        page_number = request.GET.get('page')
        try:
            search_products = paginator.page(page_number)
        except PageNotAnInteger:
            search_products = paginator.page(1)
        except EmptyPage:
            search_products = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {'search_products': search_products})
    
def detail(request, prod_id=None):
    product = models.ProductModel.objects.get(prod_id=prod_id)
    return render(request,"cart/detail.html",locals())

@login_required(login_url='Login')
def cart(request):
    order = models.OrderModel.objects.filter(user=request.user, status='cart').first()
    if order:    
        order_items = models.OrderItem.objects.filter(order=order)
  
        grandtotal = sum(item.product.prod_price * item.quantity for item in order_items)

        context = {
            'order': order,
            'order_items': order_items,
            'grandtotal': grandtotal,
        }
        return render(request, 'cart/cart.html', context)
    elif request.method == 'POST':
        print('checkout')
    else:
        return render(request, 'cart/cart_empty.html', {"context":"你的購物車是空的"})
    
    
@login_required(login_url='Login')
def empty_cart(request):
    try:
        order = models.OrderModel.objects.get(user=request.user, status='cart')
        order.orderitem_set.all().delete()  # 删除所有订单项
        order.delete()  # 删除订单
    except models.OrderModel.DoesNotExist:
        pass  # 如果购物车订单不存在，则什么也不做
    
    return redirect('Cart')  # 重定向到购物车页面

@login_required(login_url='Login')
def remove_from_cart(request, productid):
    try:
        order = models.OrderModel.objects.get(user=request.user, status='cart')
        product = models.ProductModel.objects.get(prod_id=productid)
        order_item = models.OrderItem.objects.get(order=order, product=product)
        order_item.delete()  # 删除指定的订单项
    except (models.OrderModel.DoesNotExist, models.ProductModel.DoesNotExist, models.OrderItem.DoesNotExist):
        pass
    
    return redirect('Cart')  # 重定向到购物车页面

@login_required(login_url='Login')
def addtocart(request, ctype=None, productid=None):
    product = models.ProductModel.objects.get(prod_id=productid)
    
    # 检查当前用户是否有未完成的购物车订单，如果没有则创建一个新的订单
    order, created = models.OrderModel.objects.get_or_create(user=request.user, status='cart', grandtotal=0)

    # 检查购物车中是否已经有此商品，如果有则增加数量，如果没有则创建一个新的 OrderItem
    order_item, item_created = models.OrderItem.objects.get_or_create(order=order, product=product, quantity=1)
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    
    return redirect('/cart')

@login_required(login_url='Login')
def cartorder(request):
    order = models.OrderModel.objects.get(user=request.user, status='cart')
    order_items = models.OrderItem.objects.filter(order=order)


    grandtotal = sum(item.product.prod_price * item.quantity for item in order_items)
    context = {
        'order': order,
        'order_item':order_items,
        'grandtotal':grandtotal,
    }
   
    
    return render(request, 'cart/cartorder.html', context)


    """ mailsubject = "動漫購物網 - 訂單通知"
    mailcontent = "感謝您的光臨，您已經成功完成訂購程序\n您的訂單編號為:" + str(orderid)
    send_email_user.send_simple_message(mailto, mailsubject, mailcontent)
    
    # send to seller
    orderuser = firstname +' '+ lastname
    mailcontent_toseller = orderuser + "提交了訂單，訂單內容如下:\n"
    # order detail
    for list in cartlist:
        product_name = list[1]
        quantity = list[4]
        subtotoal = list[5]
        mailcontent_toseller += product_name + ' ' + '數量×'+str(quantity) + f' 小計{subtotoal}元' + '\n'
    mailcontent_toseller += f'總共{grandtotal}元'
    send_email_user.send_simple_message('Lutingyang@gmail.com', orderuser+"的訂單", mailcontent_toseller)"""
    
    return render(request,'cart/cartorder.html',locals())

@login_required(login_url='Login')
def order_confirmation(request, order_id):
    order = get_object_or_404(models.OrderModel, id=order_id, user=request.user)
    order_items = models.OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    
    return render(request, 'cart/order_confirmation.html', context)
