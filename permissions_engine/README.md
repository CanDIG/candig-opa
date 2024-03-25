# Permissions Engine

This is the configuration for OPA, which here serves as the permissions engine.

The User is defined in the jwt presented in the authorization header.

Interactions with the IdP are handled by rego code in [idp.rego](./idp.rego). This fetches
the appropriate endpoints from the IdP's `openid_configuration` service, then queries
`introspection` on the token and gets the users `userinfo`. The user is decoded and verified at the `/idp` endpoints.

Authorization to endpoints in the OPA service itself is defined in [authz.rego](./authz.rego).

* Token-based auth: There are two api tokens defined: the root token allows any path to be accessed, while the service token only allows the `permissions/datasets` and `permissions/allowed` endpoints to be viewed.

* Role-based auth: Roles for the site are defined in the format given in defaults/roles.json. if the User is defined as a site admin, they are allowed to view any endpoint. Other site-based roles can be similarly defined.

* Endpoint-based auth: Any service can use the `/service/verified` endpoint. Other specific endpoints can be similarly allowed.

Authorization for programs are defined at the `permissions` path: For a given User and the method of accessing a service (method, path), the `/permissions/datasets` endpoint returns the list of programs that user is allowed to access for that method/path, while the `/permissions/allowed` endpoint returns True if either the user is a site admin or the user is allowed to access that method/path. Method/path allowable combinations are defined in `defaults/paths.json`: users defined as team_members for a program are allowed to access the read paths, while users defined as program_curators are allowed to access the curate paths. Note: read and curate paths are separately allowed: if a user should be allowed to both read and curate, they should be in both the team_members and program_curators groups.
