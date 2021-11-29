FROM alpine:3.6

RUN apk add --update \
python \
curl \
which \
bash

RUN curl -sSL https://sdk.cloud.google.com | bash

ENV PATH $PATH:/root/google-cloud-sdk/bin

RUN apk add --no-cache python3 py3-pip

WORKDIR '/app'
COPY ./main.py .
COPY ./yaml ./yaml
RUN pip3 install kubernetes