from copy import deepcopy
from dataclasses import asdict
from typing import List, Dict
import os

from pre_wigs_validation.enums import (
    ValidationConfig,
    ValidationResult,
    ValidationEnforcement,
)
from pre_wigs_validation.dataclasses import ValidationOutput, FinalOutput


def sanitize_json(final_output: FinalOutput) -> Dict:
    """Remove newline characters from data before writing to JSON."""
    final_output_copy = deepcopy(final_output)
    for output in final_output_copy.validation_outputs:
        if output.message is not None:
            output.message = output.message.replace("\n", "")
    return asdict(final_output_copy)


def check_validation_config(
    default_params: List, local_params: List
) -> ValidationConfig:
    """
    Compare the passed parameter values of a validation function to its
    default parameter values.
    """
    custom = False
    for kw in default_params:
        if not (default_params[kw] == local_params[kw]):
            custom = True
    return ValidationConfig.CUSTOM if custom else ValidationConfig.DEFAULT


def get_final_output(outputs: List[ValidationOutput]) -> FinalOutput:
    """Return the final result of the pre-validation."""
    custom = False
    partial_pass = False
    failed = False
    pass_count = 0
    errored = False

    for validation_output in outputs:
        if validation_output.config is ValidationConfig.CUSTOM:
            custom = True
        if validation_output.result is ValidationResult.PASS:
            pass_count += 1
        elif validation_output.result is ValidationResult.ERROR:
            errored = True
        else:
            if validation_output.enforcement is ValidationEnforcement.RECOMMENDED:
                partial_pass = True
            else:
                failed = True

    if errored:
        final_result = ValidationResult.ERROR
        message = "Unexpected error during validation"
    elif failed:
        final_result = ValidationResult.FAIL
        message = "Not ready for ingestion"
    elif partial_pass:
        final_result = ValidationResult.PASS
        message = (
            "Passed base requirements for ingestion," " but not may be fully optimized"
        )
    else:
        final_result = ValidationResult.PASS
        message = "Ready for ingestion"

    if custom:
        config = ValidationConfig.CUSTOM
        message += ". Warning, custom config may affect final result"
    else:
        config = ValidationConfig.DEFAULT

    return FinalOutput(
        final_result=final_result,
        config=config,
        pass_count=pass_count,
        total_count=len(outputs),
        message=message,
        validation_outputs=outputs,
    )


def get_ld_library_orig() -> Dict:
    env = dict(os.environ)  # make a copy of the environment
    lp_key = "LD_LIBRARY_PATH"  # for GNU/Linux and *BSD.
    lp_orig = env.get(lp_key + "_ORIG")
    if lp_orig is not None:
        env[lp_key] = lp_orig  # restore the original, unmodified value
    else:
        # This happens when LD_LIBRARY_PATH was not set.
        # Remove the env var as a last resort:
        env.pop(lp_key, None)
    return env
