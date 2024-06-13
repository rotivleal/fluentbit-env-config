ARG PYTHON_VERSION=3.12.4
ARG PYTHON_DEBIAN_NAME=bookworm
ARG FLUENTBIT_VERSION=3.0.7
ARG BUSYBOX_VERSION=1.35.0

FROM python:${PYTHON_VERSION}-slim-${PYTHON_DEBIAN_NAME} AS python-base

ARG NONROOT_USER="user"
ARG NONROOT_GROUP="gr"

RUN groupadd ${NONROOT_GROUP} \
 && useradd -m ${NONROOT_USER} -g ${NONROOT_GROUP}

USER ${NONROOT_USER}

ENV PATH="/home/${NONROOT_USER}/.local/bin:${PATH}"

USER ${NONROOT_USER}
WORKDIR /home/${NONROOT_USER}

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM busybox:${BUSYBOX_VERSION}-uclibc as busybox

FROM fluent/fluent-bit:${FLUENTBIT_VERSION}

COPY --from=python-base /usr/local/lib/ /usr/local/lib/
COPY --from=python-base /usr/local/bin/python /usr/local/bin/python
COPY --from=python-base /etc/ld.so.cache /etc/ld.so.cache
COPY --from=busybox:1.35.0-uclibc /bin/sh /bin/sh
COPY ./script.py script.py
COPY --chmod=755 ./init.sh init.sh

ENTRYPOINT ["./init.sh"]
