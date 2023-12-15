ARG venv_python
ARG alpine_version
FROM python:${venv_python}-alpine${alpine_version}

LABEL Maintainer="CanDIG Project"
LABEL "candigv2"="opa"

USER root

RUN addgroup -S candig && adduser -S candig -G candig

RUN apk update

RUN apk add --no-cache \
	bash \
	expect \
	jq \
	curl

COPY ./ /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chown -R candig:candig /app

USER candig

RUN touch initial_setup

ENTRYPOINT ["bash", "/app/entrypoint.sh"]