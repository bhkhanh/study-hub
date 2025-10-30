from .models import Category


def category_list(request):
    """Context processor to provide the list of categories to templates."""

    try:
        # Check if Category model exists and has objects
        if hasattr(Category, "objects"):
            category_list = Category.objects.all()
            # Check if queryset is empty
            if category_list.exists():
                return {"category_list": category_list}
            else:
                return {"category_list": []}
        else:
            return {"category_list": []}
    except (Exception, ImportError) as e:
        # Print to console the error message
        print(f"--- [ERROR] --- CATEGORY LIST: {e}")
        return {"category_list": []}
