# Pre-WIGs Validator (Windows)

The Windows Pre-WIGs Validator is a tool used to determine if a computer ready for ingestion into AMS by the Workload Ingestion System (WIGS). The tool is comprised of a PowerShell module and a JSON configuration file.

### Prerequisites

The script requires PowerShell 3.0 or higher

### Getting Started

Extract the Zip file, which contains a PowerShell Module, into the folder of your choice.


### Usage

To run the functions in the module, the module will need to me imported. Open a Windows Powershell console and set the current directory to the location of the `AWSManagedServices.PreWigs.Validation.psm1` file.

**Execute the script**
1. Open a PowerShell console
2. Set the current directory to the location of the `AWSManagedServices.PreWigs.Validation.psm1` file. For example, if you extracted the zip file to `c:\temp`, set the current directory to `c:\temp\AWSManagedServices.PreWigs.Validation`
3. To execute the script interactively and view the results, run the following commands
```
Import-Module .\AWSManagedServices.PreWigs.Validation.psm1 -force
Invoke-PreWIGsValidation -RunWithoutExitCodes
```
4. If you wish to capture the error codes listed in the "Exit Codes" section below, you may run the script
without the RunWithoutExitCodes option (Note that this will terminate the active PowerShell session):
```
Import-Module .\AWSManagedServices.PreWigs.Validation.psm1 -force
Invoke-PreWIGsValidation 
```



**Logging (Optional)**

To create the optional JSON log, include the `-Log` parameter. For example,
```
Invoke-PreWIGsValidation -Log
```

## Output Table Detail

Here is a list of the table column headers along with a description of each.


1. **Validation**
Describes the name of the requirement being validated

2. **Result**
Describes the result of the validation

    * Pass - The validation passed
    * Fail - The validation did not pass. The specific problem will be listed in the description field
    * Error - An Unexpected exception occurred while running the validation. The specific error found will be listed int he description field and at the bottom of the output in red.

3. **Enforcement**
Describes whether or not the validation is a hard requirement for WIGs to succeed

    * Required
    * Recommended

4. **Configuration**
Describes whether or not the user has adjusted the default configuration through the JSON configuration file

    * Default
    * Custom

5. **Description**
Describes any pertinent information about the outcome of the validation


**Final Result**

A final result is also included indicating whether or not the instance is prepared for ingestion via WIGs
To receive a "Pass" result, each validation with a "Required" enforcement must result in a "Pass"


**Example Output**
```
PS C:\PowerShell> Invoke-PreWIGsValidation
Configuration file found. Reading...


Label                 Result Enforcement Configuration Description
-----                 ------ ----------- ------------- -----------
WMI Health            Pass   Required    Default       Validates that the Windows Management Instrumentation (WMI)
                                                       system is operational
Required Agent Status Pass   Required    Default       Validates that the required Amazon Agents are installed and
                                                       running.
Operating System      Pass   Required    Default       Validates the source instance is supported by WIGS. Supports
                                                       Windows Server 2008 R2, 2012, 2012 R2, 2016 and 2019
Unsupported Software  Pass   Required    Default       Checks Operating System for Software that conflicts with AMS.
IAM Role              Pass   Required    Default       Validates that an IAM Role is attached to the instance
DHCP Enabled          Pass   Required    Default       Validates that DHCP is enabled on at least one NIC
Free Disk Space       Pass   Required    Default       Verify this system has at least 10 Gigabytes free on drive
                                                       letter C.
Get-SysprepStatus     Pass   Required    Default       Validates that common SysPrep problems will not be encountered
                                                       during WIGS.
Required Drivers      Pass   Required    Default       Validates that AWS PV and ENA drivers exist on the instance and
                                                       are the correct version


Final Result: Pass - Ready for ingestion. All Validations Passed
```

**Exit codes**

* 0 - All required validations passed.
* 1 - Unexpected exception while running validations.
* 2 - At least one required validation did not pass.

## Custom Configuration (Optional)

A JSON configuration file is provided and pre-populated with the default parameters. Customers may edit this file to achieve the desired test results. For example, a physical server in a customer data center would not have an EC2 instance profile. In cases such as this, customers may edit the configuration file to skip the instance profile test to avoid confusion.

**Note: The JSON file must be in same directory as `Invoke-PreWIGsValidation.ps1` to be detected. This is in the `Public` subfolder**

## Validation Detail

Below is the list of each validation test along with a description and instructions for using it in the JSON configuration file

### Free Disk Space

Validate that there is the recommended amount of free disk space on the active boot volume

* Enabled (bool): Whether or not to run this validation test
* MinimumSizeInGB (int): The test will check that the system has at least this amount of free space (in Gigabytes)
* DriveLetter (string): The test will be run against this drive letter.

```json
"FreeDiskSpace": {
  "Enabled": true,
  "MinimumSizeInGB": 10,
  "DriveLetter": "C"
}
```

### Get-DHCPSetting

Validates that DHCP is enabled on at least one NIC.

* Enabled (bool): Whether or not to run this validation test

```json
"SSHConfiguration": {
  "enabled": true
}
```

### Get-RequiredDrivers

Validates that the recommended versions of the Paravirtual (PV) and Enhanced Networking Adapter (ENA) drivers are installed and loaded on the system.

* Enabled (bool): Whether or not to run this validation test
* PVBoundary (string): The minimum *Major.minor* PV driver version that will pass the test (The PV drivers must be this version or higher). Example "8.2"
* ENABoundary (string): The minimum *Major.minor* PV driver version that will pass the test (The PV drivers must be this version or higher). Example "1.0"

```json
"Get-RequiredDrivers": {
    "Enabled": true,
    "PVBoundary": "8.2",
    "ENABoundary": "1.0"
},
```

### Get-SysprepStatus

Validates that common SysPrep problems will not be encountered during WIGS.

* Enabled (bool): Whether or not to run this validation test

```json
"Get-SysprepStatus": {
  "enabled": true
}
```

### Get-IAMRole

Validates that the instance has an IAM Role attached. Only AWS EC2 instances will
pass this validaiton test. Please note that the existence of an IAM role does not guarantee that
the instance has all the needed permissions. Verify with AMS support if unsure if the correct 
profile is attached.

* Enabled (bool): Whether or not to run this validation test

```json
"Get-IAMRole": {
    "Enabled": false,
}
```

### Get-RequiredAgents

Validates that the required Amazon Agents are installed and running

* Enabled (bool): Whether or not to run this validation function

```json
"Get-RequiredAgents": {
    "Enabled": true
}
```

### Get-WMIHealth

Validates that the Windows Management Instrumentation (WMI) system is operational

* Enabled (bool): Whether or not to run this validation function

```json
"Get-WMIHealth": {
    "Enabled": true
}
```

### Get-OperatingSystem

Validates that local Operating System is supported by WIGS. Supports Server 2008 R2, 2012, 2012 R2, 2016 and 2019.

* Enabled (bool): Whether or not to run this validation function

```json
"Get-OperatingSystem": {
    "Enabled": true
}
```

### Get-InstalledSoftware

Validate that third-party software components which would conflict with AMS components have been removed, such as anti-virus clients and virtualization software. Customers are encouraged to add additional strings that correspond to software of this type. The script does a simple string check of the `DisplayName` field found in the following registry keys:
1. HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*
2. HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*


* Enabled (bool): Whether or not to run this validation function
* UnsupportedSoftware (List[str]): A list of software that conflicts with AMS

```json
"Get-InstalledSoftware": {
"Enabled": true,
"UnsupportedSoftware":["McAfee", "VMWare Tools", "AVG"]
}
```

---