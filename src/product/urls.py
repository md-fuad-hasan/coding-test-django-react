from django.urls import path
from django.views.generic import TemplateView

from .views import VariantView, VariantCreateView, VariantEditView, CreateProductView, ProductView, create_product, ProductDetailView, update_product

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', ProductView.as_view(), name='list.product'),
    path('create/submit/', create_product, name='submit.product' ),
    path("<pk>/", ProductDetailView.as_view(), name='detail.product' ),
    path('update/', update_product, name='update.product')

]
