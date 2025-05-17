Now i need the implementation of a server, and a decrypt script (to dicrypt the output) and a Dockerfile for both

The decrypt script will take in as a parameter the file and it should store the secret in a variable
(leave it empty i will set it), add also a decrypt-help.md file as well as the decrypt script will obfuscated

Make the helper file say something like "decrypts caller response", make sure not to give any hint to the file name

In the Dockerfile the decrypt file is copied than removed (they will need to go search through the overlay2 folder to find it)

The server listens on port 8000 for /submit calls (post)
The request body has the same format as the following
```json
{
    "url": "....",
    "response": {
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        3.0892858,
                        36.6039343
                    ],
                    "type": "Point"
                },
                "type": "Feature",
                "properties": {
                    "osm_id": 4768429181,
                    "country": "Algeria",
                    "city": "Sidi Moussa",
                    "countrycode": "DZ",
                    "postcode": "16189",
                    "county": "Baraki District",
                    "type": "house",
                    "osm_type": "N",
                    "osm_key": "amenity",
                    "street": "شارع علي المنصوري",
                    "osm_value": "restaurant",
                    "name": "مطعم سلسبيلا",
                    "state": "Algiers"
                }
            }
        ],
        "type": "FeatureCollection"
    },
    "secret": "..."
}
```
if first checks if the secret is the same as the secret in a variable it stores locally
what it does is make an api request to the url parameter and verifies the response from the api is the same as the 
reponse in the request

include a help.md for the server as well, tell them that the response follows the format in `https://docs.deploily.cloud/photon-api/#/operations/geocoding`
and make sure to include the general format without the details of the response, tell them to get the format from the link `https://docs.deploily.cloud/photon-api/#/operations/geocoding`

On successful verification of validity of request, the flag is returned to the player (use a variable i can set)

The provided Docker file is for both the server and the decrypt script

i also need a script that would generate a random folder structure given a starting point, each of the leaf files should
contain the same files as those logged by caller `output.encrypted  script.log` except for one and make sure they are filled with some filler text,
make the script output the path for 
it i will use it as a mount for the caller service, the depth of the generated folder structure is from 8 to 15 make it random
