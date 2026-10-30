CODE = '''
import threading

class DiningPhilosophers(object):

    def __init__(self):
        self.s_list = [threading.Semaphore(1) for _ in range(5)]

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self, philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork):

        l_s = self.s_list[philosopher]
        r_s = self.s_list[(philosopher + 4) % 5]

        if philosopher % 2 == 0:
            l_s.acquire()
            pickLeftFork()
            r_s.acquire()
            pickRightFork()
            eat()
            putRightFork()
            r_s.release()
            putLeftFork()
            l_s.release()
        else:
            r_s.acquire()
            pickRightFork()
            l_s.acquire()
            pickLeftFork()
            eat()
            putLeftFork()
            l_s.release()
            putRightFork()
            r_s.release()
'''

import re

CODE_LINES = CODE.strip('\n').split('\n')
ACT_TXT = {'pickLeft': '拿起左叉', 'pickRight': '拿起右叉', 'eat': '开始吃饭', 'putLeft': '放下左叉', 'putRight': '放下右叉'}
IDC = ['blue', 'pink', 'purple', 'cyan', 'yellow']   # 每位哲学家一种颜色


def _val(S, name):
    v = S.get(name)
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        m = re.search(r'\((\d+)\)', v) or re.search(r'value=(\d+)', v)
        if m:
            return int(m.group(1))
    return None


def _forks(S):
    v = S.get('self.s_list')
    if isinstance(v, str):
        return [int(x) for x in re.findall(r'value=(\d+)', v)]
    if isinstance(v, list):
        return [x for x in (_val({'x': i}, 'x') for i in v) if x is not None]
    return []


def _hold(log):
    hold = [None] * 5
    for p, a in log:
        if a == 'pickLeft':
            hold[p] = p
        elif a == 'pickRight':
            hold[(p + 4) % 5] = p
        elif a == 'putLeft':
            hold[p] = None
        elif a == 'putRight':
            hold[(p + 4) % 5] = None
    return hold


def _src(S):
    ln = S.get('_line')
    return CODE_LINES[ln - 1].strip() if ln and 0 < ln <= len(CODE_LINES) else ''


def _first_second(p):
    L, R = p, (p + 4) % 5
    return (L, R, '左', '右') if p % 2 == 0 else (R, L, '右', '左')


def _blocked_fork(S, B):
    """fork index the current thread is blocked on (executing acquire on a taken fork), else None"""
    m = re.match(r'(l_s|r_s)\.acquire', _src(S))
    if not m or 'philosopher' not in B:
        return None
    p = B['philosopher']
    k = p if m.group(1) == 'l_s' else (p + 4) % 5
    return k if _val(B, m.group(1)) == 0 else None


def _cut(cv, s, size, maxw, bold=False, mono=False):
    while len(s) > 1 and cv.tlen(s, size, bold, mono) > maxw:
        s = s[:-2] + '…'
    return s


