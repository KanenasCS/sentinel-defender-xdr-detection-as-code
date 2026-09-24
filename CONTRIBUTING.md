# Contributing

This repository treats detections as technical research artifacts.

## Before changing a detection

Provide evidence for the proposed change through the research queries.

A useful change should answer:

- Which telemetry supports the hypothesis?
- Which behavior is being detected?
- Which fields identify the original event?
- What is the baseline match volume?
- What benign patterns were observed?
- How does the change affect false positives?
- Does the query remain efficient enough for repeated execution?
- Does the Bicep resource compile?
- Has the deployed rule been runtime-tested?

## Detection IDs

Do not rotate the detection `id` for routine revisions.

The ID should represent the logical detection. Git history represents revisions.

## KQL

Prefer:

- explicit source tables;
- early filters;
- only the columns required for detection, entity mapping, and investigation;
- event identity preservation;
- documented exclusions backed by research.

Avoid unexplained allowlists or exclusions.

## Preview API

The repository currently targets:

```text
Microsoft.Security/detectionRules@2026-06-01-preview
```

and:

```text
br:mcr.microsoft.com/bicep/extensions/microsoftsecurity:v1.0.1
```

If Microsoft changes either version, update the documentation, compile every detection, and validate deployment before merging the version change.
