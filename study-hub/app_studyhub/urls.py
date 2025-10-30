from django.urls import path

from .views import (
    AboutView,
    CategoryDetailView,
    CategoryListView,
    ContactView,
    HomeView,
    SearchView,
    SubcategoryDetailView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("about/", AboutView.as_view(), name="about-view"),
    path("contact/", ContactView.as_view(), name="contact-view"),
    path("search/", SearchView.as_view(), name="search-all-view"),
    path("category/", CategoryListView.as_view(), name="category-list-view"),
    path(
        "category/<slug:slug_name>/",
        CategoryDetailView.as_view(),
        name="category-detail-view",
    ),
    path(
        "category/<slug:category_slugname>/<slug:subcategory_slugname>/",
        SubcategoryDetailView.as_view(),
        name="subcategory-detail-view",
    ),
]
