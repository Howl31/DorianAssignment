from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class InsurerMasterAdmin(ImportExportModelAdmin):

    class Meta:
        model = InsurerMaster
        fields = '__all__'
    list_display = ('id', 'insurer', 'name', 'clubbed_name')


class LOBMasterAdmin(ImportExportModelAdmin):

    class Meta:
        model = LOBMaster
        fields = '__all__'
    list_display = ('id', 'lob')


class CategoryMasterAdmin(ImportExportModelAdmin):

    class Meta:
        model = CategoryMaster
        fields = '__all__'
    list_display = ('id', 'clubbed_name', 'category')


class MonthMasterAdmin(ImportExportModelAdmin):

    class Meta:
        model = MonthMaster
        fields = '__all__'
    list_display = ('id', 'month_num', 'month')


class InsurerValueAdmin(ImportExportModelAdmin):

    class Meta:
        model = InsurerValue
        fields = '__all__'
    list_display = ('id', 'year', 'month', 'get_clubbed_name', 'get_category', 'product', 'value')

    @admin.display(ordering='category__category', description='category')
    def get_category(self, obj):
        return obj.category.category

    @admin.display(ordering='category__clubbed_name', description='clubbed_name')
    def get_clubbed_name(self, obj):
        return obj.category.clubbed_name


admin.site.register(InsurerMaster, InsurerMasterAdmin)
admin.site.register(MonthMaster, MonthMasterAdmin)
admin.site.register(CategoryMaster, CategoryMasterAdmin)
admin.site.register(LOBMaster, LOBMasterAdmin)
admin.site.register(InsurerValue, InsurerValueAdmin)
