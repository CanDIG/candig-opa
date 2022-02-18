COPY permissions_engine/authz.rego /
COPY permissions_engine/idp.rego /
COPY permissions_engine/permissions.rego /

RUN /bin/bash -c 'touch /data.json;'
