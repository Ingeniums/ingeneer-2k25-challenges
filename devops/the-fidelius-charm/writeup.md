# Fidelius Charm CTF Write-up

*By [Your Name]*  
*Published on May 6, 2025*  
*7 min read*

In this write-up, I’ll walk through solving the **Fidelius Charm** CTF challenge, a Docker-based puzzle involving container orchestration, environment variables, encryption, and network configuration. The challenge required analyzing Docker images, inspecting containers, recovering deleted files, and submitting data in a specific format to retrieve the flag.

---

## Initial Setup: Running the Container

The challenge provided a Docker container, but the registry lacked instructions on how to run it. To gain insight, I used:

```bash
docker history <image-id>
```

This revealed a comment hinting at **Docker-in-Docker (DinD)**, suggesting the container needed special privileges. Following the image’s documentation, I ran the container with:

```bash
docker run --privileged -d <image-id>
```

The `--privileged` flag was crucial to enable DinD functionality, allowing nested Docker operations within the container.

---

## Exploring the Container

Inside the container, I found two key files:

1. **`compose.yaml`**: A Docker Compose configuration file defining two services: `caller` and `main`.
2. **`story.md`**: A narrative file providing context for the challenge.

I started the services using:

```bash
docker compose up -d
```

However, nothing significant happened—no output, no visible activity. The challenge description pointed to issues with the **Caller** service, so I inspected its logs:

```bash
docker logs <caller-container-id>
```

The logs revealed missing environment variables:

```
2025-05-06 17:53:03,364 - INFO - Script started.
2025-05-06 17:53:03,364 - ERROR - API_KEY environment variable not found
2025-05-06 17:53:03,364 - INFO - API_KEY successfully read.
2025-05-06 17:53:03,364 - WARNING - SECRET environment variable not found. Generating random secret: d9c1b741...
2025-05-06 17:53:03,364 - ERROR - SECRET2 environment variable not found. Exiting.
2025-05-06 17:53:03,364 - INFO - Get credentials and restart service...
```

The `caller` service required `API_KEY`, `SECRET`, and `SECRET2` environment variables to function properly.

---

## Analyzing the Caller Service

Using `docker exec`, I accessed the `caller` container to examine its code:

```bash
docker exec -it <caller-container-id> bash
```

The script was making an API call to `https://api.deploily.cloud/photon/api?q=Salzbe`, processing the response, and storing it in an encrypted file (`/var/logs/output.encrypted`). The encryption used AES with a key derived from `SECRET2` and a hardcoded salt:

```
good luck finding the output file, make sure you use everything you are given ;).
```

The challenge also provided an `inspect.json` file, which revealed a mounted host directory. On the host container, I located `/var/logs/output.encrypted` and a log file matching the `caller` output, confirming the encrypted data was accessible.

---

## Inspecting the Main Service

Next, I shifted focus to the `main` service. Inside its container, I found:

- **`server-help.md`**: Described the expected format for submitting data to `/submit`.
- **`decrypt-help.md`**: Hinted at a decryption mechanism for `output.encrypted`.

However, no decryption script was present, and `server.py` was obfuscated, making it difficult to analyze directly. The hint “even containers have history” suggested checking the container’s history for clues.

I ran:

```bash
docker history <main-image-id>
```

This showed a layer where a `decrypt-script` had been removed. To recover it, I used:

```bash
docker inspect <main-container-id>
```

This provided the read-only layer paths. Navigating to the layer’s storage location, I retrieved the deleted `decrypt-script`. Executing it decrypted `output.encrypted`, yielding the plaintext API response.

---

## Formatting and Submitting the Data

The plaintext needed to match the format expected by the `main` service’s `/submit` endpoint. I referred to **Deploily’s API documentation** to restructure the data correctly.

To submit, I installed `curl` on the host container:

```bash
apt-get update && apt-get install curl
```

I attempted a POST request to `http://localhost:8000/submit`:

```bash
curl -X POST -H "Content-Type: application/json" -d '<formatted-data>' http://localhost:8000
```

This failed, indicating the `main` service was unreachable.

---

## Fixing the Network Configuration

Inspecting `compose.yaml`, I noticed both services used `network_mode: none`, isolating them from external connections:

```yaml
version: '3'
name: fidelius-charm

services:
  caller:
    image: "ymerzouka/fidelius-charm-caller:latest"
    network_mode: none
  main:
    image: "ymerzouka/fidelius-charm-main:latest"
    network_mode: none
    ports:
      - "8000:8000"
```

I modified `compose.yaml` to use a bridge network and ensure the `main` service was accessible:

```yaml
version: '3'
name: fidelius-charm

services:
  caller:
    image: "ymerzouka/fidelius-charm-caller:latest"
    networks:
      - fidelius-network
  main:
    image: "ymerzouka/fidelius-charm-main:latest"
    ports:
      - "8000:8000"
    networks:
      - fidelius-network

networks:
  fidelius-network:
    driver: bridge
```

I restarted the services:

```bash
docker compose down && docker compose up -d
```
Retrying the POST request succeeded, and the `main` service returned the flag.
