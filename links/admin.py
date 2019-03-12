from django.contrib import admin
from .models import (
    Link,
    Product,
    Inventory,
    SchedulerTestRecord
)
# Register your models here.

admin.site.register(Link)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(SchedulerTestRecord)
