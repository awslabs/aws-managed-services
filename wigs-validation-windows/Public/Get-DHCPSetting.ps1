function Get-DHCPSetting {
    <#
    .SYNOPSIS
    Validates that DHCP is enabled on at least one NIC
    .DESCRIPTION
    Validates that DHCP is enabled on at least one NIC.  Returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-DHCPSetting -Enabled $True 

    Description
    -----------
    Validates that DHCP is enabled on at least one NIC.  Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory=$True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "DHCP Enabled"
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)

    # Compare JSON Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable

    If ($FinalParams.Enabled) {
        Write-Verbose "Info - Attempting to get DHCP setting"

        $dhcpSetting = (Get-CimInstance -Class Win32_NetworkAdapterConfiguration -ErrorAction "Stop" -Filter IPEnabled=TRUE).DHCPEnabled

        if ($dhcpSetting) {
            $TestResult = "Pass"
        }
        else {
            $TestResult = "Fail"
        }

    }
    else {
        $TestResult = "Skipped"
    }

    $TestDescription = "Validates that DHCP is enabled on at least one NIC"
    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}
