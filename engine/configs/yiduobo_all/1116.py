CODE = '''
import threading

class ZeroEvenOdd(object):
    def __init__(self, n):
        self.n = n
        self.zero_s = threading.Semaphore(1)
        self.even_s = threading.Semaphore(0)
        self.odd_s = threading.Semaphore(0)
        
    # printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber):
        for index in range(1, self.n + 1):
            self.zero_s.acquire()
            printNumber(0)
            if index % 2 == 0:
                self.even_s.release()
            else:
                self.odd_s.release()

        
    def even(self, printNumber):
        for index in range(2, self.n + 1, 2):
            self.even_s.acquire()
            printNumber(index)
            self.zero_s.release()
        
        
    def odd(self, printNumber):
        for index in range(1, self.n + 1, 2):
            self.odd_s.acquire()
            printNumber(index)
            self.zero_s.release()
'''

import re

CODE_LINES = CODE.strip('\n').split('\n')


def _sv(S, name):
    """semaphore counter from a snapshot (threading primitives are stored as text like 'Semaphore(1)')"""
    v = S.get('self.' + name)
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        m = re.search(r'\((\d+)\)', v) or re.search(r'value=(\d+)', v)
        if m:
            return int(m.group(1))
    return None


def _src(S):
    ln = S.get('_line')
    return CODE_LINES[ln - 1].strip() if ln and 0 < ln <= len(CODE_LINES) else ''


def _blocked(S, B):
    """the thread of this step is executing an acquire whose counter is 0 -> it blocks"""
    m = re.search(r'self\.(\w+)\.acquire', _src(S))
    return (m.group(1) if (m and _sv(B, m.group(1)) == 0) else None)


def _cut(cv, s, size, maxw, mono=False, bold=False):
    while len(s) > 1 and cv.tlen(s, size, bold, mono) > maxw:
        s = s[:-2] + '…'
    return s


