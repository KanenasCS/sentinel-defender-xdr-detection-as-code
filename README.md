# Sentinel + Defender XDR Detection-as-Code

Technical research repository for managing Microsoft Defender XDR custom detections as code with the Microsoft Security Bicep extension and Microsoft Sentinel Repositories.

> **Status:** The custom-detection Detection-as-Code path is currently Preview. Validate the current Microsoft schema and limitations before production deployment.

## What this repository demonstrates

This lab follows the full detection-engineering path:

```text
Telemetry
   ↓
Advanced Hunting research
   ↓
KQL detection logic
   ↓
Microsoft.Security/detectionRules
   ↓
Bicep
   ↓
Git
   ↓
Validation / CI
   ↓
Sentinel Repository sync or direct Bicep deployment
   ↓
Microsoft Defender XDR custom detection
```

The sample detection identifies suspicious encoded PowerShell execution using `DeviceProcessEvents`.

## Current Microsoft resource model

The repository uses the Microsoft Security Bicep extension:

```json
{
  "extensions": {
    "MicrosoftSecurity": "br:mcr.microsoft.com/bicep/extensions/microsoftsecurity:v1.0.1"
  }
}
```

and the Preview resource type:

```text
Microsoft.Security/detectionRules@2026-06-01-preview
```

## Repository structure

```text
sentinel-defender-xdr-detection-as-code/
├── .github/
│   └── workflows/
│       ├── validate.yml
│       └── deploy.yml
├── detections/
│   └── defender-xdr/
│       └── execution/
│           └── suspicious-encoded-powershell.bicep
├── docs/
│   ├── architecture.md
│   ├── lab.md
│   └── images/
│       └── detection-as-code-cover.png
├── research/
│   └── encoded-powershell/
│       ├── 01-baseline.kql
│       ├── 02-encoded-prevalence.kql
│       ├── 03-parent-process-analysis.kql
│       ├── 04-volume-by-device.kql
│       └── 05-final-detection.kql
├── scripts/
│   ├── validate_detection.py
│   └── build-all.ps1
├── .gitignore
├── bicepconfig.json
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Research workflow

1. Confirm that the source table contains the required telemetry.
2. Measure normal PowerShell activity.
3. Measure encoded-command prevalence.
4. Analyze parent-process distribution.
5. Measure potential alert volume.
6. Preserve event identity fields required by Defender custom detections.
7. Convert the final query to `Microsoft.Security/detectionRules`.
8. Compile the Bicep definition.
9. Deploy to a test environment.
10. Validate runtime status and generated alert context.

## Sample detection

The deployed sample lives at:

```text
detections/defender-xdr/execution/suspicious-encoded-powershell.bicep
```

Its KQL logic is developed separately under:

```text
research/encoded-powershell/
```

This deliberately keeps **research queries** separate from the **deployable detection resource**.

## Local validation

### 1. Static repository validation

```bash
python scripts/validate_detection.py
```

The script checks for:

- the expected Preview resource type;
- a stable detection ID;
- a query condition;
- a schedule;
- an alert template;
- `Timestamp`;
- `DeviceId`;
- `ReportId`.

It is intentionally a lightweight static validator and does not replace Microsoft-side schema or runtime validation.

### 2. Bicep compilation

```bash
az bicep build \
  --file detections/defender-xdr/execution/suspicious-encoded-powershell.bicep
```

On Windows PowerShell you can build every detection with:

```powershell
./scripts/build-all.ps1
```

## Direct deployment

Microsoft documents direct Bicep deployment with `az deployment group create`.

Example:

```bash
az deployment group create \
  --resource-group <RESOURCE_GROUP> \
  --template-file detections/defender-xdr/execution/suspicious-encoded-powershell.bicep \
  --name detection-powershell
```

After deployment, verify in Microsoft Defender that the rule:

- exists;
- is enabled;
- runs successfully;
- returns the expected events;
- maps the expected device entity.

## Repository synchronization

For Microsoft Sentinel Repositories:

1. Push this repository to GitHub or Azure DevOps.
2. Open Microsoft Sentinel in the Microsoft Defender portal.
3. Go to **Content management > Repositories**.
4. Create or edit a repository connection.
5. Select **Custom Detection Rules** as a content type.
6. Select the branch that contains the detection files.
7. Save the connection.
8. Commit a test change and validate synchronization.

Repository synchronization and direct Bicep deployment are alternative deployment mechanisms. Do not configure both against the same rule unless you intentionally manage that state.

## GitHub Actions

### `validate.yml`

Runs for pull requests and pushes that modify detections, research queries, scripts, or Bicep configuration.

It:

- runs the custom static validator;
- installs/updates Azure CLI Bicep;
- compiles each `.bicep` file.

### `deploy.yml`

Runs manually by default through `workflow_dispatch`.

This is intentional: research code should not deploy automatically simply because it was pushed.

Configure the following GitHub values before use:

**Secrets**

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

**Repository/Environment variable**

```text
SECURITY_RESOURCE_GROUP
```

The workflow uses GitHub OIDC through `azure/login`, so a long-lived Azure client secret is not required.

## Preview limitations

At the time this repository was created, Microsoft documents the following limitations for the custom-detection Detection-as-Code Preview:

- custom frequency for Microsoft Sentinel data isn't supported through this Preview path;
- custom details aren't supported through this Preview path.

Portal functionality and Bicep/repository functionality can evolve independently. Treat the deployable feature set as the intersection of the Defender custom-detection capability, the current Bicep schema, and Sentinel Repository support.

## Important detection-engineering notes

### Event identity

For Defender for Endpoint event-based custom detections, preserve appropriate event identity columns such as:

```text
Timestamp
DeviceId
ReportId
```

Avoid aggregations that remove the original event identity unless you intentionally preserve representative event fields, for example with `arg_max()`.

### Explicit time filtering

Custom detections account for ingestion behavior. Avoid adding arbitrary `Timestamp > ago(...)` filters unless they are part of the actual detection hypothesis, because explicit event-time filters can change how delayed telemetry is evaluated.

### Alert volume

Research match distribution before production deployment. A syntactically valid query is not necessarily an operationally useful detection.

### Query performance

Use narrow table scope, early filters, minimal projections, and carefully designed joins/aggregations. A hunting query that is acceptable when run manually can become expensive when executed repeatedly as a detection.

## Microsoft documentation

- Custom detections overview:  
  https://learn.microsoft.com/en-us/defender-xdr/custom-detections-overview

- Manage content as code with Microsoft Sentinel repositories:  
  https://learn.microsoft.com/en-us/azure/sentinel/ci-cd-custom-content

- Deploy custom content from a repository:  
  https://learn.microsoft.com/en-us/azure/sentinel/ci-cd

- Compare Sentinel analytics rules and Defender custom detections:  
  https://learn.microsoft.com/en-us/azure/sentinel/compare-analytics-rules-custom-detections

- Create custom detection rules:  
  https://learn.microsoft.com/en-us/defender-xdr/custom-detection-rules

- Advanced Hunting query best practices:  
  https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-best-practices

## Disclaimer

This repository is a technical research sample. The Microsoft custom-detection Detection-as-Code capability referenced here is Preview and can change. Revalidate resource versions, extension versions, supported properties, permissions, and product limitations before production use.
