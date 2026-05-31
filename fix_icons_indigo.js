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

    // Replace the glass-panel gray with the dark indigo look
    content = content.replace(/border border-white\/10 bg-black\/50 glass-panel/g, 'bg-indigo-500/10 border border-indigo-500/20');
    
    // Also, if HowItWorksPage has bg-indigo-500/5, let's upgrade it to have the border too for consistency!
    content = content.replace(/bg-indigo-500\/5( text-indigo-400)/g, 'bg-indigo-500/10 border border-indigo-500/20$1');

    if (content !== originalContent) {
        fs.writeFileSync(file, content);
        console.log('Updated', file);
    }
});
