from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Company, Address, StoreImages

class IEMAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Company, IEMAdmin)
admin.site.register(Address, IEMAdmin)
admin.site.register(StoreImages, IEMAdmin)
