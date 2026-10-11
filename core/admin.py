from django.contrib import admin
from .models import Inquiry, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'sort_order', 'is_published', 'updated_at')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published', 'category')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = ('publish', 'unpublish')

    @admin.action(description='上架所选产品')
    def publish(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(is_published=True, updated_at=timezone.now())
        self.message_user(request, f'已上架 {count} 个产品。')

    @admin.action(description='下架所选产品')
    def unpublish(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(is_published=False, updated_at=timezone.now())
        self.message_user(request, f'已下架 {count} 个产品。')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'phone', 'company', 'request_type', 'quantity', 'city', 'budget', 'description', 'created_at')
    list_display_links = ('id', 'contact')
    list_per_page = 25
    date_hierarchy = 'created_at'
    list_filter = ('request_type', 'budget', 'created_at')
    search_fields = ('company', 'contact', 'phone', 'city')
    readonly_fields = ('created_at',)
