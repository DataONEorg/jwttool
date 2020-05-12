#!/opt/local/bin/python
# Simple tool for creating and displaying JWT tokens for DataONE

from jwcrypto import jwt, jwk
key = jwk.JWK(generate='oct', size=256)
print("KEY")
print(key.export())

# Create a signed token with the generated key::

Token = jwt.JWT(header={"alg": "HS256"},
                        claims={"info": "I'm a signed token"})
Token.make_signed_token(key)
print("TOKEN")
print(Token.serialize())

# Further encrypt the token with the same key::

Etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                         claims=Token.serialize())
Etoken.make_encrypted_token(key)
e = Etoken.serialize()
print("ETOKEN")
print(e)

# Now decrypt and verify::

k = {"k": "Wal4ZHCBsml0Al_Y8faoNTKsXCkw8eefKXYFuwTBOpA", "kty": "oct"}
key = jwk.JWK(**k)
e = u'eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.ST5RmjqDLj696xo7YFTFuKUhcd3naCrm6yMjBM3cqWiFD6U8j2JIsbclsF7ryNg8Ktmt1kQJRKavV6DaTl1T840tP3sIs1qz.wSxVhZH5GyzbJnPBAUMdzQ.6uiVYwrRBzAm7Uge9rEUjExPWGbgerF177A7tMuQurJAqBhgk3_5vee5DRH84kHSapFOxcEuDdMBEQLI7V2E0F57-d01TFStHzwtgtSmeZRQ6JSIL5XlgJouwHfSxn9Z_TGl5xxq4TksORHED1vnRA.5jPyPWanJVqlOohApEbHmxi3JHp1MXbmvQe2_dVd8FI'
print("ETOKEN2")
print(e)
ET = jwt.JWT(key=key, jwt=e)
ST = jwt.JWT(key=key, jwt=ET.claims)
print("CLAIMS")
print(ST.claims)


