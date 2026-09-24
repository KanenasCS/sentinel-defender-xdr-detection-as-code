extension MicrosoftSecurity

resource detectionRule 'Microsoft.Security/detectionRules@2026-06-01-preview' = {
  id: 'xdr-suspicious-encoded-powershell'
  displayName: 'Suspicious Encoded PowerShell Execution'
  status: 'enabled'

  queryCondition: {
    queryText: '''
DeviceProcessEvents
| where FileName in~ ("powershell.exe", "pwsh.exe")
| where ProcessCommandLine has "EncodedCommand"
    or ProcessCommandLine contains "-enc "
    or ProcessCommandLine contains "FromBase64String"
| project
    Timestamp,
    DeviceId,
    ReportId,
    DeviceName,
    FileName,
    ProcessCommandLine,
    AccountName,
    AccountSid,
    InitiatingProcessFileName,
    InitiatingProcessCommandLine
'''
  }

  schedule: {
    frequency: 'PT1H'
  }

  detectionAction: {
    alertTemplate: {
      title: 'Suspicious Encoded PowerShell Execution'
      description: 'PowerShell execution containing encoded-command or Base64-related indicators was detected. Review the complete command line, process ancestry, user context, related network activity, and subsequent process execution.'
      severity: 'medium'

      tactics: [
        {
          tactic: 'Execution'
          techniques: [
            {
              technique: 'T1059.001'
            }
          ]
        }
      ]

      entityMappings: {
        hosts: [
          {
            id: 'device'
            deviceIdColumn: 'DeviceId'
          }
        ]
      }
    }
  }
}
