from django import http
from django.contrib.admin.sites import site
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import paginator
from django.core.paginator import Paginator
from django.views import View
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from .models import Card, Category, Comment, Contact, Marka, Payment,Discount, OrderDetail, UpdateEmail, User,UserInfo,Product,Spec,Specs,Address, VirtualCard, WishList
import random
from e_commerce.settings import EMAIL_HOST_USER
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.utils.text import slugify



def user_login(request):
    if not request.user.is_active:
        if request.method == "GET":
            return render(request,"login.html", {
                "has_error": False
            })

        else:
        
            user_name=request.POST.get("username")
            password=request.POST.get("password")

            user=authenticate(username=user_name, password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/")
                else:
                    return HttpRequest("HESAP AKTİF DEĞİL")

            else:
                print("Hesabınıza biri girmeye çalıştı")
                print("Username: {} and password {}".format(user_name,password))
                return render(request, "login.html", {
                    "has_error": True
                })

    else:
        return HttpResponse("<h1>You have to logout!</h1><a href='/user_logout'>Logout</a>")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    else:
        username= request.POST.get('username')
        firstname= request.POST.get('first_name')
        lastname= request.POST.get('last_name')
        email= request.POST.get('email')
        password= request.POST.get('password')
        re_password= request.POST.get('re_password')

        if password != re_password:
            return render(request,"register.html", {
                "password_notmatch":True,
                "registered": False,
                "email_registered": False,
                "username_registered": False
            })

        try:
            user= User.objects.get(email= email)
            return render(request,"register.html", {
                "password_notmatch":False,
                "registered": False,
                "email_registered": True,
                "username_registered": False
            })
        except:
            try:
                user= User.objects.get(username=username)
                return render(request,"register.html", {
                "password_notmatch":False,
                "registered": False,
                "email_registered": False,
                "username_registered": True
                })
            except:
                new_user=User(username=username, first_name=firstname, last_name=lastname, email=email)
                new_user.set_password(password)
                user_info= UserInfo(user=new_user)
                wishlist = WishList(user= new_user)
                new_user.save()
                user_info.save()
                user_info.save()
                wishlist.save()
                return render(request, "register.html", {
                    "password_notmatch": False,
                    "registered": True,
                    "email_registered": False,
                    "username_registered": False
                })
            
        

class ChangePasswordView(View):
    def get(self, request):
        return render(request, "change-password.html")

    def post(self, request):
        current_password= request.POST.get("current-password")
        password= request.POST.get("password")
        re_password= request.POST.get("re-password")
        password_notmatch= False
        same_password= False
        wrong_password= False

        if password != re_password:
            password_notmatch= True

        elif request.user.check_password(password):
            same_password= True

        else:
            user= User.objects.get(username= request.user.username)
            if user.check_password(password):
                user.set_password(password)
                user.save()
                return HttpResponseRedirect(reverse("homepage"))
            else:
                wrong_password=True
    
        return render(request,"change-password.html", {
            "wrong_password": wrong_password,
            "password_notmatch": password_notmatch,
            "same_password": same_password
        })

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, "forgot_password.html", {
            "code_came": False
        })
 

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            code = random.randint(100000,999999)
            code = str(code)
            subject ="Recover Password"
            message ="Your code: " + code
            send_mail(subject, message,EMAIL_HOST_USER, [user.email])

            return render(request, "forgot_password.html", {
            "code_came": True,
            "code": code,
            "wrong_code": False,
            "username": user.username
        })

        except User.DoesNotExist:
            return render(request, "forgot_password.html", {
                "user_notfound": True,
                "wrong_code": False
            })

class CheckCodeView(View):
    def get (self, request):
        pass
        
    def post(self, request):
        code = request.POST.get("code")
        code_pass = request.POST.get("code_pass")
        username= request.POST.get("username")

        if code == code_pass:
            return render(request, "new_password.html", {
                "username": username
            })
        else:
            return render(request, "forgot_password.html", {
                "wrong_code": True,
                "code_came": True,
                "username": username,
                "code":code_pass
            })

class EnterNewPasswordView(View):
    def post(self, request):
        password= request.POST.get('password')
        re_password= request.POST.get('re-password')
        username= request.POST.get("username")

        if password != re_password:
            return render(request,"new_password.html", {
                "password_notmatch":True,
                "username": username
            })

        else:
            user = User.objects.get(username= username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse("homepage"))

