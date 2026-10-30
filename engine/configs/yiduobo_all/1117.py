CODE = '''
import threading

class H2O(object):
    def __init__(self):
        self.h_s = threading.Semaphore(2)
        self.o_s = threading.Semaphore(0)
        self.h_cnt = 0

    def hydrogen(self, releaseHydrogen):
        self.h_s.acquire()
        # releaseHydrogen() outputs "H". Do not change or remove this line.
        releaseHydrogen()
        self.h_cnt += 1
        if self.h_cnt == 2:
            self.h_cnt = 0
            self.o_s.release()

    def oxygen(self, releaseOxygen):
        self.o_s.acquire(2)
        # releaseOxygen() outputs "O". Do not change or remove this line.
        releaseOxygen()
        self.h_s.release()
        self.h_s.release()
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


LANES = [dict(name='H1', role='hydrogen()', color='blue', wait='h_s', role_w=150),
         dict(name='H2', role='hydrogen()', color='blue', wait='h_s', role_w=150),
         dict(name='H3', role='hydrogen()', color='blue', wait='h_s', role_w=150),
         dict(name='O1', role='oxygen()', color='pink', wait='o_s', role_w=150),
         dict(name='H4', role='hydrogen()', color='blue', wait='h_s', role_w=150),
         dict(name='O2', role='oxygen()', color='pink', wait='o_s', role_w=150)]
SEMS = [('h_s', 'blue'), ('o_s', 'pink')]


def _draw(cv, S, B, box, T):
    _threads_view(cv, S, B, box, T, LANES, SEMS, extras=[('h_cnt', 'yellow')])


def _who(S):
    return f"==线程 {S['_thread']}=="


def _out(S):
    return ' '.join(S.get('self.out') or [])


def acq(sem, why):
    def f(S, B, ret):
        v = _sv(B, sem)
        if v == 0:
            return f'{_who(S)} 请求 `{sem}`：计数是 0（{why}）→ ==阻塞==，让出 CPU'
        return f'{_who(S)} 请求 `{sem}`：计数是 {v} → 拿到许可，继续往下'
    return f


def rel_h(S, B, ret):
    a, b = _sv(B, 'h_s'), _sv(S, 'h_s')
    tail = '，再补一个' if b < 2 else '，名额补满 2 个，下一批 H 可以上了'
    return f'`h_s.release()`：氢的名额 {a} → {b}{tail}'


def if_cnt(S, B, ret):
    c = S['self.h_cnt']
    if c == 2:
        return '`h_cnt == 2`：这一批 2 个 H 都打印完了 → ==成立==，该通知氧线程了'
    return f'`h_cnt = {c}`，不等于 2 → 这一批还差 {2 - c} 个 H，先不通知氧线程'


CONFIG = dict(
    num=1117, title='H2O 生成', difficulty='Medium', category='设计',
    author='yiduobo', technique='信号量 + 全局计数 · 多线程',
    tags=[],
    threads=True,
    code=CODE,
    setup='''
import threading, time, sys
sys.setswitchinterval(100)   # 让每个线程一直跑到阻塞或结束，演示顺序固定
''',
    call='''
h2o = H2O()
h2o.out = []
h2o.st = {k: 'new' for k in ['H1', 'H2', 'H3', 'O1', 'H4', 'O2']}
rh = lambda: h2o.out.append('H')
ro = lambda: h2o.out.append('O')
def body(name, f, p):
    h2o.st[name] = 'run'
    f(p)
    h2o.st[name] = 'done'
order = ['H1', 'H2', 'H3', 'O1', 'H4', 'O2']
ths = {k: threading.Thread(target=body, args=(k, h2o.hydrogen if k[0] == 'H' else h2o.oxygen, rh if k[0] == 'H' else ro), name=k)
       for k in order}
for k in order:
    ths[k].start()
    time.sleep(0.05)
for k in order:
    ths[k].join()
