const fs=require('fs'),vm=require('vm');
const s=fs.readFileSync('outputs/index.html','utf8'); const p=s.indexOf('const quizBank = ['); let i=s.indexOf('[',p), depth=0, q=false, esc=false, end=-1;
for(let j=i;j<s.length;j++){const c=s[j];if(q){if(esc)esc=false;else if(c==='\\')esc=true;else if(c==='"')q=false;continue;}if(c==='"'){q=true;continue;}if(c==='[')depth++;else if(c===']'&&--depth===0){end=j+1;break;}}
const bank=vm.runInNewContext('('+s.slice(i,end)+')');
const words=/\b(?:vả|giứa|Lờigiải|Lờigiải|chữ cữ|khồng|sác suất|xác suẩt|phép thữ|các chử|số cánh|cach|chọnh|sốlượng|đượcđược|điềukiện|khong|duoc|nhiêu)\b/iu;
for(const x of bank){const all=[x.question,...x.options,x.explanation].join(' ');if(/[�]|\(cid:|vả|giứa|Lờigiải|điềukiện|chữ cữ/i.test(all))console.log('ID',x.id,'chapter',x.chapter,all.match(/[�]|\(cid:|vả|giứa|Lờigiải|điềukiện|chữ cữ/ig)?.join(','), '\n',all.slice(0,420).replace(/\n/g,' '));}
console.log('bank',bank.length,'characters',bank.reduce((a,x)=>a+x.question.length+x.explanation.length+x.options.join('').length,0));
