from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'card_nr', 'location', 'phone_number', 'bank_account')



# I CAN CREATE MY OWN METHOD TO DISPLAY SOMETHING
# def my_funct(self, obj):
#   return obj.WhateverIWant

# def get_queryset(self, request):
#     queryset = super(UserProfileAdmin, self).get_queryset(request)
#     queryset = queryset.order_by('-phone')
#     return queryset

# user_info.short_description = "Info"  -- prescurtare anumite campuri

admin.site.register(UserProfile, UserProfileAdmin)