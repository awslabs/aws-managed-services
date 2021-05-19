function Get-RequiredAgents {
    <#
    .SYNOPSIS
    Validates that the required Amazon Agents are installed and running
    .DESCRIPTION
    Validates that the required Amazon Agents are installed and running.  Returns an object with result and friendly description
    .PARAMETER Enabled
    Should this test be run? True/False.
    .PARAMETER Label
    Friendly name for this Test.
    .EXAMPLE
    Get-RequiredAgents -Enabled $True

    Description
    -----------
    Validates that the required Amazon Agents are installed and running.  Returns an object with result and friendly description
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(Mandatory = $True, HelpMessage = 'Should this test be run? True/False')]
        [boolean] $Enabled,

        [Parameter(HelpMessage = 'Friendly name for this Test')]
        [string] $Label = "Required Agent Status"
    )

    # Set Default Parameters in Hashtable
    $DefaultTable = New-Object HashTable
    $DefaultTable.Add('Enabled', $True)

    # Compare JSON Parameters to Default and set as required
    $JSONParms = $PSBoundParameters
    $FinalParams = Compare-Parameters $JSONParms $DefaultTable
    $OSName = (Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction "Stop").Caption

    If ($FinalParams.Enabled) {
        $RunningServices = get-service -ErrorAction Stop | Where-Object { $_.status -eq "Running" } | Select-Object Name

        # Check for SSM Agent - needed for All OSes
        if (-not ($RunningServices.Name).Contains("AmazonSSMAgent")) {
            $TestResult = "Fail"
            $Description = $Description + "AmazonSSMAgent is not found or not running`n"
        }
        
        # EC2Config is on OSes earlier than 2016 / 2019
        if ( $OSName -match "Windows Server 2016" -or $OSName -match "Microsoft Windows Server 2019") {
            write-verbose "Server 2016/2019 found. No need to check for EC2Config"
        }
        else {
            if (-not ($RunningServices.Name).Contains("Ec2Config")) {
                $TestResult = "Fail"
                $Description = $Description + "Ec2Config is not found or not running"
            }
        }

        if ( $TestResult -eq "Fail") {
            $TestDescription = $Description
        }
        Else {
            $TestResult = "Pass"
            $TestDescription = "Validates that the required Amazon Agents are installed and running."
        }
    }
    else {
        $TestResult = "Skipped"
        $TestDescription = "Validates that the required Amazon Agents are installed and running."
    }

    $ResultObject = [PSCustomObject] @{'Label' = $Label; 'Result' = $TestResult; 'Enforcement' = 'Required'; 'Configuration' = $FinalParams.Configuration; 'Description' = $TestDescription }

    return $ResultObject
}
