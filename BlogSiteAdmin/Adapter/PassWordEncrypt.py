import pyDes
import base64


class DES3:

    def __init__(self, key=""):
        # 初始化加密对象  使用对称加密算法
        self.encryption = pyDes.triple_des(key, padmode=pyDes.PAD_PKCS5)

    def des3_encrypt(self, pwd):
        """
        加密
        :param pwd: 密码明文
        :return:
        """
        sec_ = self.encryption.encrypt(pwd.encode())
        secret = base64.standard_b64encode(sec_).decode()

        return secret

    def des3_decrypt(self, text):
        """
        解密
        :param text: 加密后的密码
        :return:
        """
        pwd_ = self.encryption.decrypt(base64.standard_b64decode(text.encode()))
        pwd = pwd_.decode()

        return pwd