def _info(S, B):
    """每位哲学家此刻的状态：(kind, 文字, 在等的叉子)；以及 叉子持有者、当前线程对应的哲学家"""
    log = S.get('self.log') or []
    st = S.get('self.st') or {}
    cur = S.get('_thread')
    forks = _forks(S)
    hold = _hold(log)
    bk = _blocked_fork(S, B)
    curp = int(cur[1:]) if cur and cur[0] == 'P' and cur[1:].isdigit() else None
    info = {}
    for p in range(5):
        s = st.get(p, 'new')
        mine = [a for q, a in log if q == p]
        last = mine[-1] if mine else None
        first, second, fn, sn = _first_second(p)
        picks = [a for a in mine if a.startswith('pick')]
        if s == 'new':
            info[p] = ('new', '还没入座', None)
        elif s == 'done':
            info[p] = ('done', '吃完了，叉子都放回了', None)
        elif p == curp and bk is not None:
            info[p] = ('blocked', f'阻塞：f{bk} 被 P{hold[bk]} 拿着' if hold[bk] is not None else f'阻塞：f{bk} 已被拿走', bk)
        elif p == curp:
            info[p] = ('run', '▶ ' + _src(S), None)
        elif last == 'eat':
            info[p] = ('eat', '正在吃饭', None)
        elif last in ('putLeft', 'putRight'):
            info[p] = ('put', '放叉子中', None)
        else:
            k = first if len(picks) == 0 else second
            h = hold[k]
            if h is not None:
                t = f'等 f{k}（P{h} 拿着）'
            elif k < len(forks) and forks[k] == 0:
                t = f'刚拿到 f{k}，马上拿起'
            else:
                t = f'f{k} 已空出，等被唤醒'
            info[p] = ('blocked', t, k)
    return info, hold, forks, curp, bk


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    log = S.get('self.log') or []
    blog = B.get('self.log') or []
    info, hold, forks, curp, bk = _info(S, B)
    # ---------------- 圆桌
    cx, cy, R = x0 + 250, y0 + 254, 160
    cv.text((x0 + 18, y0 + 2), '圆桌（叉子在两位哲学家之间）', 22, T['muted'], bold=True)
    cv.d.ellipse((cx - 90, cy - 90, cx + 90, cy + 90), fill=T['panel2'], outline=T['border'], width=2)
    cv.text((cx, cy), '桌子', 26, T['dim'], anchor='mm')
    ang = lambda p: math.radians(-90 + 72 * p)
    # 叉子 k 在 P_k 与 P_(k+1) 之间
    for k in range(5):
        h = hold[k]
        if h is None:
            a, col, w = ang(k) + math.radians(36), (150, 158, 170), 7
        else:
            a = ang(h) + math.radians(14 if h == k else -14)
            col, w = T[IDC[h]], 9
        r0, r1 = (96, 130) if h is not None else (98, 132)
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        p1 = (cx + r1 * math.cos(a), cy + r1 * math.sin(a))
        cv.line([p0, p1], col, w)
        cv.d.ellipse((p1[0] - 7, p1[1] - 7, p1[0] + 7, p1[1] + 7), fill=col)
        am = ang(k) + math.radians(36)
        lx, ly = cx + 168 * math.cos(am), cy + 168 * math.sin(am)
        v = forks[k] if k < len(forks) else '?'
        cv.text((lx, ly), f'f{k}', 20, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((lx, ly + 20), f'={v}', 17, T['green'] if v == 1 else T['red'], anchor='mm', bold=True, mono=True)
    # ---------------- 哲学家节点
    for p in range(5):
        a = ang(p)
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        kind = info[p][0]
        col = T[IDC[p]]
        fill = {'new': T['panel'], 'done': (52, 58, 68)}.get(kind, col)
        ring = {'blocked': T['orange'], 'eat': T['green']}.get(kind)
        if p == curp:
            cv.d.ellipse((px - 52, py - 52, px + 52, py + 52), outline=T['text'], width=3)
        cv.d.ellipse((px - 42, py - 42, px + 42, py + 42), fill=fill, outline=ring or T['border'], width=6 if ring else 2)
        tc = T['bg'] if kind in ('run', 'blocked', 'eat', 'put') else T['dim']
        cv.text((px, py - 6), f'P{p}', 28, tc, anchor='mm', bold=True)
        cv.text((px, py + 20), {'new': '未到', 'done': '吃完', 'blocked': '等叉', 'run': '在跑', 'eat': '吃饭', 'put': '放叉'}[kind],
                18, tc, anchor='mm', bold=True)
    # ---------------- 右侧：每位哲学家一行
    rx = x0 + 520
    cv.text((rx, y0 + 2), '哲学家（奇偶拿叉顺序不同）', 22, T['muted'], bold=True)
    ry, rh = y0 + 38, 78
    for p in range(5):
        first, second, fn, sn = _first_second(p)
        kind, txt, _t = info[p]
        cv.rect((rx, ry, x1 - 10, ry + rh - 8), fill=T['panel2'] if p == curp else T['panel'],
                outline=T[IDC[p]] if p == curp else T['border'], width=3 if p == curp else 1, r=12)
        cv.rect((rx + 10, ry + 10, rx + 62, ry + rh - 18), fill=T[IDC[p]] if kind not in ('new', 'done') else (60, 66, 76), r=10)
        cv.text((rx + 36, ry + (rh - 8) / 2), f'P{p}', 24, T['bg'], anchor='mm', bold=True)
        cv.text((rx + 76, ry + 8), f"{'偶' if p % 2 == 0 else '奇'}数：先{fn} f{first}，再{sn} f{second}", 20, T['muted'])
        colr = {'blocked': T['orange'], 'eat': T['green'], 'done': T['green'], 'new': T['dim'], 'put': T['yellow']}.get(kind, T[IDC[p]])
        bd = kind in ('blocked', 'run')
        cv.text((rx + 76, ry + 38), _cut(cv, txt, 22, x1 - 26 - (rx + 76), bd, kind == 'run'), 22, colr, bold=bd,
                mono=(kind == 'run'))
        ry += rh
    # ---------------- 动作记录
    ly = y0 + 456
    cv.text((x0 + 18, ly), '叉子动作记录（最近 5 条，传给 LeetCode 的输出）', 22, T['muted'], bold=True)
    ly += 32
    recent = log[-5:]
    for j, (p, a) in enumerate(recent):
        fk = p if a.endswith('Left') else ((p + 4) % 5 if a.endswith('Right') else None)
        new = len(log) - len(recent) + j >= len(blog)
        cv.rect((x0 + 18, ly + 3, x0 + 26, ly + 21), fill=T[IDC[p]], r=3)
        cv.text((x0 + 40, ly), f"P{p}  {ACT_TXT[a]}" + (f' f{fk}' if fk is not None else ''), 21,
                T['yellow'] if new else T['text'], bold=new)
        ly += 26
    if not log:
        cv.text((x0 + 18, ly), '（还没有动作）', 21, T['dim'])


def _P(B):
    return B['philosopher']


def acq(S, B, ret):
    p = _P(B)
    m = re.match(r'(l_s|r_s)', _src(S))
    k = p if m.group(1) == 'l_s' else (p + 4) % 5
    first, second, fn, sn = _first_second(p)
    nth = '第一把' if k == first else '第二把'
    h = _hold(B.get('self.log') or [])[k]
    if _val(B, m.group(1)) == 0:
        who = f'被 P{h} 拿着' if h is not None else '已被别人拿走'
        return f'P{p} 要{nth}叉 `f{k}`：计数 0，{who} → ==阻塞==，等它放下'
    return f'P{p} 要{nth}叉 `f{k}`：计数 1，空闲 → 拿到'


def pick(side):
    def f(S, B, ret):
        p = _P(B)
        k = p if side == '左' else (p + 4) % 5
        n = len([a for q, a in (B.get('self.log') or []) if q == p and a.startswith('pick')])
        return f'P{p} 拿起{side}叉 `f{k}`' + ('：两把叉子都到手了' if n else '')
    return f


def put(side):
    def f(S, B, ret):
        p = _P(B)
        k = p if side == '左' else (p + 4) % 5
        return f'P{p} 放下{side}叉 `f{k}`'
    return f


def rel(S, B, ret):
    p = _P(B)
    m = re.match(r'(l_s|r_s)', _src(S))
    k = p if m.group(1) == 'l_s' else (p + 4) % 5
    v = _val(B, m.group(1))
    info = _info(S, B)[0]
    ws = [q for q in range(5) if q != p and info[q][0] == 'blocked' and info[q][2] == k]
    tail = f'，等它的 P{ws[0]} 被唤醒' if ws else '，暂时没人在等它'
    return f'P{p} `f{k}.release()`：归还叉子（{v} → {v + 1}）{tail}'


def _valid(log):
    """LeetCode 判题思路：同一把叉子不会同时被两人拿着；每人 拿两把 → 吃 → 放两把"""
    hold = [None] * 5
    for p, a in log:
        L, R = p, (p + 4) % 5
        if a in ('pickLeft', 'pickRight'):
            k = L if a == 'pickLeft' else R
            if hold[k] is not None:
                return f'叉子 f{k} 被重复拿起：{log}'
            hold[k] = p
        elif a == 'eat':
            if hold[L] != p or hold[R] != p:
                return f'P{p} 没有两把叉子就吃饭：{log}'
        else:
            k = L if a == 'putLeft' else R
            if hold[k] != p:
                return f'P{p} 放下了不属于自己的叉子：{log}'
            hold[k] = None
    if any(h is not None for h in hold):
        return f'有叉子没放回：{log}'
    for p in range(5):
        if sorted(a for q, a in log if q == p) != sorted(['pickLeft', 'pickRight', 'eat', 'putLeft', 'putRight']):
            return f'P{p} 的动作不对：{log}'
    return 'ok'


CONFIG = dict(
    num=1226, title='哲学家进餐', difficulty='Medium', category='设计',
    author='yiduobo', technique='奇偶错开拿叉顺序 · 多线程',
    tags=[],
    threads=True,
    code=CODE,
    setup='''
import threading, time, sys
sys.setswitchinterval(100)   # 让每个线程一直跑到阻塞或睡眠，演示顺序基本固定
''',
    call='''
dp = DiningPhilosophers()
dp.log = []
dp.st = {p: 'new' for p in range(5)}
def mk(p):
    even = p % 2 == 0
    def act(a, nap=0):
        def f():
            dp.log.append((p, a))
            if nap:
                time.sleep(nap)   # 吃饭 / 放叉子时让出 CPU，别的哲学家才有机会插进来
        return f
    return (act('pickLeft'), act('pickRight'), act('eat', 0.3),
            act('putLeft', 0.07 if even else 0), act('putRight', 0 if even else 0.07))
def body(p):
    dp.st[p] = 'run'
    pl, pr, ea, ptl, ptr = mk(p)
    dp.wantsToEat(p, pl, pr, ea, ptl, ptr)
    dp.st[p] = 'done'
ths = [threading.Thread(target=body, args=(p,), name='P%d' % p) for p in range(5)]
for t in ths:
    t.start()
    time.sleep(0.05)
for t in ths:
    t.join()
dp.log
''',
    result_fn=_valid,
    expect='ok',
    skip=['l_s = self.s_list'],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('叉子计数', lambda S: ' '.join(str(x) for x in _forks(S)) or None, 'cyan'),
           ('动作数', lambda S: len(S.get('self.log') or []) or None, 'yellow')],
    captions={
        'self.s_list = [': '主线程创建 5 把叉子：`s_list` 是 5 个 `Semaphore(1)`，每把叉子同一时刻只能被一个人拿',
        'r_s = self.s_list': lambda S, B, r: f"P{_P(B)}：左叉 `f{_P(B)}`，右叉 `f{(_P(B) + 4) % 5}`（编号取模成环）",
        'if philosopher % 2 == 0': lambda S, B, r: (
            f"P{_P(B)} 是{'偶' if _P(B) % 2 == 0 else '奇'}数 → 先拿{'左' if _P(B) % 2 == 0 else '右'}叉，"
            f"后拿{'右' if _P(B) % 2 == 0 else '左'}叉：==奇偶错开，避免人人先拿同一边=="),
        'l_s.acquire()': acq,
        'r_s.acquire()': acq,
        'pickLeftFork()': pick('左'),
        'pickRightFork()': pick('右'),
        'eat()': lambda S, B, r: f'P{_P(B)} 两把叉子都在手 → ==吃饭==，其他人趁机继续往下跑',
        'putLeftFork()': put('左'),
        'putRightFork()': put('右'),
        'l_s.release()': rel,
        'r_s.release()': rel,
    },
    cards=dict(
        one_liner='奇数号、偶数号哲学家拿叉顺序相反，避免人人各握一把互相等',
        complexity='每次调用 `O(1)`，空间 `O(1)`（5 个信号量）',
        problem=['5 位哲学家围坐圆桌，相邻两人之间 1 把叉子（共 5 把）',
                 '每人要先后拿起左、右两把叉子才能吃饭，吃完放下',
                 '5 个线程并发调用 `wantsToEat`：要不死锁、每人都能吃上'],
        quote='偶数位上的哲学家优先拿左手边的叉子，奇数位上的哲学家则优先拿右手边的叉子，这样一来就可以避免锁住的情况了。',
        quote_src='—— yiduobo 题解原文',
        idea=['如果人人都先拿左叉：5 个人各握一把，都在等右叉 → ==死锁==',
              '分奇偶：相邻的 P0、P1 都想先拿 `f0`，==只有一个人能拿到==，抢输的人手里还空着',
              '每把叉子是一个 `Semaphore(1)`：`acquire` 拿起，`release` 放下',
              '放下的顺序和拿起相反：先放第二把，再放第一把'],
        result='5 位哲学家都吃完了，叉子全部放回，没有死锁',
        summary=['每次调用 `O(1)`，空间 `O(1)`（5 个信号量）',
                 '拿叉顺序只由奇偶决定，打破了「人人先拿同一边」的对称',
                 '先 `acquire` 再 `pickFork`、先 `putFork` 再 `release`，顺序别写反',
                 '原文代码 Python 3 可直接运行，无需修改'],
    ),
)
