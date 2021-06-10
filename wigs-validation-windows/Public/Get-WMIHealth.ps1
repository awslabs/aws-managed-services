# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

function Get-WMIHealth {
    <#
    .SYNOPSIS
    Validates that the Windows Management Instrumentation (WMI) system is operational
    .DESCRIPTION
    Validates that the Windows Management Instrumentation (WMI) system is operational.  Returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-WMIHealth -Enabled $True

    Description
    -----------
    Validates that the Windows Management Instrumentation (WMI) system is operational.  Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory=$True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "WMI Health"
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)

    # Compare JSON Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable

    If ($FinalParams.Enabled) {
        try {
            Get-CimInstance -ClassName Win32_Process -ErrorAction Stop > $null
            Get-CimInstance -ClassName Win32_LogicalDisk -ErrorAction Stop > $null

            $TestResult = "Pass"
        }
        catch {
            $TestResult = "Fail"
        }
    }
    else {
        $TestResult = "Skipped"
    }

    $TestDescription = "Validates that the Windows Management Instrumentation (WMI) system is operational"
    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult;'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}