import os
import uuid
import datetime
from flask import Flask
from base import BaseView
from config import WORK_DIR, SUCC_CODE, SUCC_MSG

app = Flask(__name__)


class ImgUpload(BaseView):
    def post(self):
        file = self.request.files['file']
        business = self.request.args.get("business", "xcx")
        filename = self.gen_file_name(business=business, filetype=file.filename.split('.')[-1])
        file.save(os.path.join(WORK_DIR + filename))
        return self.formattingData(code=SUCC_CODE, msg=SUCC_MSG, data=filename)

    def gen_file_name(self, business, filetype):
        # 放在统一层级，避免文件夹是否存在的判断
        return "/{}-{}-{}.{}".format(
            business, datetime.datetime.now().strftime("%Y%m%d"), uuid.uuid4().hex, filetype
        )


app.add_url_rule('/xcx/upload', view_func=ImgUpload.as_view('img_upload'))

if __name__ == '__main__':
    if not os.path.exists(WORK_DIR):
        os.makedirs(WORK_DIR)
    app.run()
