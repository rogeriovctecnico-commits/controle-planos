import secrets

# Gera uma chave aleatória de 64 caracteres (256 bits)
secret_key = secrets.token_hex(32)

# Salva no arquivo .env
with open(".env", "w") as f:
    f.write(f"SECRET_KEY={secret_key}\n")

print("Nova SECRET_KEY gerada e salva em .env:")
print(secret_key)