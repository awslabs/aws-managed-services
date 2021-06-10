# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

function Get-InstalledSoftware {
    <#
    .SYNOPSIS
    Checks Operating System for Software that conflicts with AMS.
    .DESCRIPTION
    Checks Operating System for Software that conflicts with AMS. Returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .PARAMETER UnsupportedSoftware
    List of Unsupported Software software
    .EXAMPLE
    Get-InstalledSoftware -Enabled $True -BadSoftware "McAfee", "VMWare Tools", "AVG"

    Description
    -----------
    Checks Operating System for Software that conflicts with AMS. Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory = $True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "Unsupported Software",

        [Parameter(Mandatory = $True, HelpMessage = 'List of Unsupported Software')]
        [array] $UnsupportedSoftware
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)
    $DefaultTable.Add('UnsupportedSoftware', @("McAfee", "VMWare Tools", "AVG", "Trend Micro Deep Security Agent"))

    # Compare Passed Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable


    If ($FinalParams.Enabled) {
        Write-Verbose "Info - Checking for prohibited software"

        $32bit = (Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*).DisplayName
        $64bit = (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*).DisplayName
        $Both32and64Software = $32bit + $64bit

        $Description = ""
        $TestResult = "Pass"

        ForEach ($Software in $FinalParams.UnsupportedSoftware) {
            If ($Both32and64Software | Select-String -Pattern $Software) {
                $TestResult = "Fail"
                $Description = $Description + "`"$Software`" found on system`n"
            }
        }

        if ($TestResult -eq "Pass") {
            $Description = "Checks Operating System for Software that conflicts with AMS."
        }

    }
    else {
        $TestResult = "Skipped"
    }


    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $Description }

    return $ResultObject
}
