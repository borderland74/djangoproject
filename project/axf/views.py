from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from axf.models import SlideShow,Maindescription,Product,CategorieGroup,Childgroup,User,Address,Cart,Order
from dysms_python.demo_sms_send import send_sms
from django.contrib.auth import logout
import random
import uuid
# Create your views here.
def home(request):
    slideList = SlideShow.objects.all()
    mainList =Maindescription.objects.all()
    for item in mainList:
        products = Product.objects.filter(categoryId=item.categoryID)
        item.product1 = products.get(productId=item.product1)
        item.product2 = products.get(productId=item.product2)
        item.product3 = products.get(productId=item.product3)
    return render(request,'home/home.html',{"slideList":slideList,"mainList":mainList})

def cart(request):
    # 判断是否登录
    tokenValue = request.COOKIES.get("token")
    if  not tokenValue:
        # 说明没登录
        return redirect("/login/")
    try:
        user = User.objects.get(tokenValue=tokenValue)
    except User.DoesNotExist as e:
        return redirect("/login/")
    carts = Cart.objects.filter(user__tokenValue=tokenValue)
    return render(request, "cart/cart.html", {"carts":carts})
def changecart(request, flag):
    num = 1
    if flag == "1":
        num = -1

    # 判断是否登录
    tokenValue = request.COOKIES.get("token")
    if not tokenValue:
        # 说明没登录
        return JsonResponse({"error":1})
    try:
        user = User.objects.get(tokenValue=tokenValue)
    except User.DoesNotExist as e:
        return JsonResponse({"error": 2})

    gid = request.POST.get("gid")
    cid = request.POST.get("cid")
    pid = request.POST.get("pid")

    product = Product.objects.filter(categoryId=gid,childCid=cid).get(productId=pid)

    try:
        cart = Cart.objects.filter(user__tokenValue=tokenValue).filter(product__categoryId=gid).filter(product__childCid=cid).get(product__productId=pid)
        if flag == "2":
            if product.storeNums == "0":
                return JsonResponse({"error": 0, "num": cart.num})
        #以买过该商品，得到了该购物车数据
        cart.num = cart.num + num
        product.storeNums = str(int(product.storeNums) - num)
        product.save()
        if cart.num == 0:
            cart.delete()
        else:
            cart.save()

    except Cart.DoesNotExist as e:
        if flag == "1":
            return JsonResponse({"error":0, "num":0})
        #找一个可用的订单  isDelete为False，flag为0，在当前用户中的所有订单中最多只能有一个订单为0
        try:
            order = Order.objects2.filter(user__tokenValue=tokenValue).get(flag=0)
        except Order.DoesNotExist as e:
            #没有可用订单
            orderId = str(uuid.uuid4())
            address = Address.objects.get(pk=1)
            order = Order.create(orderId,user,address,0)
            order.save()
        #没有购买过该商品，需要创建该条购物车数据
        cart = Cart.create(user,product,order,1)
        cart.save()
        product.storeNums = str(int(product.storeNums) - num)
        product.save()
    # 告诉客户端添加成功
    return JsonResponse({"error":0, "num":cart.num})



def confirmOrder(request):
    tokenValue = request.COOKIES.get("token")

    #找到当前可用的订单
    order = Order.objects2.filter(user__tokenValue=tokenValue).get(flag=0)
    order.flag = 1
    order.save()

    #属于该订单的购物城选中数据的isOrder置为False
    carts = Cart.objects.filter(user__tokenValue=tokenValue).filter(order=order).filter(isCheck=True)
    for cart in carts:
        cart.isOrder = False
        cart.save()

    #将没有被选中的数据添加到新的订单中
    newOrder = Order.create(str(uuid.uuid4()), User.objects.get(tokenValue=tokenValue), Address.objects.get(pk=1), 0)
    newOrder.save()
    oldCarts = Cart.objects.filter(user__tokenValue=tokenValue)
    for cart in oldCarts:
        cart.order = newOrder
        cart.save()

    return JsonResponse({"error":0})



