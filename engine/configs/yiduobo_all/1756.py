def _get(S):
    f = S.get('self.f')
    v = S.get('self.v')
    if f is None and S.get('self') is not None:
        f, v = S['self'].f, S['self'].v
    return f, v


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f, v = _get(S)
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '队列的「坑位」：线段树的叶子，被取走的坑位留空，新元素放进末尾新坑位', 22, T['muted'], bold=True)
    if f is None:
        return
    order = S.get('self.order', 0)
    M = max(order, 8)
    cell = min(104, (x1 - x0 - 60) / M)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * M) / 2
    ys = y0 + 90
    ch = cell * 0.8
    cur = None
    if line in (24, 25):
        cur = S.get('p', S.get('_inner', {}).get('p'))
    elif line in (44, 45):
        cur = S.get('left')
    rank = 0
    live = []
    for p in range(M):
        X = sx + p * cell
        occ = f[4095 + p] == 1
        if occ:
            rank += 1
            live.append(v[p] + 1)
            cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=T['blue'], r=10)
            cv.text((X + cell / 2, ys + ch / 2), v[p] + 1, 34, T['bg'], anchor='mm', bold=True)
            cv.text((X + cell / 2, ys + ch + 34), f'第{rank}个', 20, T['cyan'], anchor='mt', bold=True)
        else:
            cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=T['panel2'], r=10, outline=T['border'])
            if p < order:
                cv.text((X + cell / 2, ys + ch / 2), v[p] + 1, 30, T['dim'], anchor='mm')
                cv.text((X + cell / 2, ys + ch + 34), '已搬走', 18, T['dim'], anchor='mt')
        cv.text((X + cell / 2, ys + ch + 8), p, 18, T['dim'], anchor='mt', mono=True)
        if cur is not None and p == cur:
            cv.rect((X, ys - 6, X + cell, ys + ch + 6), outline=T['yellow'], width=5, r=12)
    cv.text((x0 + 18, ys + ch + 90), f'当前队列（从前到后）：{live}', 30, T['green'], bold=True)
    r = S.get('r')
    if r is not None:
        cv.text((x0 + 18, ys + ch + 140), f'每次 fetch 的返回值 r = {r}', 26, T['text'])


def _path(S):
    line = S.get('_line')
    if line in (24, 25):
        p = S.get('p')
        if p is not None:
            return f'坑位 `{p}` 的二进制 `{p:012b}`：12 层里 ==0 进左半、1 进右半==，叶子的计数设为 1'
    if line in (44, 45):
        left = S.get('left')
        if left is not None:
            return f'沿途走到叶子 `{left}`（二进制 `{left:012b}`）：就是第 k 个元素所在的坑位'
    return ''


CONFIG = dict(
    num=1756, title='设计最近使用(MRU)队列', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='末尾开坑位 + 线段树找第 k 个',
    tags=['线段树'],
    code='''
class MRUQueue(object):

    def __init__(self, n):
        self.f = [0] * 8192
        self.v = [0] * 4096
        self.order = n
        for v in range(n):
            self.insert(v, v)

    def insert(self, p, v):
        now = 0
        left = 0
        right = 4095
        while left < right:
            self.f[now] += 1
            mid = (left + right) >> 1
            if p <= mid:
                now = now + now + 1
                right = mid
            else:
                now = now + now + 2
                left = mid + 1
        
        self.f[now] = 1
        self.v[p] = v

    def fetch(self, k):

        now = 0
        left = 0
        right = 4095
        while left < right:
            mid = (left + right) >> 1
            if k > self.f[now + now + 1]:
                k -= self.f[now + now + 1]
                self.f[now] -= 1
                now = now + now + 2
                left = mid + 1
            else:
                self.f[now] -= 1
                now = now + now + 1
                right = mid
        
        res = self.v[left]
        self.f[now] -= 1

        self.insert(self.order, res)
        self.order += 1
        return res + 1
''',
    call='''q = MRUQueue(5)
r = []
r.append(q.fetch(3))
r.append(q.fetch(2))
r.append(q.fetch(1))
r''',
    expect=[3, 2, 1],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_path, size=26, h=70),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('k', 'k', 'yellow'), ('left', 'left', 'blue'), ('order', lambda S: S.get('self.order'), 'cyan'), ('r', 'r', 'green')],
    skip=[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
    captions={
        'self.f = [0] * 8192': '线段树存在数组 `f` 里：4096 个叶子，每个节点记「这段里还剩几个元素」',
        'self.v = [0] * 4096': '`v[p]` 记坑位 `p` 上放的是哪个数',
        'self.order = n': '`order` = 下一个新坑位的位置，初始接在 `n` 后面',
        'for v in range(n)': '把 `0..n-1` 依次放进坑位 `0..n-1`',
        'self.insert(v, v)': '`insert({p}, {v})`：把数 `{v + 1}` 放进坑位 `{p}`（线段树从根到叶子，沿途计数 +1）',
        'self.f[now] = 1': '走到坑位 `{p}` 的叶子：它的计数设为 `1`，这个坑位现在有人了',
        'self.v[p] = v': '`v[{p}] = {v}`：坑位 `{p}` 里放的是数 ==`{v + 1}`==（内部存 0 起点）',
        'now = 0': '`fetch({k})`：要取队列里第 `{k}` 个。每个节点存「这段还剩几个」，从根往下找第 `k` 个',
        'res = self.v[left]': '沿途规则：`k` 大于左半的个数就扣掉它去右半，否则进左半。落在叶子 `{left}` → 取出 ==`{res}`==（对外是 `{res + 1}`）',
        'self.f[now] -= 1': '叶子计数减 1：这个坑位空出来，后面的人==不用往前挪==，名次自然前移',
        'self.insert(self.order, res)': '不挪动后面的元素，而是把它重新放到末尾的新坑位 `{self.order}`',
        'self.order += 1': '下一个新坑位往后移：`order = {self.order}`',
        'return res + 1': '返回被取出的数 ==`{ret}`==（内部从 0 开始存，所以 +1）',
    },
    cards=dict(
        one_liner='取走第 k 个后不挪动别人，把它接到末尾新坑位，用线段树数「第 k 个坑位」',
        complexity='每次 `fetch` `O(log C)`，`C = 4096` 是坑位总数；空间 `O(C)`',
        problem=['`MRUQueue(n)`：初始队列 `[1..n]`',
                 '`fetch(k)`：取出第 `k` 个元素，移到队尾，并返回它',
                 '示例：`n = 5`，`fetch(3)` → `3`，队列变成 `[1,2,4,5,3]`'],
        quote='先在当前队列的末尾额外开辟若干个坑位，数量与询问的次数相同……将第k个元素移除之后并不移动后续的元素，而是将其重新插入在末尾对应的坑位中。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次 `fetch`：原坑位清空，元素重新放到一个更靠后的新坑位',
              '坑位的先后顺序就是队列顺序 → 问题变成「动态求第 k 个有人的坑位」',
              '用线段树：每个节点存区间内有人坑位数，从根往下按 `k` 走到叶子'],
        summary=['`fetch` 与 `insert` 都是 `O(log C)`，`C = 4096`（题目 n 和操作数都不大）',
                 '线段树用堆式下标：节点 `now` 的左右孩子是 `2·now+1`、`2·now+2`',
                 '易错：`v` 里存的是 0 起点的数，返回时要 `+1`',
                 '易错：`k` 在往右走时要先扣掉左半的个数',
                 '原文就是 Python 3 可运行的写法，未做修改；演示时跳过了循环里的逐层步骤，只看关键行'],
    ),
)
