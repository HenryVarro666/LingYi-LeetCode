CODE = '''
import threading

class FizzBuzz(object):
    def __init__(self, n):
        self.n = n
        self.f_s = threading.Semaphore(0)
        self.b_s = threading.Semaphore(0)
        self.fb_s = threading.Semaphore(0)
        self.num_s = threading.Semaphore(1)

    # printFizz() outputs "fizz"
    def fizz(self, printFizz):
        for index in range(3, self.n + 1, 3):
            if index % 5 != 0:
                self.f_s.acquire()
                printFizz()
                self.num_s.release()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz):
        for index in range(5, self.n + 1, 5):
            if index % 3 != 0:
                self.b_s.acquire()
                printBuzz()
                self.num_s.release()

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz):
        for index in range(15, self.n + 1, 15):
            self.fb_s.acquire()
            printFizzBuzz()
            self.num_s.release()

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber):
        for index in range(1, self.n + 1):
            self.num_s.acquire()
            if index % 3 == 0:
                if index % 5 == 0:
                    self.fb_s.release()
                else:
                    self.f_s.release()
            elif index % 5 == 0:
                self.b_s.release()
            else:
                printNumber(index)
                self.num_s.release()
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


LANES = [dict(name='A', role='fizz()', color='blue', wait='f_s', role_w=170),
         dict(name='B', role='buzz()', color='pink', wait='b_s', role_w=170),
         dict(name='C', role='fizzbuzz()', color='purple', wait='fb_s', role_w=170),
         dict(name='D', role='number()', color='green', wait='num_s', role_w=170)]
SEMS = [('f_s', 'blue'), ('b_s', 'pink'), ('fb_s', 'purple'), ('num_s', 'green')]


def _draw(cv, S, B, box, T):
    _threads_view(cv, S, B, box, T, LANES, SEMS)


def _who(S):
    return f"==线程 {S['_thread']}=="


def _out(S):
    return ' '.join(S.get('self.out') or [])


def acq(sem, why):
    def f(S, B, ret):
        v = _sv(B, sem)
        pre = f"{_who(S)} 处理 `index = {B['index']}`：" if sem == 'num_s' else f'{_who(S)} '
        if v == 0:
            return f'{pre}请求 `{sem}`：计数 0（{why}）→ ==阻塞==，让出 CPU'
        return f'{pre}请求 `{sem}`：计数 {v} → 拿到许可'
    return f


def loop(what):
    def f(S, B, ret):
        if 'index' in B and S.get('index') == B['index']:
            return f'{_who(S)}：{what}都处理完了 → 线程结束'
        return f"{_who(S)} 取{what}：`index = {S['index']}`"
    return f


def deliver(sem, word, k):
    def f(S, B, ret):
        tail = '这是最后一个数，number 随后结束' if S['index'] == S['self.n'] else 'number ==不 release== `num_s`，下一轮先等它打完'
        return f"`{sem}.release()`：{S['index']} 是 {k} 的倍数 → 许可交给 =={word}==（{_sv(B, sem)} → {_sv(S, sem)}），{tail}"
    return f


def done_print(word):
    def f(S, B, ret):
        return f"{_who(S)} 拿到 `{word[0]}_s` → 输出 =={word[1]}==，目前输出：`{_out(S)}`"
    return f


def rel_num(S, B, ret):
    if S['_thread'] == 'D':
        return '数字打印完 → `num_s.release()`：number 自己放行下一个数'
    return (f"字符串打印完 → `num_s.release()`：把「处理下一个数」的许可还给 number"
            f"（{_sv(B, 'num_s')} → {_sv(S, 'num_s')}）")


CONFIG = dict(
    num=1195, title='交替打印字符串', difficulty='Medium', category='设计',
    author='yiduobo', technique='number 调度 + 四信号量 · 多线程',
    tags=[],
    threads=True,
    code=CODE,
    setup='''
import threading, time, sys
sys.setswitchinterval(100)   # 让每个线程一直跑到阻塞或结束，演示顺序固定
''',
    call='''
fbz = FizzBuzz(5)
fbz.out = []
fbz.st = {k: 'new' for k in 'ABCD'}
pfz = lambda: fbz.out.append('fizz')
pbz = lambda: fbz.out.append('buzz')
pfb = lambda: fbz.out.append('fizzbuzz')
pnum = lambda x: fbz.out.append(str(x))
def body(name, f, p):
    fbz.st[name] = 'run'
    f(p)
    fbz.st[name] = 'done'
fs = {'A': (fbz.fizz, pfz), 'B': (fbz.buzz, pbz), 'C': (fbz.fizzbuzz, pfb), 'D': (fbz.number, pnum)}
ths = {k: threading.Thread(target=body, args=(k, fs[k][0], fs[k][1]), name=k) for k in 'ABCD'}
for k in 'ABCD':
    ths[k].start()
    time.sleep(0.05)
for k in 'ABCD':
    ths[k].join()
