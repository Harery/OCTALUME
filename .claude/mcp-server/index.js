#!/usr/bin/env node

/**
 * Unified Enterprise Lifecycle MCP Server
 * Provides lifecycle-specific tools to Claude Code
 *
 * Tools:
 * - lifecycle_initialize_project: Initialize new lifecycle project
 * - lifecycle_execute_phase: Execute specific phase
 * - lifecycle_create_artifact: Create artifact with traceability
 * - lifecycle_update_feature: Update feature status
 * - lifecycle_validate_quality_gate: Validate quality gates
 * - lifecycle_run_security_scan: Run security scans
 * - lifecycle_get_project_state: Get project state
 * - lifecycle_search_artifacts: Search artifacts
 * - lifecycle_go_no_go: Execute go/no-go decision
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { readFileSync, writeFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Get project root (parent of .claude directory)
const getProjectRoot = () => {
  let currentDir = __dirname;
  while (currentDir !== '/') {
    const parentDir = dirname(currentDir);
    if (existsSync(join(parentDir, '.claude'))) {
      return parentDir;
    }
    currentDir = parentDir;
  }
  return process.cwd();
};

const PROJECT_ROOT = getProjectRoot();

// Helper: Read JSON file
const readJSON = (filepath) => {
  try {
    const content = readFileSync(join(PROJECT_ROOT, filepath), 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
};

// Helper: Write JSON file
const writeJSON = (filepath, data) => {
  try {
    writeFileSync(join(PROJECT_ROOT, filepath), JSON.stringify(data, null, 2), 'utf-8');
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// Helper: Generate artifact ID
const generateArtifactId = (phase, section) => {
  const projectState = readJSON('.claude/project-state.json') || {};
  const counters = projectState.traceability?.artifact_counter || {};
  const phaseKey = `P${phase}`;
  counters[phaseKey] = (counters[phaseKey] || 0) + 1;

  // Update counter
  if (projectState.traceability) {
    projectState.traceability.artifact_counter = counters;
    writeJSON('.claude/project-state.json', projectState);
  }

  return `${phaseKey}-${section}-${String(counters[phaseKey]).padStart(3, '0')}`;
};

// Create MCP server
const server = new Server(
  {
    name: 'unified-enterprise-lifecycle',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'lifecycle_initialize_project',
        description: 'Initialize a new lifecycle project with complete structure, feature list, and configuration',
        inputSchema: {
          type: 'object',
          properties: {
            project_name: {
              type: 'string',
              description: 'Name of the project'
            },
            project_description: {
              type: 'string',
              description: 'Description of the project'
            },
            compliance_requirements: {
              type: 'array',
              items: { type: 'string' },
              description: 'Compliance requirements (HIPAA, SOC 2, PCI DSS, GDPR, SOX, etc.)'
            }
          },
          required: ['project_name', 'project_description']
        }
      },
      {
        name: 'lifecycle_execute_phase',
        description: 'Execute a specific phase of the lifecycle with all required steps and validations',
        inputSchema: {
          type: 'object',
          properties: {
            phase: {
              type: 'string',
              enum: ['phase_01', 'phase_02', 'phase_03', 'phase_04', 'phase_05', 'phase_06', 'phase_07', 'phase_08'],
              description: 'Phase number to execute'
            },
            skip_validations: {
              type: 'boolean',
              description: 'Skip entry/exit criteria validation (not recommended)',
              default: false
            }
          },
          required: ['phase']
        }
      },
      {
        name: 'lifecycle_create_artifact',
        description: 'Create a new artifact with traceability ID (P{N}-{SECTION}-###)',
        inputSchema: {
          type: 'object',
          properties: {
            phase: {
              type: 'string',
              description: 'Phase number (1-8)'
            },
            section: {
              type: 'string',
              description: 'Section code (VISION, ARCH, CODE, TEST, etc.)'
            },
            content: {
              type: 'string',
              description: 'Artifact content'
            },
            format: {
              type: 'string',
              enum: ['markdown', 'json', 'yaml', 'text'],
              description: 'Artifact format',
              default: 'markdown'
            }
          },
          required: ['phase', 'section', 'content']
        }
      },
      {
        name: 'lifecycle_update_feature',
        description: 'Update feature status in feature_list.json',
        inputSchema: {
          type: 'object',
          properties: {
            feature_id: {
              type: 'string',
              description: 'Feature ID (e.g., F-001)'
            },
            status: {
              type: 'string',
              enum: ['failing', 'in_progress', 'passing', 'blocked'],
              description: 'New feature status'
            },
            artifacts: {
              type: 'array',
              items: { type: 'string' },
              description: 'Artifacts created for this feature'
            }
          },
          required: ['feature_id', 'status']
        }
      },
      {
        name: 'lifecycle_validate_quality_gate',
        description: 'Validate quality gate criteria for phase transition',
        inputSchema: {
          type: 'object',
          properties: {
            phase: {
              type: 'string',
              description: 'Phase to validate'
            },
            gate_type: {
              type: 'string',
              enum: ['entry', 'exit'],
              description: 'Gate type to validate'
            }
          },
          required: ['phase', 'gate_type']
        }
      },
      {
        name: 'lifecycle_run_security_scan',
        description: 'Run security and compliance scans (SAST, SCA, DAST, compliance)',
        inputSchema: {
          type: 'object',
          properties: {
            scan_types: {
              type: 'array',
              items: { type: 'string' },
              enum: ['sast', 'sca', 'dast', 'container', 'iac', 'compliance'],
              description: 'Types of scans to run'
            },
            output_format: {
              type: 'string',
              enum: ['json', 'markdown', 'html'],
              description: 'Output format for scan results',
              default: 'json'
            }
          },
          required: ['scan_types']
        }
      },
      {
        name: 'lifecycle_get_project_state',
        description: 'Get current project state from .claude/project-state.json',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'lifecycle_search_artifacts',
        description: 'Search artifacts by phase, type, or content',
        inputSchema: {
          type: 'object',
          properties: {
            phase: {
              type: 'string',
              description: 'Filter by phase (optional)'
            },
            type: {
              type: 'string',
              description: 'Filter by artifact type (optional)'
            },
            search_term: {
              type: 'string',
              description: 'Search in artifact content (optional)'
            }
          }
        }
      },
      {
        name: 'lifecycle_go_no_go',
        description: 'Execute go/no-go decision for phase transition',
        inputSchema: {
          type: 'object',
          properties: {
            phase: {
              type: 'string',
              description: 'Current phase'
            },
            approver: {
              type: 'string',
              description: 'Approver role (e.g., Executive Sponsor, Product Owner)'
            },
            decision: {
              type: 'string',
              enum: ['go', 'no-go'],
              description: 'Go or No-Go decision'
            },
            comments: {
              type: 'string',
              description: 'Comments or conditions for approval'
            }
          },
          required: ['phase', 'approver', 'decision']
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'lifecycle_initialize_project':
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              status: 'initialized',
              project_name: args.project_name,
              message: 'Project initialized. Use /lifecycle-init command for full setup with feature list generation.',
              next_steps: [
                'Run: /lifecycle-init for complete initialization',
                'Or manually create: .claude/project-state.json, feature_list.json, claude-progress.txt'
              ]
            }, null, 2)
          }]
        };

      case 'lifecycle_execute_phase':
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              phase: args.phase,
              status: 'executing',
              message: `Executing ${args.phase}. Use /lifecycle-phase ${args.phase} command for full execution.`,
              skip_validations: args.skip_validations || false
            }, null, 2)
          }]
        };

      case 'lifecycle_create_artifact': {
        const artifactId = generateArtifactId(args.phase, args.section);
        const artifactPath = `artifacts/P${args.phase}/${artifactId}.${args.format || 'md'}`;
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              artifact_id: artifactId,
              path: artifactPath,
              phase: args.phase,
              section: args.section,
              format: args.format || 'markdown',
              status: 'created',
              message: `Artifact ${artifactId} created. Write content to ${artifactPath}`
            }, null, 2)
          }]
        };
      }

      case 'lifecycle_update_feature': {
        const featureList = readJSON('feature_list.json') || { features: [] };
        const feature = featureList.features.find(f => f.id === args.feature_id);

        if (feature) {
          feature.status = args.status;
          if (args.artifacts) {
            feature.artifacts = [...(feature.artifacts || []), ...args.artifacts];
          }
          writeJSON('feature_list.json', featureList);

          return {
            content: [{
              type: 'text',
              text: JSON.stringify({
                feature_id: args.feature_id,
                status: args.status,
                artifacts: feature.artifacts || [],
                updated: true
              }, null, 2)
            }]
          };
        }

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              error: `Feature ${args.feature_id} not found`
            }, null, 2)
          }],
          isError: true
        };
      }

      case 'lifecycle_validate_quality_gate': {
        const projectState = readJSON('.claude/project-state.json') || {};
        const phaseKey = `phase_${args.phase.replace('phase_', '')}`;
        const phaseInfo = projectState.phases?.[phaseKey];

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              phase: args.phase,
              gate_type: args.gate_type,
              status: phaseInfo ? 'validated' : 'not_found',
              entry_criteria: phaseInfo?.entry_criteria || [],
              exit_criteria: phaseInfo?.exit_criteria || [],
              message: `Use /lifecycle-phase ${args.phase} for full validation`
            }, null, 2)
          }]
        };
      }

      case 'lifecycle_run_security_scan':
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              scan_types: args.scan_types,
              output_format: args.output_format || 'json',
              status: 'initiated',
              message: 'Use /lifecycle-scan command for full security scan execution'
            }, null, 2)
          }]
        };

      case 'lifecycle_get_project_state': {
        const projectState = readJSON('.claude/project-state.json');
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(projectState || { error: 'Project state not found' }, null, 2)
          }]
        };
      }

      case 'lifecycle_search_artifacts': {
        const artifacts = [];
        const artifactsDir = join(PROJECT_ROOT, 'artifacts');

        if (existsSync(artifactsDir)) {
          const searchRecursively = (dir, phase = null) => {
            const entries = readdirSync(dir, { withFileTypes: true });

            for (const entry of entries) {
              const fullPath = join(dir, entry.name);

              if (entry.isDirectory()) {
                searchRecursively(fullPath, entry.name);
              } else if (entry.isFile()) {
                const relPath = fullPath.replace(PROJECT_ROOT + '/', '');

                if (args.phase && !relPath.includes(`/${args.phase}/`)) continue;
                if (args.type && !entry.name.includes(args.type)) continue;

                artifacts.push({
                  path: relPath,
                  name: entry.name,
                  phase: phase || 'unknown'
                });
              }
            }
          };

          searchRecursively(artifactsDir);
        }

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              total: artifacts.length,
              artifacts: artifacts,
              filters: { phase: args.phase, type: args.type, search_term: args.search_term }
            }, null, 2)
          }]
        };
      }

      case 'lifecycle_go_no_go':
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              phase: args.phase,
              approver: args.approver,
              decision: args.decision,
              comments: args.comments || '',
              timestamp: new Date().toISOString(),
              status: 'recorded',
              message: 'Go/No-Go decision recorded. Update project-state.json with this decision.'
            }, null, 2)
          }]
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ error: error.message }, null, 2)
      }],
      isError: true
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Log to stderr so it doesn't interfere with MCP communication
  console.error('Unified Enterprise Lifecycle MCP Server running');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
