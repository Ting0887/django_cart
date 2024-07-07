function doublecheck(event){
    let userConfirmed = confirm("確認要清除購物車嗎?");
    if (userConfirmed) {
        // 如果用户确认清除购物车，则执行清除购物车的操作
        // 例如：发送请求到服务器清除购物车
        alert('购物车已清除');
        // 这里你可以添加你实际的清除购物车的代码，例如发送一个请求到服务器
        // window.location.href = '/empty_cart/'; // 或者其他的实际操作
    } else {
        // 如果用户取消操作，则不做任何事情
        alert('操作取消');
        return false;
        event.preventDefault(); 
    }
}