from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserAdmin(UserAdmin):
    model = User
    list_display = ['id','email','is_staff']
    list_filter = ['email','first_name']
    fieldsets = (
        ('user cred',{'fields':('email','password')}),
        ('personal_info',{'fields':('first_name','last_name')}),
        ('permission',{'fields':('is_staff','is_superuser','is_active')}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    
admin.site.register(User,UserAdmin)

