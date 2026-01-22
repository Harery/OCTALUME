#!/usr/bin/env node

/**
 * Task Validators
 * Implements validation functions for all task types across phases
 *
 * This module provides the 26 validation functions referenced in task-skill-binder.js
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

// ============================================================================
// PHASE 1: VISION & STRATEGY VALIDATORS
// ============================================================================

/**
 * Validate Business Case Document
 * @param {object} artifact - The business case artifact
 * @param {object} projectState - Current project state
 * @returns {object} Validation result with passed boolean and issues array
 */
export function validateBusinessCase(artifact, projectState) {
  const issues = [];
  
  // Required sections
  const requiredSections = [
    'executive_summary',
    'problem_statement',
    'proposed_solution',
    'market_analysis',
    'financial_projections',
    'roi_analysis',
    'risk_assessment',
    'success_metrics'
  ];
  
  for (const section of requiredSections) {
    if (!artifact.content?.[section] && !artifact[section]) {
      issues.push({
        severity: 'error',
        field: section,
        message: `Missing required section: ${section.replace(/_/g, ' ')}`
      });
    }
  }
  
  // Financial projections should have numbers
  if (artifact.financial_projections) {
    if (typeof artifact.financial_projections.total_cost !== 'number') {
      issues.push({
        severity: 'error',
        field: 'financial_projections.total_cost',
        message: 'Total cost must be a number'
      });
    }
    if (typeof artifact.financial_projections.expected_roi !== 'number') {
      issues.push({
        severity: 'warning',
        field: 'financial_projections.expected_roi',
        message: 'Expected ROI should be specified'
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateBusinessCase',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Product Requirements Document (PRD)
 */
export function validatePRD(artifact, projectState) {
  const issues = [];
  
  const requiredSections = [
    'product_vision',
    'target_users',
    'user_personas',
    'key_features',
    'success_metrics',
    'mvp_scope',
    'constraints',
    'assumptions'
  ];
  
  for (const section of requiredSections) {
    if (!artifact.content?.[section] && !artifact[section]) {
      issues.push({
        severity: 'error',
        field: section,
        message: `Missing required section: ${section.replace(/_/g, ' ')}`
      });
    }
  }
  
  // MVP scope should have features
  if (artifact.mvp_scope && (!artifact.mvp_scope.features || artifact.mvp_scope.features.length === 0)) {
    issues.push({
      severity: 'error',
      field: 'mvp_scope.features',
      message: 'MVP scope must include at least one feature'
    });
  }
  
  // User personas should exist
  if (artifact.user_personas && artifact.user_personas.length === 0) {
    issues.push({
      severity: 'error',
      field: 'user_personas',
      message: 'At least one user persona must be defined'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validatePRD',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Market Analysis
 */
export function validateMarketAnalysis(artifact, projectState) {
  const issues = [];
  
  const requiredSections = [
    'market_size',
    'target_market',
    'competitive_landscape',
    'market_trends',
    'opportunities',
    'threats'
  ];
  
  for (const section of requiredSections) {
    if (!artifact.content?.[section] && !artifact[section]) {
      issues.push({
        severity: 'error',
        field: section,
        message: `Missing required section: ${section.replace(/_/g, ' ')}`
      });
    }
  }
  
  // Should have at least one competitor analyzed
  if (artifact.competitive_landscape && 
      (!artifact.competitive_landscape.competitors || 
       artifact.competitive_landscape.competitors.length === 0)) {
    issues.push({
      severity: 'warning',
      field: 'competitive_landscape.competitors',
      message: 'No competitors identified - verify this is accurate'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateMarketAnalysis',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Stakeholder Alignment
 */
export function validateStakeholderAlignment(artifact, projectState) {
  const issues = [];
  
  // Must have stakeholders defined
  if (!artifact.stakeholders || artifact.stakeholders.length === 0) {
    issues.push({
      severity: 'error',
      field: 'stakeholders',
      message: 'No stakeholders defined'
    });
  }
  
  // Must have executive sponsor
  const hasExecutiveSponsor = artifact.stakeholders?.some(s => 
    s.role === 'Executive Sponsor' || s.type === 'executive_sponsor'
  );
  if (!hasExecutiveSponsor) {
    issues.push({
      severity: 'error',
      field: 'stakeholders',
      message: 'Executive Sponsor not identified'
    });
  }
  
  // All stakeholders should have alignment status
  for (const stakeholder of (artifact.stakeholders || [])) {
    if (!stakeholder.alignment_status) {
      issues.push({
        severity: 'warning',
        field: `stakeholders.${stakeholder.name || stakeholder.role}`,
        message: `Alignment status not recorded for ${stakeholder.name || stakeholder.role}`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateStakeholderAlignment',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 2: REQUIREMENTS & SCOPE VALIDATORS
// ============================================================================

/**
 * Validate Functional Requirements
 */
export function validateFunctionalRequirements(artifact, projectState) {
  const issues = [];
  
  if (!artifact.requirements || artifact.requirements.length === 0) {
    issues.push({
      severity: 'error',
      field: 'requirements',
      message: 'No functional requirements defined'
    });
    return { passed: false, issues, validator: 'validateFunctionalRequirements', validated_at: new Date().toISOString() };
  }
  
  for (const req of artifact.requirements) {
    // Each requirement must have ID
    if (!req.id) {
      issues.push({
        severity: 'error',
        field: 'requirements',
        message: 'Requirement missing ID'
      });
    }
    
    // Each requirement must have description
    if (!req.description && !req.statement) {
      issues.push({
        severity: 'error',
        field: `requirements.${req.id}`,
        message: `Requirement ${req.id} missing description`
      });
    }
    
    // Each requirement should have priority
    if (!req.priority) {
      issues.push({
        severity: 'warning',
        field: `requirements.${req.id}`,
        message: `Requirement ${req.id} missing priority`
      });
    }
    
    // Each requirement should have acceptance criteria
    if (!req.acceptance_criteria || req.acceptance_criteria.length === 0) {
      issues.push({
        severity: 'warning',
        field: `requirements.${req.id}`,
        message: `Requirement ${req.id} missing acceptance criteria`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateFunctionalRequirements',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Non-Functional Requirements (NFRs)
 */
export function validateNFRs(artifact, projectState) {
  const issues = [];
  
  const nfrCategories = [
    'performance',
    'scalability',
    'availability',
    'security',
    'maintainability',
    'usability'
  ];
  
  if (!artifact.requirements && !artifact.nfrs) {
    issues.push({
      severity: 'error',
      field: 'requirements',
      message: 'No non-functional requirements defined'
    });
    return { passed: false, issues, validator: 'validateNFRs', validated_at: new Date().toISOString() };
  }
  
  const requirements = artifact.requirements || artifact.nfrs || [];
  
  // Check for at least security and performance NFRs
  const hasPerformance = requirements.some(r => r.category === 'performance' || r.type === 'performance');
  const hasSecurity = requirements.some(r => r.category === 'security' || r.type === 'security');
  
  if (!hasPerformance) {
    issues.push({
      severity: 'error',
      field: 'requirements',
      message: 'No performance requirements defined'
    });
  }
  
  if (!hasSecurity) {
    issues.push({
      severity: 'error',
      field: 'requirements',
      message: 'No security requirements defined'
    });
  }
  
  // Each NFR should be measurable
  for (const nfr of requirements) {
    if (!nfr.metric && !nfr.measurable_target) {
      issues.push({
        severity: 'warning',
        field: `requirements.${nfr.id}`,
        message: `NFR ${nfr.id} should have measurable target`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateNFRs',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Traceability Matrix
 */
export function validateTraceabilityMatrix(artifact, projectState) {
  const issues = [];
  
  if (!artifact.matrix && !artifact.mappings) {
    issues.push({
      severity: 'error',
      field: 'matrix',
      message: 'No traceability matrix defined'
    });
    return { passed: false, issues, validator: 'validateTraceabilityMatrix', validated_at: new Date().toISOString() };
  }
  
  const mappings = artifact.matrix || artifact.mappings || [];
  
  // Each requirement should trace to at least one test
  for (const mapping of mappings) {
    if (!mapping.requirement_id) {
      issues.push({
        severity: 'error',
        field: 'matrix',
        message: 'Mapping missing requirement_id'
      });
    }
    
    if (!mapping.test_cases || mapping.test_cases.length === 0) {
      issues.push({
        severity: 'warning',
        field: `matrix.${mapping.requirement_id}`,
        message: `Requirement ${mapping.requirement_id} has no test cases mapped`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateTraceabilityMatrix',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 3: ARCHITECTURE & DESIGN VALIDATORS
// ============================================================================

/**
 * Validate System Architecture
 */
export function validateSystemArchitecture(artifact, projectState) {
  const issues = [];
  
  const requiredSections = [
    'architecture_overview',
    'components',
    'interfaces',
    'data_flow',
    'deployment_topology'
  ];
  
  for (const section of requiredSections) {
    if (!artifact.content?.[section] && !artifact[section]) {
      issues.push({
        severity: 'error',
        field: section,
        message: `Missing required section: ${section.replace(/_/g, ' ')}`
      });
    }
  }
  
  // Must have at least one component
  if (artifact.components && artifact.components.length === 0) {
    issues.push({
      severity: 'error',
      field: 'components',
      message: 'No components defined'
    });
  }
  
  // Components should have interfaces defined
  for (const component of (artifact.components || [])) {
    if (!component.interfaces || component.interfaces.length === 0) {
      issues.push({
        severity: 'warning',
        field: `components.${component.name}`,
        message: `Component ${component.name} has no interfaces defined`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateSystemArchitecture',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Security Architecture
 */
export function validateSecurityArchitecture(artifact, projectState) {
  const issues = [];
  
  const requiredSections = [
    'authentication',
    'authorization',
    'encryption',
    'network_security',
    'data_protection'
  ];
  
  for (const section of requiredSections) {
    if (!artifact.content?.[section] && !artifact[section]) {
      issues.push({
        severity: 'error',
        field: section,
        message: `Missing required security section: ${section.replace(/_/g, ' ')}`
      });
    }
  }
  
  // Must define encryption at rest and in transit
  if (artifact.encryption) {
    if (!artifact.encryption.at_rest) {
      issues.push({
        severity: 'error',
        field: 'encryption.at_rest',
        message: 'Encryption at rest not defined'
      });
    }
    if (!artifact.encryption.in_transit) {
      issues.push({
        severity: 'error',
        field: 'encryption.in_transit',
        message: 'Encryption in transit not defined'
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateSecurityArchitecture',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Threat Model
 */
export function validateThreatModel(artifact, projectState) {
  const issues = [];
  
  if (!artifact.threats || artifact.threats.length === 0) {
    issues.push({
      severity: 'error',
      field: 'threats',
      message: 'No threats identified'
    });
    return { passed: false, issues, validator: 'validateThreatModel', validated_at: new Date().toISOString() };
  }
  
  // Each threat should have mitigation
  for (const threat of artifact.threats) {
    if (!threat.id) {
      issues.push({
        severity: 'error',
        field: 'threats',
        message: 'Threat missing ID'
      });
    }
    
    if (!threat.mitigation && !threat.mitigations) {
      issues.push({
        severity: 'error',
        field: `threats.${threat.id}`,
        message: `Threat ${threat.id} has no mitigation strategy`
      });
    }
    
    if (!threat.severity && !threat.risk_level) {
      issues.push({
        severity: 'warning',
        field: `threats.${threat.id}`,
        message: `Threat ${threat.id} has no severity rating`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateThreatModel',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 4: DEVELOPMENT PLANNING VALIDATORS
// ============================================================================

/**
 * Validate Work Breakdown Structure (WBS)
 */
export function validateWBS(artifact, projectState) {
  const issues = [];
  
  if (!artifact.tasks && !artifact.work_packages) {
    issues.push({
      severity: 'error',
      field: 'tasks',
      message: 'No work breakdown structure defined'
    });
    return { passed: false, issues, validator: 'validateWBS', validated_at: new Date().toISOString() };
  }
  
  const tasks = artifact.tasks || artifact.work_packages || [];
  
  for (const task of tasks) {
    // Each task must have ID
    if (!task.id) {
      issues.push({
        severity: 'error',
        field: 'tasks',
        message: 'Task missing ID'
      });
    }
    
    // Each task must have estimate
    if (!task.estimate && !task.effort) {
      issues.push({
        severity: 'error',
        field: `tasks.${task.id}`,
        message: `Task ${task.id} missing effort estimate`
      });
    }
    
    // Each task should have assignee or skill required
    if (!task.assignee && !task.required_skill) {
      issues.push({
        severity: 'warning',
        field: `tasks.${task.id}`,
        message: `Task ${task.id} has no assignee or required skill`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateWBS',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Resource Plan
 */
export function validateResourcePlan(artifact, projectState) {
  const issues = [];
  
  if (!artifact.resources || artifact.resources.length === 0) {
    issues.push({
      severity: 'error',
      field: 'resources',
      message: 'No resources defined'
    });
    return { passed: false, issues, validator: 'validateResourcePlan', validated_at: new Date().toISOString() };
  }
  
  // Should have at least a developer
  const hasDeveloper = artifact.resources.some(r => 
    r.role?.toLowerCase().includes('developer') || 
    r.type === 'developer'
  );
  if (!hasDeveloper) {
    issues.push({
      severity: 'error',
      field: 'resources',
      message: 'No developer resources defined'
    });
  }
  
  // Each resource should have allocation
  for (const resource of artifact.resources) {
    if (!resource.allocation && !resource.availability) {
      issues.push({
        severity: 'warning',
        field: `resources.${resource.name || resource.role}`,
        message: `Resource ${resource.name || resource.role} has no allocation defined`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateResourcePlan',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Sprint Plan
 */
export function validateSprintPlan(artifact, projectState) {
  const issues = [];
  
  if (!artifact.sprints || artifact.sprints.length === 0) {
    issues.push({
      severity: 'error',
      field: 'sprints',
      message: 'No sprints defined'
    });
    return { passed: false, issues, validator: 'validateSprintPlan', validated_at: new Date().toISOString() };
  }
  
  for (const sprint of artifact.sprints) {
    // Each sprint must have number and goal
    if (!sprint.number && !sprint.id) {
      issues.push({
        severity: 'error',
        field: 'sprints',
        message: 'Sprint missing number/ID'
      });
    }
    
    if (!sprint.goal && !sprint.objective) {
      issues.push({
        severity: 'warning',
        field: `sprints.${sprint.number || sprint.id}`,
        message: `Sprint ${sprint.number || sprint.id} has no goal defined`
      });
    }
    
    // Should have start and end dates
    if (!sprint.start_date || !sprint.end_date) {
      issues.push({
        severity: 'warning',
        field: `sprints.${sprint.number || sprint.id}`,
        message: `Sprint ${sprint.number || sprint.id} missing dates`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateSprintPlan',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 5: DEVELOPMENT EXECUTION VALIDATORS
// ============================================================================

/**
 * Validate Feature Code
 */
export function validateFeatureCode(artifact, projectState) {
  const issues = [];
  
  // Must reference a feature ID
  if (!artifact.feature_id) {
    issues.push({
      severity: 'error',
      field: 'feature_id',
      message: 'No feature ID specified'
    });
  }
  
  // Must have files changed
  if (!artifact.files_changed || artifact.files_changed.length === 0) {
    issues.push({
      severity: 'error',
      field: 'files_changed',
      message: 'No files changed recorded'
    });
  }
  
  // Should have commit reference
  if (!artifact.commit_sha && !artifact.commit) {
    issues.push({
      severity: 'warning',
      field: 'commit_sha',
      message: 'No commit reference'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateFeatureCode',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Unit Tests
 */
export function validateUnitTests(artifact, projectState) {
  const issues = [];
  
  if (!artifact.test_results && !artifact.tests) {
    issues.push({
      severity: 'error',
      field: 'test_results',
      message: 'No test results provided'
    });
    return { passed: false, issues, validator: 'validateUnitTests', validated_at: new Date().toISOString() };
  }
  
  const results = artifact.test_results || artifact.tests;
  
  // Check for failures
  if (results.failed > 0) {
    issues.push({
      severity: 'error',
      field: 'test_results.failed',
      message: `${results.failed} unit test(s) failed`
    });
  }
  
  // Should have reasonable coverage
  if (results.coverage && results.coverage < 60) {
    issues.push({
      severity: 'warning',
      field: 'test_results.coverage',
      message: `Test coverage ${results.coverage}% is below 60% threshold`
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateUnitTests',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Code Review
 */
export function validateCodeReview(artifact, projectState) {
  const issues = [];
  
  // Must have reviewer
  if (!artifact.reviewer && !artifact.reviewed_by) {
    issues.push({
      severity: 'error',
      field: 'reviewer',
      message: 'No reviewer specified'
    });
  }
  
  // Must have approval status
  if (!artifact.status && !artifact.approved) {
    issues.push({
      severity: 'error',
      field: 'status',
      message: 'Review status not specified'
    });
  }
  
  // If not approved, should have comments
  if (artifact.status === 'changes_requested' || artifact.approved === false) {
    if (!artifact.comments || artifact.comments.length === 0) {
      issues.push({
        severity: 'warning',
        field: 'comments',
        message: 'Changes requested but no comments provided'
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateCodeReview',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 6: QUALITY & SECURITY VALIDATORS
// ============================================================================

/**
 * Validate Test Results (Unit and Integration)
 */
export function validateTestResults(artifact, projectState) {
  const issues = [];
  
  if (!artifact.results && !artifact.test_results) {
    issues.push({
      severity: 'error',
      field: 'results',
      message: 'No test results provided'
    });
    return { passed: false, issues, validator: 'validateTestResults', validated_at: new Date().toISOString() };
  }
  
  const results = artifact.results || artifact.test_results;
  
  // All tests must pass
  if (results.failed > 0) {
    issues.push({
      severity: 'error',
      field: 'results.failed',
      message: `${results.failed} test(s) failed`
    });
  }
  
  // Should have reasonable test count
  if (results.total < 10) {
    issues.push({
      severity: 'warning',
      field: 'results.total',
      message: 'Very few tests - consider adding more coverage'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateTestResults',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Security Scan Results
 */
export function validateSecurityScan(artifact, projectState) {
  const issues = [];
  
  if (!artifact.findings && !artifact.vulnerabilities) {
    issues.push({
      severity: 'error',
      field: 'findings',
      message: 'No security scan findings provided'
    });
    return { passed: false, issues, validator: 'validateSecurityScan', validated_at: new Date().toISOString() };
  }
  
  const findings = artifact.findings || artifact.vulnerabilities || [];
  
  // Critical vulnerabilities must be zero
  const criticals = findings.filter(f => 
    f.severity === 'critical' || f.severity === 'CRITICAL'
  );
  if (criticals.length > 0) {
    issues.push({
      severity: 'error',
      field: 'findings',
      message: `${criticals.length} critical vulnerability(s) found - must be resolved`
    });
  }
  
  // High vulnerabilities should be addressed
  const highs = findings.filter(f => 
    f.severity === 'high' || f.severity === 'HIGH'
  );
  if (highs.length > 0) {
    issues.push({
      severity: 'warning',
      field: 'findings',
      message: `${highs.length} high severity vulnerability(s) found`
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateSecurityScan',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Performance Test Results
 */
export function validatePerformanceTest(artifact, projectState) {
  const issues = [];
  
  if (!artifact.results && !artifact.metrics) {
    issues.push({
      severity: 'error',
      field: 'results',
      message: 'No performance test results provided'
    });
    return { passed: false, issues, validator: 'validatePerformanceTest', validated_at: new Date().toISOString() };
  }
  
  const results = artifact.results || artifact.metrics;
  
  // Check response time threshold (default 2 seconds)
  if (results.avg_response_time_ms && results.avg_response_time_ms > 2000) {
    issues.push({
      severity: 'warning',
      field: 'results.avg_response_time_ms',
      message: `Average response time ${results.avg_response_time_ms}ms exceeds 2000ms threshold`
    });
  }
  
  // Check error rate (should be < 1%)
  if (results.error_rate && results.error_rate > 0.01) {
    issues.push({
      severity: 'error',
      field: 'results.error_rate',
      message: `Error rate ${(results.error_rate * 100).toFixed(2)}% exceeds 1% threshold`
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validatePerformanceTest',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate UAT Signoff
 */
export function validateUATSignoff(artifact, projectState) {
  const issues = [];
  
  // Must have signoff from Product Owner or delegate
  if (!artifact.signed_off_by && !artifact.approver) {
    issues.push({
      severity: 'error',
      field: 'signed_off_by',
      message: 'No UAT signoff recorded'
    });
  }
  
  // Must have signoff date
  if (!artifact.signed_off_at && !artifact.approval_date) {
    issues.push({
      severity: 'error',
      field: 'signed_off_at',
      message: 'No UAT signoff date recorded'
    });
  }
  
  // Should document tested scenarios
  if (!artifact.tested_scenarios || artifact.tested_scenarios.length === 0) {
    issues.push({
      severity: 'warning',
      field: 'tested_scenarios',
      message: 'No tested scenarios documented'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateUATSignoff',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 7: DEPLOYMENT & RELEASE VALIDATORS
// ============================================================================

/**
 * Validate Deployment
 */
export function validateDeployment(artifact, projectState) {
  const issues = [];
  
  // Must have deployment target
  if (!artifact.environment && !artifact.target) {
    issues.push({
      severity: 'error',
      field: 'environment',
      message: 'No deployment target specified'
    });
  }
  
  // Must have version
  if (!artifact.version) {
    issues.push({
      severity: 'error',
      field: 'version',
      message: 'No version specified'
    });
  }
  
  // Must have deployment timestamp
  if (!artifact.deployed_at && !artifact.timestamp) {
    issues.push({
      severity: 'error',
      field: 'deployed_at',
      message: 'No deployment timestamp'
    });
  }
  
  // Should have deployment checklist completed
  if (artifact.checklist) {
    const incomplete = artifact.checklist.filter(item => !item.completed);
    if (incomplete.length > 0) {
      issues.push({
        severity: 'warning',
        field: 'checklist',
        message: `${incomplete.length} deployment checklist item(s) incomplete`
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateDeployment',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Smoke Tests
 */
export function validateSmokeTests(artifact, projectState) {
  const issues = [];
  
  if (!artifact.results && !artifact.tests) {
    issues.push({
      severity: 'error',
      field: 'results',
      message: 'No smoke test results provided'
    });
    return { passed: false, issues, validator: 'validateSmokeTests', validated_at: new Date().toISOString() };
  }
  
  const results = artifact.results || artifact.tests;
  
  // All smoke tests must pass
  if (results.failed > 0) {
    issues.push({
      severity: 'error',
      field: 'results.failed',
      message: `${results.failed} smoke test(s) failed - deployment may be unhealthy`
    });
  }
  
  // Should have core functionality tests
  if (results.total < 5) {
    issues.push({
      severity: 'warning',
      field: 'results.total',
      message: 'Very few smoke tests - ensure core functionality is covered'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateSmokeTests',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Rollback Plan
 */
export function validateRollbackPlan(artifact, projectState) {
  const issues = [];
  
  // Must have rollback steps
  if (!artifact.steps && !artifact.procedure) {
    issues.push({
      severity: 'error',
      field: 'steps',
      message: 'No rollback steps defined'
    });
  }
  
  // Must have rollback trigger criteria
  if (!artifact.triggers && !artifact.criteria) {
    issues.push({
      severity: 'error',
      field: 'triggers',
      message: 'No rollback trigger criteria defined'
    });
  }
  
  // Should have estimated rollback time
  if (!artifact.estimated_time) {
    issues.push({
      severity: 'warning',
      field: 'estimated_time',
      message: 'No estimated rollback time specified'
    });
  }
  
  // Should be tested
  if (!artifact.tested && artifact.tested !== true) {
    issues.push({
      severity: 'warning',
      field: 'tested',
      message: 'Rollback plan has not been tested'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateRollbackPlan',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// PHASE 8: OPERATIONS & MAINTENANCE VALIDATORS
// ============================================================================

/**
 * Validate Monitoring Setup
 */
export function validateMonitoring(artifact, projectState) {
  const issues = [];
  
  // Must have metrics defined
  if (!artifact.metrics || artifact.metrics.length === 0) {
    issues.push({
      severity: 'error',
      field: 'metrics',
      message: 'No monitoring metrics defined'
    });
  }
  
  // Must have alerts defined
  if (!artifact.alerts || artifact.alerts.length === 0) {
    issues.push({
      severity: 'error',
      field: 'alerts',
      message: 'No alerts defined'
    });
  }
  
  // Should have dashboard
  if (!artifact.dashboard_url && !artifact.dashboards) {
    issues.push({
      severity: 'warning',
      field: 'dashboard_url',
      message: 'No monitoring dashboard defined'
    });
  }
  
  // Core metrics should include availability and latency
  const metricNames = (artifact.metrics || []).map(m => m.name?.toLowerCase() || m.toLowerCase());
  if (!metricNames.some(n => n.includes('availability') || n.includes('uptime'))) {
    issues.push({
      severity: 'warning',
      field: 'metrics',
      message: 'No availability/uptime metric defined'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateMonitoring',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate Incident Procedures
 */
export function validateIncidentProcedures(artifact, projectState) {
  const issues = [];
  
  // Must have incident classification
  if (!artifact.classification && !artifact.severity_levels) {
    issues.push({
      severity: 'error',
      field: 'classification',
      message: 'No incident classification defined'
    });
  }
  
  // Must have escalation matrix
  if (!artifact.escalation_matrix && !artifact.escalation) {
    issues.push({
      severity: 'error',
      field: 'escalation_matrix',
      message: 'No escalation matrix defined'
    });
  }
  
  // Should have communication templates
  if (!artifact.communication_templates && !artifact.templates) {
    issues.push({
      severity: 'warning',
      field: 'communication_templates',
      message: 'No incident communication templates defined'
    });
  }
  
  // Should have post-incident review process
  if (!artifact.post_incident_review) {
    issues.push({
      severity: 'warning',
      field: 'post_incident_review',
      message: 'No post-incident review process defined'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateIncidentProcedures',
    validated_at: new Date().toISOString()
  };
}

/**
 * Validate On-Call Rotation
 */
export function validateOnCallRotation(artifact, projectState) {
  const issues = [];
  
  // Must have rotation schedule
  if (!artifact.schedule && !artifact.rotation) {
    issues.push({
      severity: 'error',
      field: 'schedule',
      message: 'No on-call schedule defined'
    });
  }
  
  // Must have at least 2 people in rotation
  const members = artifact.members || artifact.rotation?.members || [];
  if (members.length < 2) {
    issues.push({
      severity: 'error',
      field: 'members',
      message: 'On-call rotation must have at least 2 members'
    });
  }
  
  // Should have escalation policy
  if (!artifact.escalation_policy) {
    issues.push({
      severity: 'warning',
      field: 'escalation_policy',
      message: 'No escalation policy defined for on-call'
    });
  }
  
  // Should have coverage for all hours
  if (!artifact.coverage && artifact.coverage !== '24x7') {
    issues.push({
      severity: 'warning',
      field: 'coverage',
      message: 'On-call coverage hours not specified'
    });
  }
  
  return {
    passed: issues.filter(i => i.severity === 'error').length === 0,
    issues,
    validator: 'validateOnCallRotation',
    validated_at: new Date().toISOString()
  };
}

// ============================================================================
// EXPORTS
// ============================================================================

// Export all validators as named exports (already done above)
// Also export as a map for dynamic lookup
export const VALIDATORS = {
  // Phase 1
  validateBusinessCase,
  validatePRD,
  validateMarketAnalysis,
  validateStakeholderAlignment,
  
  // Phase 2
  validateFunctionalRequirements,
  validateNFRs,
  validateTraceabilityMatrix,
  
  // Phase 3
  validateSystemArchitecture,
  validateSecurityArchitecture,
  validateThreatModel,
  
  // Phase 4
  validateWBS,
  validateResourcePlan,
  validateSprintPlan,
  
  // Phase 5
  validateFeatureCode,
  validateUnitTests,
  validateCodeReview,
  
  // Phase 6
  validateTestResults,
  validateSecurityScan,
  validatePerformanceTest,
  validateUATSignoff,
  
  // Phase 7
  validateDeployment,
  validateSmokeTests,
  validateRollbackPlan,
  
  // Phase 8
  validateMonitoring,
  validateIncidentProcedures,
  validateOnCallRotation
};

/**
 * Run a validator by name
 * @param {string} validatorName - Name of the validator function
 * @param {object} artifact - The artifact to validate
 * @param {object} projectState - Current project state
 * @returns {object} Validation result
 */
export function runValidator(validatorName, artifact, projectState) {
  const validator = VALIDATORS[validatorName];
  if (!validator) {
    return {
      passed: false,
      error: `Unknown validator: ${validatorName}`,
      available_validators: Object.keys(VALIDATORS)
    };
  }
  
  try {
    return validator(artifact, projectState);
  } catch (error) {
    return {
      passed: false,
      error: `Validator ${validatorName} threw an error: ${error.message}`,
      stack: error.stack
    };
  }
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'list':
      console.log(JSON.stringify({
        validators: Object.keys(VALIDATORS),
        count: Object.keys(VALIDATORS).length
      }, null, 2));
      process.exit(0);

    case 'validate': {
      const validatorName = args[1];
      const artifactJson = args[2] || '{}';
      const stateJson = args[3] || '{}';
      
      try {
        const artifact = JSON.parse(artifactJson);
        const state = JSON.parse(stateJson);
        const result = runValidator(validatorName, artifact, state);
        console.log(JSON.stringify(result, null, 2));
        process.exit(result.passed ? 0 : 1);
      } catch (e) {
        console.error(JSON.stringify({ error: e.message }, null, 2));
        process.exit(1);
      }
    }

    default:
      console.error(JSON.stringify({
        error: 'Unknown command',
        usage: 'task-validators.js <command> [args...]',
        commands: [
          'list - List all available validators',
          'validate <validatorName> <artifactJson> [stateJson] - Run a validator'
        ]
      }, null, 2));
      process.exit(1);
  }
}
