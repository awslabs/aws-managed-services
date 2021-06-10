# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
    
function Compare-Parameters {
    <#
    .SYNOPSIS
    Compare the Parameters passed from the JSON to the defaults.
    .DESCRIPTION
    If the JSON params differ from the defaults, the validation is considered custom. Params from the JSON are
    returned when there is a difference.
    .EXAMPLE
    Compare-Parameters $JSONParams $DefaultTable

    Description
    -----------
    Compare the Parameters passed from the JSON to the defaults. JSON Parms are returned if they differ.
    #>

    [CmdletBinding()]

    Param
    (
        [Parameter(HelpMessage = 'Parameters for this function from the JSON file')]
        $JSONParams,

        [Parameter(HelpMessage = 'Hash table containing default values')]
        $DefaultTable
    )

    $ResultHash = @{}
    $Configuration = "Default"

    foreach ($DefaultParam in $DefaultTable.Keys) {
        If ($JSONParams.ContainsKey($DefaultParam)) {
            if (Compare-Object -ReferenceObject $JSONParams.Item($DefaultParam) -DifferenceObject $DefaultTable.$DefaultParam) {
                Write-Verbose "JSON value does not match default"
                $Configuration = "Custom"

                $ResultHash.Add($DefaultParam,$JSONParams.Item($DefaultParam))
                Continue
            }
        }
        Write-output "$DefaultParam not set with custom value - using default"
        $ResultHash.Add($DefaultParam,$DefaultTable.$DefaultParam)
    }

    $ResultHash.Add('Configuration',$Configuration)

    Return $ResultHash
}