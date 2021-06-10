# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import subprocess

from pre_wigs_validation.enums import ValidationEnforcement, ValidationResult
from pre_wigs_validation.instance import ValidationInstance
from pre_wigs_validation.dataclasses import ValidationOutput
from pre_wigs_validation.utils import check_validation_config

class SSHConfiguration:
    """Validate that SSH is properly configured."""

    validation = "SSH Configuration"
    enforcement = ValidationEnforcement.RECOMMENDED

    @classmethod
    def get_ssh_config_contents(cls):
        with open("/etc/ssh/sshd_config") as file:
            return list(file.readlines())

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

        fail_message = "Improperly configured values in /etc/ssh/sshd_config: "
        verbose_message = (
            'The lines "PubkeyAuthentication yes" and'
            ' "AuthorizedKeysFile .ssh/authorized_keys" are needed.\n'
            "In most cases, an improperly configured value just means it"
            " is commented out."
        )
        config = check_validation_config(
            default_params=cls.validate.__kwdefaults__, local_params=locals()
        )

        pubkey_good = False
        keysfile_good = False

        try:
            config_contents = cls.get_ssh_config_contents()
            for line in config_contents:
                if line.startswith("AuthorizedKeysFile"):
                    keysfile_good = True
                elif line.startswith("PubkeyAuthentication"):
                    pubkey_good = True

            if not keysfile_good:
                fail_message += "AuthorizedKeysFile"
            if not pubkey_good:
                fail_message += "PubkeyAuthentication"

        except FileNotFoundError as error:
            fail_message += str(error)

        if pubkey_good and keysfile_good:
            return ValidationOutput(
                validation=cls.validation,
                result=ValidationResult.PASS,
                enforcement=cls.enforcement,
                config=config,
            )

        return ValidationOutput(
            validation=cls.validation,
            result=ValidationResult.FAIL,
            enforcement=cls.enforcement,
            config=config,
            message=fail_message,
            verbose_message=verbose_message,
        )
