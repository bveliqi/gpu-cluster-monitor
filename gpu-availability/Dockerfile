FROM python:3.6-alpine3.7

LABEL maintainer="behar@veliqi.de"

ADD . .

RUN pip install --upgrade -r requirements.txt

ENTRYPOINT [ "python", "free_nodes.py" ]
