from django.contrib import admin
from .models import Category,Discount,Product,Spec,Specs,Comment
from .models import VirtualCard,OrderDetail,Contact,Payment,Address,UserInfo,WishList,Card,Marka, Color, UpdateEmail

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("model",)}

class SpecSAdmin(admin.ModelAdmin):
    list_filter = ("value")

admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Product, ProductAdmin)
admin.site.register(Spec)
admin.site.register(Specs)
admin.site.register(OrderDetail)
admin.site.register(Address)
admin.site.register(UserInfo)
admin.site.register(Card)
admin.site.register(Comment)
admin.site.register(Marka)
admin.site.register(Color)
admin.site.register(Payment)
admin.site.register(WishList)
admin.site.register(Contact)
admin.site.register(VirtualCard)
admin.site.register(UpdateEmail)