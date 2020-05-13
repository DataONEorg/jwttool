#!/opt/local/bin/python
# Simple tool for creating, displaying, and verifying JWT tokens for DataONE

from jwcrypto import jwt, jwk

algorithm = 'HS256'
key = jwk.JWK(generate='oct', size=256)
print("KEY")
k = key.export()
print(k)

algorithm = 'RS256'
with open("dataone_org.key", "rb") as pemfile:
    key = jwk.JWK.from_pem(pemfile.read())
k = key.export()
print(k)

# Create a signed token with the generated key::
#         claimsSet.setClaim("consumerKey", consumerKey);
#         claimsSet.setClaim("userId", userId);
#         claimsSet.setClaim("issuedAt", DateTimeMarshaller.serializeDateToUTC(now.getTime()));
#         claimsSet.setClaim("ttl", TTL_SECONDS);
#         claimsSet.setClaim("fullName", fullName);
#         // standard JWT fields: https://tools.ietf.org/html/rfc7519#section-4.1.4
#         claimsSet.setSubject(userId);
#         claimsSet.setIssueTime(now.getTime());
#         claimsSet.setExpirationTime(expires.getTime());

consumerKey = "foo"
userId = "subject!"
ttl = 100001
fullName = "Matt Jones"
Token = jwt.JWT(header={"alg": algorithm},
                        claims={
                            "consumerKey": consumerKey,
                            "userId": userId,
                            "issuedAt": consumerKey,
                            "ttl": ttl,
                            "fullName": fullName,
                            "subject": userId
                        })
Token.make_signed_token(key)
t = Token.serialize()
print("TOKEN")
print(t)

# Further encrypt the token with the same key::
#Etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
#                         claims=Token.serialize())
#Etoken.make_encrypted_token(key)
#e = Etoken.serialize()
#print("ETOKEN")
#print(e)

# Now decrypt and verify::

#k = {"k":"J50L6gAEvbFp0jFEVBYLXY0iZE2uLSJo2G8_TZWWB_I","kty":"oct"}
#k = {"k": "Wal4ZHCBsml0Al_Y8faoNTKsXCkw8eefKXYFuwTBOpA", "kty": "oct"}
#newkey = jwk.JWK(**k)
#e = u'eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.ST5RmjqDLj696xo7YFTFuKUhcd3naCrm6yMjBM3cqWiFD6U8j2JIsbclsF7ryNg8Ktmt1kQJRKavV6DaTl1T840tP3sIs1qz.wSxVhZH5GyzbJnPBAUMdzQ.6uiVYwrRBzAm7Uge9rEUjExPWGbgerF177A7tMuQurJAqBhgk3_5vee5DRH84kHSapFOxcEuDdMBEQLI7V2E0F57-d01TFStHzwtgtSmeZRQ6JSIL5XlgJouwHfSxn9Z_TGl5xxq4TksORHED1vnRA.5jPyPWanJVqlOohApEbHmxi3JHp1MXbmvQe2_dVd8FI'
#print("ETOKEN2")
#print(e)
#ET = jwt.JWT(key=key, jwt=e)
#ST = jwt.JWT(key=key, jwt=ET.claims)
ST = jwt.JWT(key=key, jwt=t)
print("CLAIMS")
print(ST.claims)

#jt = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJodHRwOlwvXC9vcmNpZC5vcmdcLzAwMDAtMDAwMy0wMDc3LTQ3MzgiLCJmdWxsTmFtZSI6Ik1hdHRoZXcgQi4gSm9uZXMiLCJpc3N1ZWRBdCI6IjIwMjAtMDUtMTJUMjM6NDQ6MDAuMzE4KzAwOjAwIiwiY29uc3VtZXJLZXkiOiJ0aGVjb25zdW1lcmtleSIsImV4cCI6MTU4OTM5MTg0MCwidXNlcklkIjoiaHR0cDpcL1wvb3JjaWQub3JnXC8wMDAwLTAwMDMtMDA3Ny00NzM4IiwidHRsIjo2NDgwMCwiaWF0IjoxNTg5MzI3MDQwfQ.rXxJ3HJ5VMe_nPNiZJ9Rkv7a1zH40JWGgeq5fyl01iZlYvMC8sDUk2webb8mLNubECKCqdGcEYA0qBVfrwZ4SoHfi4raEDglahp4Cs-oBWcsA5SDX9XFiKsfaxmsr5VHYwe7eUXRi55_PB0zx-j_kc5fdL8FskazWFkCyfrhiaqNJ-KiOcqVUkzF338NyP4_mnjHQXCe-KR_IVMRBJ0UP1B3Fe_Zj6oJ_iYDRmGmSMP6a01PMxPDRWNaqZkOeTP0m4jRlTzBhgnS8vqoYKLny-WiQM3M0Q7cakHjqpifsJCocps784rbAtbeTVZI6g4YS55Dgk4tMRk-7zIlZP3Ctg"
#mbj_token = jwt.JWT(jwt=jt, key=key)
#print(mbj_token.claims)


