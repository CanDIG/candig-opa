ARG venv_python
ARG alpine_version
FROM python:${venv_python}-alpine${alpine_version}

LABEL Maintainer="CanDIG Project"

USER root

RUN apk update

RUN apk add --no-cache \
	bash \
	expect \
	jq

COPY ./ /app/

RUN pip install --no-cache-dir -r app/tests/requirements.txt

ARG idp
ENV IDP=${idp}
RUN python3 app/permissions_engine/fetch_keys.py

ARG katsu_url
ENV KATSU_URL=${katsu_url}
RUN python3 app/tests/create_katsu_test_datasets.py

ENTRYPOINT ["top", "-b"]
