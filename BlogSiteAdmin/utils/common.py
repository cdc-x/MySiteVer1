import hashlib


def encrypt_str(key, text):
    """
    加密字符串
    :param key: 密钥
    :param text: 要加密的内容
    :return:
    """
    m = hashlib.md5()
    m.update(key.encode('utf-8'))  # 对内容加盐
    m.update(text.encode('utf-8'))

    return m.hexdigest()