fbz.out
''',
    expect=['1', '2', 'fizz', '4', 'buzz'],
    skip=['for index in range(3, self.n', 'for index in range(5, self.n', 'for index in range(1, self.n'],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('f_s', lambda S: _sv(S, 'f_s'), 'blue'), ('b_s', lambda S: _sv(S, 'b_s'), 'pink'),
           ('fb_s', lambda S: _sv(S, 'fb_s'), 'purple'), ('num_s', lambda S: _sv(S, 'num_s'), 'green'),
           ('out', lambda S: _out(S) or None, 'yellow')],
    captions={
        'self.n = n': '主线程创建对象：`n = {n}`，输出 1…n，3 的倍数 fizz，5 的倍数 buzz，15 的倍数 fizzbuzz',
        'self.f_s = threading': '`f_s = Semaphore(0)`：fizz 线程的开关，==关着==，number 发现 3 的倍数才打开',
        'self.b_s = threading': '`b_s = Semaphore(0)`：buzz 的开关，也关着',
        'self.fb_s = threading': '`fb_s = Semaphore(0)`：fizzbuzz 的开关，也关着',
        'self.num_s = threading': '`num_s = Semaphore(1)`：==number 的开关，开着==，由它调度每个数',
        'for index in range(3, self.n + 1, 3)': loop('下一个 3 的倍数'),
        'for index in range(5, self.n + 1, 5)': loop('下一个 5 的倍数'),
        'for index in range(15, self.n + 1, 15)': lambda S, B, r: (
            f"{_who(S)}：`range(15, {S['self.n'] + 1}, 15)` 是空的，`n = {S['self.n']}` 还不到 15 → 这个线程什么也不打印，直接结束"
            if 15 > S['self.n'] else f"{_who(S)} 取 15 的倍数：`index = {S['index']}`"),
        'for index in range(1, self.n + 1)': loop('下一个数'),
        'if index % 5 != 0': lambda S, B, r: f"`{S['index']} % 5 != 0` ==成立==：{S['index']} 只是 3 的倍数，由 fizz 负责（15 的倍数归 fizzbuzz）",
        'if index % 3 != 0': lambda S, B, r: f"`{S['index']} % 3 != 0` ==成立==：{S['index']} 只是 5 的倍数，由 buzz 负责（15 的倍数归 fizzbuzz）",
        'self.f_s.acquire()': acq('f_s', 'number 还没发现 3 的倍数'),
        'self.b_s.acquire()': acq('b_s', 'number 还没发现 5 的倍数'),
        'self.fb_s.acquire()': acq('fb_s', 'number 还没发现 15 的倍数'),
        'self.num_s.acquire()': acq('num_s', '上一个数还在打印'),
        'printFizz()': done_print(('f', '"fizz"')),
        'printBuzz()': done_print(('b', '"buzz"')),
        'printFizzBuzz()': done_print(('fb', '"fizzbuzz"')),
        'printNumber(index)': lambda S, B, r: (f"{_who(S)} `{S['index']}` 不是 3、5 的倍数 → 自己输出 =={S['index']}==，目前输出：`{_out(S)}`"),
        'self.num_s.release()': rel_num,
        'if index % 3 == 0': lambda S, B, r: (f"`{S['index']} % 3 == 0` ==成立==：3 的倍数，再看是否 15 的倍数"
                                              if S['index'] % 3 == 0 else
                                              f"`{S['index']} % 3 == 0` 不成立：不是 3 的倍数"),
        'elif index % 5 == 0': lambda S, B, r: (f"`{S['index']} % 5 == 0` ==成立==：5 的倍数 → 交给 buzz"
                                                if S['index'] % 5 == 0 else
                                                f"`{S['index']} % 5 == 0` 不成立：普通数字，自己打印"),
        'if index % 5 == 0': lambda S, B, r: (f"`{S['index']} % 5 == 0` ==成立==：也是 5 的倍数 → fizzbuzz"
                                              if S['index'] % 5 == 0 else
                                              f"`{S['index']} % 5 == 0` 不成立：只是 3 的倍数 → fizz"),
        'self.fb_s.release()': deliver('fb_s', 'fizzbuzz', '15'),
        'self.f_s.release()': deliver('f_s', 'fizz', '3'),
        'self.b_s.release()': deliver('b_s', 'buzz', '5'),
    },
    cards=dict(
        one_liner='所有数都经 number 调度：普通数自己打，3/5/15 的倍数交给字符串线程',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['四个线程：`fizz`、`buzz`、`fizzbuzz` 输出对应字符串，`number` 输出数字',
                 '对 1…n：3 的倍数 fizz，5 的倍数 buzz，15 的倍数 fizzbuzz，否则输出数字本身',
                 '本视频 `n = 5` → `1 2 fizz 4 buzz`（n < 15，fizzbuzz 线程用不上）'],
        quote='所有打印任务都经过number，由number控制当前应该直接打印数字，还是唤起打印字符串的线程，'
              '那么可以使用三个信号量分别控制fizz、buzz以及fizzbuzz的输出，然后使用另一个信号量负责控制number。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f_s`、`b_s`、`fb_s` 初值 0（字符串线程先等着）；`num_s` 初值 1（number 先跑）',
              'number 逐个处理：普通数自己打印并 `release(num_s)`；3 / 5 / 15 的倍数只 `release` 对应线程，==不 release num_s==',
              '字符串线程打印完才 `release(num_s)`，number 才处理下一个数 → 严格按 1…n 的顺序'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`num_s` 是总闸：同一时刻只有一个线程在工作，所以输出不会乱序',
                 'fizz / buzz 线程里的 `index % 5 != 0`、`index % 3 != 0` 要和 number 的分发条件配套，否则有线程永远等不到许可',
                 '原文缩进里混了制表符，已改成空格，代码逻辑未改；n ≥ 15 时第 15 个数走 `fb_s`'],
    ),
)
