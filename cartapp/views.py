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
    print(order)
    if order:    
        order_items = models.OrderItem.objects.filter(order=order)
        if not order_items:
            return render(request, 'cart/cart_empty.html', {"context":"你的購物車是空的"})
        
        grandtotal = sum(int(item.product.prod_price) * int(item.quantity) for item in order_items)

        context = {
            'order': order,
            'order_items': order_items,
            'grandtotal': grandtotal,
        }
        # 準備去結帳
        if request.method == 'POST':
            order_list = []
            grandtotal = 60
            for item in order_items:
                prod_id = item.product.prod_id
                prod_name = item.product.prod_name
                prod_quantity = request.POST.get(f'input-quantity-{item.product.prod_id}')
                prod_subtotal = int(prod_quantity)*item.product.prod_price
                
                print('quantity:',prod_quantity)
                print('subtotal:',prod_subtotal)
                
                print(prod_id)
                q = models.OrderItem.objects.filter(product_id=prod_id).update(quantity=prod_quantity)
                
                grandtotal += prod_subtotal
                order_list.append({'prod_name':prod_name,
                                'prod_quantity':prod_quantity,
                                'prod_subtotal':prod_subtotal})

            return render(request, 'cart/cartorder.html',{'order_list':order_list,'grandtotal':grandtotal})
        else:
            return render(request, 'cart/cart.html', context)
    else:
        return render(request, 'cart/cart_empty.html', {"context":"你的購物車是空的"})
    
    
@login_required(login_url='Login')
def empty_cart(request):
    try:
        order = models.OrderModel.objects.get(user=request.user, status='cart')
        order.orderitem_set.all().delete()  # 删除所有訂單
        order.delete()  
    except models.OrderModel.DoesNotExist:
        pass 
    
    return redirect('Cart')

@login_required(login_url='Login')
def remove_from_cart(request, productid):
    order = models.OrderModel.objects.get(user=request.user, status='cart')
    product = models.ProductModel.objects.get(prod_id=productid)
    order_item = models.OrderItem.objects.get(order=order, product=product)
    order_item.delete()  # 删除指定的購買項目

    return redirect('Cart')

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
    if request.method == 'POST':
        order = models.OrderModel.objects.get(user=request.user, status='cart')
        order_items = models.OrderItem.objects.filter(order=order)


        grandtotal = sum(item.product.prod_price * item.quantity for item in order_items)+60
        context = {
            'order': order,
            'order_item':order_items,
            'grandtotal':grandtotal,
        }
        first_name = request.POST.get('billing_first_name')
        last_name = request.POST.get('billing_last_name')
        username = first_name + ' ' + last_name
        
        address = request.POST.get('billing_address')
        phone = request.POST.get('billing_phone')
        email = request.POST.get('billing_email')
        
        """
        將填寫的個人資訊寫入資料表並更新訂單狀態(status=order)...
        """
        order.address = address
        order.phone = phone
        order.email = email
        order.status = 'ordered'
        order.grandtotal = grandtotal
        order.save()
    
        email_to_customer(email, order.id, order_items, username, grandtotal)
        email_to_seller(username, order_items, grandtotal)
        
        return render(request, 'cart/cartok.html')   
    return render(request, 'cart/cartorder.html', context)

def email_to_customer(mailto, orderid, order_items, username, grandtotal):
    mailsubject = "動漫購物網 - 訂單通知"
    mailcontent = f"感謝{username}的光臨，您已經成功完成訂購程序\n您的訂單編號為:{orderid}\n"
    
    for item in order_items:
        prod_name = item.product.prod_name
        prod_quantity = item.quantity
        prod_price = item.product.prod_price
        subtotoal = int(prod_quantity)*prod_price
        mailcontent += prod_name + ' ' + '數量×'+str(prod_quantity) + f' 小計:{subtotoal}元' + '\n'
    mailcontent += f'總共{grandtotal}元(包含運費60元)'
    send_email_user.send_simple_message(mailto, mailsubject, mailcontent)
    
def email_to_seller(username, order_items, grandtotal):
    orderuser = username
    mailcontent_toseller = orderuser + "提交了訂單，訂單內容如下:\n"

    for item in order_items:
        prod_name = item.product.prod_name
        prod_quantity = item.quantity
        prod_price = item.product.prod_price
        subtotoal = int(prod_quantity)*prod_price
        mailcontent_toseller += prod_name + ' ' + '數量×'+str(prod_quantity) + f' 小計:{subtotoal}元' + '\n'
    mailcontent_toseller += f'總共{grandtotal}元(包含運費60元)'
    send_email_user.send_simple_message('Lutingyang@gmail.com', orderuser+"的訂單", mailcontent_toseller)