def check_discount():
    products = Product.objects.all()
    for i in products:
        if i.discount:
            i.discount_applied=True
            i.discount_price = i.price- i.price* i.discount.discount_percent/100
            i.save()
    

class HomePage(View):
    def get(self, request):
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse("adminproducts"))
        check_discount()
        featured_products= Product.objects.filter(is_featured=True)
        new_products = Product.objects.filter(is_new=True)
        categories= Category.objects.all()[:3]
        context = {
                 "new": new_products,
                 "featured": featured_products,
                 "categories": categories,
                 "cart": get_products_from_cart(request)
            }
        if request.user.is_active:
           context2= {
               "wishlist": WishList.objects.get(user= request.user).product.all()
           }
           context= {**context, **context2}
        return render(request, "index.html", context)

class Blank(View):
    def get(self, request):

        # if request.is_ajax():
        #     template= loader.get_template("data.html")
        #     context= {
        #         "categories": "sdgsdgsd"
        #     }
        #     return HttpResponse(template.render(context, self.request))

        
        return render(request, "order_confirmation.html")



class Profile(View):
    def get(self,request):
        user= request.user
        user_info = UserInfo(user=user)
        return render(request, "profile.html", {
            "user_info": user_info
        })

            
def is_in_wishlist(the_product, request):
    try:
        wishlist = WishList.objects.get(user= request.user)
        products_inwishlist = wishlist.product.all()

        if the_product in products_inwishlist:
            is_in= True
        else:
            is_in=False

        return is_in
    except:
        return False

def is_incard(product, request):
    try:
        card= Card.objects.filter(user= request.user)
        for i in card:
            if product == i.product:
                is_in= True
                break
            else:
                is_in=False
        return is_in
    except:
        return False

def get_wishlist(request):
    if request.user.is_authenticated:
        wishlist= WishList.objects.get(user= request.user)
        return wishlist.product.all()

class ProductView(View):
    def get(self,request,slug):
        check_discount()
        the_product= Product.objects.get(slug=slug)
        related_products= Product.objects.filter(category= the_product.category)[:4]
        product_comments= the_product.commentsofproduct.all()
        total_comment= len(product_comments)
        specs = the_product.specs.all()
        try:
            orders= OrderDetail.objects.get(user=request.user, product=the_product, status="Delivered")
            is_bought= True
        except:
            is_bought= False

        one_star=0
        two_star=0
        three_star=0
        four_star=0
        five_star=0

        for i in product_comments:
            print(i.rating)
            if i.rating == 1:
                one_star+=1
            elif i.rating == 2:
                two_star+=1
            elif i.rating == 3:
                three_star+=1
            elif i.rating == 4:
                four_star+=1
            else:
                five_star+=1
        
        context= {
                "product": the_product,
                "comments": product_comments,
                "comment_amount": len(product_comments),
                "total_comment": total_comment,
                "specs": specs,
                "related_products": related_products,
                "in_wishlist": is_in_wishlist(the_product ,request),
                "is_incard": is_incard(the_product, request),
                "wishlist": get_wishlist(request),
                "cart": get_products_from_cart(request),
                "one_star": one_star,
                "two_star": two_star,
                "three_star": three_star,
                "four_star": four_star,
                "five_star": five_star,
                "is_bought": is_bought
            }
        if the_product.discount:
            the_product.discount_price = the_product.price- the_product.price* the_product.discount.discount_percent/100
            the_product.save()
        return render(request, "product.html", context)
       
