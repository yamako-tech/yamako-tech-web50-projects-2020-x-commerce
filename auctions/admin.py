from django.contrib import admin
from .models import User, Category, Auction, Bid, Comment



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'title', 'user', 'starting_price', 'date')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name','last_name', 'email', 'last_login')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'myproduct')



admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)