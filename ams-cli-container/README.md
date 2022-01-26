# Steps to build amscli container image

The AMS CLI is an easy way to interact with the AMS API.
For more information refer to 
https://docs.aws.amazon.com/managedservices/latest/userguide/understand-sent-api.html

## Important Note
AMS CLI is only available to AMS customers and it should not be distributed to non-AMS customers.

## How to use it

1. Git clone this repository
2. Login to AMS managed AWS account and download `AMS CLI` from `Developer 
resources` under `Managed Services`
3. From the downloaded zip file copy the content of `amscm` and `amsskms` 
and place it under `ams-cli-container\ams-cli` of this repository
4. Make sure to switch to `ams-cli-container` directory before executing docker build
5. `docker build -t amscli .`
6. Make sure you are authenticated and authorized to use target AMS account
7. `docker run amscli amscm get-rfc --rfc-id <RFC-ID> --region us-east-1`

