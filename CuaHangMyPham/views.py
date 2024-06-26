from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .forms import CategoryForm, BrandForm, UserForm, LoginForm,ProductForm, SignUpForm, OrderForm, OrderDetailForm, UpdateOrderStatusForm
from .models import Category, Product, Brand, Cart, User, Order, OrderDetail
from django.db.models import Sum, Count
#---------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------TRANG CỬA HÀNG-----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 
def index(request):
    # Lấy top 5 sản phẩm có ID lớn nhất
    top_id_products = Product.objects.order_by('-id')[:5]

    # Lấy top 5 sản phẩm có tổng số lượt mua nhiều nhất
    top_sold_products = Product.objects.annotate(total_sales=Sum('orderdetail__quantity')).order_by('-total_sales')[:5]

    # Không cần lấy tất cả sản phẩm, chỉ cần sử dụng paginator cho danh sách top sản phẩm
    items_per_page = 5
    paginator_top_id = Paginator(top_id_products, items_per_page)
    paginator_top_sold = Paginator(top_sold_products, items_per_page)

    page_number_top_id = request.GET.get('page')
    page_number_top_sold = request.GET.get('page')

    page_obj_top_id = paginator_top_id.get_page(page_number_top_id)
    page_obj_top_sold = paginator_top_sold.get_page(page_number_top_sold)

    data = {
        'topProNew': page_obj_top_id,
        'topProHot': page_obj_top_sold,
    }

    return render(request, 'page/index.html', data)


def DSSPTheoLoai(request,ml):
    dssp =Product.objects.all().filter(id=ml)
    # data ={
    #     'dm_sanpham':dssp,
    # }

    #PHÂN TRANG
    items_per_page = 5  # Số sản phẩm trên mỗi trang
    paginator = Paginator(dssp, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    end_page = min(total_pages, start_page + 2)

    page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    data = {
        'dm_sanpham': page_obj,
        'page_range': page_range,  # Pass the page range to the template
        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
    }

    return render(request,"page/shop_theoloai.html",data)


def DSSPTheoTH(request,ml):
    dssp =Product.objects.all().filter(id=ml)
    # data ={
    #     'dm_sp':dssp,
    # }

    #PHÂN TRANG
    items_per_page = 5  # Số sản phẩm trên mỗi trang
    paginator = Paginator(dssp, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    end_page = min(total_pages, start_page + 2)

    page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    data = {
        'dm_sp': page_obj,
        'page_range': page_range,  # Pass the page range to the template
        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
    }

    return render(request,"page/shop_ThuongHieu.html",data)

def news(request):
    return render(request, 'page/news.html')

def contact(request):
    return render(request, 'page/contact.html')

def about(request):
    return render(request, 'page/about.html')

# def shop(request):
#     san_phams = Product.objects.all()
#     data = {
#         'san_phams': san_phams,
#     }
#     return render(request, 'page/shop.html',data)

def shop(request):
    san_phams = Product.objects.all()

    sort_order = request.GET.get('sort','asc')

    if sort_order == 'desc':
        san_phams_sort = Product.objects.all().order_by('-price')
    else:
        san_phams_sort = Product.objects.all().order_by('price')

    #PHÂN TRANG
    items_per_page = 5  # Số sản phẩm trên mỗi trang
    paginator = Paginator(san_phams, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    end_page = min(total_pages, start_page + 2)

    page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    data = {
        'san_phams': page_obj,
        'page_range': page_range,  # Pass the page range to the template
        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
        'san_phams_sort': san_phams_sort,
    }
    return render(request, 'page/shop.html', data)


def shop_detail(request,sp_id):
    ma_sanPham = get_object_or_404(Product, id=sp_id)
    context = {
        'DM_SanPham': ma_sanPham,
    }
    return render(request, 'page/shop_detail.html',context)

def signup(request):
    session_info = is_logged_in(request)
    if session_info['email']:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'page/signup.html', {'form': form})

def login(request):
    session_info = is_logged_in(request)
    if session_info['email']:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email, password=password).first()
            if user:
                # Lưu thông tin user vào session
                request.session['email'] = user.email
                request.session['role'] = user.role
                request.session['user'] = user.id
                request.session['name'] = user.name     
                if user.role == 'admin':
                    return HttpResponseRedirect('/admin')
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, 'Email hoặc mật khẩu không đúng')
    else:
        form = LoginForm()


    return render(request, 'page/login.html', {'form': form})


