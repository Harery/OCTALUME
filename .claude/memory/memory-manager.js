#!/usr/bin/env node
/**
 * OCTALUME Memory Manager v2.0
 * Cross-session memory persistence and context loading for Claude Code
 * 
 * Usage:
 *   node memory-manager.js save --session "session-id" --data '{"key": "value"}'
 *   node memory-manager.js load --query "search term"
 *   node memory-manager.js context --task "task description"
 *   node memory-manager.js stats
 */

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = path.join(__dirname);
const MEMORY_FILE = path.join(MEMORY_DIR, 'memory.json');
const SESSIONS_DIR = path.join(MEMORY_DIR, 'sessions');
const INSIGHTS_DIR = path.join(MEMORY_DIR, 'insights');

// Ensure directories exist
[SESSIONS_DIR, INSIGHTS_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

/**
 * Load memory from file
 */
function loadMemory() {
  if (!fs.existsSync(MEMORY_FILE)) {
    return createEmptyMemory();
  }
  try {
    return JSON.parse(fs.readFileSync(MEMORY_FILE, 'utf8'));
  } catch (e) {
    console.error('Error loading memory:', e.message);
    return createEmptyMemory();
  }
}

/**
 * Save memory to file
 */
function saveMemory(memory) {
  fs.writeFileSync(MEMORY_FILE, JSON.stringify(memory, null, 2), 'utf8');
}

/**
 * Create empty memory structure
 */
function createEmptyMemory() {
  return {
    version: "2.0",
    schema: "octalume-memory-v2",
    project: { name: "", type: "", stack: [], initialized: "", description: "" },
    sessions: [],
    knowledge_base: {
      architecture_decisions: [],
      code_patterns: [],
      gotchas: [],
      best_practices: [],
      lessons_learned: []
    },
    feature_history: [],
    current_context: { active_phase: "", active_feature: "", pending_tasks: [], last_session_id: "" },
    statistics: { total_sessions: 0, total_artifacts: 0, total_decisions: 0, phases_completed: [] }
  };
}

/**
 * Start a new session
 */
function startSession(sessionData) {
  const memory = loadMemory();
  const sessionId = `session-${Date.now()}`;
  const timestamp = new Date().toISOString();
  
  const session = {
    id: sessionId,
    timestamp: timestamp,
    phase: sessionData.phase || memory.current_context.active_phase || 'unknown',
    summary: sessionData.summary || '',
    artifacts_created: [],
    decisions: [],
    patterns_learned: [],
    issues_encountered: [],
    status: 'active'
  };
  
  memory.sessions.push(session);
  memory.current_context.last_session_id = sessionId;
  memory.statistics.total_sessions++;
  
  saveMemory(memory);
  
  // Also save to sessions directory
  const sessionFile = path.join(SESSIONS_DIR, `${sessionId}.json`);
  fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2), 'utf8');
  
  console.log(JSON.stringify({ success: true, session_id: sessionId, timestamp }));
  return sessionId;
}

/**
 * End current session with insights
 */
