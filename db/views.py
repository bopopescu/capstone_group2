import base64

from PIL import Image
import io
from django.core.serializers import json
from django.db import connection


import datetime
import time

try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse
from django.http import JsonResponse
from .models import User, Likes, Order, Product,Hashtag,Seller,Wishlist,Seller, Commentrating, Bankaccount

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


class USER(object):
    phoneNumber = "1"
    password = "1"

    # The class "constructor" - It's actually an initializer
    def __init__(self, phoneNumber, password):
        self.phoneNumber = phoneNumber
        self.password = password
        print("init")

    def toJSON(self):
        return {
            'phoneNumber': self.phoneNumber,
            'password': self.password,

        }


def make_user(phoneNumber, password):
    user = USER(phoneNumber, password)
    return user


class USER2(object):
    userID = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, userID):
        self.userID = userID

    def toJSON(self):
        return {
            'userID': self.userID,

        }


def make_user2(userID):
    user = USER2(userID)
    return user


class PREFERENCE(object):
    catID = 0
    likeFirstHand = True

    # The class "constructor" - It's actually an initializer
    def __init__(self, catID, likeFirstHand):
        self.catID = catID
        self.likeFirstHand = likeFirstHand

    def toJSON(self):
        return {
            'catID': self.catID,
            'likeFirstHand': self.likeFirstHand

        }


def make_preference(catID, likeFirstHand):
    preference = PREFERENCE(catID, likeFirstHand)
    return preference


# class PRODREC(object):
#     productID=0
#     productPic=""
#
#     # The class "constructor" - It's actually an initializer
#     def __init__(self,productID,productPic):
#         self.productID = productID
#         self.productPic=productPic
#
#     def toJSON(self):
#         return {
#             'productID': self.productID,
#             'productPic' : self.productPic
#
#                }
# def make_prodrec(productID,productPic):
#     prodrec = PRODREC(productID,productPic)
#     return prodrec

def makeDict(a):
    new_dict = []
    for i in a:
        new_dict.append(i.toJSON())
    return new_dict


# function0:find userID from phone
@ensure_csrf_cookie
@csrf_exempt
def getuid(request):
    data1 = request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content1 = dataJson['phoneNum']
    U, = User.objects.filter(phoneNumber=content1)
    uid: [USER2] = []
    user_a = make_user2(U.userID)
    uid.append(user_a)
    a = {'user2': makeDict(uid)}
    print(a)
    return JsonResponse(a)


# function1 :register
@ensure_csrf_cookie
@csrf_exempt
def register(request):
    data1 = request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content1 = dataJson['phoneNum']
    content2 = dataJson['password']
    U = User.objects.create(phoneNumber=content1, password=content2)
    return HttpResponse("success")


users: [USER] = []


# function2 :login
@ensure_csrf_cookie
@csrf_exempt
def log_in(request):
    data = User.objects.all()

    try:
        for row in data:
            spn = row.phoneNumber
            print("phoneNum")
            print(spn)
            spw = row.password
            print("password")
            print(spw)
            user_a = make_user(spn, spw)
            users.append(user_a)

    except:
        print("Error: unable to fetch data")

    a = {'users': makeDict(users)}
    print(a)
    return JsonResponse(a)


# function3 :preference
@ensure_csrf_cookie
@csrf_exempt
def addpref(request):
    data1 = request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content1 = dataJson['phoneNum']
    content2 = dataJson['catID']
    content3 = dataJson['likeFirstHand']
    buyer, = User.objects.filter(phoneNumber=content1)
    buyerID1 = buyer.userID
    L = Likes.objects.create(buyerID=buyerID1, catID=content2, likeFirstHand=content3)
    return HttpResponse("success")


# function4 :check preference
@ensure_csrf_cookie
@csrf_exempt
def checkforpref(request):
    preferences: [PREFERENCE] = []
    data2 = request.body.decode('utf-8')
    dataJson2 = json.loads(data2)
    content1 = dataJson2['userID']
    U, = Likes.objects.filter(buyerID=content1)
    pref1 = make_preference(U.catID, U.likeFirstHand)
    preferences.append(pref1)
    a = {'PREF': makeDict(preferences)}
    return JsonResponse(a)


