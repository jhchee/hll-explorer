FROM postgres:14.6-alpine

ENV CITUS_HLL_VERSION v2.17
RUN set -ex \
    \
    # Get some basic deps required to download the extensions and name them fetch-deps so we can delete them later
    && apk add --no-cache --virtual .fetch-deps \
        ca-certificates \
        openssl \
        tar \
    \
    # Get the dependencies
    && apk add --no-cache --virtual .build-deps \
        autoconf \
        automake \
        g++ \
        clang \
        llvm \
        libtool \
        libxml2-dev \
        make \
        perl \
    # Download pg_partman \
    && wget -O citus_hll.tar.gz "https://github.com/citusdata/postgresql-hll/archive/refs/tags/$CITUS_HLL_VERSION.tar.gz" \
    # Create a folder to put the src files in
    && mkdir -p /usr/src/citus_hll \
    # Extract the src files
    && tar \
        --extract \
        --file citus_hll.tar.gz \
        --directory /usr/src/citus_hll \
        --strip-components 1 \
    # Delete src file tar
    && rm citus_hll.tar.gz \
    # Move to src file folder
    && cd /usr/src/citus_hll \
    # Build the extension
    && make \
    # Install the extension
    && make install \
    # Delete the src files for pg_partman
    && rm -rf /usr/src/citus_hll \
    # Delete the dependencies for downloading and building the extensions, we no longer need them
    && apk del .fetch-deps .build-deps

# Copy the init script
# The Docker Postgres initd script will run anything
# in the directory /docker-entrypoint-initdb.d
COPY initdb.sh /docker-entrypoint-initdb.d/initdb.sh