''.join(h2o.out)
''',
    expect='HHOHHO',
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('h_s', lambda S: _sv(S, 'h_s'), 'blue'), ('o_s', lambda S: _sv(S, 'o_s'), 'pink'),
           ('h_cnt', 'self.h_cnt', 'yellow'), ('out', lambda S: _out(S) or None, 'green')],
    captions={
        'self.h_s = threading': '`h_s = Semaphore(2)`：氢线程一批最多放行 ==2 个==，因为一个水分子要 2 个 H',
        'self.o_s = threading': '`o_s = Semaphore(0)`：氧线程先等着，要等 2 个 H 都打印完才放行',
        7: '`h_cnt = 0`：额外记「这一批已打印几个 H」。原文说 Python 的信号量看不到计数，所以用一个变量代替',
        'self.h_s.acquire()': acq('h_s', '这一批 2 个 H 的名额已用完，要等氧线程补充'),
        'self.o_s.acquire(2)': acq('o_s', '2 个 H 还没都打印完'),
        'releaseHydrogen()': lambda S, B, r: f'{_who(S)} 拿到名额 → 输出 =="H"==，目前输出：`{_out(S)}`',
        'releaseOxygen()': lambda S, B, r: f'{_who(S)} 拿到 `o_s` → 输出 =="O"==，目前输出：`{_out(S)}`',
        'self.h_cnt += 1': lambda S, B, r: f"打印完一个 H：`h_cnt` {B['self.h_cnt']} → {S['self.h_cnt']}",
        'if self.h_cnt == 2': if_cnt,
        15: '一批满了：`h_cnt` 清零，准备记下一批',
        'self.o_s.release()': '`o_s.release()`：计数 0 → 1，告诉氧线程 =="2 个 H 都好了，可以出 O"=='
                              '，氧线程拿到许可就能打印 O',
        'self.h_s.release()': rel_h,
    },
    cards=dict(
        one_liner='H 信号量放行 2 个，计数凑满后通知 O；O 打印完再补 2 个名额',
        complexity='时间 `O(1)`（每个线程），空间 `O(1)`',
        problem=['水分子 `H2O`：一个氧线程 + 两个氢线程凑成一组才能输出',
                 '每个线程调用 `releaseHydrogen()`（输出 H）或 `releaseOxygen()`（输出 O）',
                 '输出里每连续 3 个字符必须是一个水分子，如 `"HHO"`、`"HOH"`',
                 '本视频：4 个 H、2 个 O，启动顺序 H1 H2 H3 O1 H4 O2 → `"HHOHHO"`'],
        quote='H的计数器应该设为2，而O的计数器则设为0。当执行完某次releaseHydrogen之后，若当前的semo_H的计数器为0，那么才能释放掉semo_O。'
              '而执行完releaseOxygen之后，则需要将semo_H的计数器加上2。',
        quote_src='—— yiduobo 题解原文',
        idea=['`h_s = Semaphore(2)`：一批只放 2 个 H 进来；`o_s = Semaphore(0)`：O 先等着',
              '每个 H 打印完 `h_cnt += 1`，数到 2 说明 ==2 个 H 都好了==，才 `o_s.release()`',
              'O 打印完 `h_s.release()` 两次，把 2 个名额还回去，下一批 H 才能上',
              '第 3 个 H 会卡在 `h_s.acquire()`，直到 O 出来，保证 H、O 不会错批'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`h_cnt += 1` 不是原子操作，两个 H 并发时理论上有竞态（原文也说这个变量「不优美」）',
                 '`acquire(2)` 里的 2 其实是 `blocking` 参数，等价于 `acquire()`，只拿 1 个许可',
                 '原文代码 Python 3 可直接运行，无需修改',
                 '要点：H 名额 = 2，O 名额 = 0，「凑满 2 个 H 才放行 O，O 打完再补 2 个名额」'],
    ),
)
