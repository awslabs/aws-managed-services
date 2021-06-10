# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import shutil

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config

class FreeDiskSpace:
    """Validate that there is enough free disk space on the root volume."""

    validation = "Free Disk Space"
    enforcement = ValidationEnforcement.REQUIRED

    @classmethod
    def validate(
        cls, *, min_gb: int = 5, enabled: bool = True, instance: ValidationInstance
    ) -> ValidationOutput:

        """
        Parameters:
        min_gb (int): the minimum amount of gigabytes in free space to check for
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

        pass_message = None
        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        total, used, free = shutil.disk_usage("/")
        giga = 2 ** 30
        utilization = used / total
        diff = min_gb - (free // giga)
        pass_message = f"There are {free // giga}gb free, {min_gb}gb are required"
        verbose_message = None
        if diff <= 0:
            if utilization >= 0.85:
                verbose_message = (
                    "Warning, disk utilization seems to be"
                    f" {round(utilization * 100)}%,"
                    " we recommend less than 85%"
                )
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.PASS,
                enforcement=cls.enforcement,
                config=config,
                message=pass_message,
                verbose_message=verbose_message,
            )
        fail_message = (
            f"Please free up about {diff}gb on the root volume, at least"
            f" {min_gb}gb are required"
        )
        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.FAIL,
            enforcement=cls.enforcement,
            config=config,
            message=fail_message,
        )
