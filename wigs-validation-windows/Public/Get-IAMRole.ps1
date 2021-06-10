# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

function Get-IAMRole {
    <#
    .SYNOPSIS
    Validates that the instance has an IAM Role attached
    .DESCRIPTION
    Validates that the instance has an IAM Role.
    It returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-IAMRole -Enabled $True

    Description
    -----------
    Validates that the instance has an IAM Role attached.  Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory = $True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "IAM Role"
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)

    # Compare Passed Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable

    $TestDescription = "Validates that an IAM Role is attached to the instance"

    If ($FinalParams.Enabled) {
        Write-Verbose "Info - Attempting to get IAM Role"
        $webClient = New-Object System.Net.WebClient;

        try {
            $InstanceProfile = $webClient.DownloadString("http://169.254.169.254/latest/meta-data/iam/security-credentials/")
            $TestResult = "Pass"
            $TestDescription = "An IAM Role ($InstanceProfile) is attached to the instance. Please check with AMS support
            if unsure if this role has required permissions"
        }
        catch {
            $TestResult = "Fail"
            $InstanceProfile = "NoInstanceMetadataConnection"
        }
    }
    else {
        $TestResult = "Skipped"
    }


    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}