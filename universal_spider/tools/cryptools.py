# -*- coding: UTF-8 -*-
'''
@Project ：spider_toolsbox
@File    ：cryptools.py
@IDE     ：PyCharm
@Author  ：JOUSKA.
@Date    ：2024-05-17 12:35
'''
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import hashlib
import hmac
import base64

class Cryptor:
    def encrypt_AESCBC(self, data, key, iv, output_format='base64'):
        """
        使用AES CBC模式加密数据，支持自定义key、iv及输出格式
        :param data: 待加密的明文数据（bytes类型）
        :param key: 自定义的密钥（bytes类型）
        :param iv: 自定义的初始化向量（bytes类型，长度必须为16字节）
        :param output_format: 输出格式，可选'base64'或'hex'（默认'base64'）
        :return: 根据指定格式编码后的加密密文（str类型）
        """
        if len(iv) != AES.block_size:
            raise ValueError("IV length must be 16 bytes")

        cipher = AES.new(key.encode(), AES.MODE_CBC, iv=iv.encode())
        padded_data = pad(data.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_data)

        if output_format == 'base64':
            encoded_ciphertext = base64.b64encode(ciphertext)
            return encoded_ciphertext.decode('utf-8')
        elif output_format == 'hex':
            encoded_ciphertext = ciphertext.hex()
            return encoded_ciphertext
        else:
            raise ValueError("Invalid output format. Supported formats are 'base64' and 'hex'.")

    def decrypt_AESCBC(self, encoded_ciphertext, key, iv, input_format='base64'):
        """
        使用AES CBC模式解密数据，支持自定义key、iv及输入格式
        :param encoded_ciphertext: 经过编码的密文数据（str类型）
        :param key: 自定义的密钥（bytes类型）
        :param iv: 自定义的初始化向量（bytes类型，长度必须为16字节）
        :param input_format: 输入格式，可选'base64'或'hex'（默认'base64'）
        :return: 解密后的明文数据（bytes类型）
        """
        if len(iv) != AES.block_size:
            raise ValueError("IV length must be 16 bytes")

        if input_format == 'base64':
            ciphertext = base64.b64decode(encoded_ciphertext.encode('utf-8'))
        elif input_format == 'hex':
            ciphertext = bytes.fromhex(encoded_ciphertext)
        else:
            raise ValueError("Invalid input format. Supported formats are 'base64' and 'hex'.")

        cipher = AES.new(key.encode(), AES.MODE_CBC, iv=iv.encode())
        padded_data = cipher.decrypt(ciphertext)
        data = unpad(padded_data, AES.block_size)

        return data.decode()

    def encrypt_AESECB(self, data, key, output_format='base64'):
        """
        使用AES ECB模式加密数据，支持自定义key及输出格式
        :param data: 待加密的明文数据（bytes类型）
        :param key: 自定义的密钥（bytes类型）
        :param output_format: 输出格式，可选'base64'或'hex'（默认'base64'）
        :return: 根据指定格式编码后的加密密文（str类型）
        """
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        padded_data = pad(data.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_data)

        if output_format == 'base64':
            encoded_ciphertext = base64.b64encode(ciphertext)
            return encoded_ciphertext.decode('utf-8')
        elif output_format == 'hex':
            encoded_ciphertext = ciphertext.hex()
            return encoded_ciphertext
        else:
            raise ValueError("Invalid output format. Supported formats are 'base64' and 'hex'.")

    def decrypt_AESECB(self, encoded_ciphertext, key, input_format='base64'):
        """
        使用AES ECB模式解密数据，支持自定义key及输入格式
        :param encoded_ciphertext: 经过编码的密文数据（str类型）
        :param key: 自定义的密钥（bytes类型）
        :param input_format: 输入格式，可选'base64'或'hex'（默认'base64'）
        :return: 解密后的明文数据（bytes类型）
        """
        if input_format == 'base64':
            ciphertext = base64.b64decode(encoded_ciphertext.encode('utf-8'))
        elif input_format == 'hex':
            ciphertext = bytes.fromhex(encoded_ciphertext)
        else:
            raise ValueError("Invalid input format. Supported formats are 'base64' and 'hex'.")

        cipher = AES.new(key.encode(), AES.MODE_ECB)
        padded_data = cipher.decrypt(ciphertext)
        data = unpad(padded_data, AES.block_size)

        return data.decode()

    def encrypt_DESCBC(self, data, key, iv, output_format='base64'):
        """
        使用DES CBC模式加密数据，支持自定义key、iv及输出格式
        :param data: 待加密的明文数据（bytes类型）
        :param key: 自定义的密钥（bytes类型，长度必须为8字节）
        :param iv: 自定义的初始化向量（bytes类型，长度必须为8字节）
        :param output_format: 输出格式，可选'base64'或'hex'（默认'base64'）
        :return: 根据指定格式编码后的加密密文（str类型）
        """
        if len(iv) != DES.block_size:
            raise ValueError("DES key length must be 8 bytes and IV length must be 8 bytes.")

        cipher = DES.new(key.encode(), DES.MODE_CBC, iv=iv.encode())
        padded_data = pad(data.encode(), DES.block_size)
        ciphertext = cipher.encrypt(padded_data)

        if output_format == 'base64':
            encoded_ciphertext = base64.b64encode(ciphertext)
            return encoded_ciphertext.decode('utf-8')
        elif output_format == 'hex':
            encoded_ciphertext = ciphertext.hex()
            return encoded_ciphertext
        else:
            raise ValueError("Invalid output format. Supported formats are 'base64' and 'hex'.")

    def decrypt_DESCBC(self, encoded_ciphertext, key, iv, input_format='base64'):
        """
        使用DES CBC模式解密数据，支持自定义key、iv及输入格式
        :param encoded_ciphertext: 经过编码的密文数据（str类型）
        :param key: 自定义的密钥（bytes类型，长度必须为8字节）
        :param iv: 自定义的初始化向量（bytes类型，长度必须为8字节）
        :param input_format: 输入格式，可选'base64'或'hex'（默认'base64'）
        :return: 解密后的明文数据（bytes类型）
        """
        if len(iv) != DES.block_size:
            raise ValueError("DES key length must be 8 bytes and IV length must be 8 bytes.")

        if input_format == 'base64':
            ciphertext = base64.b64decode(encoded_ciphertext.encode('utf-8'))
        elif input_format == 'hex':
            ciphertext = bytes.fromhex(encoded_ciphertext)
        else:
            raise ValueError("Invalid input format. Supported formats are 'base64' and 'hex'.")

        cipher = DES.new(key.encode(), DES.MODE_CBC, iv=iv.encode())
        padded_data = cipher.decrypt(ciphertext)
        data = unpad(padded_data, DES.block_size)

        return data.decode()

    def encrypt_DESECB(self, data, key, output_format='base64'):
        """
        使用DES ECB模式加密数据，支持自定义key及输出格式
        :param data: 待加密的明文数据（bytes类型）
        :param key: 自定义的密钥（bytes类型，长度必须为8字节）
        :param output_format: 输出格式，可选'base64'或'hex'（默认'base64'）
        :return: 根据指定格式编码后的加密密文（str类型）
        """
        if len(key) != DES.key_size:
            raise ValueError("DES key length must be 8 bytes.")

        cipher = DES.new(key.encode(), DES.MODE_ECB)
        padded_data = pad(data.encode(), DES.block_size)
        ciphertext = cipher.encrypt(padded_data)

        if output_format == 'base64':
            encoded_ciphertext = base64.b64encode(ciphertext)
            return encoded_ciphertext.decode('utf-8')

        elif output_format == 'hex':
            encoded_ciphertext = ciphertext.hex()
            return encoded_ciphertext
        else:
            raise ValueError("Invalid output format. Supported formats are 'base64' and 'hex'.")

    def decrypt_DESECB(self, encoded_ciphertext, key, input_format='base64'):
        """
        使用DES ECB模式解密数据，支持自定义key及输入格式
        :param encoded_ciphertext: 经过编码的密文数据（str类型）
        :param key: 自定义的密钥（bytes类型，长度必须为8字节）
        :param input_format: 输入格式，可选'base64'或'hex'（默认'base64'）
        :return: 解密后的明文数据（bytes类型）
        """
        if len(key) != DES.key_size:
            raise ValueError("DES key length must be 8 bytes.")

        if input_format == 'base64':
            ciphertext = base64.b64decode(encoded_ciphertext.encode('utf-8'))
        elif input_format == 'hex':
            ciphertext = bytes.fromhex(encoded_ciphertext)
        else:
            raise ValueError("Invalid input format. Supported formats are 'base64' and 'hex'.")

        cipher = DES.new(key.encode(), DES.MODE_ECB)
        padded_data = cipher.decrypt(ciphertext)
        data = unpad(padded_data, DES.block_size)

        return data.decode()

    def encrypt_RSA(self, data, pubkey=None):
        """
        使用RSA加密数据。

        参数:
        - data: 待加密的字节串数据。
        - pubkey: 公钥，默认情况下会生成一个具有指定模值n的新密钥对。
        - n: RSA模数，默认值10001，注意此值在实际应用中应足够大以保证安全性。

        返回:
        - 加密后的数据（base64编码的字节串）。
        """
        if pubkey is None:
            raise ValueError("Public key must be provided for RSA encryption")
        else:
            key = RSA.import_key(pubkey)

        cipher = PKCS1_OAEP.new(key)
        encrypted_data = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()

    def decrypt_RSA(self, encrypted_data, privkey):
        """
        使用RSA解密数据。

        参数:
        - encrypted_data: 已加密的Base64编码的字节串数据。
        - privkey: 私钥，用于解密数据。

        返回:
        - 原始的明文字符串数据。
        """
        # 将接收到的Base64编码的加密数据解码回字节串
        encrypted_data_bytes = base64.b64decode(encrypted_data)

        # 导入私钥
        key = RSA.import_key(privkey)

        # 创建一个PKCS1_OAEP模式的解密器
        cipher = PKCS1_OAEP.new(key)

        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data_bytes)

        # 返回解密后的原始数据
        return decrypted_data.decode()

    def encrypt_Base64(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过base64编码转换后的数据

        此函数用于还原JS中base64编码转换

        使用示例:
        spidertool.encrypt_Base64(data)
        '''
        encoded_data = base64.b64encode(str(data).encode())
        return encoded_data.decode('utf-8')

    def decrypt_Base64(self, encoded_data):
        '''
        :param encoded_data: 经过base64编码的数据
        :return: 原始数据

        此函数用于还原经过base64编码的数据回到其原始格式

        使用示例:
        spidertool.decrypt_Base64(encoded_data)
        '''
        decoded_data = base64.b64decode(encoded_data.encode('utf-8'))
        return decoded_data.decode('utf-8')

    def encrypt_MD5(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过md5加密后的数据

        此函数用于还原JS中md5算法加密

        使用实例:
        spidertool.encrypt_MD5(data)
        '''
        md5_hash = hashlib.md5()

        data_bytes = str(data).encode('utf-8')

        md5_hash.update(data_bytes)

        hex_digest = md5_hash.hexdigest()

        return hex_digest

    def encrypt_SHA1(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA1加密后的数据

        此函数用于还原JS中SHA1算法加密

        使用实例:
        spidertool.encrypt_SHA1(data)
        '''
        sha1 = hashlib.sha1()
        sha1.update(str(data).encode())
        return sha1.hexdigest()

    def encrypt_SHA256(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA256加密后的数据

        此函数用于还原JS中SHA256算法加密

        使用实例:
        spidertool.encrypt_SHA256(data)
        '''
        sha256 = hashlib.sha256()
        sha256.update(str(data).encode())
        return sha256.hexdigest()

    def encrypt_SHA512(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA512加密后的数据

        此函数用于还原JS中SHA512算法加密

        使用实例:
        spidertool.encrypt_SHA512(data)
        '''
        sha512 = hashlib.sha512()
        sha512.update(str(data).encode())
        return sha512.hexdigest()

    def encrypt_SHA384(self, data):
        '''
        :param data: 待加密的数据
        :return: 经过SHA384加密后的数据

        此函数用于还原JS中SHA384算法加密

        使用实例:
        spidertool.encrypt_SHA384(data)
        '''
        hash_object = hashlib.sha384(str(data).encode())
        return hash_object.hexdigest()

    def encrypt_HMAC(self, data, key, digestmod='md5', output_format='base64'):
        """
        使用HMAC进行数据加密，并支持指定输出格式（Base64或Hex）。

        :param data: 待加密的数据 (str)
        :param key: 加密密钥 (str)
        :param digestmod: 加密模式，默认为 'md5'。可用选项包括 'md5', 'sha1', 'sha256' 等。
        :param output_format: 输出格式，'base64' 或 'hex'，默认为 'base64'。
        :return: 加密后的数据 (str)，根据指定的输出格式。
        :raises ValueError: 如果提供了无效的输出格式或 digestmod。
        """

        # 支持的摘要算法映射
        supported_digests = {'md5': hashlib.md5, 'sha1': hashlib.sha1, 'sha256': hashlib.sha256,
                             'sha384': hashlib.sha384, 'sha512': hashlib.sha512}

        # 验证digestmod是否有效
        if digestmod not in supported_digests:
            raise ValueError(f"Unsupported digestmod '{digestmod}'. Use one of {list(supported_digests.keys())}.")

        # 验证输出格式
        if output_format not in ['base64', 'hex']:
            raise ValueError("Invalid output format. Use 'base64' or 'hex'.")

        # 使用指定的摘要算法创建HMAC对象
        hash_func = supported_digests[digestmod]
        hmac_obj = hmac.new(key.encode(), data.encode(), hash_func)

        # 根据输出格式返回结果
        if output_format == 'base64':
            # 返回Base64编码的结果
            return base64.b64encode(hmac_obj.digest()).decode('utf-8')
        else:  # output_format == 'hex'
            # 返回Hex格式的结果
            return hmac_obj.hexdigest()

    def encrypt_PBKDF2(self, password, salt, output_format='base64', *args, **kwargs):
        '''
        :param password: 要派生的密码（字节串）。
        :param salt: 随机生成的盐（字节串）。
        :param iterations: 迭代次数，用于增加计算难度。
        :param key_length: 指定派生密钥的长度（以字节为单位）。
        :param hash_algorithm: 用于内部哈希计算的算法，如'sha256'、'sha512'等。
        :return: 派生的密钥（字节串）

        此函数用于还原JS中PBKDF2算法加密,使用PBKDF2算法从密码派生密钥。

        使用示例:
                spidertool.encrypt_PBKDF2(password, salt, iterations, key_length, hash_algorithm)

        '''
        key = PBKDF2(password, salt.encode(), *args, **kwargs)
        if output_format == 'base64':
            base64_key = base64.b64encode(key).decode('utf-8')
            return base64_key
        elif output_format == 'hex':
            return key.hex()
        else:
            raise ValueError("Invalid output format. Use 'base64' or 'hex'.")