# ────────────────────────────────────────────────────────────
# Multi-stage build for MAZA Network daemon (mazad)
# Source: https://github.com/MazaCoin/maza
# MAZA is a Litecoin Cash fork with MinotaurX + Hive mining
# ────────────────────────────────────────────────────────────

# ── Stage 1: Build ──
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV BUILD_PACKAGES="\
    build-essential libtool autotools-dev automake pkg-config \
    libssl-dev libevent-dev libboost-all-dev libsqlite3-dev \
    libzmq3-dev bsdmainutils python3 git ca-certificates"

RUN apt-get update && \
    apt-get install -y --no-install-recommends $BUILD_PACKAGES && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Clone MAZA source
RUN git clone --depth 1 https://github.com/MazaCoin/maza.git /build/maza

# Build BerkeleyDB 4.8 for wallet compatibility
RUN cd /build/maza && \
    ./contrib/install_db4.sh /build && \
    export BDB_PREFIX="/build/db4"

# Build mazad (no GUI, no UPnP — headless server)
RUN cd /build/maza && \
    ./autogen.sh && \
    ./configure \
        --without-gui \
        --without-miniupnpc \
        --with-incompatible-bdb \
        BDB_CFLAGS="-I/build/db4/include" \
        BDB_LIBS="-L/build/db4/lib -ldb_cxx" \
        CXXFLAGS="-O2 -pthread" && \
    make -j$(nproc) && \
    strip src/mazad src/maza-cli

# ── Stage 2: Runtime ──
FROM ubuntu:22.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libssl3 libevent-2.1-7 libboost-system1.74.0 \
        libboost-filesystem1.74.0 libboost-thread1.74.0 \
        libboost-chrono1.74.0 libboost-program-options1.74.0 \
        libsqlite3-0 libzmq3-dev wget curl && \
    rm -rf /var/lib/apt/lists/*

# Copy built binaries
COPY --from=builder /build/maza/src/mazad /usr/local/bin/mazad
COPY --from=builder /build/maza/src/maza-cli /usr/local/bin/maza-cli

# Data directory
VOLUME ["/data"]
ENV MAZA_DATADIR=/data

EXPOSE 12835 12832

ENTRYPOINT ["mazad", "-datadir=/data", "-printtoconsole"]
