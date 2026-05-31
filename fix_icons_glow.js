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

    // We want to replace 'border border-indigo-500/20' with 'border border-indigo-400/40 shadow-glow-sm'
    content = content.replace(/border border-indigo-500\/20/g, 'border border-indigo-400/40 shadow-glow-sm');
    
    // Deduplicate shadow-glow-sm if it was already there (e.g., 'shadow-glow-sm shadow-glow-sm')
    content = content.replace(/shadow-glow-sm\s+shadow-glow-sm/g, 'shadow-glow-sm');
    
    // Also catch 'shadow-glow-sm group-hover:scale-110 shadow-glow-sm' (if separated by other classes)
    // Actually, deduplicating classes in a string safely:
    const classRegex = /className="([^"]+)"/g;
    content = content.replace(classRegex, (match, classStr) => {
        const classes = classStr.split(' ');
        const uniqueClasses = [...new Set(classes)];
        return `className="${uniqueClasses.join(' ')}"`;
    });

    if (content !== originalContent) {
        fs.writeFileSync(file, content);
        console.log('Updated', file);
    }
});
