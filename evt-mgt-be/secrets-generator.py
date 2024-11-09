import secrets

# Generate a 32-byte hexadecimal key for SECRET_KEY
secret_key = secrets.token_hex(32)
print("SECRET_KEY:", secret_key)

# Generate a separate 32-byte key for JWT_SECRET_KEY
jwt_secret_key = secrets.token_hex(32)
print("JWT_SECRET_KEY:", jwt_secret_key)
