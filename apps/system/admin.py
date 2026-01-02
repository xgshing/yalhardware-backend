# apps/system/admin.py
from django.contrib import admin
from .models.company import CompanyProfile

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'contact_person',
        'mobile',
        'email',
        'updated_at'
    )

    fieldsets = (
        ('基本信息', {
            'fields': ('company_name', 'address')
        }),
        ('联系方式', {
            'fields': ('contact_person', 'mobile', 'email')
        }),
    )

    def has_add_permission(self, request):
        # ❗只允许存在一条公司信息
        return not CompanyProfile.objects.exists()
