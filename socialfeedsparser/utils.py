def get_source(slug):
    """
    Return source class from given slug
    """
    from .models import SOURCE
    for cls in SOURCE:
        if cls.slug == slug:
            return cls
