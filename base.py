# -*- coding: utf-8 -*-
# @Time    : 2021/7/1 1:02 上午
# @Author  : xu.junpeng

# from functools import wraps
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 1:
#             return
#         return f(*args, **kwargs)
#
#     return decorated_function
import traceback
from config import USER_VALID_CODE, USER_VALID_MSG
from flask.views import MethodView
from flask import request, jsonify
from logger import request_logger
import requests


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.__ckeck_login_uri = "https://weakee.com/xcx/check_user_valid"
        self.__setattr__('request', request)
        self.__setattr__('session_id', request.headers.get("Token"))
        request_logger.info("request json params is:{}".format({} if not self.request.data else self.request.json))
        request_logger.info("request args params is:{}".format(self.request.args))
        super(BaseView, self).__init__(*args, **kwargs)

    def check_login(self):
        """
        这是个临时服务，目前由于微信要进行图片检查，需要携带access_token, 所以借用这个接口返回请求的uri
        :return:
        """
        if not self.session_id:
            return False
        else:
            try:
                res = requests.request(
                    method="get", url=self.__ckeck_login_uri,
                    headers={"Token": self.session_id}
                ).json()
                request_logger.info(res)
                assert res['code'] == 20000
                return res['data']
            except Exception as e:
                request_logger.error("check user raise error, session id is {}".format(self.session_id))
                request_logger.error(traceback.format_exc())
        return False

    def formattingData(self, code, msg, data):
        return jsonify(
            {
                "code": code,
                "message": msg,
                "data": data
            }
        )

    def dispatch_request(self, *args, **kwargs):
        res = self.check_login()
        if not res:
            return jsonify({"code": USER_VALID_CODE, "message": USER_VALID_MSG, "data": None})
        else:
            self.img_check_uri = res
        return super(BaseView, self).dispatch_request(*args, **kwargs)
