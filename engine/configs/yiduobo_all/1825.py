def _node_info(S):
    t = S.get('self.tree')
    if t is None:
        return '（线段树尚未创建）'
    return f'线段树根：w[0] = {t.w[0]}（窗口里数的个数），s[0] = {t.s[0]}（它们的和）'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nl = S.get('self.num_list')
    k, m = S.get('self.k'), S.get('self.m')
    if nl is None:
        return
    vals = sorted(v for v in nl if v is not None)
    cv.text((x0 + 18, y0 + 4), f'窗口排序（k={k}）：蓝=最小k 粉=最大k 绿=中间', 22, T['muted'], bold=True)
    n = len(vals)
    cell = min(96, (x1 - x0 - 40) / max(1, n))
    sx = x0 + 20
    for i, v in enumerate(vals):
        if n >= m:
            c = T['blue'] if i < k else (T['pink'] if i >= n - k else T['green'])
        else:
            c = T['panel2']
        cv.rect((sx + i * cell + 3, y0 + 56, sx + (i + 1) * cell - 3, y0 + 56 + 62), fill=c, r=8)
        cv.text((sx + i * cell + cell / 2, y0 + 87), v, 30, T['bg'] if n >= m else T['text'], anchor='mm', bold=True)
    if n >= m and m - 2 * k > 0:
        mid = vals[k:n - k]
        cv.text((x0 + 20, y0 + 140), f'去掉两头各 {k} 个，剩 {mid}：平均 = {sum(mid) // len(mid)}', 22, T['yellow'])


