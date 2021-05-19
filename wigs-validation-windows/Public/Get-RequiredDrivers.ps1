function Get-RequiredDrivers {
    <#
    .SYNOPSIS
    Validates that AWS PV and ENA drivers exist on the instance and are the correct version
    .DESCRIPTION
    Validates that AWS PV and ENA drivers exist on the instance and are the correct version.  Returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-RequiredDrivers -Enabled $true -PVBoundary 8.2 -ENABoundary 1.0

    Description
    -----------
    Validates that AWS PV and ENA drivers exist on the instance and are the correct version.  Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory = $True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "Required Drivers",

        [Parameter(Mandatory = $True, HelpMessage = 'Minimum version for PV drivers')]
        [version] $PVBoundary,

        [Parameter(Mandatory = $True, HelpMessage = 'Minimum version for ENA drivers')]
        [version] $ENABoundary
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)
    $DefaultTable.Add('PVBoundary', "8.2")
    $DefaultTable.Add('ENABoundary', "1.0")

    # Compare JSON Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable

    if ($FinalParams.Enabled) {
        Write-Verbose "Info - Attempting to get required drivers"

        $Description = ""

        # Check if PV Drivers are installed
        if (Test-Path HKLM:\SOFTWARE\Amazon\PVDriver) {
            $InstalledPVVersion = (Get-ItemProperty HKLM:\SOFTWARE\Amazon\PVDriver).Version
            If ( $InstalledPVVersion -lt $FinalParams.PVBoundary) {
                $Failed = $True
                $Description = $Description + "Installed PV Drivers are version $InstalledPVVersion, but must be $($FinalParams.PVBoundary) or higher`n"
            }
        }
        else {
            $Failed = $True
            $Description = $Description + "PV Drivers were not found`n"
        }

        # Check if ENA Driver is installed
        if (Test-Path c:\windows\System32\DriverStore\FileRepository\ena.inf*\*.sys) {
            $InstalledENAVersion = (get-item -Path c:\windows\System32\DriverStore\FileRepository\ena.inf*\*.sys)[0].VersionInfo.ProductVersion
            if ( $InstalledENAVersion -lt $FinalParams.ENABoundary) {
                $Failed = $True
                $Description = $Description + "Installed ENA Driver is version $InstalledENAVersion, but must be $($FinalParams.ENABoundary) or higher`n"
            }
        }
        else {
            $Failed = $True
            $Description = $Description + "ENA Driver was not found`n"
        }

        if ($Failed) {
            $TestResult = "Fail"
        }
        else {
            $TestResult = "Pass"
            $Description = "Validates that AWS PV and ENA drivers exist on the instance and are the correct version"
        }
    }
    else {
        $TestResult = "Skipped"
    }

    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $Description }

    return $ResultObject

}