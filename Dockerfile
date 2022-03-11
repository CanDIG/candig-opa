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

ARG idp
ENV IDP=${idp}
RUN python3 app/permissions_engine/fetch_keys.py

ARG client_id
ENV CLIENT_ID=${client_id}
RUN sed -i s/CLIENT_ID/$CLIENT_ID/ app/permissions_engine/idp.rego

ARG katsu_url
ENV KATSU_URL=${katsu_url}
RUN python3 app/tests/create_katsu_test_datasets.py

ENTRYPOINT ["top", "-b"]
