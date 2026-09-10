# Local classroom runtime recipe. NOT an image that has been built/verified here.
# Base tags are mutable: export actual image IDs/digests after a successful build.
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless tini ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")" /opt/java \
 && groupadd --gid 1000 masar \
 && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash masar \
 && mkdir -p /workspace /opt/masar-runtime /home/masar/.ivy2 \
 && chown -R masar:masar /workspace /home/masar
ENV JAVA_HOME=/opt/java PATH="/opt/java/bin:${PATH}" \
    SPARK_LOCAL_IP=127.0.0.1 MASAR_IVY_DIR=/home/masar/.ivy2 \
    DBT_SEND_ANONYMOUS_USAGE_STATS=false DO_NOT_TRACK=1
WORKDIR /opt/masar-course
COPY requirements-runtime.txt requirements-day04.txt requirements-dbt.txt requirements-course.txt ./
COPY infrastructure/runtime/requirements-notebook.txt /opt/masar-runtime/requirements-notebook.txt
RUN python -m pip install --no-cache-dir -r requirements-course.txt -r /opt/masar-runtime/requirements-notebook.txt \
 && python -m pip check \
 && python -m pip freeze --all > /opt/masar-runtime/resolved-requirements.txt \
 && python -m pip list --format=json > /opt/masar-runtime/package-versions.json
COPY --chown=masar:masar . /opt/masar-course
USER masar
# Required build-time real Delta write/read and JAR resolution. No skip flag.
# This is a storage smoke test, NOT acceptance of the eight course labs.
RUN python scripts/prime_runtime.py --report /home/masar/build-smoke.json
WORKDIR /workspace
ENTRYPOINT ["/usr/bin/tini", "--", "python", "/opt/masar-course/infrastructure/runtime/start.py"]
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.root_dir=/workspace"]
