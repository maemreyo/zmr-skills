ARG PYTHON_BASE_IMAGE
FROM ${PYTHON_BASE_IMAGE}

ARG LIBREOFFICE_VERSION=25.2.3
RUN test -n "${LIBREOFFICE_VERSION}" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       libreoffice-writer \
       libreoffice-impress \
       fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
ENV PYTHONUNBUFFERED=1
