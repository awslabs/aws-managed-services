# Documentation 


## Configuration

A JSON config file is provided (pre-populated with default params)

**Note: must be in same directory as application to be detected**



### Enhanced Networking

Validate that Enhanced Networking drivers are installed and enabled

* enabled (bool): whether or not to run this validation function
* interface (int): the network interface on which to search for ENA drivers

```json
"EnhancedNetworking": {
  "enabled": true,
  "interface": 0
}
```



### Free Disk Space

Validate that there is enough free disk space on the root volume

* enabled (bool): whether or not to run this validation function
* min_gb (int): the minimum amount of gigabytes in free space to check for

```json
"FreeDiskSpace": {
  "enabled": true,
  "min_gb": 20
}
```



### Third Party Software

Validate that third-party software components which would conflict with AMS components have been removed, such as anti-virus clients, backup clients, virtualization software, and access management software

* enabled (bool): whether or not to run this validation function
* custom_software_list (List[str]): a list of additional blacklisted binaries to search for

```json
"ThirdPartySoftware": {
  "enabled": true,
  "custom_software_list": null
}
```



### SSH Configuration

Validate that SSH is properly configured

* enabled (bool): whether or not to run this validation function

```json
"SSHConfiguration": {
  "enabled": true
}
```



### Repo Access

Validate that the instance has access to Package Repositories

* enabled (bool): whether or not to run this validation function

```json
"RepoAccess": {
  "enabled": true
}
```



### Instance Profile

Validate that the appropriate instance profile is attached to the instance

* enabled (bool): whether or not to run this validation function
* role_name (str): the IAM role to validate is attached to the instance

```json
"InstanceProfile": {
  "enabled": true,
  "role_name": "customer-mc-ec2-instance-profile"
}
```



### SSM Agent

Validate that SSM Agent is installed and running on the instance

* enabled (bool): whether or not to run this validation function

```json
"SSMAgent": {
  "enabled": true
}
```



### Operating System

Validate that the instance operating system is supported by AMS

* enabled (bool): whether or not to run this validation function

```json
"OperatingSystem": {
  "enabled": true
}
```


---


## Output


The fields provided in the output are validation, result, enforcement, configuration, and message


### Validation


Describes the name of the requirement being validated


### Result


Describes the result of the validation


* Pass: the instance meets all requirements within the scope of the validation
* Fail: the instance does not meet all requirements within the scope of the validation
* Error: it cannot be validated whether or not the instance meets requirements due to an unexpected environment
* Not Run: the user has disabled the validation through the config file


### Enforcement


Describes whether or not the validation is a hard requirement for WIGs to succeed


* Required
* Recommended


### Configuration


Describes whether or not the user has adjusted the default configuration through the JSON config file


* Default
* Custom


### Message


Describes any pertinent information about the outcome of the validation


### Final Result


A final result is also included indicating whether or not the instance is prepared for ingestion via WIGs


To receive a "Pass" result, each validation with a "Required" enforcement must result in a "Pass"


---



