# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Union, Optional, List
from dataclasses import dataclass

from pre_wigs_validation.enums import (
    ValidationResult,
    ValidationEnforcement,
    ValidationConfig,
    Colors,
)
from pre_wigs_validation.constants import COLOR_MAP


@dataclass
class ValidationOutput:
    validation: str
    result: Union[ValidationResult, str]
    enforcement: Union[ValidationEnforcement, str]
    config: Optional[Union[ValidationConfig, str]] = None
    message: Optional[str] = None
    verbose_message: Optional[str] = None
    # TODO maybe remove __str__
    def __str__(self) -> str:
        return (
            f"{self.validation}: {self.result}"
            + (f" ({self.config})" if (self.config is ValidationConfig.CUSTOM) else "")
            + (f"... {self.message}" if (self.message is not None) else "")
        )


@dataclass
class FinalOutput:
    final_result: Union[ValidationResult, str]
    config: Union[ValidationConfig, str]
    pass_count: int
    total_count: int
    message: str
    validation_outputs: List[ValidationOutput]

    def __str__(self) -> str:
        return (
            f"{COLOR_MAP[self.final_result]}"
            f"{self.final_result}{Colors.ENDC}: {self.message}"
        )