class CheckOutView(View):
    def get(self, request):
        
        try:
            addresses = UserInfo.objects.get(user=request.user).address.all()[:5]
            context= {
                 "addresses": addresses,
                 "from" :"checkout"
            }
        except:
            context= {
                "from" :"checkout"
            }

        if request.GET.get("buy_now"):
            name=request.GET.get("product")
            product= Product.objects.get(pk=name)
            card=Card.objects.all()
            card.delete()
            if product.discount_applied:
                card = Card(user=request.user, product=product, quantity=1, price=product.discount_price)
            else:
                card = Card(user=request.user, product=product, quantity=1, price=product.price)

            card.save()
       
        return render(request, "checkout.html", context)
    def post(self,request):
        address_id = request.POST.get("adres_radio")
        if not address_id:
            return render(request, "checkout.html", {
                "addresses": UserInfo.objects.get(user= request.user).address.all()[:5],
                "no_address": True
            })
        card_holder= request.POST.get("card_holder")
        card_number= request.POST.get("card_number")
        expiry= request.POST.get("expiry")
        cvv = request.POST.get("cvv")

        try:
            get_card= VirtualCard.objects.get(
                holder= card_holder,
                number=card_number,
                expiry= expiry,
                cvc= cvv
            )
        except:
            return render(request, "checkout.html", {
            "addresses": UserInfo.objects.get(user= request.user).address.all()[:5],
            "no_address": False,
            "not_enough": False,
            "no_card": True
        })
        total = request.POST.get("total_price")
        if get_card.amount > float(total):
            random_code= random.randint(1000000,9999999)
            card= Card.objects.filter(user= request.user)
            product= []
            for i in card:
                product.append(i.product)
            address = Address.objects.get(id=address_id)

            try:
                payment= Payment.objects.get(holder= card_holder,number= card_number, expiry=expiry, cvv=cvv, kind=get_card.kind,user= request.user)  
            except:
                payment= Payment.objects.create(
                    holder= card_holder, 
                    number= card_number, 
                    expiry=expiry, 
                    cvv=cvv, 
                    user= request.user
                )
                
            new_order= OrderDetail.objects.create(
                order_code=random_code,
                user= request.user, 
                status="Order Received",
                total=total, 
                payment=payment, 
                address= address
            )

            new_order.product.set(product)
            get_card.amount-=float(total)
            get_card.save()



            session_card= request.session.get("order_confirm")
        
            if session_card is None:
                session_card = []

            else:
                del request.session['order_confirm']
                session_card = []

            session_card.append(new_order.order_code)
            
            request.session["order_confirm"] = session_card




            Card.objects.all().delete()
                    
            return HttpResponseRedirect(reverse("order_confirmation"))
        else:
            return render(request, "checkout.html", {
            "addresses": UserInfo.objects.get(user= request.user).address.all()[:5],
            "no_address": False,
            "not_enough": True
        })
     
        

class CategoryView(View):
    def get(self, request): 
        categories = Category.objects.all()
        return render(request, "categories.html" , {
            "categories": categories
        })

def get_products_from_cart(request):
    if request.user.is_authenticated:
        cart= Card.objects.filter(user= request.user)
        products_incart= []
        for item in cart:
            products_incart.append(item.product)
        return products_incart
    
    else:
        return None
    

class ProductsinCategoryView(View):
    def get(self, request, name):
        check_discount()
        is_vertical=False
        view= request.GET.get("view")
        sort_by= request.GET.get("sort_by")
        if view and view=="vertical":
            is_vertical= True
        page=request.GET.get("page")
        if not page:
            page=1
        the_category = Category.objects.get(name=name)
        the_products= Product.objects.filter(category=the_category)
        if sort_by or sort_by == "price":
            the_products= the_products.order_by('price')
        top_selling = the_products.filter(is_featured=True)
        result= len(the_products)
        brands= Marka.objects.filter(category= the_category)
        min_price = request.GET.get("min_price")
        max_price= request.GET.get("max_price")
        screen_size= Spec.objects.get(name="Screen Size")
        sizes= Specs.objects.filter(spec=screen_size)
        spec= Spec.objects.filter(category= the_category )
        # specs= Specs.objects.filter(spec_in=spec)
        # print(specs)

        if min_price:
            the_products=the_products.exclude(price__lt=min_price)

        if max_price:
            the_products=the_products.exclude(price__gt=max_price)

        paginator= Paginator(the_products,6)  #show 6 products per page
        p=paginator.page(page)
        p_range=paginator.page_range
        has_next=p.has_next()
        has_previous=p.has_previous()
        next_page=p.next_page_number
        previous_page=p.previous_page_number

        context={
            "name": name,
            "products": p,
            "result": result,
            "top_selling": top_selling,
            "range": p_range,
            "has_next": has_next,
            "has_previous": has_previous,
            "previous_page": previous_page,
            "next_page": next_page,
            "current_page": page,
            "categoryofproducts": name,
            "brands": brands,
            "get_view": view, 
            "is_vertical": is_vertical,
            "sizes": sizes,
            "cart": get_products_from_cart(request),
            "specs": spec
        }

        if request.user.is_authenticated:
            wishlist= WishList.objects.get(user= request.user)
            context2= {
                "wishlist": wishlist.product.all(),
            }
            context= {**context, **context2}

        return render(request, "store.html", context)
       