def is_logged_in(request):
    return {
        'email': request.session.get('email', False),
        'role': request.session.get('role', False),
        'user': request.session.get('id', False),
        'name':request.session.get('name', False),
    }

def is_admin(request):
    return {request.session.get('role', False) == 'admin'}


def session_info(request):
    session_info = {
        'email': request.session.get('email', 'Not set'),
        'role': request.session.get('role', 'Not set'),
        'user': request.session.get('id', 'Not set'),
    }
    return render(request, 'page/session_info.html', {'session_info': session_info})

def auth_logout(request):
    # Xóa session
    request.session.flush()  # Cách tốt hơn để xóa tất cả session
    #request.session.set_expiry(0)  # Hết phiên làm việc khi đóng trình duyệt
    return HttpResponseRedirect('/login')





#--------------------------------------------------------GIỎ HÀNG--------------------------------------------------# 
# #hiển thị giỏ hàng của 1 người
# def cart(request):
#     user_id = request.session.get('user') # Lấy người dùng hiện tại từ session
#     if user_id: 
#         cart_items = Cart.objects.filter(user_id=user_id)
#         return render(request, 'page/cart.html', {'cart_items': cart_items})
#     else:
#         # Xử lý nếu không tồn tại thông tin người dùng trong session
#         return render(request, 'page/cart.html', {'cart_items': []})

def cart(request):
    user_id = request.session.get('user')  # Lấy người dùng hiện tại từ session
    if user_id:
        cart_items = Cart.objects.filter(user_id=user_id)
        cart_details = []
        total_price = 0

        for item in cart_items:
            item_total = item.product.price * item.quantity
            total_price += item_total
            cart_details.append({
                'product': item.product,
                'quantity': item.quantity,
                'item_total': item_total
            })

        return render(request, 'page/cart.html', {'cart_items': cart_details, 'total_price': total_price})
    else:
        # Xử lý nếu không tồn tại thông tin người dùng trong session
        return render(request, 'page/cart.html', {'cart_items': [], 'total_price': 0})

    
    
#đếm số lượng sản phẩm trong giỏ hàng
def countCart(user_id):
    try:
        total_items = Cart.objects.filter(user_id=user_id).aggregate(total_items=Sum('quantity'))['total_items']
        return total_items if total_items else 0
    except Cart.DoesNotExist:
        return 0
    
#thêm sản phẩm vô giỏ hàng
def addProToCart(request):
    if request.GET.get('action') == 'addcart' and 'id_product' in request.GET:
        product_id = request.GET['id_product']
        try:
            product = Product.objects.get(id=product_id)
            user_id = request.session.get('user') #=8
            if user_id:  # Nếu tồn tại thông tin người dùng trong session, sử dụng để thêm vào giỏ hàng
                try:
                    user = User.objects.get(id=user_id)
                    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
                    if not created:
                        cart_item.quantity += 1
                    cart_item.save()
                except User.DoesNotExist:
                    pass
            else:  # Xử lý nếu không tồn tại thông tin người dùng trong session
                return redirect('login')
        except Product.DoesNotExist:
            pass

    return redirect('shop')

#xóa tất cả sản phẩm giỏ hàng
def clearCart(request):
    user_id = request.session.get('user')  # Lấy người dùng hiện tại từ session
    if user_id:
        # Xóa tất cả các mục trong giỏ hàng của người dùng
        Cart.objects.filter(user_id=user_id).delete()
    return redirect('cart')

#xóa 1 sản phẩm trong giỏ hàng
def deleteProFromCart(request, product_id):
    user_id = request.session.get('user')  # Lấy người dùng hiện tại từ session
    if user_id:
        cart_item = get_object_or_404(Cart, user_id=user_id, product_id=product_id) # Lấy sản phẩm trong giỏ hàng của người dùng
        cart_item.delete()
    return redirect('cart')

#tăng số lượng sản phẩm trong giỏ hàng
def increase_quantity(request, product_id):
    user_id = request.session.get('user') # Lấy người dùng hiện tại từ session
    if user_id:
        cart_item = get_object_or_404(Cart, user_id=user_id, product_id=product_id) # Lấy sản phẩm trong giỏ hàng của người dùng
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

#giảm số lượng sản phẩm trong giỏ hàng
def decrease_quantity(request, product_id):
    user_id = request.session.get('user') # Lấy người dùng hiện tại từ session
    if user_id:
        cart_item = get_object_or_404(Cart, user_id=user_id, product_id=product_id) # Lấy sản phẩm trong giỏ hàng của người dùng
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete() # Xóa sản phẩm khỏi giỏ hàng nếu số lượng giảm về 0
    return redirect('cart')

