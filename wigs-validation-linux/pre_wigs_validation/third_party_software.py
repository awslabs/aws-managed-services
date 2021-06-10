# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import List
import shutil

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config

class ThirdPartySoftware:
    """
    Validate that third-party software components which would conflict
    with AMS components have been removed, such as anti-virus clients,
    backup clients, virtualization software, and access management software.
    """

    validation = "Third Party Software"
    enforcement = ValidationEnforcement.REQUIRED
    software_list = [
        "ma",
        "cma",
        "aex-bootstrap",
        "aex-configure",
        "aex-diagnostics",
        "aex-env",
        "aex-uninstall",
        "aex-helper",
        "aex-cta",
        "pbis",
        "domainjoin-cli",
        "adinfo",
        "adcheck",
        "adquery",
        "vmware-toolbox-cmd",
        "vmware-user",
        "realmd"
    ]

    @classmethod
    def validate(
        cls,
        *,
        custom_software_list: List[str] = None,
        enabled: bool = True,
        instance: ValidationInstance,
    ) -> ValidationOutput:

        """
        Parameters:
        custom_software_list (List[str]): a list of additional blacklisted binaries to search for
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

        pass_message = "Unwanted software may exist, but nothing was found"
        fail_message = "Please remove the following software: "
        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        # paths = ["/usr/bin/", "/usr/local/bin/", "/opt/", "/usr/local/"]
        # empty_message = "No software provided in config file"

        total_software_list = cls.software_list
        if custom_software_list is not None:
            total_software_list += custom_software_list

        failed = False
        for software in total_software_list:
            if shutil.which(software) is not None:
                failed = True
                fail_message += f"{software}, "

        if not failed:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.PASS,
                enforcement=cls.enforcement,
                config=config,
                message=pass_message,
            )
        fail_message = fail_message[0:-2]
        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.FAIL,
            enforcement=cls.enforcement,
            config=config,
            message=fail_message,
        )
