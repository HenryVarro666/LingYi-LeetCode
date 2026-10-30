class _Sk:
    pass


def _sk(S):
    h = S.get('self.head')
    if h is None:
        return None
    o = _Sk()
    o.head, o.level = h, S.get('self.level', 0)
    return o


def _levels(sk):
    """从最高层 head 往下，返回 [[node, ...], ...]（每层从头哨兵沿 next 走到底），最高层在前"""
    rows, h = [], sk.head
    while h is not None and len(rows) < 12:
        row, x = [], h
        while x is not None and len(row) < 14:
            row.append(x)
            x = x.next
        rows.append(row)
        h = h.down
    return rows


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '跳表：每层是一条有序链表，竖线 = down 指针（最底层是完整数据）', 22, T['muted'], bold=True)
    sk = _sk(S)
    if sk is None or sk.head is None:
        cv.text((x0 + 18, y0 + 60), '（空跳表：还没有任何层）', 26, T['dim'])
        return
    rows = _levels(sk)
    vals = sorted({n.val for r in rows for n in r if n.val != -1})
    col = {v: i + 1 for i, v in enumerate(vals)}
    col[-1] = 0
    ncol = len(col)
    cw = min(120, (x1 - x0 - 170) / max(ncol, 1))
    bw, bh = min(70, cw * 0.62), 46
    L = len(rows)
    gap = min(105, (y1 - y0 - 120) / max(L, 1))
    ys = y0 + 70
    sx = x0 + 120

    def pos(n, r):
        return sx + col[n.val] * cw + bw / 2, ys + r * gap + bh / 2

    now, tmp, last = S.get('now'), S.get('tmp'), S.get('last_level_node')
    for r, row in enumerate(rows):
        lvl = L - r
        cv.text((x0 + 22, ys + r * gap + bh / 2), f'第{lvl}层', 22, T['dim'], anchor='lm', bold=True)
        for a, b in zip(row, row[1:]):
            (ax, ay), (bx, by) = pos(a, r), pos(b, r)
            cv.arrow((ax + bw / 2 + 2, ay), (bx - bw / 2 - 3, by), T['muted'], 3, 10)
        for n in row:
            if n.down is not None and r + 1 < L:
                (ax, ay), (bx, by) = pos(n, r), pos(n.down, r + 1)
                cv.line([(ax, ay + bh / 2), (bx, by - bh / 2)], T['dim'], 2)
    for r, row in enumerate(rows):
        for n in row:
            cx, cy = pos(n, r)
            fill, tc = T['panel2'], T['text']
            if n is tmp:
                fill, tc = T['green'], T['bg']
            elif n is last:
                fill, tc = T['yellow'], T['bg']
            if n is now:
                cv.rect((cx - bw / 2 - 5, cy - bh / 2 - 5, cx + bw / 2 + 5, cy + bh / 2 + 5), outline=T['blue'], width=5, r=12)
            cv.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=fill, outline=T['border'], r=9)
            cv.text((cx, cy), '头' if n.val == -1 else n.val, 26, tc, anchor='mm', bold=True, mono=True)
    if now is not None:
        for r, row in enumerate(rows):
            for n in row:
                if n is now:
                    cx, cy = pos(n, r)
                    cv.text((cx, cy - bh / 2 - 12), 'now', 20, T['blue'], anchor='mb', bold=True)
    tg = S.get('target', S.get('num'))
    if tg is not None:
        cv.text((x1 - 20, y1 - 10), f'操作的值 = {tg}', 22, T['orange'], anchor='rb', bold=True)


def _op(S):
    if 'add_level' in S and 'num' in S:
        return f'add({S["num"]})：这个节点要有 =={S["add_level"]} 层==（抛硬币决定）'
    if 'target' in S:
        return f'search({S["target"]})：从最高层的头出发，向右走、走不动就向下'
    if 'num' in S and 'flag' in S:
        return f'erase({S["num"]})：每层找前置节点，找到就摘掉'
    if 'num' in S:
        return f'add({S["num"]})'
    return ''


