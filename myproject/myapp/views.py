from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import re
from rest_framework.response import Response
from . models import *
from . authentication import create_access_token,decode_access_token
from django.contrib.auth.models import User
from rest_framework.authentication import get_authorization_header
from . serializers import AuthorSerializer,BookSerializer,ReviewAuthorSerializer

# Create your views here.


class SignUpApiview(APIView):
    def post(self,request):
        data = request.data

        if data['username'].isspace() or data['username'] == "":
            return JsonResponse({"message": "customer name is Manadatory", "status": False})
        if data['email'].isspace() or data['email'] == "":
            return JsonResponse({"message": "Email is Manadatory", "status": False})
        if data['password'].isspace() or data['password'] == "":
            return JsonResponse({"message": "password is Manadatory", "status": False})
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return Response({'message': "Enter Valid Email", "status": False})
        elif User.objects.filter(username=data['username']).exists():
            return Response({'message':"An account with the given username already exists","status":False})
        elif User.objects.filter(email=data['email']).exists():
            return Response({'message':"An account with the given email-id already exists","status":False})
        else:
            user = User.objects.create_user(username = data['username'],email=data['email'],password = data['password'])
            user.save()

            access_token = create_access_token(user.id)
            response = Response()
            response.data = {
                'token': access_token,
                'message': "successfully created",
                'status': True,
                'username': user.username,
            }

            return response

class LoginApiview(APIView):
    def post(self,request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user:
            # raise APIException("Invalid credentials!")
            return Response({"message":"Invalid credentials",'status':False})

        if not user.check_password(data['password']):
            return Response({"message": "Invalid Password", 'status': False})

        access_token = create_access_token(user.id)
        response = Response()
        response.data = {
            'token': access_token,
            'status':True,
            'username':user.username,
        }

        return response


class AuthorApi(APIView):
    def get(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            query_set = Authors.objects.filter(auth_user_id = user_id)
            serializer_class = AuthorSerializer
            data_json = {}
            serializer = serializer_class(query_set, many=True)
            data_json['author_list'] = serializer.data
            return Response(data_json)
        else:
            return Response({"message": "Unauthorized", 'status': False})


    def post(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            data = request.data
            if Authors.objects.filter(auth_user_id = user_id,name = data['name']).exists():
                return Response({'message': "Author Name Exists", "status": False})
            data_create = Authors.objects.create(
                auth_user_id = user_id,
                name = data['name']
            )
            return Response({'message':"successfully created","status":True})
        else:
            return Response({"message": "Unauthorized", 'status': False})



class BookApi(APIView):
    def get(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            query_set = Books.objects.filter(auth_user_id = user_id)
            serializer_class = BookSerializer
            data_json = {}
            serializer = serializer_class(query_set, many=True)
            data_json['book_list'] = serializer.data
            return Response(data_json)
        else:
            return Response({"message": "Unauthorized", 'status': False})


    def post(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            data = request.data
            if Books.objects.filter(auth_user_id = user_id,author_id_id=data['author_id'],name = data['name']).exists():
                return Response({'message': "Book Exists", "status": False})
            data_create = Books.objects.create(
                auth_user_id = user_id,
                author_id_id=data['author_id'],
                name = data['name']
            )
            return Response({'message':"successfully created","status":True})
        else:
            return Response({"message": "Unauthorized", 'status': False})

    def patch(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            book_id = request.query_params.get('id')
            data = request.data
            if Books.objects.filter(id=book_id,auth_user_id = user_id,author_id_id=data['author_id'],name = data['name']).exists():
                return Response({'message': "No Updates", "status": False})
            elif Books.objects.filter(auth_user_id = user_id,author_id_id=data['author_id'],name = data['name']).exists():
                return Response({'message': "Book Exists", "status": False})
            else:
                data_update = Books.objects.filter(id=book_id).update(
                    author_id_id=data['author_id'],
                    name=data['name']
                )
            return Response({'message':"Updated Successfully","status":True})
        else:
            return Response({"message": "Unauthorized", 'status': False})


from django.db.models import Sum
class ReviewApi(APIView):
    def post(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            data = request.data
            if data['author_id']:
                data_create = Reviews.objects.create(
                    auth_user_id=user_id,
                    author_id_id=data['author_id'],
                    review=data['review'],
                    rating=data['rating']
                )
                total_rating = Reviews.objects.filter(auth_user_id=user_id,author_id_id=data['author_id']).aggregate(total_count=Sum('rating'))['total_count']
                count = Reviews.objects.filter(auth_user_id=user_id,author_id_id=data['author_id']).count()
                avg_rating = float(total_rating / count)
                rounded_avg = round(avg_rating, 2)
                data_update = Authors.objects.filter(auth_user_id=user_id,id=data['author_id']).update(
                    total_rating=rounded_avg
                )
                return Response({'message':"successfully created","status":True})
            elif data['book_id']:
                data_create = Reviews.objects.create(
                    auth_user_id=user_id,
                    book_id_id=data['book_id'],
                    review=data['review'],
                    rating=data['rating']
                )
                total_rating = Reviews.objects.filter(auth_user_id=user_id,book_id_id=data['book_id']).aggregate(total_count=Sum('rating'))['total_count']
                count = Reviews.objects.filter(auth_user_id=user_id,book_id_id=data['book_id']).count()
                avg_rating = float(total_rating / count)
                rounded_avg = round(avg_rating, 2)
                data_update = Books.objects.filter(auth_user_id=user_id, id=data['book_id']).update(
                    total_rating=rounded_avg
                )
                return Response({'message':"successfully created","status":True})
            else:
                return Response({'message': "something went wrong", "status": False})
        else:
            return Response({"message": "Unauthorized", 'status': False})


class ReviewAuthor(APIView):
    def get(self,request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            decoded = decode_access_token(token)
            if decoded is None or decoded == "":
                return Response({"message": "authorization error", 'status': False})
            user_id = decoded['user_id']
            author_id = request.query_params.get('id')
            query_set = Reviews.objects.filter(auth_user_id = user_id,author_id=author_id)
            if query_set:
                serializer_class = ReviewAuthorSerializer
                data_json = {}
                serializer = serializer_class(query_set, many=True)
                data_json['review_author_list'] = serializer.data
                return Response(data_json)
            else:
                return Response({"message": "Invalid Data", 'status': False})
        else:
            return Response({"message": "Unauthorized", 'status': False})