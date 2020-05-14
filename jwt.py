#!/opt/local/bin/python
# Simple tool for creating, displaying, and verifying JWT tokens for DataONE

from jwcrypto import jwt, jwk
from datetime import datetime, timedelta, timezone

algorithm = 'HS256'
key = jwk.JWK(generate='oct', size=256)
print("KEY")
k = key.export()
print(k)

algorithm = 'RS256'
with open("privkey.pem", "rb") as pemfile:
    key = jwk.JWK.from_pem(pemfile.read())
k = key.export()
print(k)

consumerKey = "theconsumerkey"
userId = "http://orcid.org/0000-0003-0077-4738"
fullName = "Matthew B. Jones"

ttl = 18*60*60
now = datetime.now(timezone.utc)
expires = now + timedelta(seconds=ttl)

# standard JWT fields: https://tools.ietf.org/html/rfc7519#section-4.1.4
Token = jwt.JWT(header={"alg": algorithm},
                claims={
                    "sub":userId,
                    "fullName": fullName,
                    "issuedAt":now.isoformat(),
                    "consumerKey": consumerKey,
                    "exp":expires.timestamp(),
                    "userId": userId,
                    "ttl":ttl,
                    "iat":now.timestamp()
                })
Token.make_signed_token(key)
t = Token.serialize()
print("TOKEN")
print(t)

# Convert tokenstring to Token and validate
ST = jwt.JWT(key=key, jwt=t)
print("CLAIMS")
print(ST.claims)

