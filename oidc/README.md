# Permissions Engine

This is the configuration for OPA, which here serves as the permissions engine.
It accepts a user's authorization token, and the method of accessing a service (method and path),
and returns the list of datasets authorized for that operation by that user.

The actual permissions policies are written out in [permissions.rego](./permissions.rego).
Any users can access the open datasets `open1` and `open2`; registered access users
(here assessed by the existence of a `trusted researcher` claim in the userinfo)
can access dataset `registered1`; and user1 can access controlled dataset `controlled4`
while user2 can access `controlled5`.

Interactions with the IdP are handled by rego code in [idp.rego](./idp.rego).  This fetches
the appropriate endpoints from the IdP's `openid_configuration` service, then queries
`introspection` on the token and gets the users `userinfo`.

Authorization to the OPA service itself is defined in [authz.rego](./authz.rego).  A bearer
apikey is required in the authorization header; two roles for apikeys are defined, one (`beacon`)
which allows access only to the permissions endpoint, and one (`root`) which allows all access
(including posting new policies or modifying old ones).
