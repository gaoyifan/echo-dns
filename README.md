# Echo DNS Server

An echo DNS server designed for debugging purposes, deployed as a public service at `myip.yfgao.com`. This self-hosted DNS server echoes back information about the client making the request, including the client's IP address and the original DNS query details. It's a handy tool for network debugging and testing DNS configurations.

## Features

- **IPv4 and IPv6 Support**: Responds to DNS queries for both IPv4 (`A` records) and IPv6 (`AAAA` records) addresses.
- **TXT Record Support**: Provides detailed client information, including IP address, port, and the raw DNS query, via `TXT` records.
- **Dockerized**: Easily deployable as a Docker container for local testing or production use.
- **Minimal Dependencies**: Built on Python with only the `dnslib` package as a dependency.

## Usage

### Accessing the Public Service

You can directly use the public DNS service hosted at `myip.yfgao.com` to test your DNS queries:

- **A Record (IPv4)**:
  ```bash
  dig any-sub-domain.myip.yfgao.com A
  dig @myip.yfgao.com any.domain A
  ```

- **AAAA Record (IPv6)**:
  ```bash
  dig any-sub-domain.myip.yfgao.com AAAA
  dig @myip.yfgao.com any.domain AAAA
  ```

- **TXT Record**:
  ```bash
  dig any-sub-domain.myip.yfgao.com TXT
  dig @myip.yfgao.com any.domain TXT
  ```

### Running the Server Locally
   ```bash
   docker run -d --name dns-server -p 53:53/udp -p 53:53/tcp ghcr.io/gaoyifan/echo-dns:latest
   ```

   This will start the DNS server in a detached mode, binding to port 53 for both TCP and UDP on your host machine.

## How It Works

The DNS server is implemented in Python using the `dnslib` library. It listens for DNS queries on port 53 and responds based on the query type:

- **A Records**: Returns the client's IPv4 address.
- **AAAA Records**: Returns the client's IPv6 address.
- **TXT Records**: Returns the original DNS query details.

This server is useful for debugging DNS configurations, testing how DNS queries are processed, and understanding client-server interactions in different network environments.