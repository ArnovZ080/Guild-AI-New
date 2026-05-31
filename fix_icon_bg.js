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

    // We previously inserted 'border border-white/10 glass-panel' for all icon wrappers.
    // Let's replace that specific sequence with 'border border-white/10 bg-black/40 glass-panel' 
    // Wait, let's just do 'border border-white/10 bg-zinc-950/80 glass-panel' to be safe.
    
    // Some were 'border border-white/10 glass-panel shadow-glow-sm'
    // Some were 'border border-white/10 glass-panel'
    
    // Let's replace 'border border-white/10 glass-panel' with 'border border-white/10 bg-zinc-950/80 glass-panel'
    // But we should make sure we only replace it on the icon wrappers, which typically have 'w-12 h-12' or 'w-14 h-14' or 'w-10 h-10' or 'p-2'
    
    content = content.replace(/(w-\d+ h-\d+|p-2)([^>]*?)border border-white\/10 glass-panel/g, '$1$2border border-white/10 bg-black/50 glass-panel');

    if (content !== originalContent) {
        fs.writeFileSync(file, content);
        console.log('Updated', file);
    }
});
