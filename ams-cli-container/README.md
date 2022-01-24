# amscli docker container image

The AMS CLI is an easy way to interact with the AMS API.
For more information refer to 
https://docs.aws.amazon.com/managedservices/latest/userguide/understand-sent-api.html

## How to use it

1. Git clone the repository
2. `cd ams-cli-container`
3. `docker build -t amscli .`
4. Make sure you have authenticated and authorized to use target AMS account
4. `docker run amscli amscm get-rfc --rfc-id <RFC-ID> --region us-east-1`
   