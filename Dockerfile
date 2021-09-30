FROM continuumio/miniconda3

RUN conda install -c conda-forge mamba
COPY ysi_prediction/environment.yml /tmp/environment.yml
WORKDIR /tmp
RUN mamba env update -f environment.yml && \
    rm -rf /tmp/* && conda clean --all --yes

RUN mkdir -p /deploy/app
COPY ysi_prediction /deploy/app

WORKDIR /deploy/app
ENV PYTHONPATH "${PYTHONPATH}:/deploy/app"
env PORT 8889

CMD gunicorn --worker-tmp-dir /dev/shm --bind 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker --log-level debug wsgi:app
