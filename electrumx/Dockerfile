# ────────────────────────────────────────────────────────────
# ElectrumX server for MAZA Network
# Uses custom coin class injection (no coins.py patching needed)
# ────────────────────────────────────────────────────────────

FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libssl-dev libffi-dev \
        libsecp256k1-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install electrumx 1.16 (last generic version before BSV fork)
RUN pip install --no-cache-dir \
    electrumx==1.16 \
    pylru \
    aiohttp

# Custom MAZA coin definition + startup wrapper + config
COPY coins_maza.py /app/coins_maza.py
COPY start.py /app/start.py
COPY electrumx.conf /app/electrumx.conf

WORKDIR /app
ENV ELECTRUMX_CONF=/app/electrumx.conf

VOLUME ["/data"]
EXPOSE 50001 50002

ENTRYPOINT ["python3", "/app/start.py"]
