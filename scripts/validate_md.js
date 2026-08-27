const fs = require('fs');
const path = require('path');

const companiesDir = path.join(__dirname, '..', 'companies');
const files = fs.readdirSync(companiesDir).filter(f => f.endsWith('.md'));

console.log(`🔍 Validating ${files.length} Markdown files in ${companiesDir}...\n`);

let totalPassed = 0;
let totalFailed = 0;

files.forEach(file => {
  const filePath = path.join(companiesDir, file);
  const text = fs.readFileSync(filePath, 'utf8');
  const lines = text.split(/\r?\n/);

  let inTable = false;
  let count = 0;
  let errors = [];

  lines.forEach((line, idx) => {
    line = line.trim();
    if (line.startsWith('|') && line.includes('ID') && line.includes('Company Name')) {
      inTable = true;
      return;
    }
    if (line.startsWith('|') && line.includes('---|')) {
      return;
    }
    if (inTable && line.startsWith('|') && line.endsWith('|')) {
      const cells = line.split('|').map(c => c.trim()).slice(1, -1);
      if (cells.length < 6) {
        errors.push(`Line ${idx + 1}: Insufficient table columns (${cells.length}/7 required)`);
      } else {
        count++;
      }
    }
  });

  if (errors.length === 0) {
    console.log(`✅ [PASS] ${file}: ${count} companies parsed successfully.`);
    totalPassed++;
  } else {
    console.log(`❌ [FAIL] ${file}: Found ${errors.length} syntax errors.`);
    errors.forEach(e => console.log(`   - ${e}`));
    totalFailed++;
  }
});

console.log(`\n========================================`);
console.log(`Results: ${totalPassed} Passed, ${totalFailed} Failed.`);
if (totalFailed > 0) {
  process.exit(1);
} else {
  console.log(`🎉 All Markdown table files are valid and ready for deployment!`);
}
