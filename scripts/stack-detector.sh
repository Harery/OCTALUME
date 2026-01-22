#!/bin/bash
# OCTALUME v2.0 - Stack Detector
# Automatic technology stack detection and configuration
# Compatible with Claude Code CLI

set -e

SPECS_DIR="${SPECS_DIR:-.claude/specs}"
STACK_FILE="$SPECS_DIR/detected-stack.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Detection results
declare -A DETECTED

# Initialize
init_detector() {
    mkdir -p "$SPECS_DIR"
}

# Detect package manager
detect_package_manager() {
    if [ -f "package-lock.json" ]; then
        DETECTED[package_manager]="npm"
    elif [ -f "yarn.lock" ]; then
        DETECTED[package_manager]="yarn"
    elif [ -f "pnpm-lock.yaml" ]; then
        DETECTED[package_manager]="pnpm"
    elif [ -f "bun.lockb" ]; then
        DETECTED[package_manager]="bun"
    elif [ -f "requirements.txt" ] || [ -f "Pipfile" ]; then
        DETECTED[package_manager]="pip"
    elif [ -f "poetry.lock" ]; then
        DETECTED[package_manager]="poetry"
    elif [ -f "Gemfile.lock" ]; then
        DETECTED[package_manager]="bundler"
    elif [ -f "go.mod" ]; then
        DETECTED[package_manager]="go"
    elif [ -f "Cargo.lock" ]; then
        DETECTED[package_manager]="cargo"
    elif [ -f "composer.lock" ]; then
        DETECTED[package_manager]="composer"
    else
        DETECTED[package_manager]="unknown"
    fi
}

# Detect primary language
detect_language() {
    local ts_count=$(find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | wc -l)
    local js_count=$(find . -name "*.js" -o -name "*.jsx" 2>/dev/null | wc -l)
    local py_count=$(find . -name "*.py" 2>/dev/null | wc -l)
    local rb_count=$(find . -name "*.rb" 2>/dev/null | wc -l)
    local go_count=$(find . -name "*.go" 2>/dev/null | wc -l)
    local rs_count=$(find . -name "*.rs" 2>/dev/null | wc -l)
    local java_count=$(find . -name "*.java" 2>/dev/null | wc -l)
    local php_count=$(find . -name "*.php" 2>/dev/null | wc -l)
    local cs_count=$(find . -name "*.cs" 2>/dev/null | wc -l)
    
    # Determine primary language
    local max=0
    local lang="unknown"
    
    if [ "$ts_count" -gt "$max" ]; then max=$ts_count; lang="typescript"; fi
    if [ "$js_count" -gt "$max" ]; then max=$js_count; lang="javascript"; fi
    if [ "$py_count" -gt "$max" ]; then max=$py_count; lang="python"; fi
    if [ "$rb_count" -gt "$max" ]; then max=$rb_count; lang="ruby"; fi
    if [ "$go_count" -gt "$max" ]; then max=$go_count; lang="go"; fi
    if [ "$rs_count" -gt "$max" ]; then max=$rs_count; lang="rust"; fi
    if [ "$java_count" -gt "$max" ]; then max=$java_count; lang="java"; fi
    if [ "$php_count" -gt "$max" ]; then max=$php_count; lang="php"; fi
    if [ "$cs_count" -gt "$max" ]; then max=$cs_count; lang="csharp"; fi
    
    # TypeScript takes precedence if tsconfig exists
    if [ -f "tsconfig.json" ]; then
        lang="typescript"
    fi
    
    DETECTED[language]="$lang"
}

