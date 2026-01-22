---
description: Discover potential features and roadmap items from codebase analysis
---

# Discover Roadmap

Analyze the codebase to discover potential features, enhancements, and roadmap items based on:
- Current implementation patterns
- TODOs and FIXMEs in code
- Incomplete features
- Common user needs for this type of application
- Industry best practices

## Discovery Categories

### 1. Incomplete Features
- Features that are partially implemented
- Commented-out code suggesting planned work
- Stub functions or placeholder implementations

### 2. Natural Extensions
- Features that would logically extend current capabilities
- Missing CRUD operations
- Incomplete API coverage

### 3. User Experience
- Missing user feedback mechanisms
- Accessibility improvements
- Performance optimizations users would notice

### 4. Developer Experience
- Missing tooling or automation
- Documentation gaps
- Testing improvements

### 5. Integration Opportunities
- Third-party services that would add value
- API integrations
- Webhook capabilities

### 6. Scalability
- Features needed for growth
- Multi-tenancy considerations
- Performance at scale

## Output Format

```markdown
## Roadmap Discovery Report

### 🎯 Quick Wins (1-2 days each)
Features that build on existing code with minimal effort.

| Feature | Description | Dependencies | Value |
|---------|-------------|--------------|-------|
| ... | ... | ... | High/Med/Low |

### 🚀 Major Features (1-2 weeks each)
Significant additions that would enhance the product.

#### 1. [Feature Name]
- **Description**: What it does
- **User Value**: Why users want it
- **Technical Approach**: How to build it
- **Prerequisites**: What's needed first
- **Effort**: Estimated time

### 🔮 Future Vision (1+ months)
Long-term possibilities based on current architecture.

1. **[Vision Item]**: Description

### 📋 From Code Comments
TODOs and FIXMEs found in the codebase:

| File | Line | Comment | Priority |
|------|------|---------|----------|
| ... | ... | ... | ... |

### 🗺️ Suggested Roadmap

**Phase 1 (Next Sprint)**
- [ ] Feature A
- [ ] Feature B

**Phase 2 (Next Month)**
- [ ] Feature C
- [ ] Feature D

**Phase 3 (Next Quarter)**
- [ ] Feature E
- [ ] Feature F
```

## Begin Discovery

Please analyze the codebase and discover potential roadmap items, prioritizing by user value and implementation feasibility.
