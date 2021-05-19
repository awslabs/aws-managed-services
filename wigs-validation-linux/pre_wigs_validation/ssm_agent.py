import shutil
import subprocess

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config

FAIL_NOT_INSTALLED = "SSM Agent not installed"
FAIL_NOT_RUNNING = "SSM Agent installed, but not running"
ERROR_MESSAGE = "Unable to validate due to unsupported environment"
V_ERROR_SYSTEMCTL = "Command 'systemctl' not in PATH"
V_ERROR_STATUS = "Command 'status' not in PATH"


class SSMAgent:
    """Validate that SSM Agent is installed and running on the instance."""

    # TODO exhaustively check service managers (status, service, systemctl)
    # TODO deep dive into return codes of all subprocesses
    validation = "SSM Agent"
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

        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        validation_fn_map = {
            "rhel8": cls.validate_with_systemctl,
            "rhel7": cls.validate_with_systemctl,
            "rhel6": cls.validate_with_status,
            "centos6": cls.validate_with_status,
            "centos7": cls.validate_with_systemctl,
            "amzn2018": cls.validate_with_status,  # amzn1
            "amzn2": cls.validate_with_systemctl,
            "sles12": cls.validate_with_systemctl,
            "sles15": cls.validate_with_systemctl,
            "oracle7": cls.validate_with_systemctl,
        }

        distribution_major_version_key = instance.distribution + instance.major_version

        validation_fn = validation_fn_map.get(distribution_major_version_key)

        if validation_fn is not None:
            return validation_fn(config)

        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.ERROR,
            enforcement=cls.enforcement,
            config=config,
            message=ERROR_MESSAGE,
        )

    @classmethod
    def validate_with_status(cls, config):
        if shutil.which("status") is None:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.ERROR,
                enforcement=cls.enforcement,
                config=config,
                message=ERROR_MESSAGE,
                verbose_message=V_ERROR_STATUS,
            )
        try:
            proc = subprocess.run(
                ["status", "amazon-ssm-agent"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=FAIL_NOT_INSTALLED,
            )
        if "running" not in proc.stdout.decode("utf-8"):
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=FAIL_NOT_RUNNING,
            )
        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.PASS,
            enforcement=cls.enforcement,
            config=config,
        )

    @classmethod
    def validate_with_systemctl(cls, config):
        if shutil.which("systemctl") is None:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.ERROR,
                enforcement=cls.enforcement,
                config=config,
                message=ERROR_MESSAGE,
                verbose_message=V_ERROR_SYSTEMCTL,
            )
        try:
            proc = subprocess.run(
                ["systemctl", "status", "amazon-ssm-agent"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=FAIL_NOT_INSTALLED,
            )
        try:
            subprocess.run(["systemctl", "is-active", "amazon-ssm-agent"], check=True)
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.PASS,
                enforcement=cls.enforcement,
                config=config,
            )
        except subprocess.CalledProcessError:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=FAIL_NOT_RUNNING,
            )
