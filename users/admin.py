from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# from gobasic.models import Customer, Hotel, Activity,Transfer, Trip, Locations


# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "userprofile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "user_type",
    ]
    list_filter = ("is_staff", "is_active", "user_type")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "user_type", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "user_type",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)

