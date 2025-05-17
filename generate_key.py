import secrets

# Generar una SECRET_KEY de 32 caracteres (256 bits)
secret_key = secrets.token_hex(32)
print(secret_key)