from django.shortcuts import get_object_or_404

class SlugMixin(object):
    model = None
    def get_object(self, *args, **kwargs):
        # print(**kwargs)
        slug = self.kwargs.get("slug")
        model_class = self.model
        if slug is not None:
            try:
                obj = get_object_or_404(model_class, slug=slug)
            except:
                #if there are multiple slugs with the same name, return the first
                obj = model_class.objects.filter(slug=slug).order_by("name").first()
        else:
            obj = super(SlugMixin, self).get_object(*args, **kwargs)
        return obj