# Detect framework
detect_framework() {
    local framework="none"
    
    if [ -f "package.json" ]; then
        local pkg_content=$(cat package.json 2>/dev/null)
        
        # React ecosystem
        if echo "$pkg_content" | grep -q '"next"'; then
            framework="nextjs"
        elif echo "$pkg_content" | grep -q '"gatsby"'; then
            framework="gatsby"
        elif echo "$pkg_content" | grep -q '"remix"'; then
            framework="remix"
        elif echo "$pkg_content" | grep -q '"react"'; then
            framework="react"
        fi
        
        # Vue ecosystem
        if echo "$pkg_content" | grep -q '"nuxt"'; then
            framework="nuxt"
        elif echo "$pkg_content" | grep -q '"vue"'; then
            framework="vue"
        fi
        
        # Angular
        if echo "$pkg_content" | grep -q '"@angular/core"'; then
            framework="angular"
        fi
        
        # Svelte
        if echo "$pkg_content" | grep -q '"svelte"'; then
            if echo "$pkg_content" | grep -q '"@sveltejs/kit"'; then
                framework="sveltekit"
            else
                framework="svelte"
            fi
        fi
        
        # Node.js backends
        if echo "$pkg_content" | grep -q '"express"'; then
            framework="express"
        elif echo "$pkg_content" | grep -q '"fastify"'; then
            framework="fastify"
        elif echo "$pkg_content" | grep -q '"koa"'; then
            framework="koa"
        elif echo "$pkg_content" | grep -q '"nestjs"'; then
            framework="nestjs"
        elif echo "$pkg_content" | grep -q '"hono"'; then
            framework="hono"
        fi
        
        # Electron
        if echo "$pkg_content" | grep -q '"electron"'; then
            framework="electron"
        fi
    fi
    
    # Python frameworks
    if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        if grep -q "django" requirements.txt 2>/dev/null || grep -q "django" pyproject.toml 2>/dev/null; then
            framework="django"
        elif grep -q "flask" requirements.txt 2>/dev/null || grep -q "flask" pyproject.toml 2>/dev/null; then
            framework="flask"
        elif grep -q "fastapi" requirements.txt 2>/dev/null || grep -q "fastapi" pyproject.toml 2>/dev/null; then
            framework="fastapi"
        fi
    fi
    
    # Ruby frameworks
    if [ -f "Gemfile" ]; then
        if grep -q "rails" Gemfile 2>/dev/null; then
            framework="rails"
        elif grep -q "sinatra" Gemfile 2>/dev/null; then
            framework="sinatra"
        fi
    fi
    
    # Go frameworks
    if [ -f "go.mod" ]; then
        if grep -q "gin-gonic" go.mod 2>/dev/null; then
            framework="gin"
        elif grep -q "echo" go.mod 2>/dev/null; then
            framework="echo"
        elif grep -q "fiber" go.mod 2>/dev/null; then
            framework="fiber"
        fi
    fi
    
    DETECTED[framework]="$framework"
}

# Detect database
detect_database() {
    local databases=""
    
    if [ -f "package.json" ]; then
        local pkg=$(cat package.json 2>/dev/null)
        
        if echo "$pkg" | grep -qE '"(pg|postgres|postgresql)"'; then databases+="postgresql,"; fi
        if echo "$pkg" | grep -qE '"mysql2?"'; then databases+="mysql,"; fi
        if echo "$pkg" | grep -q '"mongodb"'; then databases+="mongodb,"; fi
        if echo "$pkg" | grep -q '"redis"'; then databases+="redis,"; fi
        if echo "$pkg" | grep -q '"sqlite"'; then databases+="sqlite,"; fi
        if echo "$pkg" | grep -q '"prisma"'; then databases+="prisma,"; fi
        if echo "$pkg" | grep -q '"drizzle"'; then databases+="drizzle,"; fi
        if echo "$pkg" | grep -q '"typeorm"'; then databases+="typeorm,"; fi
        if echo "$pkg" | grep -q '"sequelize"'; then databases+="sequelize,"; fi
        if echo "$pkg" | grep -q '"mongoose"'; then databases+="mongoose,"; fi
    fi
    
    # Check for database config files
    if [ -f "prisma/schema.prisma" ]; then databases+="prisma,"; fi
    if [ -f "drizzle.config.ts" ] || [ -f "drizzle.config.js" ]; then databases+="drizzle,"; fi
    
    # Remove trailing comma
    databases="${databases%,}"
    
    if [ -z "$databases" ]; then
        databases="none"
    fi
    
    DETECTED[database]="$databases"
}

# Detect testing framework
detect_testing() {
    local testing=""
    
    if [ -f "package.json" ]; then
        local pkg=$(cat package.json 2>/dev/null)
        
        if echo "$pkg" | grep -q '"jest"'; then testing+="jest,"; fi
        if echo "$pkg" | grep -q '"vitest"'; then testing+="vitest,"; fi
        if echo "$pkg" | grep -q '"mocha"'; then testing+="mocha,"; fi
        if echo "$pkg" | grep -qE '"@testing-library/(react|vue|svelte)"'; then testing+="testing-library,"; fi
        if echo "$pkg" | grep -q '"cypress"'; then testing+="cypress,"; fi
        if echo "$pkg" | grep -q '"playwright"'; then testing+="playwright,"; fi
        if echo "$pkg" | grep -q '"puppeteer"'; then testing+="puppeteer,"; fi
    fi
    
    # Python testing
    if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
        if grep -q "pytest" pytest.ini 2>/dev/null || grep -q "pytest" pyproject.toml 2>/dev/null; then
            testing+="pytest,"
        fi
    fi
    
    testing="${testing%,}"
    
    if [ -z "$testing" ]; then
        testing="none"
    fi
    
    DETECTED[testing]="$testing"
}