# function5 : getProductRec
@csrf_exempt
def getprodrec(request):
    data3 = request.body.decode('utf-8')
    dataJson3 = json.loads(data3)
    content1 = dataJson3['catID']
    content2 = dataJson3['likeFirstHand']
    if (content2):
        content3 = 0
    else:
        content3 = 1
    U = Product.objects.filter(catID=content1, secondHandStatus=content3,isActive=1)
    list: [Product] = []
    for x in U:
        list.append(x)
    print(list)
    list2: [int] = []
    for a in list:
        o = a.productID
        list2.append(o)

    a = {'ProdRec': [list2]}

    return JsonResponse(a)

#function6 : getPicByID
@csrf_exempt
def getpicbyproductid(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['productID']
    print(content1)
    U, = Product.objects.filter(productID=content1)
    print(U)
    pic =U.productPic
    # image = Image.open(io.BytesIO(pic))

    response = HttpResponse(pic, content_type='jpeg')

    response['Content-Disposition'] = 'attachment; filename="image.jpeg"'
    return response

#function7 : getAllCurrentProduct
@csrf_exempt
def getallprod(request):
    U = Product.objects.filter(isActive=1)
    list: [Product] = []
    for x in U:
        list.append(x)
    print(list)
    list2: [int] = []
    for a in list:
        o = a.productID
        list2.append(o)

    a = {'ProdAll': [list2]}

    return JsonResponse(a)

#function8 : getFilteredProduct
@csrf_exempt
def getfilteredproduct(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['catID']
    content2 = dataJson['subcatID']
    content3 = dataJson['minP']
    content4 = dataJson['maxP']
    U = Product.objects.filter(isActive=1,catID=content1,subcatID=content2,price__gt=content3,price__lt=content4)
    list: [Product] = []
    for x in U:
        list.append(x)
    print(list)
    list2: [int] = []
    for a in list:
        o = a.productID
        list2.append(o)

    a = {'ProdFilterID': [list2]}
    print(a)
    return JsonResponse(a)

#function9 :getidbyhashtag
@csrf_exempt
def getidbyhashtag(request):
    listH: [int]=[]
    listP:[int]=[]
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['hashtag']
    print(content1)
    U=Hashtag.objects.filter(hashtag=content1)
    print(U)
    V=Product.objects.filter(isActive=1)
    print(V)
    for t in V:
        listP.append(t.productID)
    for i in U :
        print(i.productID)
        for p in listP:
            if(i.productID==p):
                listH.append(i.productID)
                print(i.productID)

    a = {'ProdHashtag': [listH]}
    return JsonResponse(a)

#function10 :checkifseller
@csrf_exempt
def checkifseller(request):
    found="no"
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['userID']
    U=Seller.objects.all()
    for x in U:
        if(x.userID==content1):
            return HttpResponse("yes")
    return HttpResponse(found)
@csrf_exempt
#function11 : getProductInfo
def getproductinfo(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['productID']
    U,=Product.objects.filter(productID=content1)
    print("getproductInfo")
    print(U)
    sid=U.sellerID
    print(sid)
    price=U.price
    print(price)
    secondHand=U.secondHandStatus
    print(secondHand)
    deliveryfee=U.deliveryFee
    print(deliveryfee)
    catID=U.catID
    print(catID)
    des = U.des
    print(des)

    return JsonResponse({"sellerid":sid,"price":price,"secondHandStatus":secondHand, "deliveryFee":deliveryfee,"catID":catID,"des":des})

@csrf_exempt
#function12 : getCurrentWishlist
def getwishlistid(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['userID']
    U = Wishlist.objects.filter(buyerID=content1)
    list: [Wishlist] = []
    for x in U:
        list.append(x)
    print(list)
    list2: [int] = []
    for a in list:
        o = a.productID
        list2.append(o)

    a = {'WishList': [list2]}
    return JsonResponse(a)

@csrf_exempt
#function13 : addToWishList
def addtowishlist(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['productID']
    content2 = dataJson['userID']
    U = Wishlist.objects.create(productID=content1,buyerID=content2)
    return HttpResponse("success")

@csrf_exempt
#function13 : removefromWishList
def removefromwishlist(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['productID']
    Wishlist.objects.filter(productID=content1).delete()
    return HttpResponse("success")


@csrf_exempt
#function14: set isActive=false
def setifactivefalse(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['productID']
    Product.objects.filter(productID=content1).update(isActive=False)
    return HttpResponse("success")

@csrf_exempt
#function15 : getOrderedWishList
def getorderedwishlist(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['userID']
    content2 = dataJson['orderBy']
    if(content2=="price"):
        print("byprice")
        cursor = connection.cursor()
        cursor.execute("SELECT db_Product.productID FROM db_Wishlist JOIN db_Product ON db_Wishlist.productID=db_Product.productID WHERE db_Wishlist.buyerID="+str(content1)+" ORDER BY db_Product.price ASC ;")
        solution=cursor.fetchall()

    else:
        print("bycat")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT db_Product.productID FROM db_Wishlist JOIN db_Product ON db_Wishlist.productID=db_Product.productID WHERE db_Wishlist.buyerID="+str(content1)+" ORDER BY db_Product.catID ASC ;")
        solution = cursor.fetchall()
    list: [Wishlist] = []
    for x in solution:
        list.append(x)
    print(list)
    list2: [int] = []
    for a in list:
        print(a)
        o = a[0]
        list2.append(o)

    a = {'OrderedWishList': [list2]}
    return JsonResponse(a)

@csrf_exempt
#function15 : removefromMyWishList
def removefrommywishlist(request):
    data = request.body.decode('utf-8')
    dataJson = json.loads(data)
    content1 = dataJson['productID']
    content2 = dataJson['buyerID']
    Wishlist.objects.filter(productID=content1,buyerID=content2).delete()
    return HttpResponse("success")

###################POPP##########################
#class to create commentrating object
class cr(object):
    comment = ""
    rating = 0.0

    # The class "constructor" - It's actually an initializer
    def __init__(self,comment, rating):
        self.comment = comment
        self.rating = rating

    def toJSON(self):
        return {
            'comment': self.comment,
            'rating': self.rating,
        }

def makeCR(a):
    new_dict = []
    for i in a:
        new_dict.append(i.toJSON())
    return new_dict


# seller's profile
@ensure_csrf_cookie
@csrf_exempt
def sellerprofile(request,userid):
    user = User.objects.filter(userID=userid)
    user, = user
    uid = user.userID
    phone = user.phoneNumber
    seller = Seller.objects.filter(userID=userid)
    seller, = seller
    star = seller.avgstar
    cAndR = Commentrating.objects.filter(sellerID=userid)
    comment = []
    for each in cAndR:
        comment.append(cr(each.comment,each.star))

    comment = makeCR(comment)

    print(uid)
    print(phone)
    print(star)
    print(comment)

    response = {'uid': uid,'phone':phone,'star':star,'comment':comment}

    print(response)

    return JsonResponse(response)

# seller's product
@ensure_csrf_cookie
@csrf_exempt
def sellerproduct(request,userid,picid):

    products = Product.objects.filter(sellerID=userid,productID=picid)
    products, = products
    pic = products.productPic


    response = HttpResponse(pic, content_type='jpeg')
    response['Content-Disposition'] = 'attachment; filename="image.jpg"'

    return response


    # get seller product id
@ensure_csrf_cookie
@csrf_exempt
def selproductid(request, userid):
    product = []
    print("user:" + userid)
    products = Product.objects.filter(sellerID=userid)
    print("count" + str(products.count()))

    for a in products:
        print(a.isActive)
        if a.isActive:
            product.append(int(a.productID))
    response = {'id': [product]}
    print(response)
    return JsonResponse(response)

#add product's photo
@ensure_csrf_cookie
@csrf_exempt
def addproduct(request,userid):
    data = request.POST
    file =request.FILES.getlist('upload')[0].file

    des = data.get('description')
    price = data.get('price')
    cat = data.get('cat')
    subcat = data.get('subcat')
    status = data.get('status')
    fee = data.get('fee')
    tag = data.get('hashtag')

    print(cat)
    print(subcat)
    #return bytes
    value = file.getvalue()

    #save photo in computer
    # path = default_storage.save('image.jpg', ContentFile(file.read()))

    #keep the photo in db
    f = Product.objects.create(price=int(price),secondHandStatus=int(status),deliveryFee=float(fee),catID=int(cat),subcatID=int(subcat),sellerID=userid,isActive=1,productPic=value,des=des)

    #keep hashatag in db
    h = Hashtag.objects.create(productID=f.productID,hashtag=tag)

    print("please")
    response = {'id':f.productID}
    print(response)
    return JsonResponse(response)




#payment's photo
@ensure_csrf_cookie
@csrf_exempt
def addpayment(request,userid):
    data = request.POST
    file =request.FILES.getlist('upload')[0].file
    bankid =data.get('bankid')
    productid = data.get('pid')
    amount =data.get('amount')
    date =data.get('date')
    timestamp = time.mktime(datetime.datetime.strptime(date, "%d-%m-%Y %H:%M").timetuple())
    # print(bankid)
    # print(amount)
    # print(date)
    print(timestamp)

    #return bytes
    value = file.getvalue()

    #save photo in computer
    # path = default_storage.save('image.jpg', ContentFile(file.read()))

    #keep the photo in db
    f = Order.objects.create(confirmedStatus=0,amount=int(amount),paymentTimeStamp=date,paymentSlip=value,buyerID=userid,productID=productid,bankid=bankid)

    # response = {'id':f.productID}
    return HttpResponse(f.orderID)

###################FIRNFIRN##########################
class ORDER(object):
    orderID = 0
    confirmedStatus = False

    # The class "constructor" - It's actually an initializer
    def __init__(self, orderID, confirmedStatus):
        self.orderID = orderID
        self.confirmedStatus = confirmedStatus

    def toJSON(self):
        return {
            'orderID': self.orderID,
            'confirmedStatus' : self.confirmedStatus,

        }
def make_order(orderID, confirmedStatus):
        order = ORDER(orderID, confirmedStatus)
        return order

order1 : [Order]=[]

@ensure_csrf_cookie
@csrf_exempt
def order(request):
    data1 = request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content1 = dataJson['userID']
        # create new list for getting each object out of U
        # U ja ork ma pen [<Order: Order object>, <Order: Order object>] tong aow data ork ma
    U = list(Order.objects.filter(buyerID=content1, confirmedStatus=0))

    print(U)
    order1: [Order] = []
        # put data from U into another list
    try:
        for a in U:
            o = str(a.orderID)
            print(o)
            c = bool(a.confirmedStatus)
            print(c)
            orderA = make_order(o,c)
            order1.append(orderA)
        print(order1)
    except:
        print("Error: unable to fetch data")
    a = {'orderID': makeDict(order1)}
    print(a)
        # return HttpResponse(U)

        # wela ja send data to xcode
    return JsonResponse(a)

@ensure_csrf_cookie
@csrf_exempt
def profile(request):
        data1 = request.body.decode('utf-8')
        dataJson = json.loads(data1)
        content1 = dataJson['userID']
        # create new list for getting each object out of U
        # U ja ork ma pen [<Order: Order object>, <Order: Order object>] tong aow data ork ma
        # User has to be the same with in models
        U = list(User.objects.filter(userID=content1))
        print(U)

        # put data from U into another list
        try:
            for a in U:
                phone = str(a.phoneNumber)
                print(phone)
                uid = str(a.userID)
                print(uid)
                u = make_profile(uid, phone)
                profile1.append(u)
                print(profile1)
        except:
            print("Error: unable to fetch data")
        b = {'profile': makeDict(profile1)}
        print(b)
        # return HttpResponse(U)

        # wela ja send data to xcode
        return JsonResponse(b)

class PROFILE(object):
    userID ="0"
    phoneNumber="1"
    # The class "constructor" - It's actually an initializer
    def __init__(self,userID, phoneNumber):
        self.userID = userID
        self.phoneNumber = phoneNumber
        print("init")


    def toJSON(self):
        return {
            'userID': self.userID,
            'phoneNumber': self.phoneNumber,
               }
def make_profile(userID, phoneNumber):
    profile = PROFILE(userID, phoneNumber)
    return profile
profile1 : [profile]=[]

def makeDict(a):
    new_dict = []
    for i in a:
        new_dict.append(i.toJSON())
    return new_dict

@ensure_csrf_cookie
@csrf_exempt
def updateStatus(request):
    data1=request.body.decode('utf-8')
    dataJson=json.loads(data1)
    content1 = dataJson['orderID']
    to_update = Order.objects.filter(orderID=content1, confirmedStatus=False).update(confirmedStatus=True)
    # t = Order.objects.get(orderID=1)
    # print(t.confirmedStatus)
    # print(t.orderID)
    # t.confirmedStatus = True
    # t.save(confirmedStatus=['True'])
    # change field
     # this will update only
    print("Updated")

    return HttpResponse("success")

#function 5 comment
class PRODUCT(object):
    # productID = 0
    sellerID = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self,  sellerID,):
        # self.productID = productID
        self.sellerID = sellerID

    def toJSON(self):
        return {
            # 'productID': self.productID,
            'sellerID' : self.sellerID,
        }

def make_product(sellerID):
        product = PRODUCT(sellerID)
        return product

@ensure_csrf_cookie
@csrf_exempt
def product(request):
    data1 = request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content3 = dataJson['orderID']
    M = list(Order.objects.filter(orderID=content3))
    print(M)
    product1: [Product] = []
    try:
        for a in M:
                o = str(a.orderID)
                print(o)
                p = str(a.productID)
                print(p)
#
    except:
            print("Error: unable to fetch data")

    L = list(Product.objects.filter(productID=p))
#         # return HttpResponse(U)
    try:
            for c in L:
                s = str(c.sellerID)
                print(s)
                productA = make_product(s)
                product1.append(productA)
    except:
            print("pung")
    a = {'product': makeDict(product1)}
    print(a)
#         # wela ja send data to xcode
    return JsonResponse(a)


class COMMENT(object):
    comment=" "
    star="1.0"
    sellerID= "1"
    orderID= "1"
    buyerID= "1"
    # The class "constructor" - It's actually an initializer
    def __init__(self,comment, star, sellerID, buyerID, orderID):
        self.comment = comment
        self.star = star
        self.sellerID = sellerID
        self.buyerID = buyerID
        self.orderID = orderID
        print("init")


    def toJSON(self):
        return {
            'comment': self.comment,
            'star': self.star,
            'sellerID': self.sellerID,
            'buyerID': self.buyerID,
            'orderID': self.orderID,

               }
def make_comment(comment,star, sellerID, buyerID, orderID):
    comment = COMMENT(comment,star,sellerID, buyerID, orderID)
    return comment


@ensure_csrf_cookie
@csrf_exempt
def comment(request):
    data1=request.body.decode('utf-8')
    dataJson=json.loads(data1)
    content1 = dataJson['comment']
    content2 = dataJson['star']
    content3 = dataJson['sellerID']
    content4 = dataJson['orderID']
    content5 = dataJson['buyerID']
    # print(content2)
    # print(content1)
    # print(content2)
    # print(content3)
    num = float(content2)
    print(num)
    C2 = Commentrating.objects.create(comment=content1, star=num, sellerID = content3, buyerID = content5, orderID = content4)
    print(C2)
    print("updated")
    return HttpResponse("success")

# function 6 edit phone
class PHONE(object):
    phoneNumber = "1"

    # The class "constructor" - It's actually an initializer
    def __init__(self, phoneNumber):
        self.phoneNumber = phoneNumber
        print("init")

    def toJSON(self):
        return {
            'phoneNumber': self.phoneNumber,
        }

def make_phone(phoneNumber):
        phone = PHONE(phoneNumber)
        return phone

@ensure_csrf_cookie
@csrf_exempt
def editPhone(request):
    data1=request.body.decode('utf-8')
    dataJson=json.loads(data1)
    content1 = dataJson['newNum']
    content2 = dataJson['oldNum']
    U = User.objects.filter(phoneNumber=content2).update(phoneNumber=content1)
    print(U)
    return HttpResponse("success")

@ensure_csrf_cookie
@csrf_exempt
def editPass(request):
    data1=request.body.decode('utf-8')
    dataJson=json.loads(data1)
    content1 = dataJson['password']
    content2 = dataJson['phoneNumber']
    U = User.objects.filter(phoneNumber=content2).update(password=content1)
    print(U)
    return HttpResponse("success")

class SELLER(object):
    sellerID= "1"
    emailAddress = " "
    bank = " "

    # The class "constructor" - It's actually an initializer
    def __init__(self, sellerID, email, bank):
        self.bank = bank
        self.sellerID = sellerID
        self.email = email
        print("init")

    def toJSON(self):
        return {
            'sellerID' : self.sellerID,
            'bank': self.bank,
            'email' : self.email,
        }

def make_seller( sellerID, email, bank):
        seller = SELLER( sellerID, email, bank)
        return seller

@ensure_csrf_cookie
@csrf_exempt
def editEmail(request):
    data1=request.body.decode('utf-8')
    dataJson=json.loads(data1)
    content1 = dataJson['sellerID']

    num = int(content1)
    content2 = dataJson['email']
    U = Seller.objects.filter(userID=num).update(emailAddress=content2)
    print(U)
    return HttpResponse("success")


@ensure_csrf_cookie
@csrf_exempt
def editBank(request):
    data1=request.body.decode('utf-8')
    dataJson=json.loads(data1)
    content1 = dataJson['bankAcc']
    content2 = dataJson['bankName']
    content3 = dataJson['sellerID']


    U = Bankaccount.objects.filter(sellerID=content3).update(accountNo=content1, bankName=content2)
    print(U)
    return HttpResponse("success")


@ensure_csrf_cookie
@csrf_exempt
def getSeller(request):
    U = Seller.objects.all()
    print(U)
    seller1: [SELLER] = []

    try:
        for a in U:
            id = str(a.userID)
            print(id)
            e = str(a.emailAddress)
            print(e)
            s = make_seller(id, e, " ")
            seller1.append(s)
        print(seller1)
    except:
        print("Error: unable to fetch data")
    b = {'seller2': makeDict(seller1)}
    print(b)
    return JsonResponse(b)

@ensure_csrf_cookie
@csrf_exempt
def showSeller(request):
        data1 = request.body.decode('utf-8')
        dataJson = json.loads(data1)
        content1 = dataJson['userID']
        seller1: [SELLER] = []
        # create new list for getting each object out of U
        # U ja ork ma pen [<Order: Order object>, <Order: Order object>] tong aow data ork ma
        # User has to be the same with in models
        # pull sellerID = 2
        num1 = int(content1)
        U = list(Seller.objects.filter(userID=num1))
        M = list(Bankaccount.objects.filter(sellerID=num1))
        # print(U)

        # put data from U into another list
        for a in U:
            email = str(a.emailAddress)
            sellerID = str(a.userID)
            print(email)

        try:
            for c in M:
                bank1 = str(c.accountNo)
                print(bank1)
                u = make_seller(sellerID, email, bank1)
                seller1.append(u)
                print(seller1)
        except:
            print("not working")



        b = {'seller': makeDict(seller1)}
        print(b)
        # return HttpResponse(U)

        # wela ja send data to xcode
        return JsonResponse(b)

@ensure_csrf_cookie
@csrf_exempt
def createSeller(request):
    data1 = request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content1 = dataJson['email']
    content3 = dataJson['sellerID']
    content2 = dataJson['bank']
    num1 = int(content3)
    U = Seller.objects.create(emailAddress=content1, userID=num1, avgstar=5)

    return HttpResponse("success")

@ensure_csrf_cookie
@csrf_exempt
def getProductIDByOrder(request):
    data1=request.body.decode('utf-8')
    dataJson = json.loads(data1)
    content1 = dataJson['orderID']
    U,=Order.objects.filter(orderID=content1)
    productID=U.productID
    return HttpResponse(str(productID))

