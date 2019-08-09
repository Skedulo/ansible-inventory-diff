FROM python:3.7.4-slim

WORKDIR /work
#RUN apk add --no-cache git
RUN apt-get update && \
    apt-get install -y git make gcc g++ libyaml-dev libffi-dev libssl-dev time
COPY requirements.txt /work
RUN pip install -r requirements.txt
#RUN apk add --no-cache --virtual .build-deps make gcc g++ py-yaml yaml-dev libffi-dev openssl-dev && pip install -r /work/requirements.txt && apk del .build-deps
COPY ansible-inventory-diff.py ansible-inventory-diff.sh /bin/
RUN chmod 755 /bin/ansible-inventory-diff.sh

ENTRYPOINT ["/bin/ansible-inventory-diff.sh"]
