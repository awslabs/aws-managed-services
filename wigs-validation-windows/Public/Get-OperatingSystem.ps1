# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

function Get-OperatingSystem {
    <#
    .SYNOPSIS
    Validates that local Operating System is supported by WIGS
    .DESCRIPTION
    Validates that local Operating System is supported by WIGS
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-OperatingSystem -Enabled $True

    Description
    -----------
    Validates that local Operating System is supported by WIGS.
    AMS supports Windows Server 2008 R2, 2012, 2012R2, 2016 and 2019.
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory=$True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "Operating System"
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)

    # Compare JSON Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable

    If ($FinalParams.Enabled) {
        $Major = ([version](Get-CimInstance -ClassName win32_operatingsystem -ErrorAction "Stop").Version).major
        $Minor = ([version](Get-CimInstance -ClassName win32_operatingsystem -ErrorAction "Stop").Version).minor
        [double]$OSVersion = [string]$Major + '.' + $Minor
        $OSName = (Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction "Stop").Caption
        $SupportedOperatingSystems = @(6.1, 6.2, 6.3, 10.0)
        $TestResult = "Fail"


        if ($SupportedOperatingSystems -contains $OSVersion) {
            # Remove after Windows Server 2019 is Supported by WIGS
            if ($OSName -match "Microsoft Windows 10") {
                $TestResult = "Fail"
            }
            else {
                $TestResult = "Pass"
            }
        }

    }
    else {
        $TestResult = "Skipped"
    }

    $TestDescription = "Validates the source instance is supported by WIGS. Supports Windows Server 2008 R2, 2012, 2012 R2, 2016 and 2019"
    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}
