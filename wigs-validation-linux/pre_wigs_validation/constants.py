from pre_wigs_validation.enums import ValidationResult, Colors

COLOR_MAP = {
    ValidationResult.PASS: Colors.PASS,
    ValidationResult.FAIL: Colors.FAIL,
    ValidationResult.ERROR: Colors.ERROR,
    ValidationResult.NOT_RUN: Colors.NOT_RUN,
}

VALIDATION_RESULT_ERROR_CODE_MAP = {
    ValidationResult.PASS: 0,
    ValidationResult.FAIL: 2,
    ValidationResult.ERROR: 1,
}
