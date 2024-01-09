ARG venv_python
FROM python:${venv_python}

LABEL Maintainer="CanDIG Project"
LABEL "candigv2"="opa"

USER root

RUN groupadd -r candig && useradd -rm candig -g candig

RUN apt-get update && apt-get -y install \
	bash \
	expect \
	jq \
	curl \
	vim \
	git

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./ /app/

RUN chown -R candig:candig /app

USER candig

WORKDIR /app/

RUN touch /app/initial_setup

ENTRYPOINT ["bash", "/app/entrypoint.sh"]