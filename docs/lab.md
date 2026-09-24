# Lab Guide

## Objective

Deploy and validate a Microsoft Defender XDR custom detection represented as Bicep.

## 1. Validate telemetry

Run:

```text
research/encoded-powershell/01-baseline.kql
```

Confirm `DeviceProcessEvents` contains PowerShell process telemetry.

## 2. Measure candidate behavior

Run:

```text
research/encoded-powershell/02-encoded-prevalence.kql
```

Record:

- total matches;
- unique devices;
- unique users.

## 3. Analyze parent processes

Run:

```text
research/encoded-powershell/03-parent-process-analysis.kql
```

Investigate high-volume parents before considering exclusions.

## 4. Measure endpoint distribution

Run:

```text
research/encoded-powershell/04-volume-by-device.kql
```

Check whether results are concentrated on a small number of management endpoints or distributed across the estate.

## 5. Validate final event-level query

Run:

```text
research/encoded-powershell/05-final-detection.kql
```

Confirm that the output preserves:

```text
Timestamp
DeviceId
ReportId
```

as well as useful investigation context.

## 6. Run static validation

```bash
python scripts/validate_detection.py
```

## 7. Compile Bicep

```bash
az bicep build \
  --file detections/defender-xdr/execution/suspicious-encoded-powershell.bicep
```

## 8. Deploy

```bash
az deployment group create \
  --resource-group <RESOURCE_GROUP> \
  --template-file detections/defender-xdr/execution/suspicious-encoded-powershell.bicep \
  --name detection-powershell
```

Alternatively, configure Microsoft Sentinel Repositories and select **Custom Detection Rules** as a content type.

## 9. Runtime validation

After deployment, validate:

1. The rule is visible.
2. The rule is enabled.
3. Last-run status is successful.
4. Test telemetry matches the KQL.
5. The generated alert contains the expected device context.
6. Alert volume is consistent with the pre-deployment baseline.

## 10. Performance validation

Inspect Advanced Hunting query resource consumption for the deployed custom detection.

Capture:

- CPU;
- execution duration;
- execution status;
- query frequency.

If necessary, optimize and repeat the measurement.
