from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)
senha = 'Lindo Dia'

cipher_text = cipher_suite.encrypt(senha.encode())
plain_text = cipher_suite.decrypt(cipher_text).decode()

print(cipher_text)
print(plain_text)