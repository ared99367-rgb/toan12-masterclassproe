from pathlib import Path
import re, json, html
import pdfplumber

OUT=Path('outputs')
ASSET=OUT/'quiz-assets'
PDFSEQ=Path(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf')
PDFPROB=Path(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')

# Common symbol encodings found in the source PDFs.
CHARMAP={
 '\uf022':'”','\uf028':'(','\uf029':')','\uf02b':'+','\uf02d':'−','\uf03b':';','\uf03c':'<','\uf03d':'=', '\uf03e':'>',
 '\uf044':'Δ','\uf057':'Ω','\uf070':'π','\uf0a1':'∀','\uf0a2':'⁺','\uf0a3':'≤','\uf0a5':'∞','\uf0ab':'⇒','\uf0ae':'→',
 '\uf0b3':'≥','\uf0b4':'×','\uf0b9':'≠','\uf0bb':'≈','\uf0c6':'∩','\uf0c8':'∪','\uf0ce':'∈','\uf0cf':'∉',
 '\uf0db':'Σ','\uf0de':'⇒','\uf0e0':'⇒','\uf0e5':'Σ','\uf0e6':'≤','\uf0e7':'(','\uf0e8':')','\uf0e9':'≤',
 '\uf0ea':'{','\uf0eb':'}','\uf0ec':'{','\uf0ed':'↘','\uf0f6':'≤','\uf0f7':'(','\uf0f8':')','\uf0f9':'≤','\uf0da':'∧',
 '\uf07b':'{','\uf07d':'}','\uf0fa':'[','\uf0fb':']','\uf05b':'[','\uf05d':']','\uf04d':'≡','\uf04c':'…','\uf067':'·','\uf077':'ω','\uf0b1':'±',
 '\uf0ee':' ','\uf0ef':' '
}

def normalize(s):
    for a,b in CHARMAP.items(): s=s.replace(a,b)
    s=s.replace('','=')
    # Remove PDF headers/contacts/page furniture while retaining every solution step.
    lines=[]
    for line in s.splitlines():
        z=line.strip()
        if not z: continue
        if re.match(r'(?i)^(?:email|emai)\s*[-:]',z): continue
        if re.match(r'(?i)^tác giả\s*:',z): continue
        if re.match(r'(?i)^trang\s*\d+\s*/\s*\d+',z): continue
        if 'Bài tập bổ sung chương' in z or 'Bài tập bổ sung và hướng dẫn giải phần' in z or 'Sưu tầm :' in z or 'Sưu tầm:' in z: continue
        if re.match(r'(?i)^chọn\s+[ABCD]\s*$',z): continue
        z=re.sub(r'\s+',' ',z).strip()
        lines.append(z)
    return lines

def flat(s): return ' '.join(normalize(s)).strip()
def html_lines(s): return '<br>'.join(html.escape(x,quote=False) for x in normalize(s))
def esc(s): return html.escape(str(s),quote=False)

# Hand-built choices and full solutions for the 23 foundation exercises that precede
# the 30 mixed exercises in the sequence PDF (the source has no A-D options there).
foundation=[
('Dãy số · số dư', 'Viết số hạng tổng quát của dãy số tự nhiên mà mỗi số hạng chia cho 3 dư 2.', ['$u_n=3n-1$ (n≥1)','$u_n=3n+2$ (n≥1)','$u_n=2n+3$','$u_n=3^n-1$'],0, 'Các số tự nhiên cần tìm là 2, 5, 8, … Đây là cấp số cộng có số đầu 2 và công sai 3, nên $u_n=2+3(n-1)=3n-1$. Thay n=1 được u₁=2 đúng với điều kiện chia 3 dư 2.'),
('Dãy số · truy hồi', 'Cho $u_1=3$, $u_{n+1}=2u_n$. Tìm $u_n$ và tích bốn số hạng đầu.', ['$u_n=3·2^{n-1}$; tích bằng 5184','$u_n=3·2^n$; tích bằng 10368','$u_n=2n+1$; tích bằng 945','$u_n=3^n$; tích bằng 729'],0, 'Mỗi số hạng gấp đôi số đứng trước nên $u_n=u_1·2^{n-1}=3·2^{n-1}$. Bốn số đầu là 3, 6, 12, 24; tích bằng $3·6·12·24=5184$.'),
('Dãy số · truy hồi', 'Với $u_1=3$, $u_{n+1}=2+\frac12u_n$, và với $u_1=a$, $u_{n+1}=a+bu_n$, chọn công thức đúng.', ['$u_n=4-2^{1-n}$; trường hợp tổng quát $u_n=a(1-b^n)/(1-b)$ nếu b≠1, còn b=1 thì $u_n=na$','$u_n=3·2^{n-1}$; tổng quát $u_n=a+b^n$','$u_n=4+2^{1-n}$; tổng quát $u_n=ab^{n-1}$','$u_n=2^n+3$; tổng quát $u_n=a(1+b)^n$'],0, 'Ở câu a, điểm bất động L thỏa L=2+L/2 nên L=4. Hiệu $u_n-4$ bị nhân 1/2 sau mỗi bước và $u_1-4=-1$, do đó $u_n=4-2^{1-n}$. Ở câu b, khai triển truy hồi được $u_n=a(1+b+…+b^{n-1})$. Đây là cấp số nhân; tổng bằng $a(1-b^n)/(1-b)$ khi b≠1 và bằng na khi b=1.'),
('Dãy số · đơn điệu', 'Xét đơn điệu của $u_n=\frac{n}{n^2+1}$, $v_n=\frac{2n-1}{2n}$, $w_n=(-\frac12)^n$ (n≥1).', ['$u_n$ giảm; $v_n$ tăng; $w_n$ không đơn điệu','$u_n$ tăng; $v_n$ giảm; $w_n$ tăng','$cả ba đều giảm','$cả ba đều tăng'],0, 'Với $u_n$, hiệu $u_{n+1}-u_n$ có tử số $1-n-n^2$, âm với n≥1, nên dãy giảm. $v_n=1-1/(2n)$ tăng theo n. $w_n$ đổi dấu luân phiên nên không tăng cũng không giảm.'),
('Dãy số · đơn điệu', 'Với $u_n=\frac{an+2}{bn+1}$, chọn nhận xét chính xác về hiệu hai số hạng liên tiếp.', ['$u_{n+1}-u_n=\frac{a-2b}{(bn+1)(b(n+1)+1)}$; dấu còn phụ thuộc mẫu số','$u_{n+1}-u_n=a+2b$','$u_{n+1}-u_n=2b-a$ với mọi a,b','$dãy luôn tăng'],0, 'Quy đồng trực tiếp: $(a(n+1)+2)(bn+1)-(an+2)(b(n+1)+1)=a-2b$. Vì vậy hiệu có dạng nêu ở đáp án. Nếu b≥0 thì mẫu dương với n≥1 và dấu đơn điệu do a−2b quyết định; với b tùy ý phải kiểm tra mẫu khác 0 và dấu mẫu.'),
('Dãy số · bị chặn', 'Chọn phân loại đúng cho các dãy: (a) $2n-1$; (b) $1/n^2$; (c) $1/[n(n+1)]$; (d) $3·2^{n-1}$; (e) $(-1/3)^n$.', ['a,d tăng và không bị chặn trên; b,c giảm, bị chặn; e bị chặn nhưng không đơn điệu','cả năm đều bị chặn','a,d giảm; b,c tăng; e không bị chặn','chỉ e bị chặn'],0, 'Với n≥1, (a) và (d) tăng, có cận dưới lần lượt 1 và 3 nhưng không có cận trên. (b) giảm từ 1 về 0; (c) giảm từ 1/2 về 0; cả hai bị chặn. (e) luân phiên dấu, độ lớn giảm về 0 nên bị chặn nhưng không đơn điệu.'),
('Dãy số · phép toán', 'Cho $u_n=(n-1)/n$, $v_n=(n+2)/n$. Bộ biểu thức $(u_n+v_n, u_n-v_n, u_nv_n, u_n/v_n)$ bằng gì?', ['$2+1/n, -3/n, 1+1/n-2/n², (n-1)/(n+2)$','2, 3/n, 1−1/n, (n+2)/(n−1)','$2−1/n, 3/n, 1−2/n², 1$','$2+3/n, −1/n, 1+2/n, (n+2)/(n−1)$'],0, 'Quy đồng từng biểu thức: tổng có tử 2n+1; hiệu có tử −3; tích bằng (n²+n−2)/n²; thương rút gọn n ở tử và mẫu. Suy ra lần lượt $2+1/n$, $-3/n$, $1+1/n-2/n²$, $(n-1)/(n+2)$.'),
('Cấp số cộng · tam giác vuông', 'Ba góc của một tam giác vuông lập thành cấp số cộng. Ba góc đó là?', ['$30°$, $60°$, $90°$','$20°$, $70°$, $90°$','$45°$, $45°$, $90°$','$15°$, $75°$, $90°$'],0, 'Ba góc lập thành CSC và có tổng 180°. Viết chúng là x−d, x, x+d; trung bình x=60°. Vì tam giác vuông có góc lớn nhất 90° nên ba góc là 30°, 60°, 90°.'),
('Cấp số cộng · tam giác', 'Nếu $\cot(A/2),\cot(B/2),\cot(C/2)$ theo thứ tự lập thành CSC, kết luận nào đúng về các cạnh?', ['$a,b,c$ theo thứ tự cũng lập thành CSC','a,b,c lập thành cấp số nhân','tam giác ABC đều','chỉ có $a=c$'],0, 'Dùng $A+B+C=π$ và công thức biến đổi tổng cotang, điều kiện CSC của ba cotang nửa góc tương đương quan hệ tuyến tính giữa các cạnh đối diện. Suy ra $a+c=2b$, tức a,b,c lập thành cấp số cộng.'),
('Cấp số cộng · tìm công sai', 'Trong một CSC, $u_2+u_7=92$ và $u_4+u_{11}=71$. Tìm số đầu $u_1$ và công sai d.', ['$u_1=233/4$, $d=-7/2$','$u_1=46$, $d=3$','$u_1=58$, $d=-3$','$u_1=71/2$, $d=7/2$'],0, 'Đặt $u_n=a+(n-1)d$. Ta có $2a+7d=92$ và $2a+13d=71$. Trừ hai phương trình được $6d=-21$, nên d=−7/2. Thay lại: $2a=92+49/2=233/2$, do đó $a=233/4$.'),
('Cấp số cộng · tổng', 'Một CSC có 11 số hạng, tổng bằng 176 và $u_{11}-u_1=30$. CSC là gì?', ['$1,4,7,…,31$','$2,5,8,…,32$','$−1,2,5,…,29$','$4,7,10,…,34$'],0, 'Ta có $10d=30$, nên d=3. Tổng bằng $11(u_1+u_{11})/2=176$, suy ra $u_1+u_{11}=32$. Kết hợp $u_{11}-u_1=30$ được $u_1=1$, $u_{11}=31$.'),
('Cấp số cộng · bốn số', 'Bốn số lập thành CSC, tổng bằng 22 và tổng bình phương bằng 166. Bộ số tăng dần là?', ['$1,4,7,10$','$2,4,6,10$','$−1,3,7,13$','$1,5,6,10$'],0, 'Viết bốn số đối xứng quanh trung bình 22/4=11/2: $m−3d/2,m−d/2,m+d/2,m+3d/2$. Tổng bình phương bằng $4m²+5d²=166$. Với m=11/2 suy ra $121+5d²=166$, d²=9. Chọn d=3 cho dãy tăng 1,4,7,10.'),
('Cấp số cộng · năm số', 'Năm số lập thành CSC, biết tổng S và tích P. Cách viết tổng quát nào đúng để tìm các số?', ['$x−2d,x−d,x,x+d,x+2d$, trong đó x=S/5 và $P=x(x²−d²)(x²−4d²)$','$S−2d,S−d,S,S+d,S+2d$','$x−d,x,x+d,x+2d,x+3d$ với x=S','$x,x+d,x+2d,x+3d,x+4d$ với x=P/5'],0, 'Năm số hạng đối xứng của CSC có dạng $x−2d,x−d,x,x+d,x+2d$. Tổng bằng 5x nên x=S/5. Nhân từng cặp đối xứng cho tích $x(x²−d²)(x²−4d²)=P$. Giải phương trình theo d², chỉ nhận nghiệm không âm.'),
('Cấp số cộng · số nguyên', 'Bốn số nguyên lập thành CSC, tổng bằng 20 và tổng nghịch đảo bằng 25/24. Bốn số theo thứ tự tăng là?', ['$2,4,6,8$','$1,4,7,8$','$−2,4,6,12$','$3,4,6,7$'],0, 'Trung bình bốn số là 5. Vì các số nguyên đối xứng quanh trung bình, viết chúng là $5−3k,5−k,5+k,5+3k$ với k nguyên. Tổng nghịch đảo rút gọn thành $10/(25−9k²)+10/(25−k²)=25/24$. Đặt z=k², phương trình cho z=1 hoặc z=145/9; z phải là bình phương số nguyên nên k=±1. Dãy tăng là 2,4,6,8.'),
('Cấp số cộng · số tam giác', 'Trồng 3003 cây thành các hàng 1,2,3,… cây. Có bao nhiêu hàng?', ['$77$','$76$','$78$','$81$'],0, 'Tổng n hàng là $1+2+…+n=n(n+1)/2=3003$. Suy ra $n²+n−6006=0$. Biệt thức bằng 24025=155² nên nghiệm dương $n=(−1+155)/2=77$.'),
('Cấp số cộng · tổng n số hạng', 'Một CSC thỏa $S_n=(n+1)u_n/2$ với mọi n. Quan hệ đúng giữa số đầu a và công sai d là?', ['$a=d$','$a=2d$','$a=−d$','$d=0$'],0, 'Thay $S_n=n[2a+(n−1)d]/2$ và $u_n=a+(n−1)d$ vào điều kiện. Rút gọn được $(n−1)(a−d)=0$. Với mọi n, suy ra a=d.'),
('Cấp số nhân · năm số hạng', 'cấp số nhân có $u_1=2$, công bội q=3 và 5 số hạng. Số hạng cuối và tổng là?', ['$u_5=162$, $S_5=242$','$u_5=54$, $S_5=80$','$u_5=486$, $S_5=728$','$u_5=162$, $S_5=2420$'],0, 'Số cuối $u_5=2·3^4=162$. Tổng $S_5=2(3^5−1)/(3−1)=242$.'),
('Cấp số nhân · công bội', 'cấp số nhân có 9 số hạng, $u_1=5$, $u_9=1280$. Các công bội và tổng tương ứng là?', ['$q=2$, $S_9=2555$ hoặc $q=−2$, $S_9=855$','$q=2$, $S_9=1280$','$q=−2$, $S_9=2555$','$q=4$, $S_9=32765$'],0, 'Từ $u_9=u_1q^8$ suy ra $q^8=256$, nên q=2 hoặc q=−2. Với q=2, $S_9=5(2^9−1)=2555$. Với q=−2, tổng $5(1−2+4−…+256)=855$.'),
('Cấp số nhân · xác định số hạng', 'a) cấp số nhân có 5 số hạng, đầu 3, cuối 243. b) Có 6 số hạng, đầu 243, cuối 1. c) q=1/4, n=6, S₆=2730. Chọn kết quả đúng.', ['$q=3$ hoặc $−3$ ở a; $q=1/3$ ở b; $u_1=2048,u_6=2$ ở c','$q=3$ ở a; $q=1/4$ ở b; $u_1=2730$ ở c','$q=−3$ ở a; $q=1/3$ ở b; $u_1=2$ ở c','$q=9$ ở a; $q=1/3$ ở b; $u_1=2048,u_6=8$ ở c'],0, 'a) $q^4=243/3=81$, nên q=±3. b) $q^5=1/243=1/3^5$, nên q=1/3. c) $S_6=u_1(1−4^{-6})/(1−1/4)=u_1·1365/1024=2730$, suy ra $u_1=2048$ và $u_6=2048/4^5=2$.'),
('Cấp số nhân · góc tứ giác', 'Bốn góc tứ giác lập thành cấp số nhân và góc cuối bằng 9 lần góc thứ hai. Bộ góc nào thỏa điều kiện?', ['$4,5°;13,5°;40,5°;121,5°$','$10°;30°;60°;80°$','$9°;27°;81°;63°$','$5°;15°;45°;115°$'],0, 'Đặt các góc là a, aq, aq², aq³. Điều kiện cuối/thứ hai cho q²=9; tính dương buộc q=3. Tổng góc 180° cho $40a=180°$, nên a=4,5°. Các góc lần lượt 4,5°, 13,5°, 40,5°, 121,5°.'),
('Cấp số nhân · ba số', 'Ba số dương lập thành cấp số nhân, tổng 248 và hiệu số cuối trừ số đầu là 192. Ba số theo thứ tự là?', ['$8,40,200$','$4,44,200$','$16,48,184$','$8,32,208$'],0, 'Gọi ba số a,b,c. Có $a+b+c=248$, $c−a=192$ và $b²=ac$. Suy ra a=8, b=40, c=200; kiểm tra tổng 248, hiệu 192 và $40²=8·200$.'),
('Cấp số nhân · tam giác', 'Ba cạnh của tam giác lập thành cấp số nhân có công bội q>0. Khoảng đúng của q là?', ['$\frac{\sqrt5-1}{2}<q<\frac{\sqrt5+1}{2}$','$q>1$','$0<q<1/2$','$q>2$'],0, 'Ba cạnh tỉ lệ $1,q,q²$ sau khi chia cho cạnh nhỏ nhất. Bất đẳng thức tam giác $1+q>q²$ và $q+q²>1$ cho lần lượt $q<(1+\sqrt5)/2$ và $q>(\sqrt5−1)/2$.'),
('Cấp số nhân · hình hộp', 'Hình hộp chữ nhật có thể tích $a^3$, diện tích toàn phần $2ma^2$, ba cạnh lập thành cấp số nhân dương. Tổng độ dài 12 cạnh bằng?', ['$4ma$','$2ma$','$6ma$','$12ma$'],0, 'Gọi ba cạnh là $a/q,a,aq$ vì tích bằng $a³$. Nửa diện tích toàn phần là $a²(1+q+1/q)=ma²$, nên tổng ba cạnh bằng ma. Mỗi cạnh xuất hiện 4 lần trong tổng 12 cạnh, do đó tổng độ dài là 4ma.'),
]

# Main set of 30 mixed advanced exercises: source statements and full worked solutions are preserved.
seq_text='\n'.join(p.read_text(encoding='utf-8') for p in sorted(Path('work/pdf-text').glob('seq-page-*.txt')))
main=seq_text.split('IV. BÀI TẬP TỔNG HỢP',1)[1].split('V. HƯỚNG DẪN GIẢI',1)[0]
qmarks=list(re.finditer(r'(?m)^\s*(\d+)\s*[.]\s*',main))
qstems=[]
for i,m in enumerate(qmarks):
 end=qmarks[i+1].start() if i+1<len(qmarks) else len(main)
 qstems.append(flat(main[m.start():end]))
solpart=seq_text.split('V. HƯỚNG DẪN GIẢI',1)[1]
smarks=list(re.finditer(r'(?im)^\s*Bài\s*(\d+)\s*[:.]',solpart))
solutions={}
for i,m in enumerate(smarks):
 end=smarks[i+1].start() if i+1<len(smarks) else len(solpart)
 solutions[int(m.group(1))]=html_lines(solpart[m.start():end])

# Correct result and three distractors for each of the source's 30 proof/calculation tasks.
main_choices=[
('Σxᵢ ≥ n khi xᵢ>0 và ∏xᵢ=1',['Σxᵢ=n với mọi bộ số','Σxᵢ≤n','Σxᵢ≥1'],0),
('$(a^n+b^n)/2 ≥ ((a+b)/2)^n$ với a,b≥0,n∈N*',['bất đẳng thức đảo chiều','chỉ đúng khi a=b','$(a^n+b^n)/2 = ((a+b)/2)^n$ luôn đúng'],0),
('a) tăng, bị chặn dưới bởi 2 nhưng không chặn trên; b) bị chặn nhưng không đơn điệu',['cả hai tăng và bị chặn','a giảm; b tăng','cả hai không bị chặn'],0),
('Số 35351 là số hạng thứ 101',['thứ 100','thứ 102','thứ 99'],0),
('Điều kiện là $m=n$ và $m>-27$ để có ba nghiệm phân biệt lập CSC',['m+n=0','m=n≤−27','m=−n'],0),
('$m=5$ hoặc $m=−25/19$',['m=0','m=5/2','m=−5/19'],0),
('Tam giác có hai góc không quá 60°',['có đúng một góc không quá 60°','tam giác đều','cả ba góc đều lớn hơn 60°'],0),
('Bốn số là $4,16/3,64/9,256/27$',['4,8,16,32','2,8/3,32/9,128/27','4,12,36,108'],0),
('Hai cấp số nhân: $8,16,32,64,128$ hoặc $−12,36,−108,324,−972$',['chỉ có dãy thứ nhất','8,2,1/2,1/8,1/32','−12,−36,−108,−324,−972'],0),
('Bốn số xen giữa là $11.2,18.4,25.6,32.8$',['10,16,24,32','12,20,28,36','8,16,24,32'],0),
('$S=2n+\frac{4(4^n-1)}{3}+\frac{1-4^{-n}}{3}$',['$S=2n+4^n$','$S=2^n+n$','$S=\frac{4^n-1}{3}$'],0),
('Tồn tại x khi và chỉ khi $a≥12$',['a≤12','a=0','a>24'],0),
('$a_n=2·3^n$ là cấp số nhân, $q=3$, tổng 8 số đầu $S_8=17680$',['q=2, S₈=6560','q=3, S₈=13120','q=6, S₈=17680'],0),
('Giá trị biểu thức bằng 0',['bằng $a^2$','bằng $2ad$','không xác định'],0),
('$(x,y)=(10/3,4/3),(0,0),(-3/4,-3/10)$',['chỉ $(0,0)$','$(3/4,3/10)$ và $(0,0)$','$(10/3,-4/3)$'],0),
('A≥0 với mọi x nên căn thức xác định trên ℝ',['A<0 tại một khoảng x','chỉ xác định khi x≥u₄','điều kiện phải là $u_1u_4-u_2u_3>6$'],0),
('Điều kiện tương đương là $\frac{\log_N a}{\log_N c}=\frac{\log_N a-\log_N b}{\log_N b-\log_N c}$',['điều kiện là tổng ba log bằng 0','tỉ số log bằng 1','không phụ thuộc thứ tự a,b,c'],0),
('$\log_b y=\frac{2\log_a x\log_c z}{\log_a x+\log_c z}$',['$\log_b y=\log_a x+\log_c z$','$\log_b y=\log_a x\log_c z$','$\log_b y=\frac{\log_a x+\log_c z}{2}$'],0),
('$x=3^{6/7}, y=3^{8/7}, q=3^{1/7}$',['x=3,y=9,q=3','$x=3^{7/6},y=3^{7/8},q=1/3$','$x=3^{6/7},y=3^{8/7},q=3'],0),
('Ba số là 3, 15, 75',['1, 30, 62','3, 30, 60','5, 15, 73'],0),
('a) $S_n=(10^{n+1}-10-9n)/27$; b) $x=5/2$',['a) $(10^n-1)/3$; b) x=2','a) $(10^{n+1}-1)/27$; b) x=−1/2','a) $3n$; b) x=5'],0),
('(2,4,8,12) hoặc $(25/2,15/2,9/2,3/2)$',['(1,2,4,8) בלבד','(2,4,6,8) בלבד','(12,8,4,2) בלבד'],0),
('$S_{10}=3069$',['$S_{10}=2046$','$S_{10}=1023$','$S_{10}=3000$'],0),
('Tam giác có $A=90°$, $B=60°$, $C=30°$',['tam giác đều','B=30°, C=60°','B=C=45°'],0),
('$\cot(A/2)\cot(C/2)=3$',['bằng 1','bằng 2','bằng 4'],0),
('$\tan A,\tan B,\tan C$ lập CSC với công sai 1',['lập CSC công sai 3','lập CSN công bội 2','không lập thành cấp số'],0),
('a,b,c lập thành CSC',['a,b,c lập thành CSN','a=c','b²=ac'],0),
('$a^2,b^2,c^2$ lập CSC',['a,b,c lập CSN','a²=c²','a²+b²+c²=0'],0),
('$q=\sqrt{(1+\sqrt2)/2}$',['$q=1/2$','$q=\sqrt2$','$q=\sqrt{2(\sqrt2-1)}$'],0),
('$d=\frac32r(\tan(C/2)-\tan(A/2))$',['$d=r(\tan A+\tan C)$','$d=\frac12r(\tan(C/2)+\tan(A/2))$','$d=3r(\tan C/2-\tan A/2)$'],0),
]

# Corrections/clarifications to copied source statements where PDF text extraction loses layout.
qstems[10]='Tính $S=2^2+(1/2)^2+4^2+(1/4)^2+…+(2^n)^2+(1/2^n)^2$.'
qstems[23]='Cho tam giác ABC vuông tại A. Ba số $a,b,(\sqrt6/3)c$ theo thứ tự lập thành cấp số nhân. Xác định các góc của tam giác.'

quiz=[]
# The 23 lead-in exercises have no multiple-choice options in the source; they are converted into MCQ with worked answers.
for i,(topic,q,opts,ans,ex) in enumerate(foundation,1):
    if len(opts)!=4: raise ValueError(f'foundation choices {i}')
    quiz.append({'chapter':6,'question':f'Bài nền tảng {i} · {topic}: {q}','options':opts,'correct':ans,'explanation':ex})

for i,(ans,distractors,correct_rot) in enumerate(main_choices,1):
    choices=[ans]+distractors
    shift=i%4
    choices=choices[shift:]+choices[:shift]
    correct=(4-shift)%4
    # Preserve source problem wording and diagrams from the relevant pages.
    q=qstems[i-1]
    if i==24: q=qstems[23]
    if i==1: q='Cho $x_1,x_2,\ldots,x_n>0$ và $x_1x_2\cdots x_n=1$. Chứng minh bất đẳng thức nào đúng?'
    if i==2: q='Với $a,b\ge0$ và $n\in\mathbb{N}^*$, bất đẳng thức nào đúng?'
    img=None
    if i==29: img='sequence-triangle-q29.svg'
    if i==30: img='sequence-triangle-q30.svg'
    if img: q+=f'<br><img src="./quiz-assets/{img}" alt="Sơ đồ tam giác trong bài {i}" class="mt-3 max-h-56 max-w-full rounded-lg border border-slate-200 bg-white p-2">'
    ex=solutions.get(i,'')
    if i==1: ex='Theo bất đẳng thức AM-GM, $\frac{x_1+\cdots+x_n}{n}\ge\sqrt[n]{x_1\cdots x_n}=1$. Suy ra $x_1+\cdots+x_n\ge n$. Dấu bằng xảy ra khi và chỉ khi mọi $x_i=1$.'
    if i==2: ex='Hàm $f(t)=t^n$ lồi trên $[0,+\infty)$ với $n\ge1$. Theo Jensen, $\frac{a^n+b^n}{2}\ge\left(\frac{a+b}{2}\right)^n$. Dấu bằng khi $a=b$ (hoặc $n=1$).'
    if i==5: ex += '<br><strong>Bổ sung điều kiện phân biệt:</strong> $d^2=m+27>0$, nên m=n>−27.'
    if i==9: ex += '<br><strong>Kiểm tra đủ 5 số hạng:</strong> với $u_1=8,q=2$ được 8,16,32,64,128; với $u_1=−12,q=−3$ được −12,36,−108,324,−972.'
    if i==24: ex += '<br>Kết luận: $B=60°$, $C=30°$.'
    if not ex: raise ValueError(f'no solution for sequence problem {i}')
    quiz.append({'chapter':6,'question':q,'options':choices,'correct':correct,'explanation':ex})

# Native multiple-choice material: 29 counting/combinatorics + 70 probability questions.
prob_text='\n'.join(p.read_text(encoding='utf-8') for p in sorted(Path('work/pdf-text').glob('prob-page-*.txt')))
marks=list(re.finditer(r'(?im)^\s*Câu\s*(\d+)\s*[.]',prob_text))
if len(marks)!=99: raise ValueError(f'expected 99 question starts, found {len(marks)}')
reconstructed=json.loads(Path('work/reconstructed-options.json').read_text(encoding='utf-8'))
for idx,m in enumerate(marks):
    end=marks[idx+1].start() if idx+1<len(marks) else len(prob_text)
    block=prob_text[m.start():end]
    solmark=re.search(r'(?i)Lờ\s*i\s*giải',block)
    if not solmark: raise ValueError(f'missing solution marker at item {idx+1}')
    before=block[:solmark.start()]
    after=block[solmark.end():]
    om=re.search(r'(?is)(?:^|\n)\s*A\s*[.]\s*(.*?)\s+B\s*[.]\s*(.*?)\s+C\s*[.]\s*(.*?)\s+D\s*[.]\s*([^\n]*)(?:\n|$)',before)
    if om:
        stem=flat(before[:om.start()])
        opts=[flat(om.group(j)) for j in range(1,5)]
    else:
        stem=flat(before); opts=[]
    stem=re.sub(r'^Câu\s*\d+\s*[.]\s*','',stem,flags=re.I)
    if not opts and idx==8:
        # The source omits the printed choices on this page; its solution says 24.
        opts=['24','18','36','12']
    if len(opts)!=4: raise ValueError(f'question {idx+1}: options={len(opts)}')
    am=re.search(r'(?i)Chọn\s*([ABCD])',after)
    correct='ABCD'.index(am.group(1).upper()) if am else None
    # The PDF's multi-column math layout is read out of order by plain text extraction.
    # Recover those choices from their page coordinates when the text choices are missing.
    broken=sum(not v.strip(' .') for v in opts)>=2 or len(set(opts))<4
    if broken and str(idx+1) in reconstructed:
        opts=[flat(re.sub(r'/\s*Lời.*$', '', v)) for v in reconstructed[str(idx+1)]]
    if idx==2: correct=0 # geometric count is 2876 (option A; source label conflicts with its calculation)
    if idx==44: correct=3 # 2/105, derived from the printed counting solution
    if idx==49: correct=3 # m+n=127, from the printed probability calculation
    if idx==8: correct=0
    if correct is None: raise ValueError(f'question {idx+1}: missing key')
    if idx==39:
        opts=['45/473','64/473','2/210','2/473']; correct=3
    if idx==38:
        opts=['1/3','9/83','2/83','2/9']; correct=1
    if idx==17:
        # Render the combinations with their indices in a readable form.
        opts=['C(5,4)·C(6,2)','C(16,6)','C(9,4)·C(7,2)','C(6,4)·C(10,5)']; correct=2
    if idx==98:
        opts=['C(2018,18)','C(2000,18)','C(1999,17)','C(2000,18)+C(1999,17)']; correct=3
    # Explicitly typeset expressions whose numerator/denominator alignment is split in the PDF.
    if idx==25:
        opts=['(4^2018+4)/3','(4^2018+3)/3','(4^2018+2)/3','(4^2018+1)/3']; correct=2
    if idx==30:
        opts=['0','1/C(2019,2)','2/C(2019,2)','5/C(2019,2)']; correct=1
    if idx==34:
        opts=['4/7','17/35','281/540','2/3']; correct=2
    if idx==48:
        opts=['257/90000','257/18000','127/90000','127/30000']; correct=1
    if idx==62:
        opts=['(366^6−A(366,6))/366^6','(366^6−C(366,6))/366^6','C(366,6)/366^6','A(366,6)/366^6']; correct=0
    if idx==72:
        opts=['3/4','24/49','25/49','1/4']; correct=1
    if idx==73:
        opts=['703/820','701/820','351/410','341/420']; correct=0
    if idx==85:
        opts=['C(50,10)·3^40/4^50','C(50,30)·3^20/4^50','C(50,20)·3^30/4^50','C(50,40)·3^10/4^50']; correct=1
    stem_fixes={
        25:'Có bao nhiêu số tự nhiên chia hết cho 3, biết số đó gồm 2018 chữ số lấy từ tập hợp $X=\{3,5,7,9\}$?',
        30:'Cho $A=\{1,2,\ldots,2019\}$. Chọn ngẫu nhiên đồng thời hai số phân biệt. Tính xác suất để bình phương của số lớn cộng ba lần số bé đều là số chính phương.',
        34:'Cho $A=\{0,1,2,3,4,5,6\}$. Gọi $X$ là tập các số tự nhiên có 5 chữ số khác nhau lập từ $A$. Chọn ngẫu nhiên một số trong $X$. Tính xác suất để số đó có đúng 3 chữ số chẵn.',
        38:'Gọi $S$ là tập các ước nguyên dương của $79413075$. Chọn ngẫu nhiên đồng thời hai phần tử của $S$. Tính xác suất để cả hai số đều không chia hết cho 5.',
        46:'Hai người bắn độc lập vào mục tiêu, mỗi người bắn một lần. Xác suất trúng của người thứ nhất là $0.9$, người thứ hai là $0.7$. Với biến cố $A$ được tạo từ hai biến cố trúng/trượt này, đặt $p=P(A)$. Tìm giá trị lớn nhất của $M=13p-10p^2$.',
        48:'Gọi $A$ là tập các số tự nhiên có 5 chữ số. Chọn ngẫu nhiên một số trong $A$. Tính xác suất để số đó chia hết cho 7 và có chữ số hàng đơn vị bằng 2.',
        62:'Một nhóm 6 người đều sinh năm 2004 (năm nhuận). Tính xác suất để có ít nhất hai người cùng ngày, tháng sinh.',
        72:'Cho $E=\{1,2,3,4,5,6,7\}$. Viết ngẫu nhiên lên bảng hai số tự nhiên có 3 chữ số, mỗi số có các chữ số đôi một khác nhau thuộc $E$. Tính xác suất để trong hai số có đúng một số chứa chữ số 5.',
        73:'Một lớp có 42 học sinh xếp thành vòng tròn. Chọn ngẫu nhiên 3 học sinh. Tính xác suất để không có hai học sinh được chọn đứng kề nhau.',
        85:'Bài thi có 50 câu, mỗi câu đúng được 0.2 điểm, sai bị trừ 0.1 điểm. Hoa chọn ngẫu nhiên một phương án trong 4 phương án ở mỗi câu. Tính xác suất để Hoa đạt đúng 4 điểm.'
    }
    if idx in stem_fixes: stem=stem_fixes[idx]
    if idx==25:
        ex='Gọi $R_n$ là số dãy gồm n chữ số từ $\{3,5,7,9\}$ có tổng chia hết cho 3. Với mỗi tiền tố dài n có tổng dư 0, có 2 cách nối thêm chữ số dư 0; với tổng dư 1 hoặc 2, mỗi loại tiền tố có một cách nối để tổng mới chia hết cho 3. Suy ra $R_{n+1}=R_n+4^n$, còn $R_1=2$. Do đó $R_{2018}=2+4+4^2+\cdots+4^{2017}=(4^{2018}+2)/3$, chọn C.'
    ex=html_lines(after)
    if not ex: raise ValueError(f'question {idx+1}: empty solution')
    # Crop/embed each schematic associated with a question.
    image_map={2:('count-cube-q3.png','Khối lập phương chia thành 8 khối nhỏ'),8:('count-triangle-q9.png','Sơ đồ điền số vào các nút tam giác'),17:('count-grid-q18.png','Lưới ô vuông với các điểm A, B, C'),39:('prob-triangle-q11.svg','Lưới tam giác đều cạnh 8'),88:('prob-polygon-q60.png','Các trường hợp tam giác tạo bởi dây cung đa giác')}
    if idx in image_map:
        file,alt=image_map[idx]
        stem+=f'<br><img src="./quiz-assets/{file}" alt="{esc(alt)}" class="mt-3 max-h-72 max-w-full rounded-lg border border-slate-200 bg-white p-2">'
    chapter=7 if idx<29 else 8
    quiz.append({'chapter':chapter,'question':stem,'options':opts,'correct':correct,'explanation':ex})

# Escape source PDF text before HTML insertion, retain formula delimiters and illustration tags.
for q in quiz:
    # Image HTML was appended as markup; escape only text around the single generated img.
    marker='<br><img src="./quiz-assets/'
    if marker in q['question']:
        pre,rest=q['question'].split(marker,1)
        tagrest=rest.split('>',1)
        img='<br><img src="./quiz-assets/'+tagrest[0]+'>'
        q['question']=esc(pre)+img
    else:
        q['question']=esc(q['question'])
    q['options']=[esc(v) for v in q['options']]

Path('work/new-quiz-data.json').write_text(json.dumps(quiz,ensure_ascii=False,indent=2),encoding='utf-8')
Path('work/new-quiz-diagnostics.txt').write_text(f'generated={len(quiz)} foundation={len(foundation)} sequence-main={len(main_choices)} source-mcq={len(marks)}; chapters=' + json.dumps({c:sum(x['chapter']==c for x in quiz) for c in [6,7,8]}),encoding='utf-8')
print(Path('work/new-quiz-diagnostics.txt').read_text(encoding='utf-8'))

