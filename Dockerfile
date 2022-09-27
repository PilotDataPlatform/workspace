FROM python:3.9-buster AS production-environment

WORKDIR /usr/src/app

ENV TZ=America/Toronto

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev vim-tiny less && \
    ln -s /usr/bin/vim.tiny /usr/bin/vim && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==1.1.12
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root --no-interaction
COPY . .

FROM production-environment AS workspace-image

CMD ["python", "run.py"]

FROM production-environment AS development-environment

RUN poetry install --no-root --no-interaction
