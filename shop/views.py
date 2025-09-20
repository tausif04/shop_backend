from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
# CORRECTED: Import all necessary models with their correct names
from .models import Shops, ShopShop, ShopShopdocument, ShopShopattachment
# CORRECTED: Import the missing ShopDetailSerializer
from .serializers import ShopSerializer, ShopDetailSerializer, ShopDocumentSerializer, ShopAttachmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([IsAdminUser])
def shop_groups(request):
    qs = Shops.objects.all()
    serialize = lambda q: ShopSerializer(q, many=True).data
    groups = {
        'pending': serialize(qs.filter(status='pending')),
        'approved': serialize(qs.filter(status='approved')),
        'rejected': serialize(qs.filter(status='rejected')),
        'modification': serialize(qs.filter(status='modification')),
    }
    return Response(groups)


@api_view(['GET'])
@permission_classes([AllowAny])
def shop_list_public(request):
    qs = Shops.objects.all()
    data = ShopSerializer(qs, many=True).data
    return Response({'shops': data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_shop(request, pk: int):
    try:
        s = Shops.objects.get(pk=pk)
        s.status = 'approved'
        s.save(update_fields=['status']) # Note: updated_at is likely auto-updating
        return Response({'ok': True})
    except Shops.DoesNotExist:
        return Response({'ok': False, 'error': 'not_found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_shop(request, pk: int):
    try:
        s = Shops.objects.get(pk=pk)
        s.status = 'rejected'
        s.save(update_fields=['status'])
        return Response({'ok': True})
    except Shops.DoesNotExist:
        return Response({'ok': False, 'error': 'not_found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_shops(request):
    # The decorator already ensures request.user is authenticated
    qs = Shops.objects.filter(owner__keycloak_user_id=request.user.username) # Assuming keycloak_user_id matches username
    return Response(ShopSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_shop_detail(request, pk: int):
    # The decorator ensures user is authenticated
    shop = get_object_or_404(Shops, pk=pk, owner__keycloak_user_id=request.user.username)
    # CORRECTED: This now uses the ShopDetailSerializer which you must create
    serializer = ShopDetailSerializer(shop, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_shop(request):
    user = request.user
    name = request.data.get('name')
    if not name:
        return Response({'detail': 'name required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # This assumes a UserProfile is created for the user. 
    # This might need adjustment based on your user creation logic.
    user_profile = get_object_or_404("UserProfiles", keycloak_user_id=user.username)
    
    s = Shops.objects.create(owner=user_profile, shop_name=name, status='pending')
    return Response(ShopSerializer(s).data, status=status.HTTP_201_CREATED)


# --- Views for Legacy Shop Models ---
# NOTE: These views now correctly interact with the legacy ShopShop models.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request, pk: int):
    user = request.user
    # CORRECTED: Fetches the legacy ShopShop model, not the new Shops model
    shop = get_object_or_404(ShopShop, pk=pk, owner=user)
    
    doc_type = request.data.get('doc_type') or request.data.get('type')
    number = request.data.get('number', '')
    file = request.FILES.get('file')
    
    if not file or not doc_type:
        return Response({'detail': 'file and doc_type are required'}, status=400)
    
    # CORRECTED: Creates the correct legacy document model
    doc = ShopShopdocument.objects.create(shop=shop, doc_type=doc_type, number=number, file=file)
    serializer = ShopDocumentSerializer(doc, context={'request': request})
    return Response(serializer.data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_attachment(request, pk: int):
    user = request.user
    # CORRECTED: Fetches the legacy ShopShop model
    shop = get_object_or_404(ShopShop, pk=pk, owner=user)
    
    file = request.FILES.get('file')
    name = request.data.get('name', '')
    
    if not file:
        return Response({'detail': 'file is required'}, status=400)
        
    # CORRECTED: Creates the correct legacy attachment model
    att = ShopShopattachment.objects.create(shop=shop, file=file, name=name or getattr(file, 'name', ''))
    serializer = ShopAttachmentSerializer(att, context={'request': request})
    return Response(serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def shop_detail_admin(request, pk: int):
    shop = get_object_or_404(Shops, pk=pk)
    # CORRECTED: Uses the ShopDetailSerializer
    serializer = ShopDetailSerializer(shop, context={'request': request})
    return Response(serializer.data)
