FROM continuumio/miniconda3

COPY ysi_prediction/environment.yml /tmp/environment.yml
WORKDIR /tmp
RUN conda env update -f environment.yml && \
    rm -rf /tmp/* && conda clean --all --yes

RUN mkdir -p /deploy/app
COPY ysi_prediction /deploy/app

WORKDIR /deploy/app
ENV PYTHONPATH "${PYTHONPATH}:/deploy/app"

CMD gunicorn --worker-tmp-dir /dev/shm --bind 0.0.0.0:$PORT --log-level debug wsgi:app