#---------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------TRANG THANH TOÁN-----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 

def checkout(request):
    order_form = OrderForm()
    order_detail_form = OrderDetailForm()

    user = request.session.get('user') # Lấy người dùng hiện tại từ session

    # Lấy giỏ hàng từ cơ sở dữ liệu cho người dùng đã đăng nhập
    cart_items = Cart.objects.filter(user=user)

    cart_details = []
    total_amount = 0
    index = 0

# lấy thông tin các sp trong giỏ hàng để hiển thị trong template
    for item in cart_items:
        product_total = item.product.price * item.quantity
        total_amount += product_total
        index+=1

        cart_details.append({
            'index' : index,
            'product': item.product,
            'quantity': item.quantity,
            'product_total': "{:,.0f}".format(product_total).replace(",", ".")
        })

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_detail_form = OrderDetailForm(request.POST)

        if order_form.is_valid():
            recipient_name = request.POST.get('recipient_name')
            ward = request.POST.get('ward')
            district = request.POST.get('district')
            city = request.POST.get('city')
            recipient_address = request.POST.get('recipient_address')
            recipient_phone = request.POST.get('recipient_phone')
            method_payment = request.POST.get('method_payment')

            full_recipient_address = f"{recipient_address}, {ward}, {district}, {city}"

            # Tạo và lưu đơn hàng mới
            order = Order.objects.create(
                user_id=user, # Giả sử người dùng đã đăng nhập
                recipient_name=recipient_name,
                recipient_address=full_recipient_address,
                recipient_phone=recipient_phone,
                method_payment=method_payment,
                total_amount=0  # Tính toán tổng số tiền sau
            )

            total_amount = 0
            for item in cart_items:
                product = item.product
                quantity = item.quantity
                price = product.price
                total_amount += price * quantity

                # Tạo và lưu chi tiết đơn hàng
                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            # Cập nhật tổng số tiền đơn hàng
            order.total_amount = total_amount
            order.save()

            # Xóa giỏ hàng sau khi đặt hàng thành công
            cart_items.delete()

            return HttpResponseRedirect('/order_details')

        
    total_amount = "{:,.0f}".format(total_amount).replace(",", ".") #format tổng tiền

    return render(request, 'page/checkout.html',  {'order_form': order_form,
    'order_detail_form': order_detail_form, 'cart_items': cart_items, 'cart_details':cart_details,
    'total_amount': total_amount})

def order_user(request):
    session_info = is_logged_in(request)
    if not session_info['email']:
        return HttpResponseRedirect('/login')

    user_id = request.session.get('user')  # Lấy người dùng hiện tại từ session
    if user_id:
        orders = Order.objects.filter(user_id=user_id) # lấy tất cả các hd của user 
        
        order_list = []
        total_price = 0

# lập lấy các thông tin trong từng hd của user (lấy chi tiết hd)
        for order in orders:
            order_details = OrderDetail.objects.filter(order=order) # lấy thông tin của 1 hd
            details_list = []

            for detail in order_details: # lặp lấy các sản phẩm trong 1 hd (lấy các sp trong cthd)
                product_total = detail.product.price * detail.quantity
                sub_total = "{:,.0f}".format(product_total).replace(",", ".")
                total_price += product_total
                details_list.append({ # add vào list để hiển thị bên html
                    'product_id': detail.product.id,
                    'product_name': detail.product.name,
                    'product_image': detail.product.image,
                    'quantity': detail.quantity,
                    'product_price':  "{:,.0f}".format(detail.product.price).replace(",", "."),
                    'product_total': sub_total,
                })

            order_list.append({ # add từng hd vào list để hiển thị bên html
                'order_id': order.id,
                'order_date': order.order_date,
                'status': order.status,
                'details': details_list,
            })

        total_price = "{:,.0f}".format(total_price).replace(",", ".")  # Format tổng tiền

        return render(request, 'page/order_details.html', {
            'order_list': order_list,
            'total_price': total_price
        })
    else:
        # Xử lý nếu không tồn tại thông tin người dùng trong session
        return render(request, 'page/order_details.html', {'order_list': [], 'total_price': 0})




