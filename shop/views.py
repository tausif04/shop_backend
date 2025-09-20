from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Shop
from .serializers import ShopSerializer, ShopDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from users.models import User

@api_view(['GET'])
@permission_classes([IsAdminUser])
def shop_groups(request):
    qs = Shop.objects.all()
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
    qs = Shop.objects.all()
    data = ShopSerializer(qs, many=True).data
    return Response({'shops': data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_shop(request, pk: int):
    try:
        s = Shop.objects.get(pk=pk)
        s.status = 'approved'
        s.save(update_fields=['status'])
        return Response({'ok': True})
    except Shop.DoesNotExist:
        return Response({'ok': False, 'error': 'not_found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_shop(request, pk: int):
    try:
        s = Shop.objects.get(pk=pk)
        s.status = 'rejected'
        s.save(update_fields=['status'])
        return Response({'ok': True})
    except Shop.DoesNotExist:
        return Response({'ok': False, 'error': 'not_found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_shops(request):
    qs = Shop.objects.filter(owner=request.user)
    return Response(ShopSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_shop_detail(request, pk: int):
    shop = get_object_or_404(Shop, pk=pk, owner=request.user)
    serializer = ShopDetailSerializer(shop, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_shop(request):
    user = request.user
    name = request.data.get('name')
    if not name:
        return Response({'detail': 'name required'}, status=status.HTTP_400_BAD_REQUEST)
    
    s = Shop.objects.create(owner=user, name=name, status='pending')
    return Response(ShopSerializer(s).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def shop_detail_admin(request, pk: int):
    shop = get_object_or_404(Shop, pk=pk)
    serializer = ShopDetailSerializer(shop, context={'request': request})
    return Response(serializer.data)
