import distro
import requests


class ValidationInstance:
    def __init__(self):
        """The instance being validated for ingestion."""
        self.distribution = distro.id()
        self.major_version = distro.major_version()
        self.minor_version = distro.minor_version()
        self.is_ec2_instance = self.__get_is_ec2()

    def __get_is_ec2(self, timeout: int = 5) -> bool:
        """Determine whether the instance is in EC2 or on-prem."""
        metadata_url = "http://169.254.169.254/latest/meta-data/"
        try:
            response = requests.get(metadata_url, timeout=timeout)
        except OSError:
            return False
        return response.ok
