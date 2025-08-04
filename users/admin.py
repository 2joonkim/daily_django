from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('name', 'email')
    ordering = ('-id',)
    list_display_links = ('name',)
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'email', 'password')
        }),
        ('권한', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('로그인 정보', {
            'fields': ('last_login',)
        }),
    )
    
    add_fieldsets = (
        ('새 사용자 생성', {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_active'),
        }),
    )
    
    readonly_fields = ('last_login',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # 새로 생성하는 경우
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)
