
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from app.models import UserModel, UserTicket
from datetime import datetime


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 统一验证要求
        # if request.path == '/axf/login/' or request.path == '/axf/regist/' or request.path == '/axf/home/':
        #     return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            # 没有登录，页面不作处理
            # return HttpResponseRedirect('/axf/login')
            return None
        # users = UserModel.objects.filter()
        user_ticket = UserTicket.objects.filter(ticket=ticket)
        # if users:
        #     pass
        #
        # if not users:
        #     return HttpResponseRedirect('/axf/login/')
        # request.user = users[0]
        if user_ticket:
            # 判断令牌是否有效
            out_time = user_ticket[0].out_time.replace(tzinfo=None)
            now_time = datetime.utcnow()

            if out_time > now_time:
                # 没有失效
                request.user = user_ticket[0].user

            else:
                # 失效
                user_ticket.delete()
