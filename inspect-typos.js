const fs=require('fs'),vm=require('vm'); const s=fs.readFileSync('outputs/index.html','utf8');let i=s.indexOf('[',s.indexOf('const quizBank = [')),d=0,q=false,e=false,k;
for(k=i;k<s.length;k++){let c=s[k];if(q){if(e)e=false;else if(c==='\\')e=true;else if(c==='"')q=false;continue;}if(c==='"')q=true;else if(c==='[')d++;else if(c===']'&&--d===0)break;}
const a=vm.runInNewContext('('+s.slice(i,k+1)+')'); for(const id of [229,232,233]){let x=a.find(y=>y.id===id);console.log('\n=== '+id+' QUESTION ===\n'+x.question+'\nOPTIONS '+JSON.stringify(x.options)+'\nEXPLANATION\n'+x.explanation);}
