import shutil
import subprocess

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config, get_ld_library_orig


class RepoAccess:
    """Validate that an instance has access to Yum Repositories."""

    validation = "Repo Access"
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

        if instance.distribution == "sles":
            repo_check_command = ["zypper", "refresh"]
            verbose_error_message = "Command 'zypper' not in $PATH"
            package_manager_found = not shutil.which("zypper") == None
        else:
            repo_check_command = ["yum", "check-update"]
            verbose_error_message = "Command 'yum' not in $PATH"
            package_manager_found = not shutil.which("yum") == None

        error_message = "Unable to validate due to unsupported environment"
        fail_message = "Unable to access repositories"

        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        if not package_manager_found:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=error_message,
                verbose_message=verbose_error_message,
            )

        proc = subprocess.run(
            repo_check_command,
            env=get_ld_library_orig(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        if proc.returncode == 1:
            verbose_message = proc.stderr.decode("utf-8")
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=fail_message,
                verbose_message=verbose_message,
            )

        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.PASS,
            enforcement=cls.enforcement,
            config=config,
        )
