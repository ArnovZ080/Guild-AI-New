const fs = require('fs');
const path = require('path');

function walk(dir) {
    let results = [];
    if (!fs.existsSync(dir)) return results;
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

const files = walk('services/web/src/components');

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let originalContent = content;

    // 1. Em-dashes to hyphens
    content = content.replace(/—/g, '-');

    // 2. Icon wrappers standardisation (if they existed as gradient or old glass panel)
    // Replace gradient wrappers
    content = content.replace(/bg-gradient-to-br from-[a-z]+-[0-9]+ to-[a-z]+-[0-9]+/g, 'bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm');
    content = content.replace(/bg-gradient-to-br \$\{[^\}]+\}/g, 'bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm');
    
    // Replace generic color wrappers for icons (w-X h-X or p-2)
    content = content.replace(/(w-\d+ h-\d+|p-2)([^>]*?)bg-(indigo|emerald|purple|blue|rose|pink|teal|violet)-500\/(10|20)/g, '$1$2bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm');
    
    // Replace gradient-cobalt
    content = content.replace(/(w-\d+ h-\d+\s+(?:rounded-[a-z0-9]+)?\s*)gradient-cobalt/g, '$1bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm');

    // Make icon text indigo-400
    content = content.replace(/(bg-indigo-500\/10[^>]*?)text-white/g, '$1text-indigo-400');
    content = content.replace(/(bg-indigo-500\/10[^>]*?)text-emerald-400/g, '$1text-indigo-400');
    content = content.replace(/(bg-indigo-500\/10[^>]*?)text-purple-400/g, '$1text-indigo-400');

    // Fix specific Lucide icons colors inside the replaced wrappers
    content = content.replace(/<([A-Z][a-zA-Z0-9]+)[^>]*className="([^"]*)text-emerald-400([^"]*)"/g, '<$1 className="$2text-indigo-400$3"');
    content = content.replace(/<([A-Z][a-zA-Z0-9]+)[^>]*className="([^"]*)text-purple-400([^"]*)"/g, '<$1 className="$2text-indigo-400$3"');
    content = content.replace(/<([A-Z][a-zA-Z0-9]+)[^>]*className="([^"]*)text-pink-400([^"]*)"/g, '<$1 className="$2text-indigo-400$3"');

    // Deduplicate shadow-glow-sm
    content = content.replace(/shadow-glow-sm\s+shadow-glow-sm/g, 'shadow-glow-sm');
    
    // Clean up generic shadows if glow is present
    content = content.replace(/(shadow-glow-sm[^>]*?)shadow-lg/g, '$1');
    content = content.replace(/(bg-indigo-500\/10[^>]*?)shadow-lg/g, '$1shadow-glow-sm');

    // Fix classes cleanly
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
