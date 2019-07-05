FROM continuumio/miniconda3

COPY ysipred/environment.yml /tmp/environment.yml
WORKDIR /tmp
RUN apt-get update && \
    apt-get install -y --no-install-recommends libxrender1 libsm6 && \
    conda env update -f environment.yml && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    conda clean --all --yes

RUN mkdir -p /deploy/app
COPY ysipred /deploy/app

WORKDIR /deploy/app

# ENTRYPOINT ["/bin/bash", "-c"]
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:2222", "main:app"]