def _threads_view(cv, S, B, box, T, lanes, sems, name_w=64, extras=()):
    x0, y0, x1, y1 = box
    W = x1 - x0
    lh = max(44, min(84, ((y1 - y0) - 330) / len(lanes)))
    cur = S.get('_thread')
    st = S.get('self.st') or {}
    src = _src(S)
    bsem = _blocked(S, B) if cur in [l['name'] for l in lanes] else None
    y = y0 + 2
    cv.text((x0 + 18, y), '线程（谁在 CPU 上跑）', 22, T['muted'], bold=True)
    y += 36
    for ln in lanes:
        n, c = ln['name'], T[ln['color']]
        s = st.get(n, 'new')
        is_cur = cur == n
        cv.rect((x0 + 10, y, x1 - 10, y + lh - 8), fill=T['panel2'] if is_cur else T['panel'],
                outline=c if is_cur else T['border'], width=3 if is_cur else 1, r=12)
        faded = s in ('new', 'done') and not is_cur
        cv.rect((x0 + 22, y + 6, x0 + 22 + name_w, y + lh - 14), fill=c if not faded else (60, 66, 76), r=10)
        cv.text((x0 + 22 + name_w / 2, y + (lh - 8) / 2), n, 26 if len(n) < 4 else 20, T['bg'], anchor='mm', bold=True)
        tx = x0 + 22 + name_w + 16
        cv.text((tx, y + (lh - 8) / 2), ln['role'], 22, T['text'] if not faded else T['dim'], anchor='lm', mono=True)
        sx = tx + ln.get('role_w', 200)
        mw = x1 - 24 - sx
        if is_cur and s != 'done':
            if bsem:
                cv.text((sx, y + (lh - 8) / 2), _cut(cv, f'{src}   阻塞：{bsem} 是 0，拿不到', 22, mw, True), 22,
                        T['orange'], anchor='lm', mono=True)
            else:
                cv.text((sx, y + (lh - 8) / 2), _cut(cv, '▶ ' + src, 22, mw, True), 22, c, anchor='lm', mono=True, bold=True)
        elif s == 'new':
            cv.text((sx, y + (lh - 8) / 2), '还没启动', 22, T['dim'], anchor='lm')
        elif s == 'done':
            cv.text((sx, y + (lh - 8) / 2), '已执行完毕', 22, T['green'], anchor='lm', bold=True)
        else:
            cv.text((sx, y + (lh - 8) / 2), f'阻塞中，等 {ln["wait"]} 的许可' if ln.get('wait') else '阻塞中', 22,
                    T['orange'], anchor='lm')
        y += lh
    y += 6
    cv.text((x0 + 18, y), '信号量（计数 = 剩余许可数，0 时 acquire 会阻塞）', 22, T['muted'], bold=True)
    y += 36
    m = len(sems) + len(extras)
    gap = 14
    bw = min(300, (W - 20 - (m - 1) * gap) / m)
    bh = 112
    for k, (a, cname) in enumerate(sems):
        X = x0 + 10 + k * (bw + gap)
        v, vb = _sv(S, a), _sv(B, a)
        changed = v is not None and vb is not None and v != vb
        hot = (bsem == a)
        cv.rect((X, y, X + bw, y + bh), fill=T['panel2'], outline=T['orange'] if hot else (T['yellow'] if changed else T['border']),
                width=4 if (hot or changed) else 1, r=14)
        cv.text((X + 14, y + 10), a, 22, T[cname], mono=True, bold=True)
        if v is None:
            cv.text((X + bw / 2, y + bh / 2 + 10), '还没创建', 22, T['dim'], anchor='mm')
            continue
        cv.text((X + bw - 16, y + 8), v, 44, T['text'] if v else T['red'], anchor='ra', bold=True)
        for j in range(min(v, 6)):
            cv.rect((X + 14 + j * 34, y + 62, X + 14 + j * 34 + 26, y + 88), fill=T[cname], r=13)
        if v == 0:
            cv.rect((X + 14, y + 62, X + 40, y + 88), outline=T['dim'], width=2, r=13)
        if hot:
            cv.text((X + bw - 14, y + bh - 12), '阻塞', 20, T['orange'], anchor='rb', bold=True)
        elif changed:
            cv.text((X + bw - 14, y + bh - 12), f'{vb} → {v}', 20, T['yellow'], anchor='rb', bold=True)
    for k, (a, cname) in enumerate(extras):
        X = x0 + 10 + (len(sems) + k) * (bw + gap)
        v, vb = S.get('self.' + a), B.get('self.' + a)
        changed = v is not None and vb is not None and v != vb
        cv.rect((X, y, X + bw, y + bh), fill=T['panel2'], outline=T['yellow'] if changed else T['border'],
                width=4 if changed else 1, r=14)
        cv.text((X + 14, y + 10), a + '（普通变量）', 20, T[cname], mono=True, bold=True)
        if v is not None:
            cv.text((X + bw / 2, y + bh / 2 + 14), v, 52, T['text'], anchor='mm', bold=True)
        if changed:
            cv.text((X + bw - 14, y + bh - 12), f'{vb} → {v}', 20, T['yellow'], anchor='rb', bold=True)
    y += bh + 14
    cv.text((x0 + 18, y), '输出（按打印顺序）', 22, T['muted'], bold=True)
    y += 36
    out = S.get('self.out') or []
    bout = B.get('self.out') or []
    X, Y = x0 + 14, y
    for k, o in enumerate(out):
        w = cv.tlen(str(o), 28, True, True) + 28
        if X + w > x1 - 14:
            X, Y = x0 + 14, Y + 52
        new = k >= len(bout)
        cv.rect((X, Y, X + w, Y + 44), fill=T['yellow'] if new else T['green'], r=10)
        cv.text((X + w / 2, Y + 22), o, 28, T['bg'], anchor='mm', bold=True, mono=True)
        X += w + 10
    if not out:
        cv.text((x0 + 18, y + 6), '（还没有输出）', 22, T['dim'])


LANES = [dict(name='A', role='zero()', color='blue', wait='zero_s', role_w=150),
         dict(name='B', role='even()', color='pink', wait='even_s', role_w=150),
         dict(name='C', role='odd()', color='green', wait='odd_s', role_w=150)]
SEMS = [('zero_s', 'blue'), ('even_s', 'pink'), ('odd_s', 'green')]


def _draw(cv, S, B, box, T):
    _threads_view(cv, S, B, box, T, LANES, SEMS)


def _who(S):
    return f"==线程 {S['_thread']}=="


def acq(sem, why):
    def f(S, B, ret):
        v = _sv(B, sem)
        if v == 0:
            return f'{_who(S)} 请求 `{sem}`：计数是 0（{why}）→ ==阻塞==，让出 CPU'
        return f'{_who(S)} 请求 `{sem}`：计数是 {v} → 拿到许可，可以打印'
    return f


def loop(what):
    def f(S, B, ret):
        if 'index' in B and S.get('index') == B['index']:
            return f'{_who(S)}：{what}都打印完了 → 线程结束'
        return f"{_who(S)} 取下一个：`index = {S['index']}`"
    return f


def rel(sem, what):
    def f(S, B, ret):
        return f"`{sem}.release()`：{what}（{_sv(B, sem)} → {_sv(S, sem)}）"
    return f


def _out(S):
    return ' '.join(S.get('self.out') or [])


