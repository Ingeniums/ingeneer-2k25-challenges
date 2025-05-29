# Fidelius Charm CTF Write-up

## Initial Setup: Running the Container

The challenge provided a Docker container, but the registry lacked instructions on how to run it. To gain insight, the following command can be used:

```bash
docker history <image-id>
```

This reveals a comment hinting at **Docker-in-Docker (DinD)**, suggesting the container needs special privileges. Following the image’s documentation, the container is run with:

```bash
docker run --privileged -d <image-id>
```

The `--privileged` flag is crucial to enable DinD functionality, allowing nested Docker operations within the container.

---

## Exploring the Container

Inside the container, two key files will be found:

1.  **`compose.yaml`**: A Docker Compose configuration file defining two services: `caller` and `main`.
2.  **`story.md`**: A narrative file providing context for the challenge.

The services are started using:

```bash
docker compose up -d
```

However, nothing significant happens—no output, no visible activity. The challenge description points to issues with the **Caller** service, so its logs should be inspected:

```bash
docker logs <caller-container-id>
```

The logs reveal missing environment variables:

```
2025-05-06 17:53:03,364 - INFO - Script started.
2025-05-06 17:53:03,364 - ERROR - API_KEY environment variable not found
2025-05-06 17:53:03,364 - INFO - API_KEY successfully read.
2025-05-06 17:53:03,364 - WARNING - SECRET environment variable not found. Generating random secret: d9c1b741...
2025-05-06 17:53:03,364 - ERROR - SECRET2 environment variable not found. Exiting.
2025-05-06 17:53:03,364 - INFO - Get credentials and restart service...
```

The `caller` service requires `API_KEY`, `SECRET`, and `SECRET2` environment variables to function properly.

---

## Analyzing the Caller Service

Using `docker exec`, the `caller` container can be accessed to examine its code:

```bash
docker exec -it <caller-container-id> bash
```

The script is making an API call to `https://api.deploily.cloud/photon/api?q=Salzbe`, processing the response, and storing it in an encrypted file (`/var/logs/output.encrypted`). The encryption uses AES with a key derived from `SECRET2` and a hardcoded salt:

```
good luck finding the output file, make sure you use everything you are given ;).
```

The challenge also provided an `inspect.json` file, which revealed a mounted host directory. On the host container, `/var/logs/output.encrypted` and a log file matching the `caller` output were located, confirming the encrypted data was accessible.

---

## Inspecting the Main Service

Next, attention shifts to the `main` service. Inside its container, the solver will find:

* **`server-help.md`**: Describes the expected format for submitting data to `/submit`.
* **`decrypt-help.md`**: Hints at a decryption mechanism for `output.encrypted`.

However, no decryption script is present, and `server.py` is obfuscated, making it difficult to analyze directly. The hint “even containers have history” suggests checking the container’s history for clues.

Running:

```bash
docker history <main-image-id>
```

shows a layer where a `decrypt-script` had been removed. To recover it, use:

```bash
docker inspect <main-container-id>
```

This provides the read-only layer paths. Navigating to the layer’s storage location (credit to `1nitramfs` for the idea of using layers), the deleted `decrypt-script` can be retrieved. Executing it decrypts `output.encrypted`, yielding the plaintext API response.

---

## Formatting and Submitting the Data

The plaintext needs to match the format expected by the `main` service’s `/submit` endpoint. Refer to **Deploily’s API documentation** to restructure the data correctly.

To submit, `curl` is installed on the host container:

```bash
apt-get update && apt-get install curl
```

An attempt to make a POST request to `http://localhost:8000/submit`:

```bash
curl -X POST -H "Content-Type: application/json" -d '<formatted-data>' http://localhost:8000
```

This will fail, indicating the `main` service is unreachable.

---

## Fixing the Network Configuration

Inspecting `compose.yaml` reveals that both services use `network_mode: none`, isolating them from external connections:

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

The `compose.yaml` file is modified to use a bridge network and ensure the `main` service is accessible:

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

The services are then restarted:

```bash
docker compose down && docker compose up -d
```

Retrying the POST request will succeed, and the `main` service returns the flag.
