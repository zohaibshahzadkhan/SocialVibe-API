from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from django.db.models import Q



@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
    else:
        message = form.errors.as_json()

    return JsonResponse({'message': message}, safe=False)

@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []
    can_send_request = True 

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)

    existing_request = FriendshipRequest.objects.filter(
        (Q(created_for=user) & Q(created_by=request.user)) |
        (Q(created_for=request.user) & Q(created_by=user))
    ).first()

    are_friends = user.friends.filter(pk=request.user.pk).exists()
     
    if (existing_request and existing_request.status == FriendshipRequest.SENT) or are_friends:
        can_send_request = False
        
    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendshipRequestSerializer(requests, many=True).data,
        'can_send_request': can_send_request
    }, safe=False)


@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    try:
        friendship_request = FriendshipRequest.objects.get(created_for=request.user, created_by=user)
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'error': 'Friendship request not found'}, status=404)

    if status not in [FriendshipRequest.ACCEPTED, FriendshipRequest.REJECTED]:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    friendship_request.status = status
    friendship_request.save()

    if status == FriendshipRequest.ACCEPTED:
        user.friends.add(request.user)
        user.friends_count += 1
        user.save()

        request_user = request.user
        request_user.friends.add(user)
        request_user.friends_count += 1
        request_user.save()
    elif status == FriendshipRequest.REJECTED:
        friendship_request.delete()

    return JsonResponse({'message': 'Friendship request updated', 'status': status})

@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)

        return JsonResponse({'message': 'information updated', 'user': serializer.data})