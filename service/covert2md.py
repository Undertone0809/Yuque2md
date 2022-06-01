# -*- coding: utf-8 -*-
# @Time    : 2022/6/1 18:39
# @Author  : Zeeland
# @File    : covert2md.py
# @Software: PyCharm
import os
import re

class Covert2md:

    """
    @attention: file_path is needed absolute path
    """
    def __init__(self,file_path=''):
        self.file_path = file_path
        self.original_text = ''
        self.after_text = ''

    def set_file_path(self,file_path):
        self.file_path = file_path

    def get_original_text(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.original_text = file.read()
            file.close()
            return self.original_text

    def covert(self):
        # judge file_path is empty
        if self.file_path=='':
            return
        with open(self.file_path,'r',encoding='utf-8') as file:
            self.original_text = file.read()
            self.after_text = self.original_text
            all_img_feature_text = re.findall("#clientId=.*width=.*\\)",self.original_text)
            print('[info by service] all_img_feature_text :{}'.format(all_img_feature_text))

            # covert text
            for item in all_img_feature_text:
                self.after_text = self.after_text.replace(item[:-1],'')
            file.close()

        with open(self.file_path, 'w', encoding='utf-8') as file:
            # write the modified text
            file.write(self.after_text)
            print('[info by service] write to successfully')
            file.close()

    def get_after_text(self):
        return self.after_text

# you can run this demo to test the function
if __name__ == '__main__':
    FILE_PATH = os.path.abspath(os.path.join(os.getcwd(), '..')) + '\static\Computer Network.md'
    covert_serivce = Covert2md(FILE_PATH)
    covert_serivce.covert()
