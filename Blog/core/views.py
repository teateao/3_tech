from django.shortcuts import render
from django.views.generic import View
from core.models import User, Article
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.


class AccountCreateView(View):
    def __init__(self):

        self.form = {
            'success': True,
            'msg': 'サインアップ完了'
        }

    # def get(self, request):
    #     return render(request, 'account/register.html')
    # post を追加

    def post(self, request):
        reactObj = json.loads(request.body)
        try:
            User.objects.create_user(
                username=reactObj['username'],
                email=reactObj['email'],
                password=reactObj['password'],
            )
        except:
            self.form = {
                'success': False,
                'msg': 'サインアップに失敗しました'
            }
        return (JsonResponse(self.form))


class AccountLoginView(View):
    def post(self, request):
        reactObj = json.loads(request.body)
        try:
            user = User.objects.get(email=reactObj['email'])
            if check_password(reactObj['password'], user.password):
                token = str(Token.objects.get(user=user))
                return JsonResponse({'is_error': False, 'token': token,})
            else:
                return JsonResponse({'is_error': True, 'msg': 'パスワードが一致しません'})
        except User.DoesNotExist:
            return JsonResponse({'is_error': True, 'msg': 'アカウントが見つかりません'})



class ArticleApiView(APIView):
    # authentication_classes = []
    # permission_classes = []
    def get(self, request):
        articles = Article.objects.all()
        dict_articles = []
        for article in articles:
            dict_article = {
                "id": article.id,
                "title": article.title,
            }
            dict_articles.append(dict_article)
        json = {
            "articles": dict_articles,
        }
        return JsonResponse(json)
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        json_dict = json.loads(request.body)
        try:
            article = Article(
                title=json_dict["title"],
                body=json_dict["body"],
                number=json_dict["number"],
                user=request.user
            )
            article.save()
        except:
            return JsonResponse({
                'is_error':True,
            })
        return JsonResponse({
            'is_error':False
        })
