function Get-SysprepStatus {
    <#
    .SYNOPSIS
    Validates that common SysPrep problems will not be encountered during WIGS.
    .DESCRIPTION
    Validates that common SysPrep problems will not be encountered during WIGS.
    For 2008 R2 and 2012 Base and R2, it will verify that 1) The Operating System has not been
    upgraded  2) Sysprep has not run more than the maximum number of times
    per Microsoft guidelines. For 2016, both of these checks are skipped as neither
    cause problems for that OS.
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-SysprepStatus -Enabled $True

    Description
    -----------
    Validates that common SysPrep problems will not be encountered during WIGS.
    For 2008 R2 and 2012 Base and R2, it will verify that 1) The Operating System has not been
    upgraded  2) Sysprep has not run more than the maximum number of times
    per Microsoft guidelines. For 2016, both of these checks are skipped as neither
    cause problems for that OS.
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory=$True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "Get-SysprepStatus"
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)

    # Compare JSON Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable

    If ($FinalParams.Enabled) {
        Write-Verbose "Info - Checking OS to determine which checks need to run"
        $OSName = (Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction "Stop").Caption

        # Set Defaults before Tests
        $TestResult = "Pass"
        $TestDescription = "Validates that common SysPrep problems will not be encountered during WIGS."
        $FailDescription = $null

        if ($OSName -match "Windows Server 2016" -or $OSName -match "Microsoft Windows Server 2019") {
            Write-Verbose "Info - Windows Server 2016/2019 detected. Skipping validations..."
        }
        else  {
            Write-Verbose "Info - Attempting to get in-place upgrade registry key"
            $RegistryUpgradePath = 'HKLM:\SYSTEM\Setup\Upgrade'

            if (Test-Path -Path $RegistryUpgradePath) {
                $TestResult = "Fail"
                $FailDescription = "An In-place upgrade of the Operating System has been detected in the registry. SysPrep will fail.`n"
            }

            Write-Verbose "Info - Attempting to Check current ReArm count"
            $RearmCount = [int](Get-CimInstance -ClassName SoftwareLicensingService -ErrorAction Stop).RemainingWindowsReArmCount

            If ($RearmCount -lt 1) {
                $TestResult = "Fail"
                $FailDescription = $FailDescription + "Rearm count is less than 1. SysPrep will fail."
            }

            if ( $TestResult -eq "Fail") {
                $TestDescription = $FailDescription
            }
        }
    }
    else {
        $TestResult = "Skipped"
        $TestDescription = "Validates that common SysPrep problems will not be encountered during WIGS."
    }


    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}