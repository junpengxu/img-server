import os
import uuid
import json
import datetime
import requests
import traceback
from flask import Flask
from base import BaseView
from logger import request_logger
from config import WORK_DIR, SUCC_CODE, SUCC_MSG, FAIL_CODE, FAIL_MSG, IMG_VALID_CODE, IMG_VALID_MSG
app = Flask(__name__)
app.config.from_object("config")


class ImgUpload(BaseView):
    def post(self):
        try:
            file = self.request.files['file']
            business = self.request.args.get("business", "xcx")
            filename = self.gen_file_name(business=business, filetype=file.filename.split('.')[-1])
            file.save(os.path.join(WORK_DIR + filename))
            with open(os.path.join(WORK_DIR + filename),'rb+') as new_file:
            # 进行图片检查
                try:
                    self.wx_img_sec_check(self.img_check_uri, new_file)
                except AssertionError:
                    return self.formattingData(code=IMG_VALID_CODE, msg=IMG_VALID_MSG, data=None)
                except Exception as e:
                    request_logger.error(traceback.format_exc())
            return self.formattingData(code=SUCC_CODE, msg=SUCC_MSG, data=filename)
        except Exception as e:
            request_logger.error(traceback.format_exc())
            return self.formattingData(code=FAIL_CODE, msg=FAIL_MSG, data=None)

    def gen_file_name(self, business, filetype):
        # 放在统一层级，避免文件夹是否存在的判断
        return "/{}-{}-{}.{}".format(
            business, datetime.datetime.now().strftime("%Y%m%d"), uuid.uuid4().hex, filetype
        )

    @staticmethod
    def wx_img_sec_check(uri, file):
        res = requests.post(uri, files={"media": file}).json()
        print(res)
        assert res["errcode"] == 0


app.add_url_rule('/xcx/upload', view_func=ImgUpload.as_view('img_upload'))

if __name__ == '__main__':
    if not os.path.exists(app.config["WORK_DIR"]):
        os.makedirs(app.config["WORK_DIR"])
    app.run(port=app.config["SERVER_PORT"], debug=False)