class CardView(View):
    def get(self, request):
        # products = Product.objects.all()[:8]
        products = Product.objects.order_by("?")[:8]
        return render(request, "card.html", {
            "products": products
        })

    def post(self, request):

        if request.is_ajax():
            operation = request.POST.get("operation")
            user= request.user
            product_slug = request.POST.get("product_slug")
            print(product_slug)
            the_product = Product.objects.get(slug=product_slug)
            cart=get_products_from_cart(request)
            if operation == "add":
                if request.user.is_active:
                    print("Adding in pyhton")
                    if the_product in cart:
                        return HttpResponseRedirect("")
                    else:
                        if the_product.discount:
                            card = Card(user=user, product=the_product, quantity=1, price=the_product.discount_price)
                        else:
                            card = Card(user=user, product=the_product, quantity=1, price=the_product.price)
                        card.save()
                else:
                    session_card= request.session.get("my_card")
                    if session_card is None:
                        session_card = []

                    if product_slug not in session_card:
                        session_card.append(product_slug)
                    else:
                        session_card.remove(product_slug)

                    request.session["my_card"] = session_card

            else:
                if request.user.is_active:
                    print("Deleting in pyhton")
                    card= Card.objects.get(user=request.user, product= the_product)
                    card.delete()
                else:
                    session_card = request.session.get("my_card")
            
                    if product_slug not in session_card:
                        return HttpResponse("No")
                    else:
                        session_card.remove(product_slug)
                        request.session["my_card"] = session_card

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        operation = request.POST.get("operation")

        if operation == "add":
            if request.user.is_active:
                user= request.user
                product_slug = request.POST.get("product_slug")
                the_product = Product.objects.get(slug=product_slug)

           
            
                if the_product.discount:
                    card = Card(user=user, product=the_product, quantity=1, price=the_product.discount_price)
                else:
                    card = Card(user=user, product=the_product, quantity=1, price=the_product.price)
                card.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                session_card= request.session.get("my_card")
        
                if session_card is None:
                    session_card = []

                product_slug = request.POST.get("product_slug")

                if product_slug not in session_card:
                    session_card.append(product_slug)
                else:
                    session_card.remove(product_slug)

                request.session["my_card"] = session_card
                return HttpResponseRedirect(reverse("homepage"))
        elif operation == "delete":
            slug= request.POST.get("delete_slug")
            if request.user.is_active:
                the_product= Product.objects.get(slug=slug)
                card= Card.objects.get(user=request.user, product= the_product)
                card.delete()
                
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                session_card = request.session.get("my_card")
        
                if slug not in session_card:
                    return HttpResponse("No")
                else:
                    session_card.remove(slug)
                    request.session["my_card"] = session_card
                    return HttpResponseRedirect(reverse("card"))

        elif operation == "increase":
            item = request.POST.get("item")
            the_product= Product.objects.get(slug=item)
            card= Card.objects.get(user=request.user, product= the_product)
            if the_product.stock > card.quantity:
                card.quantity+=1
                if the_product.discount_applied:
                    card.price+=card.product.discount_price
                else:
                    card.price+=card.product.price
                card.save()

            return HttpResponseRedirect(reverse("card"))

        else:
            item = request.POST.get("item")
            the_product= Product.objects.get(slug=item)
            card= Card.objects.get(user=request.user, product= the_product)
            if card.quantity >1:
                card.quantity-=1
                if the_product.discount_applied:
                    card.price-=card.product.discount_price
                else:
                    card.price-=card.product.price
                card.save()
            else:
                card.delete()
            return HttpResponseRedirect(reverse("card"))

class ProfileView(View):

    def get(self,request):
        if not request.user.is_active:
            return HttpResponseRedirect(reverse("user_login"))
        user = User.objects.get(username= request.user.username)
        user_info = UserInfo.objects.get(user=user)
        context= {
            "user":user,
            "user_info": user_info
        }
        # context = { **context, **showcard(request.user)}
        return render(request, "profile.html", context)

