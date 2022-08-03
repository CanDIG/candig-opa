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

RUN touch initial_setup
ENTRYPOINT ["bash", "/app/entrypoint.sh"]