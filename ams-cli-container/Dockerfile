FROM amazon/aws-cli
COPY ./ams-cli/amscm/  /root/.aws/models/amscm
COPY ./ams-cli/amsskms/ /root/.aws/models/amsskms
WORKDIR /aws
ENTRYPOINT ["/usr/local/bin/aws"]