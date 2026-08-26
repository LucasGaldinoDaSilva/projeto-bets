FROM apache/airflow:2.9.3-python3.11

ARG AIRFLOW_UID=50000

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN if [ "${AIRFLOW_UID}" != "50000" ]; then \
        usermod -u "${AIRFLOW_UID}" airflow; \
    fi \
    && chown -R airflow:root /home/airflow

USER airflow

RUN pip install --no-cache-dir \
    pyspark==3.5.6 \
    python-dotenv \
    requests
