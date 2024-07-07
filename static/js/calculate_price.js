function show_subtotal(price, product_id){
    quantity = document.getElementById('input-quantity-'+product_id).value;
    document.getElementById('product_' + product_id).innerHTML = `$${price * quantity}`;
    show_grandtotoal();
}

function show_grandtotoal(){
    let grandtotal = 0;
    let sub = document.querySelectorAll('.product-subtotal');
    for(var i=0; i<sub.length; i++){
        grandtotal += parseInt(sub[i].textContent.replace('$',''));
    }
    shipping_fee = parseInt(document.getElementById('shipping_fee').textContent.replace('$',''));
    document.getElementById('grandtotal').innerHTML = `$${grandtotal+shipping_fee}`;
}

function updateCartItem(input) {
    // 提交表單以更新購物車數據
    document.getElementById('cart-form').submit();
  }