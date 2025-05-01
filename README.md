CanDIG uses Opa as the policy authorization engine. Its policies are defined in [permissions_engine](permissions_engine)
The User is defined in the jwt presented in the authorization header.

Interactions with the IdP are handled by rego code in [idp.rego](permissions_engine/idp.rego). This fetches
the appropriate endpoints from the IdP's `openid_configuration` service, then queries
`introspection` on the token and gets the users `userinfo`. The user is decoded and verified at the `/idp` endpoints.

Interactions with Vault are handled by [vault.rego](permissions_engine/vault.rego). Secrets stored in the opa's service store are retrieved here.

Authorization to endpoints in the OPA service itself is defined in [authz.rego](permissions_engine/authz.rego).

* Role-based auth: Roles for the site are defined in the format given in [site_roles.json](defaults/site_roles.json).
  * If the User is defined as a site admin, they are allowed to access any endpoint.
  * If the User is defined as a site curator, they are allowed to use any of the curate method/path combinations defined in [paths.json](defaults/paths.json) for all programs known to the system.
  * Other site-based roles can be similarly defined.

* Endpoint-based auth: Any service can use the `/service/verified` endpoint. Other specific endpoints can be similarly allowed.

* An authenticated and authorized user is allowed to find out their own user ID, the key of which is defined system-wide in the .env file as CANDIG_USER_KEY. By default, this is the user's email address. This is the user ID by which user-based and program-based authorizations are keyed.

* Program-based and user-based authorizations are defined at the `permissions` path: A User can access these Opa endpoints to introspect their own authorizations. For a given method of accessing a service (method, path), the `/permissions/datasets` endpoint returns the list of programs that the User is allowed to access for that method/path, while the `/permissions/allowed` endpoint returns True if either the User is a site admin or the User is allowed to access that method/path. The following two types of authorizations are available:

  * Authorizations for roles in particular programs: users defined as team_members for a program are allowed to access the read paths specified in [paths.json](defaults/paths.json), while users defined as program_curators are allowed to access the curate and delete paths. Note: read and curate paths are separately allowed: if a user should be allowed to both read and curate, they should be in both the team_members and program_curators groups. Program authorizations can be created, edited, and deleted through the ingest microservice. Default test examples can be found in [programs.json](defaults/programs.json).

  * Users can also be specifically authorized to read data for a particular program through a data access authorization. User Read authorizations can be created, edited, and revoked through the ingest microservice.


The OPA response from the `permissions` endpoint contains the information used by OPA to resolve the permission question. It is used in two ways:
  * The authx library parses this response and returns a result. For example, in the `is_site_admin` method, authx returns `response.json()["result"]["site_admin"]` (in the example below, this is false).
  * The decision log is added to the CanDIG logs for future auditing. The dictionary `debug` contains extra information that may help diagnose why permissions weren't assigned as expected.

```
{
  "decision_id": "7f38aeb3-5902-42ad-b2a6-f45f000e37c2",
  "result": {
    "allowed": true,
    "curateable_method_path": true,
    "datasets": [
      "LOCAL-SYNTH_01",
      "SYNTH_04"
    ],
    "debug": {
      "local_issuer": "http://candig.docker.internal:8080/auth/realms/candig",
      "user_key_has_curator_programs": [
        "LOCAL-SYNTH_01"
      ],
      "user_key_has_dac_programs": [
        "SYNTH_04"
      ],
      "user_key_has_team_member_programs": [
        "LOCAL-SYNTH_01"
      ],
      "user_key_listed_as_site_admin": false,
      "user_key_listed_as_site_curator": false
    },
    "is_local_token": true,
    "issuer": "http://candig.docker.internal:8080/auth/realms/candig",
    "readable_method_path": true,
    "site_admin": false,
    "site_curator": false,
    "user_is_candig_authorized": true,
    "user_key": "user1@test.ca",
    "valid_token": true
  }
}
```
