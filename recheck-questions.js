const fs=require('fs'),vm=require('vm'); const s=fs.readFileSync('outputs/index.html','utf8');let i=s.indexOf('[',s.indexOf('const quizBank = [')),d=0,q=false,e=false,k;
for(k=i;k<s.length;k++){let c=s[k];if(q){if(e)e=false;else if(c==='\\')e=true;else if(c==='"')q=false;continue;}if(c==='"')q=true;else if(c==='[')d++;else if(c===']'&&--d===0)break;}
const bank=vm.runInNewContext('('+s.slice(i,k+1)+')');
for(const id of [229,232,233]){const x=bank.find(y=>y.id===id);console.log('\nQ'+id,'options=',x.options,'correct=',x.correct,'answer=',x.options[x.correct]);console.log(x.explanation.replace(/<br>/g,'\n'));}
const bad=[];for(const x of bank){for(const t of [x.question,...x.options,x.explanation])if(/[�]|\(cid:|vả|giứa|Lờigiải|Số cáchchọn/i.test(t))bad.push(x.id);}
console.log('bank',bank.length,'text warnings',Array.from(new Set(bad)));
