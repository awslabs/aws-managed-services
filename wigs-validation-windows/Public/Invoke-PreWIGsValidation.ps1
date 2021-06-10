# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

function Invoke-PreWIGsValidation {
    <#
        .SYNOPSIS
        This script runs the Pre-WIGs validation tests

        .Example
        Invoke-PreWIGsValidation

        .DESCRIPTION
        Runs the Pre-WIGs validation tests

        # The script/code shared is copyright AWS or its affiliates and is AWS Content subject to the terms of the Customer Agreement - https://aws.amazon.com/agreement/
    #>
    [CmdletBinding()]
    param
    (
        [Parameter(Mandatory = $False,
            HelpMessage = 'When enabled the valdiation output will be logged to a json file in the System Temp Directory')]
        [switch]$Log,

        [Parameter(Mandatory = $False,
            HelpMessage = 'You can select the validation output format. Default: Table')]
        [ValidateSet("Table", "JSON")]
        [string]$Output = "Table",

        [Parameter(Mandatory = $False,
            HelpMessage = 'When enabled, the process will not send the exit codes mentioned in the readme.
             This is helpful if when viewing the results of an interactive execution. ')]
        [switch]$RunWithoutExitCodes
    )

    #Array of Tests
    $TestArray = @(
        "Get-FreeDiskSpace",
        "Get-DHCPSetting",
        "Get-RequiredDrivers",
        "Get-SysprepStatus",
        "Get-IAMRole",
        "Get-RequiredAgents",
        "Get-WMIHealth",
        "Get-InstalledSoftware",
        "Get-OperatingSystem"
    )

    $ResultArray = @()
    $ErrorsOccurred = $false
    $FailedValidatonCount = 0
    $AllErrors = $null

    # ------------------ Main ------------------------------------------------------------------------------


    # Get the data from the Config file if it is found in the local directory.
    Try {

        $ConfigFilePath = "$PSSCriptRoot\WIGValidationWindows-Config.json"
        Write-Output($ConfigFilePath)
        If (test-path $ConfigFilePath) {
            Write-Output "Configuration file found. Reading...`n`r"
            $TestConfigRaw = Get-Content -Raw -Path $ConfigFilePath
            $TestConfigConverted = ConvertFrom-Json -InputObject $TestConfigRaw

            $ConfigFileExists = $True
        }
        else {
            $ConfigFileExists = $False
        }
    }
    catch {
        $ErrorMessage = $error.ToString()
        $fullmessage = "Error - Config file problem.  Error:$errorMessage"
        Write-Output $fullmessage
        exit
    }


    # Loop Through each test
    foreach ($Test in $TestArray) {
        try {
            if ($ConfigFileExists) {
                $Parameters = New-Object HashTable
                foreach ($property in ($TestConfigConverted.$test).PSObject.Properties) {
                    $Parameters.Add($property.Name, $property.Value)
                }

                # Call the function with the Params from the JSON
                $TestOutput = & $test @Parameters

                $ResultArray += $TestOutput
            }
            else {
                $TestOutput = & $test
                $ResultArray += $TestOutput
            }
        }
        catch {
            $ErrorsOccurred = $True
            $ErrorMessage = $error.ToString()
            $Message = "Error - Unable to run test $Test. Detail: $ErrorMessage`n"
            $AllErrors = $AllErrors + $Message

            $ResultObject = [PSCustomObject] @{'Label' = $Test; 'Result' = 'Error'; 'Enforcement' = ''; 'Configuration' = ''; 'Description' = $Message }
            $ResultArray += $ResultObject
        }
    }

    if ($Output -eq "Table") {
        # Display Results
        try {
            $ResultArray | Sort-Object Result | Format-Table -AutoSize -Wrap
        }
        catch {
            $ErrorsOccurred = $True
            $ErrorMessage = $error.ToString()
            $Message = "Error - Unable to Display results.   Error: $ErrorMessage"
            Write-Error -Message $Message
        }
    }
    else {
        Write-Output "Beginning Pre-WIGS Validation"
        Write-Output $ResultArray | ConvertTo-Json
    }

    if ($Log) {
        # Generate Log file
        try {
            $LogContent = $ResultArray | ConvertTo-Json
            $UniversalDate = (get-date).ToUniversalTime()
            $FilePrefix = get-date $UniversalDate -Format "yyyy-MM-ddTHH.mm.ssZ"
            $FilePath = "$env:temp\$FilePrefix-TestResults.json"

            Write-Output "Beginning Pre-WIGS Validation"
            Write-Output $LogContent

            Add-Content -Path $FilePath -Value $LogContent
            Write-Output "`nLog file generated at $FilePath`r"
        }
        catch {
            $ErrorsOccurred = $True
            $ErrorMessage = $error.ToString()
            $Message = "Error - Unable to create log file  Error: $ErrorMessage"
            Write-Error -Message $Message
        }
    }

    # Check validation results
    foreach ($array in $ResultArray) {
        if ($array.Enforcement -match "Required" -and $array.Result -match "Fail") {
            $FailedValidatonCount += 1
        }
    }

    # Send Exit codes
    If ($ErrorsOccurred) {
        Write-Host "An Exception was raised by the AMS validation code:"
        Write-Host $AllErrors -ForegroundColor Red
        Write-Host "Please request AMS assistance as needed."

        if (-not $RunWithoutExitCodes) {
            Exit 1
        }

    }
    elseif ($FailedValidatonCount -gt 0) {
        Write-Host "Final Result: Fail - Not ready for ingestion: $FailedValidatonCount failed validation(s)" -ForegroundColor Red
        
        if (-not $RunWithoutExitCodes) {
            Exit 2
        }
    }
    else {
        Write-Host "Final Result: Pass - Ready for ingestion. All Validations Passed" -ForegroundColor Green

        if (-not $RunWithoutExitCodes) {
            Exit 0
        }        

    }
}

New-Alias -Name Start-AMSValidation -Value Invoke-PreWIGsValidation -Description 'Alias to avoid changing hard coded Automaton function name'