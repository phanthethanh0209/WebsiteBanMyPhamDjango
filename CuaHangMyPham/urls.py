from django.contrib import admin
from django.urls import path
from . import views


urlpatterns= [

#---------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------TRANG CỬA HÀNG-----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('shop/', views.shop, name='shop'),
    path('shop_detail/<int:sp_id>/', views.shop_detail, name='shop_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('session_info/', views.session_info, name='session_info'),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('cart/', views.cart, name='cart'),
    path('shop_theoloai/<int:ml>/', views.DSSPTheoLoai, name='DSSPTheoLoai'),
    path('shop_ThuongHieu/<int:ml>/', views.DSSPTheoTH, name='DSSPTheoTH'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_details/', views.order_user, name='order_details'),



#----------------------------------------------------------GIỎ HÀNG---------------------------------------------------#   
    path('cart/', views.cart, name='cart'),
    path('addCart/', views.addProToCart, name='addCart'),
    path('clearCart/', views.clearCart, name='clearCart'),
    path('deleteOnePro/<int:product_id>/', views.deleteProFromCart, name='deleteOnePro'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),



#---------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------TRANG ADMIN--------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 



#--------------------------------------TRANG CHỦ ADMIN--------------------------------------------#
    path('admin/', views.indexAdmin, name='index'),

#--------------------------------------QUẢN LÝ SẢN PHẨM--------------------------------------------#
    path('admin/products/', views.products, name='products'),
    path('admin/detail_product/<int:product_id>/', views.detail_product, name='detail_product'),
    path('admin/add_product/', views.add_product, name='add_product'),#thêm sản phẩm
    path('admin/edit_product/<int:id_product>/', views.edit_product, name='edit_product'),
    path('admin/products/<int:id>/delete', views.delete_product, name='delete_product'),#xóa sản phẩm


#--------------------------------------QUẢN LÝ THƯƠNG HIỆU--------------------------------------------#
    path('admin/brands/', views.brands, name='brands'),#danh sách thương hiệu
    path('admin/add_brand/', views.add_brand, name='add_brand'),#thêm thương hiệu
    path('admin/edit_brand/<int:id_brand>/', views.edit_brand, name='edit_brand'),#sửa thương hiệu
    path('delete_brand/<int:id_brand>/', views.delete_brand, name='delete_brand'),#xóa thương hiệu

#--------------------------------------QUẢN LÝ LOẠI HÀNG--------------------------------------------#
    path('admin/categorys/', views.categorys, name='categorys'),#danh sách loại hàng
    path('admin/detail_category/<int:id_category>/', views.detail_category, name='detail_category'),#xem chi tiết loại hàng
    path('admin/add_category/', views.add_category, name='add_category'),#thêm loại hàng
    path('admin/edit_category/<int:id_category>/', views.edit_category, name='edit_category'),#sửa loại hàng
    path('admin/categorys/<int:id_category>/delete', views.delete_category, name='delete_category'),#xóa loại hàng

#--------------------------------------QUẢN LÝ ĐƠN HÀNG--------------------------------------------#
    path('admin/orders/', views.orders, name='orders'), #danh sách đơn hàng
    path('admin/detail_order/<int:id_order>/', views.detail_order, name='detail_order'), #chi tiết đơn hàng
    
#--------------------------------------QUẢN LÝ NGƯỜI DÙNG--------------------------------------------#
    path('admin/users/', views.users, name='users'), #danh sách người dùng
    path('admin/add_user/', views.add_user, name='add_user'), #thêm người dùng
    path('admin/users/<int:user_id>/delete', views.delete_user, name='delete_user'),
    path('admin/edit_user/<int:user_id>/', views.edit_user, name='edit_user'), #sửa người dùng


]