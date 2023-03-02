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
from rest_framework.decorators import authentication_classes, permission_classes, api_view


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Auth(self, request):
    return (JsonResponse({"logged": True}))


class AccountCreateView(APIView):
    def __init__(self):

        self.form = {
            'success': True,
            'msg': 'サインアップ完了'
        }

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

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        User.objects.get(request.user).delete()


class AccountLoginView(View):
    def post(self, request):
        reactObj = json.loads(request.body)
        try:
            user = User.objects.get(email=reactObj['email'])
            if check_password(reactObj['password'], user.password):
                token = str(Token.objects.get(user=user))
                return JsonResponse({'is_error': False, 'token': token, })
            else:
                return JsonResponse({'is_error': True, 'msg': 'パスワードが一致しません'})
        except User.DoesNotExist:
            return JsonResponse({'is_error': True, 'msg': 'アカウントが見つかりません'})


class ArticleApiView(APIView):
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

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        json_dict = json.loads(request.body)
        print(json_dict["seikaku"])
        try:
            article = Article(
                title=json_dict["title"],
                body=json_dict["body"],
                numbers=json_dict["numbers"],
                seikaku=json_dict["seikaku"],
                user=request.user,
            )
            article.save()
        except Exception as e:
            return JsonResponse({
                'is_error': True,
                'error': e
            })
        return JsonResponse({
            'is_error': False
        })

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        id = json.loads(request.body)
        article = Article.objects.get(id=id)
        if article.user == request.user:
            article.delete()


class EactArticleApiView(APIView):
    def get(self, request, id):
        try:
            article = Article.objects.get(id=id)
        except Exception as e:
            return JsonResponse({
                'error': e
            })
        num = article.numbers
        res = {
            'titel': article.title,
            'body': article.body,
            'seikaku': article.seikaku,
            'user': article.user.username,
            'user_id': article.user.id,
        }
        list = num.split(",")
        status = ['basenum', 'kotainum', 'doryokunum', 'jisuunum']
        for i in status:
            dict = list[0:6]
            list = list[6:]
            dictstr = ""
            for j in dict:
                dictstr += f"{j},"
            res[i] = dictstr
        return JsonResponse(res)

class MypageApiView(APIView):
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self,request):
        articles = Article.objects.filter(id=request.user.id)
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