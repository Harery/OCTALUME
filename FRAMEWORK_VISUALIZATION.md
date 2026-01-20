# OCTALUME Framework Visualization

Complete visual guide to the OCTALUME Enterprise Lifecycle Framework

**Note:** This file contains Mermaid diagram definitions. For best viewing, use a markdown viewer that supports Mermaid diagrams (GitHub, GitLab, VS Code with Mermaid preview, or Mermaid Live Editor).

## Who This Is For

This document serves these audiences:

- **Developers** - Understanding workflow and process flows
- **Architects** - Visualizing system and phase transitions
- **Project Managers** - Understanding milestone dependencies
- **Technical Leads** - Planning phase transitions and go/no-go decisions

**Prerequisites:** Familiarity with Mermaid diagrams or access to a Mermaid-compatible viewer.

## Table of Contents

1. [Complete Lifecycle Overview](#complete-lifecycle-overview)
2. [Phase Timeline](#phase-timeline)
3. [Agent Orchestration Flow](#agent-orchestration-flow)
4. [Quality Gates State Machine](#quality-gates-state-machine)
5. [Skill Loading Sequence](#skill-loading-sequence)
6. [Traceability Chain](#traceability-chain)
7. [Shared Services Across Phases](#shared-services-across-phases)
8. [Claude Code Integration](#claude-code-integration)
9. [Beginner Onboarding Flow](#beginner-onboarding-flow)

## Complete Lifecycle Overview

The following diagram shows the complete 8-phase lifecycle with quality gates:

```mermaid
flowchart TB
    Start([Business Idea]) --> P1

    subgraph P1 [Phase 1: Vision & Strategy]
        P1_Owner[Product Owner]
        P1_Docs[PRD, Business Case<br/>Market Analysis]
        P1_Out[Approved PRD]
    end

    P1 --> Gate1{Go/No-Go?<br/>Executive Sponsor}
    Gate1 -->|Go| P2
    Gate1 -->|No-Go| End([Terminated])

    subgraph P2 [Phase 2: Requirements & Scope]
        P2_Owner[Product Owner]
        P2_Docs[Requirements, NFRs<br/>Security, Compliance<br/>Traceability Matrix]
        P2_Out[Approved Requirements]
    end

    P2 --> Gate2{Go/No-Go?<br/>Product Owner}
    Gate2 -->|Go| P3

    subgraph P3 [Phase 3: Architecture & Design]
        P3_Owner[CTA]
        P3_Docs[System Architecture<br/>Security Architecture<br/>Data Architecture]
        P3_Out[Approved Design]
    end

    P3 --> Gate3{Go/No-Go?<br/>CTA}
    Gate3 -->|Go| P4

    subgraph P4 [Phase 4: Development Planning]
        P4_Owner[Project Manager]
        P4_Docs[WBS, Resource Plan<br/>Sprint Plan, Risk Mgmt]
        P4_Out[Approved Plan]
    end

    P4 --> Gate4{Go/No-Go?<br/>Tech Lead}
    Gate4 -->|Go| P5

    subgraph P5 [Phase 5: Development Execution]
        P5_Owner[Tech Lead]
        P5_Docs[Code, Reviews<br/>Unit Tests, Integration]
        P5_Out[Working Software]
        P5_Note[Agile Sprints<br/>2-week iterations]
    end

    P5 --> Gate5{Go/No-Go?<br/>QA Lead}
    Gate5 -->|Go| P6

    subgraph P6 [Phase 6: Quality & Security]
        P6_Owner[QA Lead]
        P6_Docs[QA Testing, Security<br/>Performance, Pen Test<br/>UAT, Compliance]
        P6_Out[Validated Build]
    end

    P6 --> Gate6{Go/No-Go?<br/>Product Owner}
    Gate6 -->|Go| P7

    subgraph P7 [Phase 7: Deployment & Release]
        P7_Owner[DevOps]
        P7_Docs[Deployment Plan<br/>Release Notes<br/>Rollback Plan]
        P7_Out[Released to Production]
    end

    P7 --> Gate7{Go/No-Go?<br/>Executive}
    Gate7 -->|Go| P8

    subgraph P8 [Phase 8: Operations & Maintenance]
        P8_Owner[SRE]
        P8_Docs[Monitoring, Incidents<br/>Patches, Improvements<br/>Audit, Compliance]
        P8_Out[Operating System]
    end

    P8 --> Ongoing[Continuous Improvement]

    style Start fill:#e1f5e1
    style End fill:#f5e1e1
    style Gate1 fill:#fff4e1
    style Gate2 fill:#fff4e1
    style Gate3 fill:#fff4e1
    style Gate4 fill:#fff4e1
    style Gate5 fill:#fff4e1
    style Gate6 fill:#fff4e1
    style Gate7 fill:#fff4e1
    style Ongoing fill:#e1f5e1
```

## Phase Timeline

Visual timeline of all 8 phases showing key activities:

```mermaid
timeline
    title OCTALUME Framework - Complete Project Timeline
    section Phase 1: Vision
        Product Owner : Create PRD : Business case : Market analysis
        Security Lead : Security considerations
    section Phase 2: Requirements
        Product Owner : Functional requirements : NFRs
        Security Lead : Security requirements
        Compliance Officer : Compliance requirements
    section Phase 3: Architecture
        CTA : System architecture : Security architecture
        Data Architect : Data architecture
        Cloud Architect : Infrastructure design
    section Phase 4: Planning
        Project Manager : WBS : Resource plan : Sprint plan
        QA Lead : Test strategy
        DevOps : CI/CD plan
    section Phase 5: Development
        Tech Lead : Sprint planning : Code reviews
        Developers : Code development : Unit tests
        Security Lead : Shift-left security
    section Phase 6: Quality
        QA Lead : Test execution : Defect management
        Security Lead : Security testing : Pen testing
        Performance Engineer : Performance testing
        Compliance Officer : Compliance validation
    section Phase 7: Deployment
        DevOps : Deployment execution : Release
        SRE : Monitoring setup
    section Phase 8: Operations
        SRE : Monitoring : Incidents : Maintenance
        Security Lead : Security operations
        Compliance Officer : Audit readiness
```

## Agent Orchestration Flow

How agents work together in the OCTALUME framework:

```mermaid
flowchart TB
    subgraph Session[Claude Code Session Start]
        LoadCLAUDE[Load CLAUDE.md<br/>Auto-loaded context]
        LoadState[Read .claude/project-state.json]
        LoadProgress[Read claude-progress.txt]
        LoadGit[Check git status/log]
    end

    Session --> CheckState{Project State?}

    CheckState -->|Not Exists| Init[Spawn Initializer Agent]
    CheckState -->|Exists| CheckPhase{Phase Status?}

    Init --> Setup[Create project structure<br/>Generate features 200-500<br/>Initialize git<br/>Create init.sh]
    Setup --> P1_Start[Start Phase 1]

    CheckPhase -->|not_started| SpawnAgent[Spawn Phase Agent]
    CheckPhase -->|in_progress| Continue[Continue Current Phase]
    CheckPhase -->|blocked| Diagnose[Diagnose Blocker]
    CheckPhase -->|complete| NextPhase[Move to Next Phase]

    SpawnAgent --> PhaseWork[Phase Agent Work]
    Continue --> PhaseWork
    Diagnose --> Resolve[Resolve Blocker]
    Resolve --> PhaseWork

    PhaseWork --> Validate{Quality Gate?}
    Validate -->|Pass| UpdateState[Update project-state.json]
    Validate -->|Fail| Fix[Fix Issues]
    Fix --> PhaseWork

    UpdateState --> Commit[Commit to git<br/>Update progress.txt<br/>Clean state]
    Commit --> SessionEnd[Session Complete]

    NextPhase --> Gate{Go/No-Go?}
    Gate -->|Go| SpawnAgent
    Gate -->|No-Go| Escalate[Escalate to Executive]

    style LoadCLAUDE fill:#e1f0ff
    style Init fill:#ffe1f0
    style SpawnAgent fill:#f0ffe1
    style SessionEnd fill:#e1f5e1
```

## Quality Gates State Machine

State machine showing quality gate transitions:

```mermaid
stateDiagram-v2
    [*] --> Phase1: Start
    Phase1 --> Gate1: Phase 1 Complete
    Gate1 --> Phase2: Go
    Gate1 --> [*]: No-Go

    Phase2 --> Gate2: Phase 2 Complete
    Gate2 --> Phase3: Go
    Gate2 --> [*]: No-Go

    Phase3 --> Gate3: Phase 3 Complete
    Gate3 --> Phase4: Go
    Gate3 --> [*]: No-Go

    Phase4 --> Gate4: Phase 4 Complete
    Gate4 --> Phase5: Go
    Gate4 --> [*]: No-Go

    Phase5 --> Gate5: Phase 5 Complete
    Gate5 --> Phase6: Go
    Gate5 --> [*]: No-Go

    Phase6 --> Gate6: Phase 6 Complete
    Gate6 --> Phase7: Go
    Gate6 --> [*]: No-Go

    Phase7 --> Gate7: Phase 7 Complete
    Gate7 --> Phase8: Go
    Gate7 --> [*]: No-Go

    Phase8 --> Ongoing: Monitoring Active
    Ongoing --> Phase8: Continuous Improvement

    note right of Gate1
        Executive Sponsor Approval
        PRD + Business Case
    end note

    note right of Gate2
        Product Owner Approval
        Requirements Complete
    end note

    note right of Gate3
        CTA Approval
        Architecture Approved
    end note

    note right of Gate4
        Tech Lead Approval
        WBS + Sprint Plan
    end note

    note right of Gate5
        QA Lead Approval
        Code + Tests Pass
    end note

    note right of Gate6
        Product Owner Approval
        UAT Signed Off
    end note

    note right of Gate7
        Executive Approval
        Deployed to Production
    end note
```

## Skill Loading Sequence

How skills load progressively to optimize context usage:

```mermaid
flowchart TB
    subgraph Level1[Level 1: Metadata Only]
        L1_Load[Load YAML frontmatter<br/>~500 tokens]
        L1_Data[name, description<br/>phase, owner<br/>entry/exit criteria]
    end

    subgraph Level2[Level 2: SKILL.md Body]
        L2_Load[When skill triggered<br/>Load full SKILL.md]
        L2_Data[Process steps<br/>Deliverables<br/>Quality gates<br/>~3,000 tokens]
    end

    subgraph Level3[Level 3: Referenced Files]
        L3_Load[On-demand retrieval<br/>When specific info needed]
        L3_Data[Artifacts, templates<br/>Examples, related docs<br/>Variable size]
    end

    Level1 -->|Skill Triggered| Level2
    Level2 -->|Need Detail| Level3

    style Level1 fill:#e1f0ff
    style Level2 fill:#f0e1ff
    style Level3 fill:#ffe1f0
```

## Traceability Chain

How artifacts trace through the entire lifecycle:

```mermaid
flowchart LR
    Epic[Epic] --> Feature[Feature]
    Feature --> Story[Story]
    Story --> Commit[Commit]
    Commit --> Build[Build]
    Build --> Artifact[Artifact]
    Artifact --> Release[Release]
    Release --> Test[Test]
    Test --> Result[Result]

    subgraph Traceability
        Epic -.->|Maps to| P1[Phase 1: Vision]
        Feature -.->|Maps to| P2[Phase 2: Requirements]
        Story -.->|Maps to| P5[Phase 5: Development]
        Artifact -.->|Stored in| ArtifactsDir[artifacts/PX/]
        Test -.->|Validates| P6[Phase 6: Quality]
    end

    style Epic fill:#e1f0ff
    style Feature fill:#f0e1ff
    style Artifact fill:#ffe1f0
    style Result fill:#e1f5e1
```

## Shared Services Across Phases

How shared services (security, quality, compliance, governance) serve all phases:

```mermaid
flowchart TB
    subgraph Phases[All 8 Phases]
        P1[Phase 1]
        P2[Phase 2]
        P3[Phase 3]
        P4[Phase 4]
        P5[Phase 5]
        P6[Phase 6]
        P7[Phase 7]
        P8[Phase 8]
    end

    subgraph Shared[Shared Services]
        Security[Security Framework<br/>shared/security/SKILL.md]
        Quality[Quality Framework<br/>shared/quality/SKILL.md]
        Compliance[Compliance Framework<br/>shared/compliance/SKILL.md]
        Governance[Governance Framework<br/>shared/governance/SKILL.md]
        Roles[16 Roles<br/>shared/roles/SKILL.md]
    end

    P1 & P2 & P3 & P4 & P5 & P6 & P7 & P8 -.->|Available to all| Security
    P1 & P2 & P3 & P4 & P5 & P6 & P7 & P8 -.->|Available to all| Quality
    P1 & P2 & P3 & P4 & P5 & P6 & P7 & P8 -.->|Available to all| Compliance
    P1 & P2 & P3 & P4 & P5 & P6 & P7 & P8 -.->|Available to all| Governance
    P1 & P2 & P3 & P4 & P5 & P6 & P7 & P8 -.->|Reference| Roles

    style Security fill:#ffe1e1
    style Quality fill:#e1ffe1
    style Compliance fill:#e1e1ff
    style Governance fill:#fff4e1
    style Roles fill:#f0e1ff
```

## Claude Code Integration

How OCTALUME integrates with Claude Code:

```mermaid
flowchart TB
    subgraph Claude[Claude Code Environment]
        CLAUDE_MD[CLAUDE.md<br/>Auto-loaded main brain]
        Settings[.claude/settings.json<br/>Permissions, MCP, Agents]
        Commands[commands/<br/>/lifecycle-init<br/>/lifecycle-phase<br/>/lifecycle-feature<br/>/lifecycle-scan]
    end

    subgraph Framework[Framework Files]
        Skills[skills/<br/>8 phase skills<br/>5 shared skills]
        Agents[.claude/agents/<br/>Initializer<br/>Coding<br/>Orchestrator]
        Tools[.claude/tools/<br/>Tool search system]
        Hooks[.claude/hooks/<br/>3 hook scripts]
    end

    subgraph MCP[MCP Server]
        MCPServer[.claude/mcp-server/<br/>index.js<br/>9 lifecycle tools]
    end

    subgraph State[Project State]
        PState[.claude/project-state.json]
        FList[feature_list.json]
        Progress[claude-progress.txt]
    end

    Claude --> Framework
    Claude --> MCP
    Framework --> State
    MCP --> State

    style CLAUDE_MD fill:#e1f0ff
    style MCPServer fill:#ffe1f0
    style State fill:#f0ffe1
```

## Beginner Onboarding Flow

Step-by-step flow for new users:

```mermaid
flowchart TD
    Start([Start Here]) --> Install[Install Claude Code<br/>npm install -g @anthropic-ai/claude-code]
    Install --> Login[claude login]
    Login --> Navigate[cd to project directory]
    Navigate --> Init[/lifecycle-init<br/>Initialize new project]
    Init --> Create[Framework creates:<br/>• Project structure<br/>• 200-500 features<br/>• Git repository<br/>• Configuration files]
    Create --> Work[Claude works on features<br/>ONE AT A TIME]
    Work --> Test[Test each feature<br/>thoroughly]
    Test --> Commit[Commit to git<br/>with artifacts]
    Commit --> More{More features?}
    More -->|Yes| Work
    More -->|No| Phase{Phase complete?}
    Phase -->|No| Work
    Phase -->|Yes| Gate[Go/No-Go decision]
    Gate --> NextPhase[Move to next phase]
    NextPhase --> Work

    style Start fill:#e1f5e1
    style Init fill:#f0e1ff
    style Work fill:#e1f0ff
    style Test fill:#fff4e1
    style Commit fill:#f0ffe1
```

## Viewing These Diagrams

### Options for Viewing Mermaid Diagrams

1. **GitHub/GitLab** - Native support, automatic rendering
2. **VS Code** - Install "Markdown Preview Mermaid Support" extension
3. **Mermaid Live Editor** - https://mermaid.live/
4. **Typora** - Markdown editor with Mermaid support
5. **Obsidian** - Note-taking app with Mermaid plugin

### How to View

1. Copy the diagram code block (including ```mermaid markers)
2. Paste into Mermaid Live Editor (https://mermaid.live/)
3. Or open this file in a supported markdown viewer

## Additional Resources

For more details, see:
- `README.md` - Main framework overview
- `SETUP_GUIDE.md` - Setup and usage guide
- `CLAUDE.md` - Auto-loaded framework context
- `DIRECTORY_STRUCTURE.md` - Complete project directory listing

---

**Version:** 1.0.0
**Last Updated:** 2026-01-16
**Review Completed By:** OCTALUME TEAM
