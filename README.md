# jwttool

A simple tool for creating and managing JWT tokens for DataONE.

## Example usage

### To create a token
(storing it in the environment variable `token`):

```sh
token=`./jwttool -s "http://orcid.org/0000-0003-0077-4738" -n "Matthew B. Jones" --ttl 86400 --key privkey.pem`
```

### To create a token using a private key that requires a passphrase
(assuming the environment variable `${PASS}` already contains the passphrase):

```sh
token=`./jwttool -s "http://orcid.org/0000-0003-0077-4738" -n "Matthew B. Jones" --ttl 86400 --key privkey.pem -p ${PASS}`
```

> **Tip:** On macOS, instead of setting an environment variable for the passphrase, you can copy
> the passphrase to your clipboard (⌘C), and then substitute `$(pbpaste)` for `${PASS}` in the
> above command


### To validate and print the claims from a token:

```sh
./jwttool --key privkey.pem $token
{"consumerKey":"jwttool","exp":1589509379.022425,"fullName":"Matthew B. Jones","iat":1589422979.022425,"issuedAt":"2020-05-14T02:22:59.022425+00:00","sub":"http://orcid.org/0000-0003-0077-4738","ttl":86400,"userId":"http://orcid.org/0000-0003-0077-4738"}
# if the key requires a passphrase, use:    -p ${PASS}
```

## Help documentation

```sh
$ ./jwttool --help
usage: jwttool [-h] [-v] [-t TTL] [-k KEY] [-p PASSPHRASE] [-s SUBJECT] [-n NAME] [token]

Create or display JSON Web Tokens (JWT). If subject and name are provided,
create a token. If a token is provided, validate it and print the claims.
Optionally provide a TTL value in seconds, a signing key, and/or a key passphrase

positional arguments:
  token

options:
  -h, --help            show this help message and exit
  -v, --version         show program’s version number and exit
  -t TTL, --ttl TTL     optional time-to-live in seconds
  -k KEY, --key KEY     optional filename or path to signing key
  -p PASSPHRASE, --passphrase PASSPHRASE
                        optional passphrase for key
  -s SUBJECT, --subject SUBJECT
                        subject identifier for the created token
  -n NAME, --name NAME  name to be included in the created token
```
