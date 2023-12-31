
import os
import shutil
import pytest
from conf.settings import BASE_DIR
from utils.AllureHandler import AllureOperate

if __name__ == '__main__':
    # 删除之前的json文件
    dir_path = os.path.join(BASE_DIR, 'report', 'json_result')
    shutil.rmtree(dir_path)
    # 更改工作目录
    os.chdir(BASE_DIR)
    # 执行用例
    pytest.main()
    # 生成allure报告
    allure_obj = AllureOperate()
    allure_obj.get_allure_report()
    # 压缩文件
    allure_obj.check_zip()
    # 发邮件
    # allure_obj.send_mail()