class CommentView(View):
    def get(self, request, slug, page):
        the_product= Product.objects.get(slug=slug)
        comments= the_product.commentsofproduct.all()
        paginator= Paginator(comments,5)  #show 3 comments per page
        p=paginator.page(page)
        p_range=paginator.page_range
        has_next=p.has_next()
        has_previous=p.has_previous()
        next_page=p.next_page_number
        previous_page=p.previous_page_number
        

        context= {
            "product": the_product,
            "comments": p,
            "range": p_range,
            "has_next": has_next,
            "has_previous": has_previous,
            "previous_page": previous_page,
            "next_page": next_page,
            "current_page": page
        }
        return render(request, "comments.html", context)


    def post(self, request, slug, page):
        name= request.POST.get("name")
        email= request.POST.get("email")
        review= request.POST.get("review")
        rating= request.POST.get("rating")
        slug= request.POST.get("slug")
        total_rating=0

        the_product= Product.objects.get(slug=slug)
        comment= Comment(user_name=name,email=email, text= review, rating=rating, product=the_product)
        product_comments= the_product.commentsofproduct.all()  
        comment.save()

        for i in product_comments:
            print(i.rating)
            total_rating += i.rating
        total_rating /= len(product_comments)
        the_product.rating=total_rating
        the_product.save()
        
        

        return HttpResponseRedirect(reverse("product", args=[the_product.slug]))

class ViewAddress(View):
    def get(self, request):
        user_info = UserInfo.objects.get(user= request.user)
        address = user_info.address.all()
        return render(request, "address.html", {
            "address": address,
            "user_info": user_info,
            "url" : "address"
        })
        

class AddAddress(View):
    def get(self, request):
        from_url= request.GET.get("from")
        return render(request, "add_address.html", {
            "from_url": from_url
        })

    def post(self, request):
        kind = request.POST.get("kind")
        city = request.POST.get("city")
        district = request.POST.get("district")
        full_address = request.POST.get("full_address")
        url= request.POST.get("from")

        user_info = UserInfo.objects.get(user= request.user)
        address = Address(kind=kind, city=city, district=district, full_address=full_address)
        address.save()
        user_info.address.add(address)

        return HttpResponseRedirect(reverse(url))
        
class EditAddress(View):
    def get(self, request, id):
        url= request.GET.get("from")
        adres= Address.objects.get(id=id)
        return render(request, "edit_address.html", {
            "address": adres,
            "url": url
        })

    def post(self, request, id):
        url= request.POST.get("from")
        kind = request.POST.get("kind")
        city = request.POST.get("city")
        district = request.POST.get("district")
        full_address = request.POST.get("full_address")
        address = Address.objects.get(id=id)
        address.kind= kind
        address. city= city
        address.district = district
        address.full_address= full_address
        address.save()
        
        return HttpResponseRedirect(reverse(url))

class DeleteAddress(View):
    def get(self, request, id):
        address= Address.objects.get(pk=id)
        url= request.GET.get("from")
        return render(request, "delete_address_confirmation.html", {
            "address": address,
            "url": url
        })

    def post(self, request, id):
        url= request.POST.get("url")
        print(url)
        address = Address.objects.get(id=id)
        address.delete()
        return HttpResponseRedirect(reverse(url))

