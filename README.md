# jwttool

A simple tool for creating and managing JWT tokens for DataONE.

## Example usage

To create a token (storing it in the environment variable `token`):

```sh
token=`./jwttool -s "http://orcid.org/0000-0003-0077-4738" -n "Matthew B. Jones" --ttl 86400 --key privkey.pem`
```

To validate and print the claims from a token:

```sh
./jwttool --key privkey.pem $token
{"consumerKey":"jwttool","exp":1589509379.022425,"fullName":"Matthew B. Jones","iat":1589422979.022425,"issuedAt":"2020-05-14T02:22:59.022425+00:00","sub":"http://orcid.org/0000-0003-0077-4738","ttl":86400,"userId":"http://orcid.org/0000-0003-0077-4738"}
```
