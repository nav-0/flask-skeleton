FROM python:3.8

COPY ./ /opt/igo_by
WORKDIR /opt/igo_by
RUN pip3 install -U pip && pip3 install .

ENV PYTHONPATH "${PYTHONPATH}:/opt/igo_by"
ENV INGEST_HOST_BIND "0.0.0.0"

EXPOSE 8080
CMD ["i_go_by_api"]
