function Get-FreeDiskSpace {
    <#
    .SYNOPSIS
    Checks Free Diskspace against passed minimum value
    .DESCRIPTION
    Checks Free Diskspace against passed minimum value. Returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .PARAMETER DriveLetter
    Drive letter to check for freespace.
    .PARAMETER MinimumSizeInGB
    If the free space in GB is less than this value, then the result is Fail
    .EXAMPLE
    Get-FreeDiskSpace -Enabled $True -DriverLetter C -MinimumSizeInGB 20

    Description
    -----------
    Checks Free Diskspace against passed minimum value. Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory=$True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "Free Disk Space",

        [Parameter(Mandatory=$True, HelpMessage = 'Drive Letter to Verify, for example: C')]
        [string] $DriveLetter,

        [Parameter(Mandatory=$True, HelpMessage = 'Minimum amount of recommended Free Disk Space on Selected Drive Letter')]
        [int]$MinimumSizeInGB
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)
    $DefaultTable.Add('DriveLetter', 'C')
    $DefaultTable.Add('MinimumSizeInGB', 10)

    # Compare Passed Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable


    If ($FinalParams.Enabled) {
        Write-Verbose "Info - Attempting to get free disk space"

        $FreeSpaceInGBLong = [long]((get-ciminstance Win32_LogicalDisk  -ErrorAction "Stop" -Filter "DeviceID='$($FinalParams.DriveLetter):'").freespace) / 1GB
        $FreeSpaceInGB = [math]::Round($FreeSpaceInGBLong, 2)

        Write-Verbose "Info - Free space for drive $($FinalParams.Driveletter): $($FreeSpaceInGB)"

        if ($FreeSpaceInGB -ge $FinalParams.MinimumSizeInGB) {
            $TestResult = "Pass"
        }
        else {
            $TestResult = "Fail"
        }
    }
    else {
        $TestResult = "Skipped"
    }

    $TestDescription = "Verify this system has at least $MinimumSizeInGB Gigabytes free on drive letter $DriveLetter. "
    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}