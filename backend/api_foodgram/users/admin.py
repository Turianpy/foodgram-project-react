from django.contrib import admin

from .models import User, UserProfile


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    min_num = 1
    max_num = 1
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    inlines = (UserProfileInline,)


admin.site.register(User, admin_class=UserAdmin)
admin.site.register(UserProfile)
