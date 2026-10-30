CODE = '''
import threading

class Foo(object):
    def __init__(self):
        self.first_s = threading.Semaphore(0)
        self.second_s = threading.Semaphore(0)

    def first(self, printFirst):
        
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.first_s.release()

    def second(self, printSecond):
        
        self.first_s.acquire()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.second_s.release()
            
    def third(self, printThird):
        
        self.second_s.acquire()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()
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


LANES = [dict(name='A', role='first()', color='blue', wait=None),
         dict(name='B', role='second()', color='pink', wait='first_s'),
         dict(name='C', role='third()', color='green', wait='second_s')]
SEMS = [('first_s', 'cyan'), ('second_s', 'orange')]


def _draw(cv, S, B, box, T):
    _threads_view(cv, S, B, box, T, LANES, SEMS)


def _who(S):
    return f"==线程 {S['_thread']}=="


def acq(sem, why):
    def f(S, B, ret):
        v = _sv(B, sem)
        if v == 0:
            return f'{_who(S)} 请求 `{sem}`：计数是 0（{why}）→ ==阻塞==，让出 CPU 给别的线程'
        return f'{_who(S)} 请求 `{sem}`：计数是 {v} → 拿到许可，继续往下'
    return f


CONFIG = dict(
    num=1114, title='按序打印', difficulty='Easy', category='设计',
    author='yiduobo', technique='信号量接力 · 多线程',
    tags=[],
    threads=True,
    code=CODE,
    setup='''
import threading, time, sys
sys.setswitchinterval(100)   # 让每个线程一直跑到阻塞或结束，演示顺序固定
''',
    call='''
foo = Foo()
foo.out = []
foo.st = {'A': 'new', 'B': 'new', 'C': 'new'}
pf = lambda: foo.out.append('first')
ps = lambda: foo.out.append('second')
pt = lambda: foo.out.append('third')
def body(name, f, p):
    foo.st[name] = 'run'
    f(p)
    foo.st[name] = 'done'
ths = {'A': threading.Thread(target=body, args=('A', foo.first, pf), name='A'),
       'B': threading.Thread(target=body, args=('B', foo.second, ps), name='B'),
       'C': threading.Thread(target=body, args=('C', foo.third, pt), name='C')}
for k in 'CBA':
    ths[k].start()
    time.sleep(0.05)
for k in 'CBA':
    ths[k].join()
foo.out
''',
    expect=['first', 'second', 'third'],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('first_s', lambda S: _sv(S, 'first_s'), 'cyan'), ('second_s', lambda S: _sv(S, 'second_s'), 'orange'),
           ('out', lambda S: ' '.join(S.get('self.out') or []) or None, 'green')],
    captions={
        'self.first_s = threading': '主线程创建对象：`first_s = Semaphore(0)`，0 个许可，表示 =="first 还没打印完"=='
                                    '（后面线程按 C、B、A 的最乱顺序启动）',
        'self.second_s = threading': '`second_s = Semaphore(0)`：=="second 还没打印完"==。两个信号量就是两道门，先都关着',
        'self.second_s.acquire()': acq('second_s', 'second 还没打印'),
        'self.first_s.acquire()': acq('first_s', 'first 还没打印'),
        'printFirst()': '==线程 A== 第一个方法不用等任何人，直接 `printFirst()` → 输出 =="first"==',
        'self.first_s.release()': '`first_s.release()`：计数 0 → 1，相当于告诉 second =="first 已经打印完了"==，'
                                  '阻塞在这里的线程 B 被唤醒',
        'printSecond()': '==线程 B== 拿到 `first_s` 的许可（A 已经 release）→ 轮到它 `printSecond()` → 输出 =="second"==',
        'self.second_s.release()': '`second_s.release()`：计数 0 → 1，通知 third =="second 已经打印完了"==，线程 C 被唤醒',
        'printThird()': '==线程 C== 拿到 `second_s` 的许可 → `printThird()` → 输出 =="third"==，'
                        '三个线程接力完成：`first second third`',
    },
    cards=dict(
        one_liner='两个信号量当两道门，first → second → third 接力放行',
        complexity='时间 `O(1)`，空间 `O(1)`（两个信号量）',
        problem=['三个线程分别调用 `first()`、`second()`、`third()`',
                 '线程谁先启动不确定，但输出必须是 ==first、second、third==',
                 '本视频让线程按 C、B、A 的顺序启动，是最乱的情况，结果仍是 `firstsecondthird`'],
        quote='设置两个信号量first_semo以及second_semo用来表示first和second是否执行完毕。'
              '对于second，初始需要请求first_semo。只有当printFirst执行完毕，first_semo release掉之后才能请求到',
        quote_src='—— yiduobo 题解原文',
        idea=['`Semaphore(0)` 就是一道关着的门：`acquire` 拿不到许可就阻塞',
              '`first` 打印完 `release` 第一道门，`second` 才能通过',
              '`second` 打印完再 `release` 第二道门，`third` 才能通过',
              '不管谁先启动，后面的线程都会先卡在 `acquire` 上等前一个'],
        before=[dict(heading='信号量是什么', chapter='② 概念',
                     lines=['`Semaphore(n)` 里存着 n 个许可', '`acquire()`：许可 > 0 就拿走一个继续；==等于 0 就阻塞==',
                            '`release()`：许可加 1，并唤醒在等的线程', '计数器画在右边：圆点个数 = 剩余许可数'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '初值必须是 0：门一开始是关着的，只有前一个线程 `release` 才会开',
                 '`first` 不需要 `acquire`，因为它没有前驱',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '同类题：1115、1116、1117、1195，都是给每个角色配信号量'],
    ),
)
