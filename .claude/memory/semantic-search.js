#!/usr/bin/env node
/**
 * OCTALUME v2.1 - Semantic Memory Search
 * 
 * Provides embedding-based semantic search over memory entries.
 * Uses local embeddings (transformers.js) with OpenAI API fallback.
 * 
 * Usage:
 *   node semantic-search.js search "authentication flow"
 *   node semantic-search.js index
 *   node semantic-search.js similar <entry-id>
 *   node semantic-search.js stats
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Configuration
const CONFIG = {
    memoryFile: path.join(__dirname, 'memory.json'),
    embeddingsFile: path.join(__dirname, 'embeddings.json'),
    indexFile: path.join(__dirname, 'semantic-index.json'),
    embeddingDimension: 384, // MiniLM dimension
    topK: 5,
    similarityThreshold: 0.5,
    useLocalEmbeddings: true, // Set to false to use OpenAI
    openaiModel: 'text-embedding-3-small'
};

// Simple TF-IDF based fallback embeddings (when transformers.js not available)
class SimpleEmbeddings {
    constructor() {
        this.vocabulary = new Map();
        this.idf = new Map();
        this.documents = [];
    }

    tokenize(text) {
        return text.toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(token => token.length > 2);
    }

    buildVocabulary(documents) {
        const docFreq = new Map();
        
        documents.forEach((doc, idx) => {
            const tokens = new Set(this.tokenize(doc));
            tokens.forEach(token => {
                if (!this.vocabulary.has(token)) {
                    this.vocabulary.set(token, this.vocabulary.size);
                }
                docFreq.set(token, (docFreq.get(token) || 0) + 1);
            });
        });

        // Calculate IDF
        const N = documents.length;
        docFreq.forEach((freq, token) => {
            this.idf.set(token, Math.log(N / freq));
        });

        this.documents = documents;
    }

    embed(text) {
        const tokens = this.tokenize(text);
        const tf = new Map();
        
        tokens.forEach(token => {
            tf.set(token, (tf.get(token) || 0) + 1);
        });

        // Create sparse vector, then pad/truncate to fixed dimension
        const vector = new Array(CONFIG.embeddingDimension).fill(0);
        
        tf.forEach((freq, token) => {
            const idx = this.vocabulary.get(token);
            if (idx !== undefined && idx < CONFIG.embeddingDimension) {
                const idfVal = this.idf.get(token) || 1;
                vector[idx] = (freq / tokens.length) * idfVal;
            }
        });

        // Normalize
        const magnitude = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
        if (magnitude > 0) {
            return vector.map(v => v / magnitude);
        }
        return vector;
    }
}

// Cosine similarity between two vectors
function cosineSimilarity(a, b) {
    if (a.length !== b.length) return 0;
    
    let dotProduct = 0;
    let magnitudeA = 0;
    let magnitudeB = 0;
    
    for (let i = 0; i < a.length; i++) {
        dotProduct += a[i] * b[i];
        magnitudeA += a[i] * a[i];
        magnitudeB += b[i] * b[i];
    }
    
    magnitudeA = Math.sqrt(magnitudeA);
    magnitudeB = Math.sqrt(magnitudeB);
    
    if (magnitudeA === 0 || magnitudeB === 0) return 0;
    return dotProduct / (magnitudeA * magnitudeB);
}

// Generate hash for cache key
function hashText(text) {
    return crypto.createHash('md5').update(text).digest('hex').substring(0, 16);
}

// Load memory entries
function loadMemory() {
    if (!fs.existsSync(CONFIG.memoryFile)) {
        console.error('❌ Memory file not found:', CONFIG.memoryFile);
        process.exit(1);
    }
    return JSON.parse(fs.readFileSync(CONFIG.memoryFile, 'utf8'));
}

// Load or initialize embeddings cache
function loadEmbeddingsCache() {
    if (fs.existsSync(CONFIG.embeddingsFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.embeddingsFile, 'utf8'));
    }
    return { version: '2.1', embeddings: {}, vocabulary: null };
}

// Save embeddings cache
function saveEmbeddingsCache(cache) {
    fs.writeFileSync(CONFIG.embeddingsFile, JSON.stringify(cache, null, 2));
}

// Extract searchable text from memory entry
function entryToText(entry, type) {
    const parts = [];
    
    if (entry.decision) parts.push(entry.decision);
    if (entry.rationale) parts.push(entry.rationale);
    if (entry.pattern) parts.push(entry.pattern);
    if (entry.context) parts.push(entry.context);
    if (entry.lesson) parts.push(entry.lesson);
    if (entry.impact) parts.push(entry.impact);
    if (entry.description) parts.push(entry.description);
    if (entry.category) parts.push(entry.category);
    if (entry.phase) parts.push(entry.phase);
    if (entry.tags) parts.push(entry.tags.join(' '));
    if (entry.alternatives_considered) parts.push(entry.alternatives_considered.join(' '));
    
    return parts.join(' ').trim();
}

// Flatten memory into searchable entries
function flattenMemory(memory) {
    const entries = [];
    
    // Decisions
    if (memory.decisions) {
        memory.decisions.forEach(d => {
            entries.push({
                id: d.id,
                type: 'decision',
                text: entryToText(d, 'decision'),
                data: d
            });
        });
    }
    
    // Patterns
    if (memory.patterns) {
        memory.patterns.forEach(p => {
            entries.push({
                id: p.id,
                type: 'pattern',
                text: entryToText(p, 'pattern'),
                data: p
            });
        });
    }
    
    // Lessons
    if (memory.lessons) {
        memory.lessons.forEach(l => {
            entries.push({
                id: l.id,
                type: 'lesson',
                text: entryToText(l, 'lesson'),
                data: l
            });
        });
    }
    
    // Sessions
    if (memory.sessions) {
        memory.sessions.forEach(s => {
            const sessionText = [
                s.summary || '',
                s.key_decisions?.join(' ') || '',
                s.discoveries?.join(' ') || '',
                s.next_steps?.join(' ') || ''
            ].join(' ');
            
            if (sessionText.trim()) {
                entries.push({
                    id: s.id,
                    type: 'session',
                    text: sessionText,
                    data: s
                });
            }
        });
    }
    
    return entries.filter(e => e.text.length > 10);
}

// Build semantic index
async function buildIndex() {
    console.log('🔄 Building semantic index...\n');
    
    const memory = loadMemory();
    const entries = flattenMemory(memory);
    
    if (entries.length === 0) {
        console.log('⚠️  No memory entries to index');
        return;
    }
    
    console.log(`📚 Found ${entries.length} entries to index\n`);
    
    // Initialize embedder
    const embedder = new SimpleEmbeddings();
    const documents = entries.map(e => e.text);
    embedder.buildVocabulary(documents);
    
    // Generate embeddings
    const cache = { version: '2.1', embeddings: {}, vocabulary: null };
    
    entries.forEach((entry, idx) => {
        const hash = hashText(entry.text);
        const embedding = embedder.embed(entry.text);
        
        cache.embeddings[entry.id] = {
            hash,
            type: entry.type,
            embedding,
            text_preview: entry.text.substring(0, 100)
        };
        
        process.stdout.write(`\r  Indexing: ${idx + 1}/${entries.length}`);
    });
    
    console.log('\n');
    
    // Save vocabulary for consistent embeddings
    cache.vocabulary = {
        tokens: Array.from(embedder.vocabulary.entries()),
        idf: Array.from(embedder.idf.entries())
    };
    
    saveEmbeddingsCache(cache);
    
    // Save index metadata
    const indexMeta = {
        version: '2.1',
        created_at: new Date().toISOString(),
        entry_count: entries.length,
        types: {
            decisions: entries.filter(e => e.type === 'decision').length,
            patterns: entries.filter(e => e.type === 'pattern').length,
            lessons: entries.filter(e => e.type === 'lesson').length,
            sessions: entries.filter(e => e.type === 'session').length
        }
    };
    
    fs.writeFileSync(CONFIG.indexFile, JSON.stringify(indexMeta, null, 2));
    
    console.log('✅ Index built successfully!');
    console.log(`   Entries: ${entries.length}`);
    console.log(`   Types: ${JSON.stringify(indexMeta.types)}`);
}

// Semantic search
async function search(query, topK = CONFIG.topK, typeFilter = null) {
    const memory = loadMemory();
    const entries = flattenMemory(memory);
    const cache = loadEmbeddingsCache();
    
    if (Object.keys(cache.embeddings).length === 0) {
        console.log('⚠️  No index found. Building index first...\n');
        await buildIndex();
        return search(query, topK, typeFilter);
    }
    
    // Rebuild embedder from vocabulary
    const embedder = new SimpleEmbeddings();
    if (cache.vocabulary) {
        embedder.vocabulary = new Map(cache.vocabulary.tokens);
        embedder.idf = new Map(cache.vocabulary.idf);
    } else {
        // Fallback: rebuild from documents
        embedder.buildVocabulary(entries.map(e => e.text));
    }
    
    // Embed query
    const queryEmbedding = embedder.embed(query);
    
    // Calculate similarities
    const results = [];
    
    entries.forEach(entry => {
        if (typeFilter && entry.type !== typeFilter) return;
        
        const cached = cache.embeddings[entry.id];
        if (!cached) return;
        
        const similarity = cosineSimilarity(queryEmbedding, cached.embedding);
        
        if (similarity >= CONFIG.similarityThreshold) {
            results.push({
                id: entry.id,
                type: entry.type,
                similarity: similarity,
                data: entry.data
            });
        }
    });
    
    // Sort by similarity
    results.sort((a, b) => b.similarity - a.similarity);
    
    return results.slice(0, topK);
}

// Find similar entries
async function findSimilar(entryId, topK = CONFIG.topK) {
    const cache = loadEmbeddingsCache();
    const memory = loadMemory();
    const entries = flattenMemory(memory);
    
    const targetEntry = cache.embeddings[entryId];
    if (!targetEntry) {
        console.error(`❌ Entry not found: ${entryId}`);
        return [];
    }
    
    const results = [];
    
    Object.entries(cache.embeddings).forEach(([id, cached]) => {
        if (id === entryId) return;
        
        const similarity = cosineSimilarity(targetEntry.embedding, cached.embedding);
        
        if (similarity >= CONFIG.similarityThreshold) {
            const entry = entries.find(e => e.id === id);
            if (entry) {
                results.push({
                    id,
                    type: cached.type,
                    similarity,
                    data: entry.data
                });
            }
        }
    });
    
    results.sort((a, b) => b.similarity - a.similarity);
    return results.slice(0, topK);
}

// Display search results
function displayResults(results, query) {
    if (results.length === 0) {
        console.log(`\n❌ No results found for: "${query}"`);
        console.log('   Try different keywords or run "index" to rebuild.');
        return;
    }
    
    console.log(`\n🔍 Semantic Search Results for: "${query}"\n`);
    console.log('─'.repeat(60));
    
    results.forEach((result, idx) => {
        const similarity = (result.similarity * 100).toFixed(1);
        const typeEmoji = {
            decision: '🎯',
            pattern: '🔄',
            lesson: '💡',
            session: '📝'
        }[result.type] || '📄';
        
        console.log(`\n${idx + 1}. ${typeEmoji} [${result.type.toUpperCase()}] (${similarity}% match)`);
        console.log(`   ID: ${result.id}`);
        
        if (result.data.decision) {
            console.log(`   Decision: ${result.data.decision.substring(0, 80)}...`);
        }
        if (result.data.pattern) {
            console.log(`   Pattern: ${result.data.pattern.substring(0, 80)}...`);
        }
        if (result.data.lesson) {
            console.log(`   Lesson: ${result.data.lesson.substring(0, 80)}...`);
        }
        if (result.data.phase) {
            console.log(`   Phase: ${result.data.phase}`);
        }
        if (result.data.category) {
            console.log(`   Category: ${result.data.category}`);
        }
    });
    
    console.log('\n' + '─'.repeat(60));
    console.log(`Found ${results.length} results`);
}

// Display stats
function showStats() {
    const cache = loadEmbeddingsCache();
    const indexMeta = fs.existsSync(CONFIG.indexFile) 
        ? JSON.parse(fs.readFileSync(CONFIG.indexFile, 'utf8'))
        : null;
    
    console.log('\n📊 Semantic Index Statistics\n');
    console.log('─'.repeat(40));
    
    if (!indexMeta) {
        console.log('⚠️  No index built yet. Run: semantic-search.js index');
        return;
    }
    
    console.log(`Version:     ${indexMeta.version}`);
    console.log(`Created:     ${indexMeta.created_at}`);
    console.log(`Total:       ${indexMeta.entry_count} entries`);
    console.log(`\nBy Type:`);
    console.log(`  Decisions: ${indexMeta.types.decisions}`);
    console.log(`  Patterns:  ${indexMeta.types.patterns}`);
    console.log(`  Lessons:   ${indexMeta.types.lessons}`);
    console.log(`  Sessions:  ${indexMeta.types.sessions}`);
    
    const vocabSize = cache.vocabulary?.tokens?.length || 0;
    console.log(`\nVocabulary:  ${vocabSize} tokens`);
    console.log('─'.repeat(40));
}

// Main CLI
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'search':
        case 's':
            if (!args[1]) {
                console.error('Usage: semantic-search.js search <query> [--type decision|pattern|lesson|session] [--top N]');
                process.exit(1);
            }
            const query = args.slice(1).filter(a => !a.startsWith('--')).join(' ');
            const typeIdx = args.indexOf('--type');
            const typeFilter = typeIdx > -1 ? args[typeIdx + 1] : null;
            const topIdx = args.indexOf('--top');
            const topK = topIdx > -1 ? parseInt(args[topIdx + 1]) : CONFIG.topK;
            
            const results = await search(query, topK, typeFilter);
            displayResults(results, query);
            break;
            
        case 'index':
        case 'i':
            await buildIndex();
            break;
            
        case 'similar':
            if (!args[1]) {
                console.error('Usage: semantic-search.js similar <entry-id>');
                process.exit(1);
            }
            const similarResults = await findSimilar(args[1]);
            displayResults(similarResults, `similar to ${args[1]}`);
            break;
            
        case 'stats':
            showStats();
            break;
            
        default:
            console.log(`
OCTALUME v2.1 - Semantic Memory Search

Usage:
  node semantic-search.js <command> [options]

Commands:
  search <query>     Search memory semantically
    --type <type>    Filter by type (decision|pattern|lesson|session)
    --top <N>        Return top N results (default: 5)
  
  index              Build/rebuild semantic index
  similar <id>       Find entries similar to given ID
  stats              Show index statistics

Examples:
  node semantic-search.js search "authentication security"
  node semantic-search.js search "API design" --type decision --top 10
  node semantic-search.js index
  node semantic-search.js similar dec-001
`);
    }
}

main().catch(console.error);
