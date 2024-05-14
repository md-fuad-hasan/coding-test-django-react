from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect
from product.forms import VariantForm
from product.models import Variant,Product,ProductVariant, ProductVariantPrice, ProductImage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import HttpResponseRedirect
from django.urls import reverse

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

class ProductView(ListView):
    model = Product
    template_name='products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = Product .objects.all()
        date = self.request.GET.get('date')
        title = self.request.GET.get('title')
        if title:
            queryset =  queryset.filter(title=title)
        if date:
            queryset = queryset.filter(created_at=date)
        return queryset



    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        ls = []
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')
        for q in list(context['products']):
            qs = ProductVariantPrice.objects.filter(product=q.id)
            if price_from:
                if price_from =='':
                    price_from = 0 
                qs = qs.filter(price__range=(price_from,price_to))
            if date:
                qs = qs.filter(created_at=date)
            ls.append(qs)
            context['prod'] = ls



        variants = Variant.objects.all()
        variantDic = {}
        for var in list(variants):
            prodVar_title = ProductVariant.objects.filter(variant=var.id).values('variant_title').distinct()
            variantDic[var.title]=prodVar_title

        context.update({'variant':variantDic})


        return context
    
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        body = data.get('body','')
        product = body['product']
        image = body['image']
        productVariants = body['productVariants']
        productVariantPrices = body['productVariantPrices']
        image = image[0]['path']

        prod = Product.objects.create(title=product['title'], sku=product['sku'], description=product['description'])
        
        img = ProductImage.objects.create(product=prod, file_path=image)
        
        if prod is not None:
            for item in productVariants:
                option = item['option']  # Access 'option' value
                variant = Variant.objects.get(id=option)
                
                tags = item['tags']      
                for tag in tags:
                    prodVar = ProductVariant.objects.create(variant_title=tag, variant=variant,product=prod)
            if prodVar :
                for proVarPrice in productVariantPrices:
                    title = proVarPrice['title']
                    price = proVarPrice['price']  
                    stock = proVarPrice['stock']
                    product_variant_one = None
                    product_variant_two = None
                    product_variant_three = None
                    varint = title.split('/')
                    for var in varint:
                        if var != '':
                            prodVarObj = ProductVariant.objects.filter(variant_title=var, product=prod)
                            prodVarObj = prodVarObj[0]

                            if prodVarObj.variant.id == 1:
                                product_variant_one = prodVarObj
                            elif prodVarObj.variant.id == 2:
                                product_variant_two = prodVarObj
                            else:              
                                product_variant_three = prodVarObj
                    obj = ProductVariantPrice.objects.create(product_variant_one=product_variant_one,product_variant_two=product_variant_two,product_variant_three=product_variant_three,price=price,stock=stock,product=prod)

                if obj:
                    return redirect('product:list.product')
                         

        return HttpResponse('Data received successfully')
    else:
        return HttpResponse('Only POST requests are allowed')
    


class BaseVariantView(generic.View):
    form_class = VariantForm
    model = Variant
    template_name = 'variants/create.html'
    success_url = '/product/variants'


class VariantView(BaseVariantView, ListView):
    template_name = 'variants/list.html'
    paginate_by = 10

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Variant.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET['title__icontains']
        return context


class VariantCreateView(BaseVariantView, CreateView):
    pass


class VariantEditView(BaseVariantView, UpdateView):
    pk_url_kwarg = 'id'
