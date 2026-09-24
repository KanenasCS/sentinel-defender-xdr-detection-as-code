# Detection-as-Code Architecture

## Resource path

```text
Advanced Hunting telemetry
          |
          v
      KQL research
          |
          v
 Microsoft Security Bicep extension
          |
          v
Microsoft.Security/detectionRules@2026-06-01-preview
          |
          +-----------------------------+
          |                             |
          v                             v
Sentinel Repository sync          Direct Bicep deployment
          |                             |
          +---------------+-------------+
                          |
                          v
              Defender XDR custom detection
                          |
                          v
                     Alert / action
```

## Git flow

```mermaid
flowchart LR
    A[Telemetry research] --> B[KQL]
    B --> C[Bicep detection]
    C --> D[Feature branch]
    D --> E[Pull request]
    E --> F[Static validation]
    E --> G[Bicep build]
    F --> H[Merge]
    G --> H
    H --> I{Deployment path}
    I --> J[Sentinel Repository sync]
    I --> K[Direct Bicep deployment]
    J --> L[Defender XDR custom detection]
    K --> L
    L --> M[Runtime validation]
```

## State model

The repository should represent the desired detection state.

```text
Desired state  = Git/Bicep
Observed state = Defender XDR detection

Drift = Desired state != Observed state
```

Avoid maintaining a repository-managed rule and an independently edited portal copy as separate authoritative states.
