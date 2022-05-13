ARG venv_python
ARG alpine_version
FROM python:${venv_python}-alpine${alpine_version}

LABEL Maintainer="CanDIG Project"

USER root

RUN apk update

RUN apk add --no-cache \
	bash \
	expect \
	jq \
	curl

COPY ./ /app/

RUN pip install --no-cache-dir -r app/tests/requirements.txt

ARG client_id
ENV CLIENT_ID=${client_id}
RUN sed -i s/CLIENT_ID/$CLIENT_ID/ app/permissions_engine/idp.rego && sed -i s/CLIENT_ID/$CLIENT_ID/ app/permissions_engine/authz.rego

ARG opa_site_admin_key
ENV OPA_SITE_ADMIN_KEY=${opa_site_admin_key}
RUN sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ app/permissions_engine/idp.rego && sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ app/permissions_engine/authz.rego

ENTRYPOINT ["top", "-b"]