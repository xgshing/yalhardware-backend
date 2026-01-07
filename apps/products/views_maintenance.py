# apps/products/views_maintenance.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.products.models import Product, ProductImage, ProductVariant

@api_view(['POST'])
def clean_media_paths(request):
    c1 = ProductImage.objects.filter(image__startswith='media/').update(image='')
    c2 = ProductVariant.objects.filter(style_image__startswith='media/').update(style_image='')
    c3 = Product.objects.filter(cover__startswith='media/').update(cover='')

    return Response({
        'detail_images_cleared': c1,
        'variant_images_cleared': c2,
        'covers_cleared': c3,
    })
