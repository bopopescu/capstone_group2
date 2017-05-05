from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'getuid/$', views.getuid, name='getuid'),
    url(r'register/$', views.register, name='register'),
    url(r'log_in/$', views.log_in, name='log_in'),
    url(r'addpref/$', views.addpref, name='addpref'),
    url(r'checkforpref/$', views.checkforpref, name='checkforpref'),
    url(r'getprodrec/$', views.getprodrec, name='getprodrec'),
    url(r'getpicbyproductid/$', views.getpicbyproductid, name='getpicbyproductid'),
    url(r'getallprod/$', views.getallprod, name='getallprod'),
    url(r'getfilteredproduct/$', views.getfilteredproduct, name='getfilteredproduct'),
    url(r'getidbyhashtag/$', views.getidbyhashtag, name='getidbyhashtag'),
    url(r'checkifseller/$', views.checkifseller, name='checkifseller'),
    url(r'getproductinfo/$', views.getproductinfo, name='getproductinfo'),
    url(r'getwishlistid/$', views.getwishlistid, name='getwishlistid'),
    url(r'addtowishlist/$', views.addtowishlist, name='addtowishlist'),
    url(r'removefromwishlist/$', views.removefromwishlist, name='removefromwishlist'),
    url(r'setisactivefalse/$', views.setifactivefalse, name='setisactivefalse'),
    url(r'getorderedwishlist/$', views.getorderedwishlist, name='getorderedwishlist'),
    url(r'removefrommywishlist/$', views.removefrommywishlist, name='removefrommywishlist'),
url(r'sellerprofile/(?P<userid>[0-9]+)/$', views.sellerprofile, name='sellerprofile'),
    url(r'sellerproduct/(?P<userid>[0-9]+)/(?P<picid>\d+)/$', views.sellerproduct, name='sellerproduct'),
    url(r'selid/(?P<userid>[0-9]+)/$', views.selproductid, name='getselproid'),
    url(r'addproduct/(?P<userid>[0-9]+)/$', views.addproduct, name='addproduct'),
    url(r'addpayment/(?P<userid>[0-9]+)/$', views.addpayment, name='addpayment'),
url(r'Kaidee/Order/$', views.order, name='order'),
    url(r'Kaidee/profile/$' ,views.profile, name = 'profile'),
    url(r'Kaidee/status/$' , views.updateStatus, name = 'status'),
    url(r'Kaidee/product/$' , views.product, name = 'product'),
    url(r'Kaidee/comment/$', views.comment, name='comment'),
    url(r'Kaidee/seller/$', views.showSeller, name='seller'),
    url(r'Kaidee/editPhone/$', views.editPhone, name='editPhone'),
    url(r'Kaidee/editPass/$', views.editPass, name='editPass'),
    url(r'Kaidee/editEmail/$', views.editEmail, name='editEmail'),
    url(r'Kaidee/editBank/$', views.editBank, name='editBank'),
    url(r'Kaidee/createSeller/$', views.createSeller, name='createSeller'),
    url(r'Kaidee/getSeller/$', views.getSeller, name= 'getSeller'),
url(r'getProductIDByOrder/$', views.getProductIDByOrder, name='getProductIDByOrder')


]