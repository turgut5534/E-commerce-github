from django.http import request
from .models import Card,Product, WishList

def showcardcommon(request):
        if request.user.is_active:
            card= Card.objects.filter(user=request.user)
            total_price=0
            amount=0
            # wishlist = WishList.objects.get(user = request.user)
            # products_inwishlist = wishlist.product.all()
            # total_wish = len(products_inwishlist)
          
            for i in card:
                if i.product.discount_applied:
                    total_price+=i.product.discount_price*i.quantity
                else:
                    total_price+=i.product.price*i.quantity
                amount+=1
                
            if total_price>9999 or not card:
                ship_fee=0
            else:
                ship_fee=10.99
                total_price+=ship_fee

            context={
                "card": card,
                "total": total_price,
                "amount": amount,
                "ship_fee": ship_fee
                # "totalwish": total_wish
            }
            return context
        else:
            session_card = request.session.get("my_card")
            context2= {}
            total=0

            if session_card is None or len(session_card) == 0:
                context2["card"] = []
                context2["has_item"] = False
                    
            else:
                get_product= Product.objects.filter(slug__in = session_card)
                for i in get_product:
                    if i.discount_applied:
                        total += i.discount_price
                    else:
                        total += i.price
                context2["card"] = get_product
                context2["has_item"] = True
                context2["total"] = total
                context2["amount"] = len(get_product)

            return context2