CONFIG = dict(
    num=1825, title='求出 MK 平均值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='值域线段树 · 求最小/最大 k 个数的和',
    tags=[],
    code='''
class SegementTree(object):

    def __init__(self, maxn):
        self.maxn = maxn
        self.w = [0] * (maxn * 4)
        self.s = [0] * (maxn * 4)

    def insert(self, v):
        now = 0
        l, r = 1, self.maxn
        while l <= r:
            self.w[now] += 1
            self.s[now] += v
            if l == r:
                break
            mid = (l + r) >> 1
            if v <= mid:
                now = now + now + 1
                r = mid
            else:
                now = now + now + 2
                l = mid + 1

    def remove(self, v):
        now = 0
        l, r = 1, self.maxn
        while l <= r:
            self.w[now] -= 1
            self.s[now] -= v
            if l == r:
                break
            mid = (l + r) >> 1
            if v <= mid:
                now = now + now + 1
                r = mid
            else:
                now = now + now + 2
                l = mid + 1

    def weight(self):
        return self.w[0]

    def sum(self):
        return self.s[0]

    def min_k(self, k):
        now = 0
        l, r = 1, self.maxn
        res = 0
        while l <= r:
            if l == r:
                return res + l * k
            mid = (l + r) >> 1
            if self.w[now + now + 1] < k:
                res += self.s[now + now + 1]
                k -= self.w[now + now + 1]
                now = now + now + 2
                l = mid + 1
            else:
                now = now + now + 1
                r = mid

    def max_k(self, k):
        now = 0
        l, r = 1, self.maxn
        res = 0
        while l <= r:
            if l == r:
                return res + r * k
            mid = (l + r) >> 1
            if self.w[now + now + 2] < k:
                res += self.s[now + now + 2]
                k -= self.w[now + now + 2]
                now = now + now + 1
                r = mid
            else:
                now = now + now + 2
                l = mid + 1

class MKAverage(object):

    def __init__(self, m, k):
        self.m = m
        self.num_list = [None] * m
        self.p = 0
        self.k = k
        self.tree = SegementTree(8)

    def addElement(self, num):
        self.tree.insert(num)
        if self.tree.weight() > self.m:
            self.tree.remove(self.num_list[self.p])
        self.num_list[self.p] = num
        self.p = (self.p + 1) % self.m

    def calculateMKAverage(self):
        if self.tree.weight() < self.m:
            return -1
        return (self.tree.sum() - self.tree.max_k(self.k) - self.tree.min_k(self.k)) // (self.m - self.k - self.k)
''',
    call='''mk = MKAverage(3, 1)
mk.addElement(3)
mk.addElement(1)
r = [mk.calculateMKAverage()]
mk.addElement(7)
r.append(mk.calculateMKAverage())
mk.addElement(5)
r.append(mk.calculateMKAverage())
r''',
    expect=[-1, 3, 5],
    views=[
        dict(type='custom', draw=_draw, h=210),
        dict(type='array', var='self.num_list', label='num_list（循环队列）', pointers={'self.p': 'blue'}, h=215),
        dict(type='text', fn=_node_info, size=22, h=60),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('v', 'v', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'cyan'), ('now', 'now', 'purple'), ('k', 'k', 'yellow'), ('res', 'res', 'green')],
    skip=['self.maxn = maxn', 'self.w = [0]', 'self.s = [0]', 'self.m = m', 'self.k = k', 'self.p = 0', 'now = 0', 'l, r = 1, self.maxn',
          'res = 0', 'mid = (l + r) >> 1', 'self.num_list = [None]', 'while l <= r', 'now = now + now + 1', 'now = now + now + 2',
          'self.w[now] += 1', 'self.s[now] += v', 'self.w[now] -= 1', 'self.s[now] -= v', 'if l == r', 'break',
          'r = mid', 'l = mid + 1', 'res += self.s', 'k -= self.w',
          'return self.w[0]', 'return self.s[0]', 'self.num_list[self.p] = num', 'self.p = (self.p + 1)'],
    max_steps=110,
    captions={
        'self.tree = SegementTree(8)': '原文值域是 1~100000，演示缩成 1~8；建一棵==值域线段树==：节点管一段数值范围，记个数 `w` 和总和 `s`',
        'self.tree.insert(num)': '新数 `{num}` 进窗口：先插进线段树',
        17: lambda S, B, r_: (f'节点 `[{S.l}, {S.r}]` 记上 `{S.v}`（`w` +1，`s` +{S.v}）；`{S.v} <= {S.mid}` → 走左半 `[{S.l}, {S.mid}]`' if S.v <= S.mid
                              else f'节点 `[{S.l}, {S.r}]` 记上 `{S.v}`（`w` +1，`s` +{S.v}）；`{S.v} > {S.mid}` → 走右半 `[{S.mid + 1}, {S.r}]`'),
        33: lambda S, B, r_: (f'节点 `[{S.l}, {S.r}]` 扣掉 `{S.v}`（`w` -1，`s` -{S.v}）；`{S.v} <= {S.mid}` → 走左半 `[{S.l}, {S.mid}]`' if S.v <= S.mid
                              else f'节点 `[{S.l}, {S.r}]` 扣掉 `{S.v}`（`w` -1，`s` -{S.v}）；`{S.v} > {S.mid}` → 走右半 `[{S.mid + 1}, {S.r}]`'),
        'if self.tree.weight() > self.m': lambda S, B, r_: (f'树里有 {S["self.tree"].w[0]} 个数 > m = {S["self.m"]}：窗口满了，最旧的要删掉'
                                                           if S['self.tree'].w[0] > S['self.m'] else f'树里有 {S["self.tree"].w[0]} 个数 ≤ m = {S["self.m"]}：还不用删'),
        'self.tree.remove(self.num_list[self.p])': '循环队列 `p` 位置存的就是最旧的数，从线段树里删掉它',
        'if self.tree.weight() < self.m': lambda S, B, r_: (f'只有 {S["self.tree"].w[0]} 个数 < m = {S["self.m"]} → 返回 ==-1==' if S['self.tree'].w[0] < S['self.m']
                                                          else f'已有 {S["self.tree"].w[0]} 个数 = m，可以算'),
        'return (self.tree.sum()': lambda S, B, r_: ('总和 − 最大 k 个之和 − 最小 k 个之和，再除以 `m − 2k`' if r_ is None
                                                     else f'平均值 = =={r_}=='),
        'if self.w[now + now + 1] < k': lambda S, B, r_: (f'`[{S.l}, {S.r}]`：左孩子只有 {S.self.w[2 * S.now + 1]} 个 < k = {S.k}，整块拿走（和 {S.self.s[2 * S.now + 1]}），去右边找剩下的 `{S.k}` 个'
                                                         if S.self.w[2 * S.now + 1] < S.k else f'`[{S.l}, {S.r}]`：左孩子有 {S.self.w[2 * S.now + 1]} 个 ≥ k = {S.k}，第 k 小在左边'),
        'if self.w[now + now + 2] < k': lambda S, B, r_: (f'`[{S.l}, {S.r}]`：右孩子只有 {S.self.w[2 * S.now + 2]} 个 < k = {S.k}，整块拿走（和 {S.self.s[2 * S.now + 2]}），去左边找剩下的 `{S.k}` 个'
                                                         if S.self.w[2 * S.now + 2] < S.k else f'`[{S.l}, {S.r}]`：右孩子有 {S.self.w[2 * S.now + 2]} 个 ≥ k = {S.k}，第 k 大在右边'),
        'return res + l * k': '到叶子 `{l}`：再取 `{k}` 个 `{l}` → 最小 k 个之和 = =={ret}==',
        'return res + r * k': '到叶子 `{r}`：再取 `{k}` 个 `{r}` → 最大 k 个之和 = =={ret}==',
    },
    cards=dict(
        one_liner='数值只有 10 万：开值域线段树，记每段的个数和总和',
        complexity='每次操作 `O(log C)`，`C = 10^5`；空间 `O(C)`',
        problem=['流里不断 `addElement(num)`；`calculateMKAverage()` 看最后 `m` 个数',
                 '去掉其中最小 `k` 个和最大 `k` 个，对剩下的求平均（向下取整）',
                 '不足 `m` 个返回 `-1`。本视频：`m=3, k=1`，加入 `3,1,7,5`'],
        quote='注意到这里数字的范围在1到100000之间，所以我才用了一种取巧的做法，使用线段树来维护当前最后m个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 `m` 的循环队列记住窗口里的数，满了就覆盖最旧的那个',
              '线段树按==数值范围==分，每个节点存个数 `w` 和总和 `s`',
              '最小 k 个：看左孩子个数够不够 k，不够就整块拿走再往右；最大 k 个对称',
              '答案 = (根的总和 − 最大 k 个和 − 最小 k 个和) ÷ (m − 2k)'],
        summary=['插入、删除、求前 k 个之和都是 `O(log C)`，空间 `O(C)`',
                 '易错：先 `insert` 新数再 `remove` 旧数，所以树里会短暂有 `m + 1` 个数',
                                  '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '演示把值域 `SegementTree(100000)` 缩成 `8`，逻辑不变',
                 '其他做法：平衡树，或四个堆（调整细节复杂）'],
    ),
)
