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

from config import FAIL_MSG, FAIL_CODE
from flask.views import MethodView
from flask import request, jsonify
from logger import request_logger
import requests


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.__ckeck_login_uri = "https://weakee.com/xcx/check_user_valid"
        self.__setattr__('request', request)
        self.__setattr__('session_id', request.headers.get("Token"))
        # self.check_login()
        request_logger.info("request json params is:{}".format({} if not self.request.data else self.request.json))
        request_logger.info("request args params is:{}".format(self.request.args))
        super(BaseView, self).__init__(*args, **kwargs)

    def check_login(self):
        if not self.session_id:
            return jsonify(
                {
                    "code": FAIL_CODE,
                    "message": FAIL_CODE,
                    "data": None
                }
            )
        else:
            try:
                assert requests.request(
                    method="get", url=self.__ckeck_login_uri,
                    headers={"Token": self.session_id}
                ).json()['code'] == 20000
            except Exception as e:
                pass

    def formattingData(self, code, msg, data):
        return jsonify(
            {
                "code": code,
                "message": msg,
                "data": data
            }
        )

    def dispatch_request(self, *args, **kwargs):
        return super(BaseView, self).dispatch_request(*args, **kwargs)