# Detect CI/CD
detect_cicd() {
    local cicd=""
    
    if [ -d ".github/workflows" ]; then cicd+="github-actions,"; fi
    if [ -f ".gitlab-ci.yml" ]; then cicd+="gitlab-ci,"; fi
    if [ -f "Jenkinsfile" ]; then cicd+="jenkins,"; fi
    if [ -f ".circleci/config.yml" ]; then cicd+="circleci,"; fi
    if [ -f ".travis.yml" ]; then cicd+="travis,"; fi
    if [ -f "azure-pipelines.yml" ]; then cicd+="azure-devops,"; fi
    if [ -f "bitbucket-pipelines.yml" ]; then cicd+="bitbucket,"; fi
    
    cicd="${cicd%,}"
    
    if [ -z "$cicd" ]; then
        cicd="none"
    fi
    
    DETECTED[cicd]="$cicd"
}

# Detect containerization
detect_container() {
    local container=""
    
    if [ -f "Dockerfile" ] || [ -f "dockerfile" ]; then container+="docker,"; fi
    if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then container+="docker-compose,"; fi
    if [ -f "Containerfile" ]; then container+="podman,"; fi
    if [ -d "kubernetes" ] || [ -d "k8s" ]; then container+="kubernetes,"; fi
    if [ -f "skaffold.yaml" ]; then container+="skaffold,"; fi
    
    container="${container%,}"
    
    if [ -z "$container" ]; then
        container="none"
    fi
    
    DETECTED[container]="$container"
}

# Detect linting/formatting
detect_tooling() {
    local tooling=""
    
    if [ -f ".eslintrc" ] || [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f "eslint.config.js" ]; then
        tooling+="eslint,"
    fi
    if [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f "prettier.config.js" ]; then
        tooling+="prettier,"
    fi
    if [ -f ".editorconfig" ]; then tooling+="editorconfig,"; fi
    if [ -f "biome.json" ]; then tooling+="biome,"; fi
    if [ -f ".stylelintrc" ]; then tooling+="stylelint,"; fi
    
    tooling="${tooling%,}"
    
    if [ -z "$tooling" ]; then
        tooling="none"
    fi
    
    DETECTED[tooling]="$tooling"
}

# Detect cloud/deployment
detect_deployment() {
    local deployment=""
    
    if [ -f "vercel.json" ] || [ -d ".vercel" ]; then deployment+="vercel,"; fi
    if [ -f "netlify.toml" ]; then deployment+="netlify,"; fi
    if [ -f "fly.toml" ]; then deployment+="fly.io,"; fi
    if [ -f "railway.toml" ] || [ -f "railway.json" ]; then deployment+="railway,"; fi
    if [ -f "render.yaml" ]; then deployment+="render,"; fi
    if [ -f "app.yaml" ]; then deployment+="gcp-app-engine,"; fi
    if [ -f "serverless.yml" ] || [ -f "serverless.yaml" ]; then deployment+="serverless,"; fi
    if [ -d ".aws" ] || [ -f "samconfig.toml" ]; then deployment+="aws,"; fi
    
    deployment="${deployment%,}"
    
    if [ -z "$deployment" ]; then
        deployment="none"
    fi
    
    DETECTED[deployment]="$deployment"
}

