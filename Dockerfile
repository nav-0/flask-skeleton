FROM python:3.8

COPY ./ /opt/en_passant
WORKDIR /opt/en_passant
RUN pip3 install -U pip && pip3 install .

ENV PYTHONPATH "${PYTHONPATH}:/opt/en_passant"
ENV INGEST_HOST_BIND "0.0.0.0"

EXPOSE 8080
CMD ["en_passant_api"]
