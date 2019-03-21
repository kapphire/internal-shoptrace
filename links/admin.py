from django.contrib import admin
from .models import (
    Link,
    Product,
    Inventory,
    SchedulerRecord,
    TypeLinkRecord,
)
# Register your models here.

admin.site.register(Link)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(SchedulerRecord)
admin.site.register(TypeLinkRecord)