# Run all detections
run_detection() {
    echo -e "${BLUE}🔍 OCTALUME Stack Detector${NC}"
    echo "==========================="
    echo ""
    
    echo -e "${CYAN}Analyzing project structure...${NC}"
    echo ""
    
    detect_package_manager
    detect_language
    detect_framework
    detect_database
    detect_testing
    detect_cicd
    detect_container
    detect_tooling
    detect_deployment
    
    # Display results
    echo -e "${MAGENTA}━━━ Detected Stack ━━━${NC}"
    echo ""
    printf "  ${GREEN}%-18s${NC} %s\n" "Language:" "${DETECTED[language]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Framework:" "${DETECTED[framework]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Package Manager:" "${DETECTED[package_manager]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Database:" "${DETECTED[database]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Testing:" "${DETECTED[testing]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "CI/CD:" "${DETECTED[cicd]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Container:" "${DETECTED[container]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Tooling:" "${DETECTED[tooling]}"
    printf "  ${GREEN}%-18s${NC} %s\n" "Deployment:" "${DETECTED[deployment]}"
    echo ""
}

# Save detection to file
save_detection() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    cat > "$STACK_FILE" << EOF
{
  "version": "2.0.0",
  "detected_at": "$timestamp",
  "stack": {
    "language": "${DETECTED[language]}",
    "framework": "${DETECTED[framework]}",
    "package_manager": "${DETECTED[package_manager]}",
    "database": "${DETECTED[database]}",
    "testing": "${DETECTED[testing]}",
    "cicd": "${DETECTED[cicd]}",
    "container": "${DETECTED[container]}",
    "tooling": "${DETECTED[tooling]}",
    "deployment": "${DETECTED[deployment]}"
  },
  "recommendations": {
    "qa_checks": $(generate_qa_recommendations),
    "commands": $(generate_command_recommendations)
  }
}
EOF
    
    echo -e "${GREEN}✓ Stack saved to: $STACK_FILE${NC}"
}

# Generate QA recommendations based on stack
generate_qa_recommendations() {
    local checks="[]"
    
    case "${DETECTED[framework]}" in
        nextjs|react|vue|angular|svelte*)
            checks='["lint", "type-check", "test", "build"]'
            ;;
        express|fastify|nestjs)
            checks='["lint", "type-check", "test", "security-audit"]'
            ;;
        django|flask|fastapi)
            checks='["lint", "type-check", "test", "security-audit"]'
            ;;
        *)
            checks='["lint", "test"]'
            ;;
    esac
    
    echo "$checks"
}

# Generate command recommendations
generate_command_recommendations() {
    local cmds="{}"
    
    case "${DETECTED[package_manager]}" in
        npm)
            cmds='{"install": "npm install", "dev": "npm run dev", "build": "npm run build", "test": "npm test"}'
            ;;
        yarn)
            cmds='{"install": "yarn", "dev": "yarn dev", "build": "yarn build", "test": "yarn test"}'
            ;;
        pnpm)
            cmds='{"install": "pnpm install", "dev": "pnpm dev", "build": "pnpm build", "test": "pnpm test"}'
            ;;
        pip|poetry)
            cmds='{"install": "pip install -r requirements.txt", "dev": "python main.py", "test": "pytest"}'
            ;;
        *)
            cmds='{}'
            ;;
    esac
    
    echo "$cmds"
}

# Show current stack (from saved file)
show_stack() {
    if [ ! -f "$STACK_FILE" ]; then
        echo -e "${YELLOW}No stack detected yet. Run:${NC}"
        echo -e "  ${CYAN}./scripts/stack-detector.sh detect${NC}"
        exit 0
    fi
    
    echo -e "${BLUE}📊 Current Stack${NC}"
    echo "================"
    echo ""
    
    if command -v jq &> /dev/null; then
        jq -r '.stack | to_entries[] | "  \(.key): \(.value)"' "$STACK_FILE"
        echo ""
        echo -e "${CYAN}Detected at:${NC} $(jq -r '.detected_at' "$STACK_FILE")"
    else
        cat "$STACK_FILE"
    fi
}

# Show help
show_help() {
    echo -e "${BLUE}OCTALUME v2.0 - Stack Detector${NC}"
    echo "==============================="
    echo ""
    echo "Commands:"
    echo "  detect    Analyze project and detect technology stack"
    echo "  show      Display currently detected stack"
    echo "  help      Show this help"
    echo ""
    echo "Detects:"
    echo "  - Programming language"
    echo "  - Framework (React, Vue, Next.js, Django, etc.)"
    echo "  - Package manager (npm, yarn, pip, etc.)"
    echo "  - Database (PostgreSQL, MongoDB, etc.)"
    echo "  - Testing framework (Jest, Vitest, Pytest, etc.)"
    echo "  - CI/CD (GitHub Actions, GitLab CI, etc.)"
    echo "  - Container (Docker, Kubernetes, etc.)"
    echo "  - Linting/formatting tools"
    echo "  - Deployment platform"
    echo ""
    echo "Examples:"
    echo "  ./scripts/stack-detector.sh detect"
    echo "  ./scripts/stack-detector.sh show"
}

# Main
init_detector

case "${1:-detect}" in
    detect)
        run_detection
        save_detection
        ;;
    show)
        show_stack
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