function endSession(sessionId, insights) {
  const memory = loadMemory();
  
  const sessionIndex = memory.sessions.findIndex(s => s.id === sessionId);
  if (sessionIndex === -1) {
    console.error(JSON.stringify({ error: 'Session not found', session_id: sessionId }));
    return;
  }
  
  const session = memory.sessions[sessionIndex];
  session.status = 'completed';
  session.ended_at = new Date().toISOString();
  
  if (insights) {
    if (insights.summary) session.summary = insights.summary;
    if (insights.artifacts) session.artifacts_created = insights.artifacts;
    if (insights.decisions) {
      session.decisions = insights.decisions;
      memory.statistics.total_decisions += insights.decisions.length;
      // Also add to knowledge base
      insights.decisions.forEach(d => {
        memory.knowledge_base.architecture_decisions.push({
          ...d,
          session_id: sessionId,
          timestamp: new Date().toISOString()
        });
      });
    }
    if (insights.patterns) {
      session.patterns_learned = insights.patterns;
      insights.patterns.forEach(p => {
        memory.knowledge_base.code_patterns.push({
          pattern: p,
          session_id: sessionId,
          timestamp: new Date().toISOString()
        });
      });
    }
    if (insights.issues) {
      session.issues_encountered = insights.issues;
      insights.issues.forEach(i => {
        memory.knowledge_base.gotchas.push({
          ...i,
          session_id: sessionId,
          timestamp: new Date().toISOString()
        });
      });
    }
    if (insights.artifacts) {
      memory.statistics.total_artifacts += insights.artifacts.length;
    }
  }
  
  memory.sessions[sessionIndex] = session;
  saveMemory(memory);
  
  // Update session file
  const sessionFile = path.join(SESSIONS_DIR, `${sessionId}.json`);
  fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2), 'utf8');
  
  console.log(JSON.stringify({ success: true, session_id: sessionId, status: 'completed' }));
}

/**
 * Search memory for relevant context
 */
function searchMemory(query) {
  const memory = loadMemory();
  const queryLower = query.toLowerCase();
  const results = {
    relevant_decisions: [],
    relevant_patterns: [],
    relevant_issues: [],
    relevant_sessions: []
  };
  
  // Search sessions
  for (const session of memory.sessions) {
    let relevance = 0;
    
    if (session.summary && session.summary.toLowerCase().includes(queryLower)) {
      relevance += 2;
    }
    
    // Search decisions
    for (const decision of session.decisions || []) {
      if (decision.decision && decision.decision.toLowerCase().includes(queryLower)) {
        results.relevant_decisions.push({
          ...decision,
          from_session: session.id,
          phase: session.phase
        });
        relevance++;
      }
    }
    
    // Search patterns
    for (const pattern of session.patterns_learned || []) {
      const patternText = typeof pattern === 'string' ? pattern : pattern.pattern;
      if (patternText && patternText.toLowerCase().includes(queryLower)) {
        results.relevant_patterns.push({
          pattern: patternText,
          from_session: session.id
        });
        relevance++;
      }
    }
    
    // Search issues
    for (const issue of session.issues_encountered || []) {
      if ((issue.issue && issue.issue.toLowerCase().includes(queryLower)) ||
          (issue.solution && issue.solution.toLowerCase().includes(queryLower))) {
        results.relevant_issues.push({
          ...issue,
          from_session: session.id
        });
        relevance++;
      }
    }
    
    if (relevance > 0) {
      results.relevant_sessions.push({
        id: session.id,
        phase: session.phase,
        summary: session.summary,
        relevance: relevance
      });
    }
  }
  
  // Sort sessions by relevance
  results.relevant_sessions.sort((a, b) => b.relevance - a.relevance);
  
  console.log(JSON.stringify(results, null, 2));
  return results;
}

/**
 * Get context for a specific task
 */
function getContextForTask(taskDescription) {
  const memory = loadMemory();
  const context = {
    project: memory.project,
    current_phase: memory.current_context.active_phase,
    active_feature: memory.current_context.active_feature,
    recent_sessions: memory.sessions.slice(-5).map(s => ({
      id: s.id,
      phase: s.phase,
      summary: s.summary,
      patterns: s.patterns_learned
    })),
    relevant_knowledge: searchMemory(taskDescription)
  };
  
  console.log(JSON.stringify(context, null, 2));
  return context;
}

/**
 * Add insight to knowledge base
 */
function addInsight(category, insight) {
  const memory = loadMemory();
  
  const validCategories = ['architecture_decisions', 'code_patterns', 'gotchas', 'best_practices', 'lessons_learned'];
  if (!validCategories.includes(category)) {
    console.error(JSON.stringify({ error: 'Invalid category', valid: validCategories }));
    return;
  }
  
  memory.knowledge_base[category].push({
    ...insight,
    timestamp: new Date().toISOString()
  });
  
  saveMemory(memory);
  console.log(JSON.stringify({ success: true, category, insight }));
}

