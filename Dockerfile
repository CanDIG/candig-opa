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
	curl \
	git

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./ /app/

RUN chown -R candig:candig /app

USER candig

WORKDIR /app/

RUN touch /app/initial_setup

ENTRYPOINT ["bash", "/app/entrypoint.sh"]