# ────────────────────────────────────────────────────────────
# MAZA Network daemon (mazad) — pre-built binaries from v0.16.3
# Source: https://github.com/MazaCoin/maza/releases/tag/v0.16.3
# MAZA is a Litecoin Cash fork with MinotaurX + Hive mining
# ────────────────────────────────────────────────────────────

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget ca-certificates \
        libssl3 libevent-2.1-7 libboost-system1.74.0 \
        libboost-filesystem1.74.0 libboost-thread1.74.0 \
        libboost-chrono1.74.0 libboost-program-options1.74.0 \
        libboost-test1.74.0 libsqlite3-0 libminiupnpc17 \
        libzmq3-dev && \
    rm -rf /var/lib/apt/lists/*

# Download pre-built binaries from official MAZA v0.16.3 release
WORKDIR /tmp
RUN wget -q "https://github.com/MazaCoin/maza/releases/download/v0.16.3/maza-0.16.3-x86_64-linux-gnu.tar.gz" && \
    tar xzf maza-0.16.3-x86_64-linux-gnu.tar.gz && \
    cp maza-0.16.3/bin/mazad /usr/local/bin/ && \
    cp maza-0.16.3/bin/maza-cli /usr/local/bin/ && \
    chmod +x /usr/local/bin/mazad /usr/local/bin/maza-cli && \
    rm -rf /tmp/maza-*

VOLUME ["/data"]
ENV MAZA_DATADIR=/data

EXPOSE 12835 12832

ENTRYPOINT ["mazad", "-datadir=/data", "-printtoconsole"]
