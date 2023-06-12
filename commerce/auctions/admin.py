from django.contrib import admin

from .models import User , Item , Category , Bid , Watchlist , Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment)