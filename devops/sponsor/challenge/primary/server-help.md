This server listens for incoming data submissions.

It expects a POST request to the `/submit` endpoint with a JSON body containing:
- `url`: The URL of the API endpoint that was called by the client.
- `response`: The JSON response received by the client from the API call.
- `secret`: A secret value.

The server verifies has a valid format before preceding, and that the secret is correct.

The expected format for the `response` field can be obtained from the Photon API documentation:
[https://docs.deploily.cloud/photon-api/#/operations/geocoding](https://docs.deploily.cloud/photon-api/#/operations/geocoding)

Upon successful verification, a flag is returned.
