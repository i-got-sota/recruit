import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserCreateSerializer, UserUpdateSerializer
from .models import User

@api_view(["POST"])
def signup(request):
    if (not request.data.get("user_id") and not request.data.get("password")):
        return Response(
            data = {
                "message": "Account creation failed",
                "cause": "required user_id and password"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(nickname=serializer.validated_data.get("user_id"))
        return Response(
            data={
                "message": "Account successfully created",
                "user": {
                    "user_id": serializer.data.get("user_id"),
                    "nickname": serializer.data.get("user_id")
                }
                
            },
            status=status.HTTP_200_OK
        )
    
    else:
        return Response(
            data={
                "message": "Account creation failed",
                "cause": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["GET", "PATCH"])
def users(request, pk):
    if (authorization_header := request.META.get("HTTP_AUTHORIZATION")):
        message = authorization_header.split(" ")[1][1:-1]
        decoded_message = base64.b64decode(message)
        user_id, password = decoded_message.split(":")
        try:
            user = User.objects.get(user_id=pk)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "No User found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if (user.user_id != user_id and request.method == "PATCH"):
            return Response(
                data={
                    "message": "No Permission for Update"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        if not (user.user_id == user_id and user.password == password):
            return Response(
                data={
                    "message": "Authentication Failed"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    else:
        return Response(
            data={
                "message": "Authentication Failed"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if (request.method == "GET"):
        return_dict = {
            "user_id": user.user_id,
            "nickname": user.nickname,
        }
        if user.comment:
            return_dict["comment"] = user.comment

        return Response(
            data={
                "message": "User details by user_id",
                "user": return_dict  
            },
            status=status.HTTP_200_OK
        )
    else:
        if (request.data.get("user_id") or request.data.get("password")):
            return Response(
                data={
                    "message": "User updation failed",
                    "cause": "not updatable user_id and password"
                    
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            if (not serializer.data.get("nickname") and not serializer.data.get("comment")):
                return Response(
                    data={
                        "message": "User updation failed",
                        "cause": "required nickname or comment"
                        
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                data={
                    "message": "Account successfully updated",
                    "recipe": {
                        "nickname": serializer.data.get("nickname"),
                        "comment": serializer.data.get("comment")
                    }
                    
                },
                status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                data={
                    "message": "Account creation failed",
                    "cause": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    
@api_view(["POST"])
def close(request):
    if (authorization_header := request.META.get("HTTP_AUTHORIZATION")):
        message = authorization_header.split(" ")[1][1:-1]
        decoded_message = base64.b64decode(message)
        user_id, password = decoded_message.split(":")
        try:
            delete_user = User.objects.get(user_id=user_id, password=password)
                
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "Authentication Failed"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    else:
        return Response(
            data={
                "message": "Authentication Failed"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    User.objects.delete(delete_user)

    return Response(
        data={
                "message": "Account and user successfully removed"
            },
            status=status.HTTP_200_OK
    )