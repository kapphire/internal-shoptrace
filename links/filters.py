import django_filters
from django.db.models import Q
from .models import Link

class LinkFilter(django_filters.FilterSet):

    class Meta:
        model = Link
        fields = ['link_type', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user
        # self.queryset = Link.objects.exclude(deprecated=True)
        self.queryset = Link.objects.filter(
            ~Q(deprecated=True),
            Q(user=user) | Q(user=None)
        )
