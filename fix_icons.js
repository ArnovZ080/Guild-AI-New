const fs = require('fs');
const path = require('path');

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        file = path.join(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            results = results.concat(walk(file));
        } else if (file.endsWith('.jsx')) {
            results.push(file);
        }
    });
    return results;
}

const files = walk('services/web/src/pages');

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let originalContent = content;

    // 1. Replace bg-gradient-to-br from-X to-Y
    content = content.replace(/bg-gradient-to-br from-[a-z]+-[0-9]+ to-[a-z]+-[0-9]+/g, 'border border-white/10 glass-panel');
    
    // 2. Replace bg-gradient-to-br ${X.color}
    content = content.replace(/bg-gradient-to-br \$\{[^\}]+\}/g, 'border border-white/10 glass-panel');

    // 3. Replace bg-X-500/20 or bg-X-500/10 for icon wrappers
    content = content.replace(/bg-(indigo|emerald|purple|blue|rose|pink|teal|violet)-500\/(10|20)/g, 'border border-white/10 glass-panel shadow-glow-sm');

    // 4. Replace gradient-cobalt in icon wrappers (but not on text or buttons)
    content = content.replace(/(w-\d+ h-\d+\s+(?:rounded-[a-z0-9]+)?\s*)gradient-cobalt/g, '$1border border-white/10 glass-panel shadow-glow-sm');

    // 5. Replace text-white or text-emerald-400 or text-purple-400 inside icon SVGs
    content = content.replace(/(glass-panel[^>]*?)text-white/g, '$1text-indigo-400');
    content = content.replace(/(glass-panel[^>]*?)text-emerald-400/g, '$1text-indigo-400');
    content = content.replace(/(glass-panel[^>]*?)text-purple-400/g, '$1text-indigo-400');

    // 6. Fix specific Lucide icons colors inside the replaced wrappers
    content = content.replace(/<([A-Z][a-zA-Z0-9]+)[^>]*className="([^"]*)text-emerald-400([^"]*)"/g, '<$1 className="$2text-indigo-400$3"');
    content = content.replace(/<([A-Z][a-zA-Z0-9]+)[^>]*className="([^"]*)text-purple-400([^"]*)"/g, '<$1 className="$2text-indigo-400$3"');
    content = content.replace(/<([A-Z][a-zA-Z0-9]+)[^>]*className="([^"]*)text-pink-400([^"]*)"/g, '<$1 className="$2text-indigo-400$3"');
    content = content.replace(/<Lock className="text-white/g, '<Lock className="text-indigo-400');

    // 7. Clean up extraneous shadow-lg shadow-[a-z]+-500/X
    content = content.replace(/(glass-panel[^>]*?)shadow-lg shadow-[a-z]+-[0-9]+\/[0-9]+/g, '$1shadow-glow-sm');
    
    // Also remove generic shadow-lg if shadow-glow-sm is present to avoid double shadows
    content = content.replace(/(shadow-glow-sm[^>]*?)shadow-lg/g, '$1');
    content = content.replace(/(glass-panel[^>]*?)shadow-lg/g, '$1shadow-glow-sm');

    if (content !== originalContent) {
        fs.writeFileSync(file, content);
        console.log('Updated', file);
    }
});
