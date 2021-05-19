import glob
import os

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config


class EnhancedNetworking:
    """Validate that Enhanced Networking drivers are installed and enabled."""

    # TODO check version of drivers
    validation = "Enhanced Networking"
    enforcement = ValidationEnforcement.RECOMMENDED

    @classmethod
    def validate(
        cls, *, enabled: bool = True, instance: ValidationInstance
    ) -> ValidationOutput:

        """
        Parameters:
        interface (int): the network interface on which to search for ENA drivers
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
        pass_message = "Enhanced Networking drivers enabled"
        fail_not_installed = (
            "Enhanced Networking drivers not found," " must be installed and enabled"
        )
        fail_not_active = "Enhanced Networking drivers installed," " but not enabled"
        error_message = "Unable to validate due to unsupported environment"
        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        # TODO: Put a warning for customers that we are not checking explicitly only eth0, but all active interfaces

        interface_path = "/sys/class/net"
        ena_installed = False
        ena_active = False
        ena_available = False
        try:
            if cls.ena_is_installed():
                ena_installed = True
            active_interfaces = os.listdir(interface_path)
            for interface in active_interfaces:
                if interface.startswith("lo"):
                    continue
                if cls.ena_is_active(interface=interface):
                    ena_active = True
        except FileNotFoundError as error:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.ERROR,
                enforcement=cls.enforcement,
                config=config,
                message=error_message,
                verbose_message=str(error),
            )

        if not ena_installed:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=fail_not_installed,
            )
        if not ena_active:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.FAIL,
                enforcement=cls.enforcement,
                config=config,
                message=fail_not_active,
            )
        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.PASS,
            enforcement=cls.enforcement,
            config=config,
            message=pass_message,
        )

    @staticmethod
    def ena_is_installed() -> bool:
        release = os.uname().release
        entries = glob.glob(f"/lib/modules/{release}/**/ena.ko*", recursive=True)
        return len(entries) > 0

    @staticmethod
    def ena_is_active(interface: str) -> bool:
        driver_info_file = f"/sys/class/net/{interface}/device/driver/module/drivers/pci:ena/module/initstate"
        if not os.path.isfile(driver_info_file):
            return False
        with open(driver_info_file) as file:
            return "live" in file.read()