def changecart2(request):
    cartid = request.POST.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.isCheck = not cart.isCheck
    cart.save()
    return JsonResponse({"error":0,"flag":cart.isCheck})












def market(request,gid,cid,sid):
    # tokenValue = request.COOKIES.get("token")
    # if not tokenValue:
    #     # 说明没登录
    #     return JsonResponse({"error": 1})
    # try:
    #     user = User.objects.get(tokenValue=tokenValue)
    # except User.DoesNotExist as e:
    #     return JsonResponse({"error": 2})
    # carts = Cart.objects.filter(user__tokenValue=tokenValue)
    # product=Product.objects.all()
    #
    # for i in carts:
    #     product1 = product.get(pk=i.product.id)
    #
    #

    leftCategorieList = CategorieGroup.objects.all()
    products =Product.objects.filter(categoryId=gid)
    if cid !="0":
        products = products.filter(childCid=cid)
    if sid=="1":
        products = products.order_by("price")
    elif sid=="2":
        products = products.order_by("-price")
    childs = Childgroup.objects.filter(categorie__categorieID=gid)

    return render(request,'market/market.html',{"leftCategorieList":leftCategorieList,"products":products,"childs":childs,"gid":gid,"cid":cid,"sid":sid})
def detail(request,gid,pid):
    products = Product.objects.filter(categoryId=gid)
    products = products.get(productId=pid)
    return render(request,'market/detail.html',{"products":products})

def mine(request):
    phoneNum = request.session.get("phoneNum",default = "未登录")
    return render(request,'mine/mine.html',{"phoneNum":phoneNum})
def addressDetail(request):
    phoneNum = request.session.get("phoneNum")
    if phoneNum:
        user = User.objects.get(phoneNum=phoneNum)
        address = user.address_set.all()
        return render(request,"mine/addressDetail.html",{"address":address})
    else:
        return redirect("/login/")
def addaddress(request):
    if request.method =="GET":
        return render(request,"mine/addaddress.html")
    else:

        name = request.POST.get("name")
        sex = request.POST.get("sex")
        if sex =="0":
            sex = False
        else:
            sex = True
        phoneNum = request.POST.get("phoneNum")
        postCode = request.POST.get("postCode")
        address = request.POST.get("address")
        province = request.POST.get("province")
        city = request.POST.get("city")
        county = request.POST.get("county")
        street = request.POST.get("street")
        detailAddress = province + city + county + street + address
        phone = request.session.get("phoneNum")
        usr = User.objects.get(pk=phone)
        add = Address.create(name,sex,phoneNum,postCode,address,province,city,county,street,detailAddress,usr)
        add.save()
        return redirect("/addressDetail/")

def quit(request):
    res = redirect("/mine/")
    logout(request)
    res.delete_cookie("token")
    return res
def login(request):
    if request.method =="GET":
        if request.is_ajax():
            phoneNum = request.GET.get("phoneNum")
            # rand_str = random.randrange(1000, 10000)
            rand_str = "4125"
            # __business_id = uuid.uuid1()
            # params = "{\"code\":\"%s\"}" % rand_str
            # send_sms(__business_id, phoneNum, "捷豹快快", "SMS_135740070", params)
            request.session["code"] = rand_str
            return JsonResponse({"data":"ok"})
        else:
            return render(request,'mine/login.html')

    else:
        phoneNum = request.POST.get("username")
        passwd   = request.POST.get("passwd")
        code     = request.session.get("code")
        # print(code)
        # print(passwd)
        # print(type(code))
        # print(type(passwd))
        if passwd==code:
            # print("asdasd")
            uuidStr = uuid.uuid4()
            try:
                user = User.objects.get(phoneNum=phoneNum)
                user.tokenValue = uuidStr
                user.save()
            except User.DoesNotExist as e:
                user = User.create(phoneNum,None,uuidStr,"asdawdwd")
                user.save()

            request.session["phoneNum"] = phoneNum
            response = redirect("/mine/")
            # 将tokenValue写入cookie
            response.set_cookie("token", uuidStr)
            return response
        else:
            return redirect("/login/")
