import requests

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config


class InstanceProfile:
    """
    Validate that the appropriate instance profile is attached to the instance.
    """

    validation = "Instance Profile"
    enforcement = ValidationEnforcement.RECOMMENDED

    @classmethod
    def validate(
        cls,
        *,
        role_name: str = "customer-mc-ec2-instance-profile",
        enabled: bool = True,
        instance: ValidationInstance,
    ) -> ValidationOutput:

        """
        Parameters:
        role_name (str): the IAM role to validate is attached to the instance
        enabled (bool): whether or not to run this validation function
        instance (ValidationInstance): the instance object being validated

        Returns:
        ValidationOutput: output of validation
        """

        if not enabled:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.NOT_RUN,
                enforcement=cls.enforcement,
            )

        fail_message_ec2 = (
            "Unable to connect to EC2 instance metadata," " failure is expected on-prem"
        )
        fail_message_role = f'Instance profile "{role_name}" not found'
        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        if not instance.is_ec2_instance:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=fail_message_ec2,
            )
        metadata_url = "http://169.254.169.254/latest/meta-data/"
        iam = f"iam/security-credentials/{role_name}"
        response = requests.get(f"{metadata_url}{iam}", timeout=5)
        if not response.ok:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=fail_message_role,
            )

        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.PASS,
            enforcement=cls.enforcement,
            config=config,
        )
