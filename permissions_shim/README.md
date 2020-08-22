# Permissions_shim

This service is a shim betewen the "beacon" and OPA. 

![Diagram showing interactions between services](../diagram.png)

The beacon developers prefer to pass the user's token in the Authorization:
header, whereas microservice architectures such as in Kubernetes use that
or client certs for service authentication, and pass the user credentials
in the body.  This service serves as a shim between the two.

This service exposes a single endpoint, `/permissions`, which takes in
the body three fields:

* `method`: the method called to the beacon
* `path`: the path of the call - this can be used as a general rest label
* `clientSecret`: the secret used to authenticate with the permission engine (OPA)

plus of course the user's token as a bearer token in the headers.

It returns a json object, `datasets`, which is an array of strings indicating
the allowed datasets for this request.