CONFIG = dict(
    num=1116, title='打印零与奇偶数', difficulty='Medium', category='设计',
    author='yiduobo', technique='三信号量轮流放行 · 多线程',
    tags=[],
    threads=True,
    code=CODE,
    setup='''
import threading, time, sys
sys.setswitchinterval(100)   # 让每个线程一直跑到阻塞或结束，演示顺序固定
''',
    call='''
z = ZeroEvenOdd(3)
z.out = []
z.st = {'A': 'new', 'B': 'new', 'C': 'new'}
pn = lambda x: z.out.append(str(x))
def body(name, f, p):
    z.st[name] = 'run'
    f(p)
    z.st[name] = 'done'
ths = {'A': threading.Thread(target=body, args=('A', z.zero, pn), name='A'),
       'B': threading.Thread(target=body, args=('B', z.even, pn), name='B'),
       'C': threading.Thread(target=body, args=('C', z.odd, pn), name='C')}
for k in 'CBA':
    ths[k].start()
    time.sleep(0.05)
for k in 'CBA':
    ths[k].join()
''.join(z.out)
''',
    expect='010203',
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('zero_s', lambda S: _sv(S, 'zero_s'), 'blue'), ('even_s', lambda S: _sv(S, 'even_s'), 'pink'),
           ('odd_s', lambda S: _sv(S, 'odd_s'), 'green'), ('out', lambda S: _out(S) or None, 'yellow')],
    captions={
        'self.n = n': '主线程创建对象：`n = {n}`，要输出 `0 1 0 2 0 3`：每个数前面都带一个 0',
        'self.zero_s = threading': '`zero_s = Semaphore(1)`：序列从 0 开始，所以 ==zero 先有许可==',
        'self.even_s = threading': '`even_s = Semaphore(0)`：偶数线程先等着，由 zero 决定什么时候放行',
        'self.odd_s = threading': '`odd_s = Semaphore(0)`：奇数线程同样先等着。（线程按 C、B、A 的顺序启动）',
        'for index in range(1, self.n + 1):': loop('它负责的 0'),
        'for index in range(2, self.n + 1, 2)': loop('它负责的偶数'),
        'for index in range(1, self.n + 1, 2)': loop('它负责的奇数'),
        'self.zero_s.acquire()': acq('zero_s', '上一个数还没打印完'),
        'self.even_s.acquire()': acq('even_s', 'zero 还没放行偶数'),
        'self.odd_s.acquire()': acq('odd_s', 'zero 还没放行奇数'),
        'printNumber(0)': lambda S, B, r: f"{_who(S)} 拿到 `zero_s` → 输出 ==\"0\"==，目前输出：`{_out(S)}`",
        'printNumber(index)': lambda S, B, r: f"{_who(S)} 拿到许可 → 输出 =={S['index']}==，目前输出：`{_out(S)}`",
        'if index % 2 == 0': lambda S, B, r: (f"这是第 `{S['index']}` 个 0：`{S['index']} % 2 == 0` 成立 → 后面该输出偶数 {S['index']}，放行 even"
                                              if S['index'] % 2 == 0 else
                                              f"这是第 `{S['index']}` 个 0：`{S['index']} % 2 == 0` 不成立 → 后面该输出奇数 {S['index']}，放行 odd"),
        'self.even_s.release()': rel('even_s', '许可交给 even，轮到偶数打印'),
        'self.odd_s.release()': rel('odd_s', '许可交给 odd，轮到奇数打印'),
        'self.zero_s.release()': rel('zero_s', '许可还给 zero，下一个又该打印 0'),
    },
    cards=dict(
        one_liner='zero 当调度员：打印 0 后放行奇或偶，奇偶打印完再还给 zero',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['三个线程共用 `printNumber(x)`：`zero` 只输出 0，`even` 只输出偶数，`odd` 只输出奇数',
                 '要求输出 ==0102…0n==：`n = 3` → `"010203"`',
                 '本视频线程按 odd、even、zero 的顺序启动，zero 最后才出场'],
        quote='zero中的print只能输出0，那么在print之前需要申请semo_zero，而print之后则需要根据当前是执行的第几次zero来决定后续执行什么，'
              '即应该释放semo_odd还是semo_even。',
        quote_src='—— yiduobo 题解原文',
        idea=['三个角色三个信号量：`zero_s` 初值 1（先打 0），`even_s`、`odd_s` 初值 0',
              'zero 打印 0 后看这是第几个：==奇数 → 放行 odd，偶数 → 放行 even==',
              'odd / even 打印完都 `release zero_s`，让下一个 0 出场',
              '于是顺序固定成：0 → 奇 → 0 → 偶 → 0 → 奇 …'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 'zero 是总调度员：只有它知道下一个该放行谁',
                 '`even` / `odd` 的循环次数要和 zero 发出的许可数对上，否则有线程永远阻塞',
                 '原文代码 Python 3 可直接运行，只把注释行里的制表符改成了空格',
                 '对比 1115：两个角色变成三个，多了一步「按奇偶分发」'],
    ),
)
