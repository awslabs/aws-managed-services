import distro

from warnings import warn

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config


class OperatingSystem:
    """Validate that the instance operating system is supported by AMS."""

    # Casting major_version or minor_version to int may break in unexpected cases
    validation = "Operating System"
    enforcement = ValidationEnforcement.REQUIRED

    @classmethod
    def validate(
        cls, *, enabled: bool = True, instance: ValidationInstance
    ) -> ValidationOutput:

        """
        Parameters:
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

        name = distro.name(pretty=True)
        pass_message = f"Operating system supported: {name}"
        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        if cls.is_valid_operating_system(instance):
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.PASS,
                enforcement=cls.enforcement,
                config=config,
                message=pass_message,
            )

        fail_message = f"Unsupported operating system: {name}"
        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.FAIL,
            enforcement=cls.enforcement,
            config=config,
            message=fail_message,
        )

    @classmethod
    def is_valid_operating_system(cls, instance: ValidationInstance):

        dist = instance.distribution
        major = 0 if instance.major_version == "" else int(instance.major_version)
        minor = 0 if instance.minor_version == "" else int(instance.minor_version)

        is_valid = False

        if dist == "centos":
            is_valid = major == 7 or major == 6
        elif dist == "rhel":
            is_valid = (major == 6 and minor >= 5) or major == 7 or major == 8
        elif dist == "amzn":
            is_valid = (major == 2018 and minor == 3) or major == 2
        elif dist == "sles":
            is_valid = major == 12 or major == 15
        elif dist == "oracle":
            is_valid = major == 7

        return is_valid
