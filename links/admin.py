from django.contrib import admin
from .models import (
    Link,
    Product,
    Inventory,
    SchedulerLookUp,
    SchedulerRecord,
    TypeLinkRecord,
    BestProduct,
)
# Register your models here.

admin.site.register(Link)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(SchedulerLookUp)
admin.site.register(SchedulerRecord)
admin.site.register(TypeLinkRecord)
admin.site.register(BestProduct)
