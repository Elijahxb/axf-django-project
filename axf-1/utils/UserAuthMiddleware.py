
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from app.models import UserModel


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 统一验证要求
        if request.path == '/axf/login/' or request.path == '/axf/regist/' or request.path == '/axf/home/':
            return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect('/axf/login')
        users = UserModel.objects.filter()
        if not users:
            return HttpResponseRedirect('/axf/login/')
        request.user = users[0]
