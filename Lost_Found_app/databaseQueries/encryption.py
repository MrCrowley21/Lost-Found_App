from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64

class Encryption:
    def __init__(self):
        pass 
    def base64Encoding(self,input):
        dataBase64 = base64.b64encode(input)
        dataBase64P = dataBase64.decode("UTF-8")
        return dataBase64P

    def base64Decoding(self,input):
        return base64.decodebytes(input.encode("ascii"))

    def generateSalt32Byte(self):
        return get_random_bytes(32)

    def aesCbcPbkdf2EncryptToBase64(self,password, plaintext):
        passwordBytes = password.encode("ascii")
        salt = self.generateSalt32Byte()
        PBKDF2_ITERATIONS = 15000
        encryptionKey = PBKDF2(passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)
        cipher = AES.new(encryptionKey, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext.encode("ascii"), AES.block_size))
        ivBase64 = self.base64Encoding(cipher.iv)
        saltBase64 = self.base64Encoding(salt)
        ciphertextBase64 = self.base64Encoding(ciphertext)
        return saltBase64 + ":" + ivBase64 + ":" + ciphertextBase64

    def aesCbcPbkdf2DecryptFromBase64(self,password, ciphertextBase64): 
        passwordBytes = password.encode("ascii")
        data = ciphertextBase64.split(":")
        salt = self.base64Decoding(data[0])
        iv = self.base64Decoding(data[1])
        ciphertext = self.base64Decoding(data[2])
        PBKDF2_ITERATIONS = 15000
        decryptionKey = PBKDF2(passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)
        cipher = AES.new(decryptionKey, AES.MODE_CBC, iv)
        decryptedtext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        decryptedtextP = decryptedtext.decode("UTF-8")
        return decryptedtextP
