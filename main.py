# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 09:00
# @Author  : Zeeland
# @File    : main.py
# @Software: PyCharm

from PyQt5 import QtWidgets
from controller.HomeController import HomeController
from config.PoolConfig import PoolConfig

"""
@description: application gateways
"""
class SpireApplication:
    def __init__(self):
        # driver registration_list
        self.registration_list = {}
        # page dispatcher
        self.disp = None

        self.driver_registration()
        self.disp = PageDispatcher(self.registration_list)

    def driver_registration(self):
        # self.pool_config = PoolConfig()
        # self.registration_list['pool_config'] = self.pool_config
        # print(self.registration_list)
        print('[sys] driver registered finish')


"""
@description: application page dispatcher
@param      : registration_list驱动中心
"""
class PageDispatcher:
    def __init__(self, registration_list=None):
        self.registration_list = registration_list
        self.page_home_show(registration_list)
        print('[sys] page dispatcher finish')

    def page_home_show(self, registration_list=None):
        self.page_home = HomeController()
        self.page_home.show()


# main Application
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    a = SpireApplication()
    sys.exit(app.exec_())

