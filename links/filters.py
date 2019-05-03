import django_filters
from .models import Link

class LinkFilter(django_filters.FilterSet):

    class Meta:
        model = Link
        fields = ['link_type', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Link.objects.exclude(deprecated=True)
