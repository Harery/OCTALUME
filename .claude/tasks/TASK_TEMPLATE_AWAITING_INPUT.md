# Task List Template & Organization Framework
**Ready to receive your tasks and sort them**

---

## 📝 How to Provide Your Tasks

Please write your tasks in one of these formats:

### Format 1: Simple List
```
1. Task description
2. Another task
3. Third task
...
```

### Format 2: With Categories
```
**Frontend:**
- Task 1
- Task 2

**Backend:**
- Task 3
- Task 4
```

### Format 3: With Context
```
1. Task description - context/details about why
2. Another task - what depends on this
3. Third task - blocking tasks
```

### Format 4: Numbered & Detailed
```
1. Task name
   - Details
   - Requirements
   
2. Another task
   - What's needed
   - Blockers
```

---

## 🎯 How I Will Sort & Prioritize

Once you provide tasks, I will:

### Step 1: Categorize
Group tasks by:
- Frontend / Backend / DevOps / Documentation
- Or: v2.2 Integration / Enhancement / Testing / Bugfix
- Or: Your preferred categories

### Step 2: Prioritize Using Criteria
```
Priority = Impact × Urgency / Dependencies

HIGH:
  - Blocks other work
  - High impact
  - Low dependencies
  - Critical for release

MEDIUM:
  - Moderate impact
  - Some dependencies
  - Can be delayed if needed

LOW:
  - Nice to have
  - No blockers
  - Can be deferred
```

### Step 3: Create Implementation Order
```
1. Critical path tasks first
2. High-impact, low-effort next
3. Dependent tasks sequenced
4. Nice-to-have last
```

### Step 4: Provide Roadmap
```
Sprint 1 (High priority)
├── Task A (3 days)
├── Task B (5 days)
└── Task C (2 days)

Sprint 2 (Medium priority)
├── Task D (depends on A)
├── Task E (4 days)
└── Task F (parallel with E)

Sprint 3 (Low priority)
├── Task G
└── Task H
```

---

## 📊 Example Output Format

**When you provide tasks, I will create:**

```markdown
# OCTALUME v2.2 Task Prioritization & Roadmap

## Summary
- Total Tasks: X
- Estimated Duration: X weeks
- Critical Path: X tasks
- Parallel Work: X tasks

## Priority Breakdown

### 🔴 CRITICAL (Must do first)
1. Task A - Reason: blocks 3 others
2. Task B - Reason: urgent release

### 🟡 HIGH (Do soon)
3. Task C - Reason: high impact
4. Task D - Reason: high impact

### 🔵 MEDIUM (Do after high)
5. Task E - Reason: moderate impact
6. Task F - Reason: moderate impact

### ⚪ LOW (Do if time)
7. Task G - Reason: nice to have
8. Task H - Reason: nice to have

## Proposed Roadmap

### Sprint 1 (Week 1-2)
| Task | Effort | Dependencies | Status |
|------|--------|-------------|--------|
| Task A | 3d | None | 📍 Start |
| Task B | 2d | None | 📍 Start |
| Task C | 5d | Task A | ⏳ After A |

### Sprint 2 (Week 3-4)
| Task | Effort | Dependencies | Status |
|------|--------|-------------|--------|
| Task D | 4d | Task B | 📍 Start |
| Task E | 3d | None | 📍 Start |

### Sprint 3 (Week 5+)
| Task | Effort | Dependencies | Status |
|------|--------|-------------|--------|
| Task F | 2d | Task D | ⏳ After D |

## Critical Path Analysis

Longest sequence:
```
Task A (3d) → Task C (5d) → Task F (2d) = 10 days total
```

Parallel opportunities:
```
Week 1: A + B (2 simultaneous)
Week 2: C + D (2 simultaneous)
```

Estimated savings with parallelization: 25%

## Risk Assessment

| Task | Risk | Mitigation |
|------|------|-----------|
| Task A | High | Start early |
| Task B | Low | Standard process |
| Task C | Medium | Use v2.2 features |

## Next Steps

1. Review prioritization
2. Confirm effort estimates
3. Assign team members
4. Start Sprint 1
```

---

## 📋 What Information Helps Me Prioritize

When providing tasks, mention:

1. **Business Impact**
   - Will this generate revenue?
   - Will this fix a critical bug?
   - Will this improve user experience?

2. **Timeline**
   - Is there a deadline?
   - When do stakeholders need it?
   - Is there external pressure?

3. **Dependencies**
   - What tasks must be done first?
   - What tasks depend on this?
   - Are there external blockers?

4. **Effort**
   - Do you know effort estimates?
   - Is it frontend, backend, devops?
   - Is it complex or straightforward?

5. **Status**
   - Is this already in progress?
   - Is this blocked?
   - What's the current state?

---

## 🚀 Ready to Receive Tasks

**I'm ready to:**

- ✅ Accept your complete task list
- ✅ Sort by priority
- ✅ Create implementation roadmap
- ✅ Identify critical path
- ✅ Suggest parallelization
- ✅ Estimate effort & timeline
- ✅ Track dependencies
- ✅ Create sprint breakdown

---

## 📬 Submit Your Tasks Here

Once you paste your task list, I will:

1. **Parse** all tasks
2. **Categorize** them appropriately
3. **Analyze** dependencies
4. **Prioritize** using impact/effort/dependencies
5. **Sequence** into sprints
6. **Create** comprehensive roadmap
7. **Save** to task-management file in GitHub

---

## 💡 Tips for Best Results

1. **Be specific** - "Implement recovery" vs "Integrate recovery-manager.js into phase executors"
2. **Mention blockers** - "Blocked by task X"
3. **Note urgency** - "Needed by Jan 30"
4. **Include context** - "For compliance audit"
5. **Group related** - "All testing" or "All API endpoints"

---

## 📞 I'm Waiting For

👉 **Your task list - any format, just list them!**

Then I will:
1. Sort them
2. Prioritize them
3. Create implementation roadmap
4. Save to `.claude/tasks/PRIORITIZED_ROADMAP.md`
5. Commit to GitHub

---

**Template Ready:** ✅  
**Awaiting Your Tasks:** 👈 Your input needed  
**All v2.2 Work:** ✅ Complete & Pushed

Let me know your tasks and I'll organize them!