CONFIG = dict(
    num=1206, title='设计跳表', difficulty='Hard', category='设计',
    author='yiduobo', technique='十字链表式跳表 · 随机层数',
    tags=['常用数据结构', '链表树与回溯'],
    code='''
class Node(object):

    def __init__(self, v):
        self.next = None
        self.down = None
        self.val = v

class Skiplist(object):

    def __init__(self):
        self.head = None
        self.rate = 0.5
        self.level = 0
        self.max_level = 15

    def search(self, target):
        now = self.head
        now_level = self.level
        while now_level > 0:
            while now.next is not None and now.next.val <= target:
                now = now.next
            if now.val == target:
                return True
            now = now.down
            now_level -= 1
        
        return False

    def add(self, num):
        add_level = 1
        while add_level < self.max_level and random.random() < self.rate:
            add_level += 1
        
        while self.level < add_level:
            tmp = Node(-1)
            tmp.down = self.head
            self.head = tmp
            self.level += 1
        
        now = self.head
        now_level = self.level
        last_level_node = None
        while now_level > 0:
            while now.next is not None and now.next.val <= num:
                now = now.next
            if now_level <= add_level:
                tmp = Node(num)
                tmp.next = now.next
                now.next = tmp
                if last_level_node is not None:
                    last_level_node.down = tmp
                last_level_node = tmp
            now = now.down
            now_level -= 1

    def erase(self, num):
        now = self.head
        now_level = self.level
        flag = False
        while now_level > 0:
            while now.next and now.next.val < num:
                now = now.next
            if now.next and now.next.val == num:
                flag = True
                now.next = now.next.next
            now = now.down
            now_level -= 1

        return flag
''',
    setup='import random\nrandom.seed(21)',
    call="""sl = Skiplist()
res = []
sl.add(3)
sl.add(1)
res.append(sl.search(3))
res.append(sl.erase(3))
res""",
    expect=[True, True],
    views=[
        dict(type='text', fn=_op, size=24),
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('now', 'now.val', 'blue'), ('now_level', 'now_level', 'cyan'), ('add_level', 'add_level', 'green'), ('self.level', 'self.level', 'orange')],
    skip=['self.next = None', 'self.down = None', 'self.val = v', 'self.rate', 'self.max_level', 'tmp.down = self.head', 'self.head = tmp', 'now_level = self.level', 'last_level_node = None', 'now_level -= 1', 'last_level_node = tmp', 'flag = False', 'add_level = 1', 'self.level += 1'],
    max_steps=110,
    captions={
        'self.head = None': '空跳表：还没有任何层，`level = 0`',
        'self.level = 0': '`level` 是当前总层数',
        'add_level = 1': '新节点至少在最底层（第 1 层）',
        'while add_level < self.max_level': lambda S, B, r: (f'抛硬币 `random() < 0.5` 成立 → 再往上建一层，`add_level = {S.add_level}`' if S.add_level != B.get('add_level') or 'add_level' not in B else f'没抛中（或到顶）→ 层数定为 ==`{S.add_level}`=='),
        'add_level += 1': '抛硬币抛中了（`random() < 0.5`）→ 再往上多建一层，`add_level = {add_level}`',
        'while self.level < add_level': lambda S, B, r: (f'`self.level = {S.level} < add_level = {S.add_level}`：总层数不够 → 在最上面加一层' if S.level < S.add_level else f'`self.level = {S.level} >= add_level = {S.add_level}`：层数够了，开始找每层的插入位置'),
        'tmp = Node(-1)': '新建一层的==头哨兵==（值 −1），放在现有最高层之上',
        'tmp.down = self.head': '新头的 `down` 指向旧最高层的头',
        'self.head = tmp': '`head` 换成新头，层数 +1',
        'self.level += 1': '总层数 `level = {level}`',
        'now = self.head': '从最高层的头出发',
        'now_level = self.level': '`now_level` 记录现在在第几层',
        'last_level_node = None': '`last_level_node`：上一层刚插入的节点，用来连 down',
        'while now.next is not None and now.next.val <= target': lambda S, B, r: (f'`now.next.val = {S.now.next.val} <= {S.target}`：右边还不大于目标 → 向右走' if S.now.next is not None and S.now.next.val <= S.target else ('右边没有节点了' if S.now.next is None else f'`now.next.val = {S.now.next.val} > {S.target}`：再往右就超了 → 停，准备下沉')),
        'while now.next is not None and now.next.val <= num': lambda S, B, r: (f'`now.next.val = {S.now.next.val} <= {S.num}`：右边还不大于 `{S.num}` → 向右走' if S.now.next is not None and S.now.next.val <= S.num else ('这层右边没有节点了 → 当前 `now` 就是前置节点' if S.now.next is None else f'`now.next.val = {S.now.next.val} > {S.num}` → `now` 就是这一层的前置节点')),
        'if now.val == target': lambda S, B, r: (f'`now.val = {S.now.val} == {S.target}`：找到了 → 返回 True' if S.now.val == S.target else f'`now.val = {S.now.val} != {S.target}`：这层没有，沿 `down` 下一层继续'),
        'if now_level <= add_level': lambda S, B, r: (f'`now_level = {S.now_level} <= add_level = {S.add_level}`：这一层要插入新节点' if S.now_level <= S.add_level else f'`now_level = {S.now_level} > add_level = {S.add_level}`：新节点没这么高，只下沉'),
        'tmp = Node(num)': '在这层新建节点 `{num}`',
        'tmp.next = now.next': '新节点的 `next` 接前置节点原来的后继',
        'now.next = tmp': '前置节点的 `next` 指向新节点：==这一层插入完成==',
        'if last_level_node is not None': lambda S, B, r: ('上一层已经插过 → 把上一层节点的 `down` 指向这层新节点（十字链表）' if B.last_level_node is not None else '这是最高的一层，没有上一层要连'),
        'last_level_node.down = tmp': '`down` 连好：上一层节点向下指到这层节点',
        'last_level_node = tmp': '记住这一层的新节点，给下一层连 down',
        'now = now.down': '沿 `down` 下到下一层，继续在同一位置往右找',
        'now_level -= 1': '`now_level` → {now_level}',
        'return True': '找到目标，返回 `True`',
        'return False': '所有层都没找到，返回 `False`',
        'flag = False': '`flag` 记录有没有删到',
        'while now.next and now.next.val < num': lambda S, B, r: (f'`now.next.val = {S.now.next.val} < {S.num}` → 向右走' if S.now.next and S.now.next.val < S.num else '右边没有更小的了 → `now` 是这层的前置节点'),
        'if now.next and now.next.val == num': lambda S, B, r: (f'`now.next.val == {S.num}`：这一层有要删的节点 → 摘掉' if S.now.next and S.now.next.val == S.num else '这一层没有 `{}`，直接下沉'.format(S.num)),
        'flag = True': '找到了，`flag = True`',
        'now.next = now.next.next': '前置节点的 `next` 跳过目标：==这一层已删除==',
        'return flag': '返回 `{flag}`',
    },
    cards=dict(
        one_liner='多层有序链表：高层跳着走、低层细找；节点高度靠抛硬币决定',
        complexity='期望 `O(log n)`，空间 `O(n)`',
        problem=['不用内置库，设计一个==跳表==：`add(num)`、`erase(num)`、`search(target)`',
                 '`search` 返回是否存在；`erase` 不存在返回 `False`；允许有重复值',
                 '本视频：`add(3)`、`add(1)` → `search(3)` → `erase(3)`'],
        quote='跳表的实现实际上可以认为是一种单向的十字链表，对于查找操作而言，每次查找都是从最顶层索引的头部开始向后遍历，找到该层最后一个满足值小于等于要查找的值的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个节点有 `next`（同层向右）和 `down`（同值的下一层）两个指针',
              '查找：从最高层头出发，向右走到不能走，没找到就沿 `down` 下沉',
              '插入：先抛硬币定层数 `add_level`，每层找前置节点插入，再用 `last_level_node` 把上下层连起来',
              '删除：每层找前置节点，有就摘掉，没有就下沉'],
        summary=['期望 `O(log n)`；随机层数避免退化成普通链表',
                 '易错：`search` / `add` 用 `<=` 往右走，`erase` 用 `<`（要停在目标前面）',
                 '易错：`erase` 要每一层都删，不能删到一层就停',
                 '原文用到 `random`：视频里固定 `random.seed(21)`，让层数可复现；其余代码未改动'],
    ),
)