/**
 * Update project info
 */
function updateProject(projectInfo) {
  const memory = loadMemory();
  memory.project = { ...memory.project, ...projectInfo };
  if (!memory.project.initialized) {
    memory.project.initialized = new Date().toISOString();
  }
  saveMemory(memory);
  console.log(JSON.stringify({ success: true, project: memory.project }));
}

/**
 * Set current context
 */
function setContext(contextData) {
  const memory = loadMemory();
  memory.current_context = { ...memory.current_context, ...contextData };
  saveMemory(memory);
  console.log(JSON.stringify({ success: true, context: memory.current_context }));
}

/**
 * Get statistics
 */
function getStats() {
  const memory = loadMemory();
  const stats = {
    ...memory.statistics,
    knowledge_base_size: {
      architecture_decisions: memory.knowledge_base.architecture_decisions.length,
      code_patterns: memory.knowledge_base.code_patterns.length,
      gotchas: memory.knowledge_base.gotchas.length,
      best_practices: memory.knowledge_base.best_practices.length,
      lessons_learned: memory.knowledge_base.lessons_learned.length
    },
    sessions_count: memory.sessions.length,
    active_sessions: memory.sessions.filter(s => s.status === 'active').length,
    project: memory.project.name || 'Not configured'
  };
  console.log(JSON.stringify(stats, null, 2));
  return stats;
}

/**
 * Export memory for backup
 */
function exportMemory(outputPath) {
  const memory = loadMemory();
  const exportData = {
    exported_at: new Date().toISOString(),
    ...memory
  };
  
  const outFile = outputPath || `memory-export-${Date.now()}.json`;
  fs.writeFileSync(outFile, JSON.stringify(exportData, null, 2), 'utf8');
  console.log(JSON.stringify({ success: true, file: outFile }));
}

// CLI Handler
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'start':
    const startData = {};
    for (let i = 1; i < args.length; i += 2) {
      if (args[i] === '--phase') startData.phase = args[i + 1];
      if (args[i] === '--summary') startData.summary = args[i + 1];
    }
    startSession(startData);
    break;
    
  case 'end':
    let endSessionId = '';
    let endInsights = {};
    for (let i = 1; i < args.length; i += 2) {
      if (args[i] === '--session') endSessionId = args[i + 1];
      if (args[i] === '--insights') endInsights = JSON.parse(args[i + 1]);
    }
    endSession(endSessionId, endInsights);
    break;
    
  case 'search':
    const searchQuery = args.slice(1).join(' ');
    searchMemory(searchQuery);
    break;
    
  case 'context':
    const taskDesc = args.slice(1).join(' ');
    getContextForTask(taskDesc);
    break;
    
  case 'insight':
    const category = args[1];
    const insightData = JSON.parse(args[2] || '{}');
    addInsight(category, insightData);
    break;
    
  case 'project':
    const projectData = JSON.parse(args[1] || '{}');
    updateProject(projectData);
    break;
    
  case 'set-context':
    const ctxData = JSON.parse(args[1] || '{}');
    setContext(ctxData);
    break;
    
  case 'stats':
    getStats();
    break;
    
  case 'export':
    exportMemory(args[1]);
    break;
    
  default:
    console.log(`
OCTALUME Memory Manager v2.0

Usage:
  node memory-manager.js <command> [options]

Commands:
  start --phase <phase> --summary <text>    Start new session
  end --session <id> --insights <json>      End session with insights
  search <query>                            Search memory
  context <task description>                Get context for task
  insight <category> <json>                 Add knowledge insight
  project <json>                            Update project info
  set-context <json>                        Set current context
  stats                                     Show statistics
  export [path]                             Export memory backup

Categories for insights:
  architecture_decisions, code_patterns, gotchas, best_practices, lessons_learned
`);
}
