import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Earliest First'),
        ('descending', 'Latest First')

    )

    ordering = django_filters.ChoiceFilter(label='Odering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Post
        fields = ('title', 'created')

    def filter_by_order(selfself, queryset, name, value):
        expression = 'created' if value == 'ascending' else '-created'
        return queryset.order_by(expression)