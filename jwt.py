#!/opt/local/bin/python
# Simple tool for creating, displaying, and verifying JWT tokens for DataONE

from jwcrypto import jwt, jwk
from datetime import datetime, timedelta, timezone
import argparse
import sys

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or display JSON Web Tokens (JWT). " +
            "If subject and name are provided, create a token. " + 
            "If a token is provided, validate it and print the claims. " +
            "Optionally provide a TTL value in seconds or signing key."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("-t", "--ttl", default=60*60, type=int)
    parser.add_argument("-k", "--key", default="privkey.pem")
    parser.add_argument("-s", "--subject")
    parser.add_argument("-n", "--name")

    parser.add_argument('token', nargs='?')
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    if all(i is not None for i in [args.subject, args.name]):
        # create a token
        claims = create_claims(args.subject, args.name, args.ttl)
        key = read_key(args.key)
        algorithm = 'RS256'
        token = create_token(algorithm, key, claims)
        print(token)
    elif (args.token is not None):
        # Validate token and show claims
        key = read_key(args.key)
        validate(args.token, key)
    else:
        # Usage
        parser.print_help(sys.stderr)
        sys.exit(1)

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