def store_file(file, name, id):
        with open("uploads/users/"+name+"_"+id+".jpg", "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

class UpdatePhotoView(View):
    def post(self, request):
        username= request.user.username
        user= User.objects.get(username=username)
        user_info=UserInfo.objects.get(user=user)
        get_id=user.id
        id=str(get_id)
        store_file(request.FILES.get("prof_img"), username, id)
        user_info.image="users/"+username+"_"+str(id)+".jpg"
        user_info.save()
        print(user_info.image.url)
      
        return HttpResponseRedirect(reverse("profile"))

class OrderView(View):
    def get(self, request):
        user_info= UserInfo.objects.get(user= request.user)
        confirmed_orders= OrderDetail.objects.filter(Q(status="Order Received") | Q(status="Shipped") | Q(status="On the Way"), user= request.user ).order_by("-order_date")
        delivered_orders= OrderDetail.objects.filter(user= request.user, status="Delivered").order_by("-order_date")
        return render(request, "orders.html", {
            "user_info": user_info,
            "confirmed_orders": confirmed_orders,
            "delivered_orders": delivered_orders
        })

class WishListView(View):
    def get(self, request):
        if request.user.is_active:
            user_info  =UserInfo.objects.get(user =request.user)
            wishlist = WishList.objects.get(user = request.user)
            products_inwishlist = wishlist.product.all()
            return render(request, "wishlist.html" ,{
                "wishlist": products_inwishlist,
                "user_info": user_info
            })
        else:
            return HttpResponseRedirect(reverse("user_login"))

    def post(self , request):
        operation = request.POST.get("operation")
        slug= request.POST.get("wishlist_slug")
        product= Product.objects.get(slug=slug)
        wishlist = WishList.objects.get(user= request.user)
        products_inwishlist = wishlist.product.all()

        if request.is_ajax():
            if operation == "add":
                if product in products_inwishlist:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    wishlist.product.add(product)
                    wishlist.save()

            else:
                wishlist.product.remove(product)
                wishlist.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        if operation == "add":

            if product in products_inwishlist:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                wishlist.product.add(product)
                wishlist.save()

        else:
            wishlist.product.remove(product)
            wishlist.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class SearchView(View):
    def get(self, request):
        item = request.GET.get("item")
        related_products = Product.objects.filter(model__icontains=item)
        all_products= Product.objects.all()
        context= {
            "related_products": related_products,  
            "all_products": all_products,
            "cart": get_products_from_cart(request),
        }
        
        if request.user.is_active: 
            wishlist= WishList.objects.get(user= request.user)
            context2= {
                "wishlist": wishlist.product.all()
            }
            context= {**context, **context2}
        
        return render(request, "search.html", context)


class FAQView(View):
    def get(self, request):
        return render(request, "FAQ.html")

    
class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")

    def post(self, request):
        name= request.POST.get("name")
        email= request.POST.get("email")
        subject= request.POST.get("subject")
        message= request.POST.get("message")

        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact.save()

        return render(request, "contact.html", {
            "is_sent": True
        })

class OrderConfirmationView(View):
    def get(self, request):
        session_card = request.session.get("order_confirm")  
        get_order= OrderDetail.objects.get(order_code__in = session_card)
        return render(request, "order_confirmation.html", {
            "order": get_order
        })

class PaymentMethods(View):
    def get(self, request):
        payments= Payment.objects.filter(user= request.user)
        return render(request, "payment_methods.html", {
            "payments": payments
        })

    def post(self, request):
        number= request.POST.get("number")
        card= Payment.objects.get(user= request.user, number=number)
        card.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AddCart(View):
    def get(self, request):
        return render(request, "add_cart.html")

    def post(self, request):
        holder = request.POST.get("holder")
        number= request.POST.get("number")
        expiry= request.POST.get("expiry")
        cvc = request.POST.get("cvc")
        
        new_payment= Payment(
            holder= holder,
            number=number,
            expiry= expiry,
            cvv= cvc,
            user= request.user
        )

        if number.startswith('4'):
            new_payment.kind= "Visa"
        else:
            new_payment.kind= "Mastercard"

        new_payment.save()

        return HttpResponseRedirect(reverse("payment_methods"))


def store_product(file, name,number):
        with open("uploads/laptops/"+name+"_"+number+".jpg", "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

class AddProductbyAdmin(View):
    def get(self, request):
        if request.is_ajax():
            category_name= request.GET.get("category")
            category= Category.objects.get(name= category_name)
            spec= Spec.objects.filter(category=category)
            template= loader.get_template("spec.html")
            context= {
                "specs": spec
            }
            return HttpResponse(template.render(context, self.request))
        else:
            context= {
                "markas": Marka.objects.all(),
                "categories": Category.objects.all()
            }
            return render(request, "add_product.html", context)

    def post(self, request):

        marka= request.POST.get("marka")
        model= request.POST.get("model")
        price= request.POST.get("price")
        weight= request.POST.get("weight")
        category= request.POST.get("category")
        warranty= request.POST.get("warranty")
        stock= request.POST.get("stock")
        is_new= request.POST.get("new")
        is_featured= request.POST.get("featured")

        marka= Marka.objects.get(name=marka)
        category= Category.objects.get(name=category)

        new_product= Product(
            marka=marka,
            model= model,
            price= float(price),
            weight=float(weight),
            category=category,
            warranty=int(warranty),
            stock=int(stock),
            is_new=True,
            is_featured=True
        )
        
        store_product(request.FILES.get("image1"), new_product.model,"1")
        store_product(request.FILES.get("image2"), new_product.model,"2")
        store_product(request.FILES.get("image3"), new_product.model,"3")
        store_product(request.FILES.get("image4"), new_product.model,"4")
        new_product.image="laptops/"+new_product.model+"_1"+".jpg"
        new_product.imagetwo="laptops/"+new_product.model+"_2"+".jpg"
        new_product.imagethree="laptops/"+new_product.model+"_3"+".jpg"
        new_product.imagefour="laptops/"+new_product.model+"_4"+".jpg"
        new_product.save()
        return HttpResponseRedirect(reverse("homepage"))

class CancelOrder(View):
    def get(self, request):
        id= request.GET.get("id")
        return render(request, "cancelorder_confirmation.html", {
            "id": id
        })

    def post(self, request):
        id= request.POST.get("id")
        order= OrderDetail.objects.get(id=id)
        order.is_cancelled= True
        order.save()
        return HttpResponseRedirect(reverse("myorders"))

def signupforupdates(request):
    if request.method == "POST":
        email= request.POST.get("emailforupdates")
        email_database= UpdateEmail.objects.create(
            email= email
        )
        subject ="SEATTY Updates"
        message ="Thank you for subscribing our e commerce website. We'll always send you emails about our campaigns"
        send_mail(subject, message,EMAIL_HOST_USER, [email])
        return HttpResponseRedirect(reverse("homepage"))

class SingleOrder(View):
    def get(self, request,id):
        order_id= request.GET.get("order_id")
        order= OrderDetail.objects.get(id=order_id)
        product= Product.objects.get(id=id)
        return render(request, "single_order.html", {
            "product": product,
            "order": order
        })

class DoComment(View):
    def get(self, request):
        id= request.GET.get("id")
        product= Product.objects.get(id=id)

        try:
            comment= Comment.objects.get(user_name= request.user.first_name, product= product)
            return render(request, "do_comment.html", {
                "product": product,
                "comment": comment
            })
        except:
            return render(request, "do_comment.html", {
                "product": product
            })

    def post(self, request):
        id= request.POST.get("product_id")
        product= Product.objects.get(pk=id)
        text= request.POST.get("comment_text")
        rating= request.POST.get("rating")

        try:
            comment= Comment.objects.get(user_name= request.user.first_name, product= product)
            comment.email= request.user.email
            comment.text=text
            comment.rating=rating
            comment.save()
        except:
            
            comment= Comment(
                user_name= request.user.first_name,
                email= request.user.email,
                text=text,
                product=product,
                rating=int(rating)
            )
            comment.save()
        
        return HttpResponseRedirect(reverse("myorders"))

class ReturnProduct(View):
    def get(self, request, id):
        order_id= request.GET.get("order_id")
        order= OrderDetail.objects.get(id=order_id)
        product= Product.objects.get(id=id)
        return render(request, "return.html", {
            "product": product,
            "order": order
        })
    
    def post(self, request, id):
        order_id= request.POST.get("order_id")
        order= OrderDetail.objects.get(id=order_id)
        reason= request.POST.get("reason")
        text= request.POST.get("textwhy")
        product= Product.objects.get(id=id)


        order.is_returned= True
        order.save()

        return HttpResponseRedirect(reverse("myorders"))

class AdminProducts(View):
    def get(self ,request):
        if request.user.is_superuser:
            categories = Category.objects.all()
            return render(request,"admin-products-category.html", {
                "categories": categories
            })
        return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

class AdminProductsEach(View):
    def get(self ,request, name):
        if request.user.is_superuser:
            category= Category.objects.get(name=name)
            products = Product.objects.filter(category=category)
            return render(request,"admin-products.html", {
                "products": products,
                "category": category
            })
        return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

def store_productbyadmin(file, name):
        with open("uploads/laptops/"+name+".jpg", "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

class AdminAddProductsEach(View):
    def get(self ,request, name):
        if request.user.is_superuser:
            brands= Marka.objects.all()
            discounts = Discount.objects.all()
            category= Category.objects.get(name=name)
            spec= Spec.objects.filter(category=category)
            if request.GET.get("the_product"):
                the_product= Product.objects.get(id=request.GET.get("the_product"))
                context=  {
                "brands": brands,
                "discounts": discounts,
                "spec": spec,
                "the_product": the_product,
                "category": name
                }
            else:
                context=  {
                "brands": brands,
                "discounts": discounts,
                "spec": spec,
                "category": name
                }
        
            return render(request,"admin-add-product.html", context)
        return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

    def post(self, request, name):
        product_id= request.POST.get("product_id")
        imageone= request.FILES.get("imageone")
        imagetwo= request.FILES.get("imagetwo")
        imagethree= request.FILES.get("imagethree")
        imagefour= request.FILES.get("imagefour")
        brand_name= request.POST.get("productbrand")
        brand= Marka.objects.get(name=brand_name)
        model= request.POST.get("model")
        price= request.POST.get("price")
        discount= request.POST.get("discount") #checkbox
        if discount:
            discountprice= request.POST.get("discountprice")
            discount_name= request.POST.get("discount_name")
            discount_object= Discount.objects.get(name= discount_name)
        weight= request.POST.get("weight")
        warranty= request.POST.get("warranty")
        stock= request.POST.get("stock")
        is_new= request.POST.get("is_new") #checkbox
        is_featured= request.POST.get("is_featured") #checkbox
        slug= slugify(brand_name+"-"+model)

        category= Category.objects.get(name=name)
        

        if request.POST.get("operation") and request.POST.get("operation") == "update":
            product= Product.objects.get(id=product_id)
            product.marka=brand
            product.model=model
            product.price=price
            product.weight=weight
            product.warranty=warranty
            product.stock=stock
            product.category=category
            product.slug= slug
        else:
            product= Product(
                marka=brand,
                model=model,
                price=price,
                weight=weight,
                warranty=warranty,
                stock=stock,
                category=category,
                slug= slug
            )

        if discount:
            product.discount_price=discountprice
            product.discount=discount_object

        if is_new:
            product.is_new=True
        else: 
            product.is_new=False
        if is_featured:
            product.is_featured=True
        else:
            product.is_featured=False
        if discount:
            product.discount_applied=True
        else:
            product.discount_applied=False

        if imageone:
            store_productbyadmin(imageone, slug+"_1")
            product.image="laptops/"+slug+"_1"+".jpg"

        if imagetwo:
            store_productbyadmin(imageone, slug+"_2")
            product.imagetwo="laptops/"+slug+"_2"+".jpg"
        if imagethree:
            store_productbyadmin(imageone, slug+"_3")
            product.imagethree="laptops/"+slug+"_3"+".jpg"
        if imagefour:
            store_productbyadmin(imageone, slug+"_4")
            product.imagefour="laptops/"+slug+"_4"+".jpg"

        spec= Spec.objects.filter(category=category)

        for i in spec:
            if request.POST.get(i.name):
                try:
                    specs= Specs.objects.get(spec=i, value=request.POST.get(i.name))
                except:
                    specs= Specs(spec=i, value=request.POST.get(i.name))
                    specs.save()
                product.save()
                product.specs.add(specs)

        product.save()

        return HttpResponseRedirect(reverse("adminproducts"))

def AdminDeleteProductsEach(request, id):
    if request.user.is_superuser:
        product= Product.objects.get(id=id)
        product.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

def AdminBrands(request):
    if request.user.is_superuser:
        brands= Marka.objects.all()
        return render(request, "admin-brands.html", {
            "brands": brands
        })
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

def AdminAddBrand(request):
    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, "admin-add-brand.html")
        else:
            name= request.POST.get("brandname")
            Marka.objects.create(name=name)
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

    return HttpResponseRedirect(reverse("adminbrands"))

def AdminCategories(request):
    if request.user.is_superuser:
        categories= Category.objects.all()
        return render(request, "admin-categories.html", {
            "categories": categories
        })
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

def AdminAddCategory(request):
    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, "admin-add-category.html")
        else:
            category_name= request.POST.get("category_name")
            Category.objects.create(name= category_name)

            return HttpResponseRedirect(reverse("admincategories"))
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

def AdminCustomers(request):
    if request.user.is_superuser:
        customers= UserInfo.objects.all()
        return render(request, "admin-customers.html", {
            "customers": customers
        })
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")

def AdminDeleteCustomer(request,id):
    if request.user.is_superuser:
        user_info= UserInfo.objects.get(id=id)
        user_id= user_info.user.id
        user= User.objects.get(id= user_id)
        user.delete()
        user_info.delete()
        print("I am here")

        return HttpResponseRedirect(reverse("admincustomers"))
    return HttpResponse("<h1>Yetkili değilsiniz!</h1>")
