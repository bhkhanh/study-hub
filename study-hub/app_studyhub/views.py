from app_account.models import Feedback
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import FeedbackForm
from .models import Category, File, Subcategory


class HomeView(TemplateView):
    """
    "Home" (Trang chủ) page view.
    """

    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        search_query = request.POST.get("search").strip()
        if search_query:
            return HttpResponseRedirect(redirect_to=reverse_lazy("search-all-view"))
        return HttpResponseRedirect(redirect_to=reverse_lazy("home-view"))


class AboutView(TemplateView):
    """
    "About us" (Về StudyHub) page view.
    """

    template_name = "about.html"
    extra_context = {
        "metadata_title": _("Về chúng tôi | StudyHub"),
    }


class ContactView(CreateView):
    """
    "Contact us" (Liên hệ) page view.
    """

    model = Feedback
    form_class = FeedbackForm
    template_name = "contact.html"
    success_url = reverse_lazy("contact-view")
    extra_context = {
        "metadata_title": _("Liên hệ | StudyHub"),
    }

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": True,
                    "message": _(
                        "Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể."
                    ),
                },
                status=201,
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            field_errors = {}
            for field_name, error_list in form.errors.items():
                field_errors[field_name] = [str(error) for error in error_list]
            non_field_errors = []
            if form.non_field_errors():
                non_field_errors = [str(error) for error in form.non_field_errors()]
            return JsonResponse(
                {
                    "success": False,
                    "errors": field_errors,
                    "non_field_errors": non_field_errors,
                },
                status=400,
            )
        return super().form_invalid(form)


class CategoryListView(ListView):
    """
    List of categories (Phân loại) page view.
    """

    model = Category
    template_name = "category/category-list.html"
    context_object_name = "category_list"
    extra_context = {
        "metadata_title": _("Phân loại | StudyHub"),
    }


class CategoryDetailView(DetailView):
    """
    Detail page view of a specific category.

    And this page view is also the list of
    subcategories/subjects belongs to a specific category.
    """

    model = Category
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    template_name = "category/category-detail.html"
    context_object_name = "category_detail"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_obj = self.get_object()
        context_data["metadata_title"] = f"{category_obj.name} | StudyHub"
        context_data["subcategory_list"] = Subcategory.objects.filter(
            category=category_obj
        )
        return context_data


class SubcategoryDetailView(DetailView):
    """
    Detail page view of a specific subcategory/subject.

    This page view is also the list of files
    belongs to a specific subcategory/subject.
    """

    model = Subcategory
    slug_field = "slug_name"
    slug_url_kwarg = "subcategory_slugname"
    template_name = "category/subcategory-detail.html"
    context_object_name = "subcategory"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        subcategory_obj = self.get_object()
        context_data["metadata_title"] = f"{subcategory_obj.name} | StudyHub"
        return context_data

    def get_datatables_data(self, request):
        """
        Handle DataTables.net Ajax requests.
        """

        obj_query = self.get_object().files.all()
        data_list = []
        for each in obj_query:
            data_list.append(
                {
                    "id": str(each.id),
                    "name": each.name,
                    "category": each.subcategory.category.name,
                    "subcategory": each.subcategory.name,
                    "file_type": each.get_file_type_display(),
                    "file_language": each.get_file_language_display(),
                    "uploaded_file": each.uploaded_file.url,
                    "last_modified": (
                        each.last_modified.date().strftime("%d/%m/%Y")
                        if each.last_modified
                        else each.date_created.date().strftime("%d/%m/%Y")
                    ),
                }
            )
        return JsonResponse({"data": data_list})

    def get(self, request, *args, **kwargs):
        # Check if this is an Ajax request or not
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.get_datatables_data(request)
        # Otherwise, render this page/view normally
        return super().get(request, *args, **kwargs)


class SearchView(ListView):
    """
    "Search" (Tìm kiếm) page view.

    This view queries all objects from File model.
    """

    model = File
    template_name = "search.html"
    extra_context = {
        "metadata_title": _("Tìm kiếm | StudyHub"),
    }

    def get_queryset(self):
        """
        Return empty query/none objects
        because DataTables.net will fetch data via Ajax.
        """
        return File.objects.none()

    def get_datatables_data(self, request):
        """
        Handle DataTables.net Ajax requests.
        """

        allObjectsQuery = File.objects.select_related("subcategory").order_by("name")
        data_list = []
        for each in allObjectsQuery:
            data_list.append(
                {
                    "id": str(each.id),
                    "name": each.name,
                    "category": each.subcategory.category.name,
                    "subcategory": each.subcategory.name,
                    "file_type": each.get_file_type_display(),
                    "file_language": each.get_file_language_display(),
                    "uploaded_file": each.uploaded_file.url,
                    "last_modified": (
                        each.last_modified.date().strftime("%d/%m/%Y")
                        if each.last_modified
                        else each.date_created.date().strftime("%d/%m/%Y")
                    ),
                }
            )
        return JsonResponse({"data": data_list})

    def get(self, request, *args, **kwargs):
        # Check if this is an Ajax request or not
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.get_datatables_data(request)
        # Otherwise, render this page/view normally
        return super().get(request, *args, **kwargs)
