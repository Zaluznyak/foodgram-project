from .models import Tag


class TagMixin:
    @property
    def extra_context(self):
        return {'active_tags': self.request.GET.getlist('tags'),
                'tags': Tag.objects.all(),
                }
