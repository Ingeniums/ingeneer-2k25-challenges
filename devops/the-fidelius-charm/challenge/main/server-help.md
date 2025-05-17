This server listens for incoming data submissions.

It expects a POST request to the `/submit` endpoint with a JSON body containing:
- `request_url`: The URL of the API endpoint that was called by the client.
- `response`: The relevant parts of the API response received by the client. This field should contain a JSON object representing a FeatureCollection with a single Feature, including its geometry and properties.
- `secret`: A secret value generated or provided to the client script.

The server verifies the submitted data against its own internal state and by re-fetching the API response from the provided URL.

**Note:** Only the fields explicitly listed above (`request_url`, `response`, and `secret`) are considered during the verification process. Any other fields present in the submitted JSON body will be ignored.

The expected structure for the `response` field, mirroring the relevant parts of the API output, can be obtained from the Photon API documentation:
[https://docs.deploily.cloud/photon-api/#/operations/geocoding](https://docs.deploily.cloud/photon-api/#/operations/geocoding)

Upon successful verification, a flag is returned.
