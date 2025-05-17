import bcrypt
hashed = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))