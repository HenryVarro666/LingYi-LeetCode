CODE = '''
import threading

class FooBar(object):
    def __init__(self, n):
        self.n = n
        self.foo_s = threading.Semaphore(1)
        self.bar_s = threading.Semaphore(0)

    def foo(self, printFoo):
        for i in range(self.n):
            
            self.foo_s.acquire()
            # printFoo() outputs "foo". Do not change or remove this line.
            printFoo()
            self.bar_s.release()

    def bar(self, printBar):
        for i in range(self.n):
            
            self.bar_s.acquire()
            # printBar() outputs "bar". Do not change or remove this line.
            printBar()
            self.foo_s.release()
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


LANES = [dict(name='A', role='foo() × n', color='blue', wait='foo_s'),
         dict(name='B', role='bar() × n', color='pink', wait='bar_s')]
SEMS = [('foo_s', 'blue'), ('bar_s', 'pink')]


def _draw(cv, S, B, box, T):
    _threads_view(cv, S, B, box, T, LANES, SEMS)


def _who(S):
    return f"==线程 {S['_thread']}=="


def acq(sem, why):
    def f(S, B, ret):
        v = _sv(B, sem)
        i = B.get('i', S.get('i', 0)) + 1
        if v == 0:
            return f'{_who(S)} 第 {i} 轮请求 `{sem}`：计数是 0（{why}）→ ==阻塞==，让出 CPU'
        return f'{_who(S)} 第 {i} 轮请求 `{sem}`：计数是 {v} → 拿到许可，可以打印'
    return f


def loop(S, B, ret):
    if 'i' in B and S.get('i') == B['i']:
        return f"{_who(S)} 已经循环了 `n = {S['self.n']}` 轮 → 线程结束"
    return f"{_who(S)} 进入第 {S['i'] + 1} 轮循环（共 `n = {S['self.n']}` 轮）"


def pr(word):
    def f(S, B, ret):
        return (f"{_who(S)} 第 {S['i'] + 1} 轮：拿到自己的许可 → 输出 =={word}==，目前输出："
                f"`{' '.join(S.get('self.out') or [])}`")
    return f


def rel(me, other):
    def f(S, B, ret):
        tail = '这是最后一轮，传完线程就结束' if S['i'] == S['self.n'] - 1 else f'{me} 的许可已用掉，下一轮得等 {other} 再传回来'
        return f"`{other}_s.release()`：把许可传给 {other}（{_sv(B, other + '_s')} → {_sv(S, other + '_s')}），{tail}"
    return f


CONFIG = dict(
    num=1115, title='交替打印FooBar', difficulty='Medium', category='设计',
    author='yiduobo', technique='双信号量交替传球 · 多线程',
    tags=[],
    threads=True,
    code=CODE,
    setup='''
import threading, time, sys
sys.setswitchinterval(100)   # 让每个线程一直跑到阻塞或结束，演示顺序固定
''',
    call='''
fb = FooBar(2)
fb.out = []
fb.st = {'A': 'new', 'B': 'new'}
pfoo = lambda: fb.out.append('foo')
pbar = lambda: fb.out.append('bar')
def body(name, f, p):
    fb.st[name] = 'run'
    f(p)
    fb.st[name] = 'done'
ths = {'A': threading.Thread(target=body, args=('A', fb.foo, pfoo), name='A'),
       'B': threading.Thread(target=body, args=('B', fb.bar, pbar), name='B')}
for k in 'BA':
    ths[k].start()
    time.sleep(0.05)
for k in 'BA':
    ths[k].join()
fb.out
''',
    expect=['foo', 'bar', 'foo', 'bar'],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('foo_s', lambda S: _sv(S, 'foo_s'), 'blue'), ('bar_s', lambda S: _sv(S, 'bar_s'), 'pink'),
           ('out', lambda S: ' '.join(S.get('self.out') or []) or None, 'green')],
    captions={
        'self.n = n': '主线程创建 `FooBar(n)`：`n = {n}`，foo 和 bar 各要打印 {n} 次',
        'self.foo_s = threading': '`foo_s = Semaphore(1)`：foo 手里 ==有 1 个许可==，所以第一个打印的一定是 foo',
        'self.bar_s = threading': '`bar_s = Semaphore(0)`：bar 手里没有许可，必须等 foo 打印完把许可传过来',
        'for i in range': loop,
        'self.foo_s.acquire()': acq('foo_s', 'bar 还没打印完'),
        'self.bar_s.acquire()': acq('bar_s', 'foo 还没打印'),
        'printFoo()': pr('"foo"'),
        'printBar()': pr('"bar"'),
        'self.bar_s.release()': rel('foo', 'bar'),
        'self.foo_s.release()': rel('bar', 'foo'),
    },
    cards=dict(
        one_liner='两个信号量当接力棒：谁有许可谁打印，打完交给对方',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两个线程：一个循环 `n` 次 `foo()`（输出 foo），一个循环 `n` 次 `bar()`（输出 bar）',
                 '要求输出 ==foobar 交替== 共 `n` 对：`n = 2` → `"foobarfoobar"`',
                 '本视频让 bar 线程先启动，它仍然得等 foo'],
        quote='题目要求foo和bar交替执行，foo先执行，那么初始化计数器的时候应该初始化semo_foo为1，semo_bar为0。'
              '在执行printFoo之前需要申请semo_foo，执行完毕之后则需要释放semo_bar',
        quote_src='—— yiduobo 题解原文',
        idea=['每个函数配一个信号量：`foo_s` 初值 1，`bar_s` 初值 0（初值决定谁先）',
              '打印前 `acquire` ==自己的==，打印后 `release` ==对方的==',
              '许可在两个线程之间来回传，每传一次就轮到对方打印一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '初值是关键：先打印的一方信号量设为 1，另一方设为 0',
                 '`acquire` 自己、`release` 对方，别写反，否则两边都卡住（死锁）',
                 '原文为 Python 2 写法，`xrange` 已改为 `range`',
                 '对比 1114：那题许可一路往后传（链），这题在两个线程间来回传（环）'],
    ),
)
