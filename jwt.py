#!/opt/local/bin/python
# Simple tool for creating, displaying, and verifying JWT tokens for DataONE

from jwcrypto import jwt, jwk
from datetime import datetime, timedelta, timezone

def main():
    subject = "http://orcid.org/0000-0003-0077-4738"
    name = "Matthew B. Jones"
    ttl = 18*60*60
    claims = create_claims(subject, name, ttl)
    key = read_key("privkey.pem")
    algorithm = 'RS256'
    token = create_token(algorithm, key, claims)
    validate(token, key)

def read_key(keyfile):
    with open(keyfile, "rb") as pemfile:
        key = jwk.JWK.from_pem(pemfile.read())
    return(key)

def create_claims(subject, full_name, ttl=60*60):
    # standard JWT fields: https://tools.ietf.org/html/rfc7519#section-4.1.4
    consumerKey = "jwttool"
    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=ttl)
    claims={
        "sub":subject,
        "fullName": full_name,
        "issuedAt":now.isoformat(),
        "consumerKey": consumerKey,
        "exp":expires.timestamp(),
        "userId": subject,
        "ttl":ttl,
        "iat":now.timestamp()
    }
    return(claims)

def create_token(algorithm, key, claims):
    Token = jwt.JWT(header={"alg": algorithm},
                    claims=claims)
    Token.make_signed_token(key)
    t = Token.serialize()
    return(t)

def validate(token, key):
    # Convert tokenstring to Token and validate
    ST = jwt.JWT(key=key, jwt=token)
    print(ST.claims)
    return(ST.token.is_valid)

if __name__ == '__main__':
    main()