#---------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------TRANG ADMIN--------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 
#trang chủ admin
def indexAdmin(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    return render(request, 'admin/indexAd.html')


#--------------------------------------------------------QUẢN LÝ SAN PHẨM-----------------------------------------------# 
def products(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    search_query = request.GET.get('search', '')  # Lấy giá trị từ trường tìm kiếm
    category_query = request.GET.get('category', '')  # Lấy giá trị từ trường tìm kiếm loại sản phẩm
    sort_option = request.GET.get('sort', '')  # Lấy giá trị từ trường sắp xếp

    # Lấy tất cả sản phẩm mặc định
    products = Product.objects.all()

    # Lọc sản phẩm theo từ khóa tìm kiếm
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Lọc sản phẩm theo loại sản phẩm
    if category_query:
        products = products.filter(category__name__icontains=category_query)

    # Sắp xếp sản phẩm
    if sort_option == 'name_asc':
        products = products.order_by('name')
    elif sort_option == 'name_desc':
        products = products.order_by('-name')
    elif sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    categories = Category.objects.all()  # Truy vấn tất cả các loại sản phẩm
    # data = {
    #     'DM_SanPham': products,
    #     'search_query': search_query,  # Truyền giá trị từ khóa tìm kiếm vào mẫu
    #     'category_query': category_query,  # Truyền giá trị loại sản phẩm vào mẫu
    #    'maloai': categories,  # Truyền danh sách các loại sản phẩm vào mẫu
    # }

    #PHÂN TRANG
    items_per_page = 5  # Số sản phẩm trên mỗi trang
    paginator = Paginator(products, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    end_page = min(total_pages, start_page + 2)

    page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    data = {
        'DM_SanPham': page_obj,
        'search_query': search_query,  # Truyền giá trị từ khóa tìm kiếm vào mẫu
        'category_query': category_query,  # Truyền giá trị loại sản phẩm vào mẫu
        'maloai': categories,  # Truyền danh sách các loại sản phẩm vào mẫu
        'page_range': page_range,  # Pass the page range to the template

        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
    }

    return render(request, 'admin/products.html', data)


#xem chi tiết sản phẩm
def detail_product(request, product_id):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    ma_sanPham = get_object_or_404(Product, id=product_id)
    context = {
        'DMSP': [ma_sanPham],  # Đảm bảo DMSP là một danh sách chứa một sản phẩm duy nhất
    }

    return render(request, 'admin/detail_product.html', context)

#thêm sản phẩm
def add_product(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/products')  # Ensure this URL is correct for your project
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = ProductForm()
    
    maloai = Category.objects.all()  # Fetch all categories
    mabrand = Brand.objects.all()  # Fetch all brands

    return render(request, 'admin/add_product.html', {'form': form, 'maloai': maloai, 'mabrand': mabrand})

#sửa sản phẩm
def edit_product(request, id_product):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    product = get_object_or_404(Product, pk=id_product)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/products')
    else:
        form = ProductForm(instance=product)
    maloai = Category.objects.all()  # Fetch all categories
    mabrand = Brand.objects.all()  # Fetch all brands
    return render(request, 'admin/edit_product.html', {'form': form, 'product': product,'maloai': maloai, 'mabrand': mabrand})
#xóa sản phẩm
def delete_product(request, id):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return HttpResponseRedirect('/admin/products')


#--------------------------------------------------------QUẢN LÝ THƯƠNG HIỆU-----------------------------------------------# 
#danh sách sản phẩm
def brands(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    # brands= Brand.objects.all()
    
    # #PHÂN TRANG
    # items_per_page = 5  # Số sản phẩm trên mỗi trang
    # paginator = Paginator(brands, items_per_page)

    # page_number = request.GET.get('page', 1)
    # page_obj = paginator.get_page(page_number)

    # total_pages = paginator.num_pages

    # previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    # next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    # start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    # end_page = min(total_pages, start_page + 2)

    # page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    # data = {
    #     'listBrand': page_obj,
    #     'page_range': page_range,  # Pass the page range to the template
    #     'total_pages': total_pages,
    #     'previous_page': previous_page,
    #     'next_page': next_page,
    # }

    data= {
        'listBrand': Brand.objects.all(),
    }

    return render(request, 'admin/brands.html', data)

#thêm sản phẩm
def add_brand(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/brands')
    else:
        form = BrandForm()
    return render(request, 'admin/add_brands.html', {'form': form})

#sửa sản phẩm
def edit_brand(request, id_brand):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    brand = get_object_or_404(Brand, pk=id_brand)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/brands')
    else:
        form = BrandForm(instance=brand)
    
    return render(request, 'admin/edit_brands.html', {'form': form, 'brand': brand})
    

#xóa sản phẩm
def delete_brand(request, id_brand): 
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    brand = get_object_or_404(Brand, pk=id_brand)
    if request.method == 'POST':
        brand.delete()
        return HttpResponseRedirect('/admin/brands')
    else:
        form = BrandForm(instance=brand)

    return render(request, 'admin/delete_brand.html', {'form': form, 'brand': brand})


#--------------------------------------------------------QUẢN LÝ LOẠI HÀNG--------------------------------------------------# 
#danh sách loại
def categorys(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    categorys= Category.objects.all()

    #PHÂN TRANG
    items_per_page = 5  # Số sản phẩm trên mỗi trang
    paginator = Paginator(categorys, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    end_page = min(total_pages, start_page + 2)

    page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    data = {
        'listCategory': page_obj,
        'page_range': page_range,  # Pass the page range to the template
        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
    }
    
    return render(request, 'admin/categorys.html', data)

#xem chi tiết loại
def detail_category(request, id_category):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    category = Category.objects.get(pk=id_category)
    return render(request, 'admin/detail_category.html', {'category': category})

#thêm loại
def add_category(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/categorys')  
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

#sửa sản phẩm
def edit_category(request, id_category):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    category = get_object_or_404(Category, pk=id_category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/categorys')
    else: #Nếu GET
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/edit_category.html', {'form': form, 'category': category})

#xóa loại
def delete_category(request, id_category):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=id_category)
        category.delete()
        return HttpResponseRedirect('/admin/categorys')

#--------------------------------------------------------QUẢN LÝ ĐƠN HÀNG-----------------------------------------------# 
#danh sách đơn hàng
def orders(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    # Lấy danh sách đơn hàng
    list_orders = Order.objects.all()

    # Định dạng tổng tiền
    for order in list_orders:
        order.total_amount = "{:,.0f}".format(order.total_amount).replace(",", ".") 

    # Tổng doanh thu
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    # Tổng số đơn hàng đã đặt
    total_orders = Order.objects.count()
    # Tổng số account
    total_accounts = User.objects.count()
    # Sản phẩm hiện có
    total_products = Product.objects.count()

    data = {
        'listOrder': list_orders,
        'total_revenue': "{:,.0f}".format(total_revenue).replace(",", ".") ,
        'total_orders': total_orders,
        'total_accounts': total_accounts,
        'total_products': total_products
    }
    
    return render(request, 'admin/orders.html', data)

#xem chi tiết đơn hàng
def detail_order(request, id_order):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    order = Order.objects.get(pk=id_order)
    order_details = OrderDetail.objects.filter(order=order)

    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            order.status = new_status
            order.save()
            return HttpResponseRedirect('/admin/orders')
    else:
        form = UpdateOrderStatusForm(initial={'status': order.status})

    return render(request, 'admin/detail_order.html', {'order': order, 'order_details': order_details, 'form': form})


#--------------------------------------------------------QUẢN LÝ NGƯỜI DÙNG-----------------------------------------------# 
#danh sách người dùng
def users(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    listUser= User.objects.all()
    

     #PHÂN TRANG
    items_per_page = 5  # Số sản phẩm trên mỗi trang
    paginator = Paginator(listUser, items_per_page)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    previous_page = max(page_obj.number - 1, 1)  # Trang trước đó
    next_page = min(page_obj.number + 1, total_pages)  # Trang tiếp theo

    start_page = max(1, min(page_obj.number - 1, total_pages - 2))  # Vị trí của nút trang đầu tiên
    end_page = min(total_pages, start_page + 2)

    page_range = range(start_page, end_page + 1) # Create a range or list of page numbers

    data = {
        'listUser': page_obj,
        'page_range': page_range,  # Pass the page range to the template
        'total_pages': total_pages,
        'previous_page': previous_page,
        'next_page': next_page,
    }
    return render(request, 'admin/users.html', data)

#thêm người dùng
def add_user(request):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/users')
    else:
        form = UserForm()
    return render(request, 'admin/add_user.html', {'form': form})

#xóa người dùng
def delete_user(request, user_id):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        # Sử dụng get_object_or_404 để xử lý ngoại lệ nếu không tìm thấy người dùng
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return HttpResponseRedirect('/admin/users/')
    

#sửa người dùng
def edit_user(request, user_id):
    session_info = is_logged_in(request)
    if not session_info['email'] or session_info['role'] != 'admin':
        return HttpResponseRedirect('/login')
    
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/users')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form})
    


