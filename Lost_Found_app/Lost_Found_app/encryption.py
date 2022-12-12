import logging

from Crypto.Cipher import AES
import logging


class Encryption:
    def encrypt_message(self, password_from_db, data):
        key = bytes(password_from_db, encoding='utf-8')
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce  # unique value for the encryption with a certain key
        encrypted_data, tag = cipher.encrypt_and_digest(data)  # get authentication tag, as well
        # to store in database
        return encrypted_data, nonce, tag

    def decrypt_data(self, password_from_db, encrypted_data, nonce, tag):
        key = bytes(password_from_db, encoding='utf-8')
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt(encrypted_data)
        try:
            cipher.verify(tag)
            return data
        except ValueError:
            logging.warning(f'Corrupted Message!!!')
            return False
