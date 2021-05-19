# Pre-WIGs Validator (Linux)

The Pre-WIGs Validator is a tool for validating whether or not an instance is prepared for ingestion via WIGs into AMS

Please see the documentation.md for information about configuring the validation tests.


## Getting Started


### Usage
**Note: must run as root**

**Run once - Set binary as executable**
```
sudo chmod +x ./pre-wigs-validator
```

**Standard usage**
```
sudo ./pre-wigs-validator --help

usage: pre-wigs-validator [-h] [-l] [-v] [-q] [-V]

Validates that a Linux machine is prepared for ingestion into AMS via WIGs

optional arguments:
  -h, --help     show this help message and exit
  -l, --log      create json log file of results in logs folder
  -v, --verbose  include in-depth error messages in console output
  -q, --quiet    suppress console output
  -V, --version  display version info


```

**Exit codes**

* 0 - All required validations passed.
* 1 - Unexpected exception while running validations.
* 2 - At least one required validation did not pass.

## Building / Converting Code into Binary


The following steps describe how to build a binary from the source code


### Prerequisites


Python3 and pip must be installed to build

Open command prompt and navigate to directory of application


### PyInstaller Build Steps

```
#  Install dependencies from setup.py/pyproject.toml
pip3 install --upgrade pip
pip3 install .
#  Run PyInstaller
pyinstaller --onefile --name=pre-wigs-validator control_script.py
#  Move binary to root directory of the application
mv dist/pre-wigs-validator ./pre-wigs-validator
```


### Alternate Process (no PyInstaller)

```
#  Install dependencies from setup.py/pyproject.toml
pip3 install --upgrade pip
pip3 install .
#  Invoke the script directly
python3 control_script.py
```



