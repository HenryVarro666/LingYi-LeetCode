CONFIG = dict(
    num=2286, title='以组为单位订音乐会的门票', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='线段树（max_v + sum_v）',
    tags=[],
    code='''
class BookMyShow(object):

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.left = [-1] * (4 * n)
        self.right = [-1] * (4 * n)
        self.max_v = [-1] * (4 * n)
        self.sum_v = [-1] * (4 * n)
        self.build(0, 0, n - 1, m)

    def build(self, now, l, r, v):
        if l == r:
            self.max_v[now] = self.sum_v[now] = v
        else:
            mid = (l + r) >> 1
            self.left[now] = now + now + 1
            self.right[now] = now + now + 2
            self.build(self.left[now], l, mid, v)
            self.build(self.right[now], mid + 1, r, v)
            self.max_v[now] = max(self.max_v[self.left[now]], self.max_v[self.right[now]])
            self.sum_v[now] = self.sum_v[self.left[now]] + self.sum_v[self.right[now]]

    def find_max(self, now, l, r, v):
        if self.max_v[now] < v:
            return -1, -1
        if l == r:
            return l, now
        else:
            mid = (l + r) >> 1
            if self.max_v[self.left[now]] >= v:
                return self.find_max(self.left[now], l, mid, v)
            else:
                return self.find_max(self.right[now], mid +1, r, v)

    def update_single(self, now, l, r, p, v):
        if l == r:
            self.max_v[now] -= v
            self.sum_v[now] -= v
        else:
            mid = (l + r) >> 1
            if p <= mid:
                self.update_single(self.left[now], l, mid, p, v)
            else:
                self.update_single(self.right[now], mid + 1, r, p, v)
            
            self.max_v[now] = max(self.max_v[self.left[now]], self.max_v[self.right[now]])
            self.sum_v[now] = self.sum_v[self.left[now]] + self.sum_v[self.right[now]]

    def gather(self, k, maxRow):
        p, node = self.find_max(0, 0, self.n - 1, k)
        if p == -1 or p > maxRow:
            return []
        
        res = [p, self.m - self.max_v[node]]

        self.update_single(0, 0, self.n - 1, p, k)

        return res

    def find_sum(self, now, l, r, v):
        if self.sum_v[now] < v:
            return -1
        if l == r:
            return l
        else:
            mid = (l + r) >> 1
            if self.sum_v[self.left[now]] >= v:
                return self.find_sum(self.left[now], l, mid, v)
            else:
                return self.find_sum(self.right[now], mid + 1, r, v - self.sum_v[self.left[now]])

    def set_seg_zero(self, now, l, r, p):
        if l == r:
            cnt = self.max_v[now]
            self.max_v[now] = self.sum_v[now] = 0
        else:
            mid = (l + r) >> 1
            if p <= mid:
                cnt = self.set_seg_zero(self.left[now], l, mid, p)
            else:
                cnt = self.sum_v[self.left[now]]
                self.max_v[self.left[now]] = self.sum_v[self.left[now]] = 0
                
                cnt += self.set_seg_zero(self.right[now], mid + 1, r, p)
            
            self.max_v[now] = max(self.max_v[self.left[now]], self.max_v[self.right[now]])
            self.sum_v[now] = self.sum_v[self.left[now]] + self.sum_v[self.right[now]]
        
        return cnt

    def scatter(self, k, maxRow):
        p = self.find_sum(0, 0, self.n - 1, k)
        if p == -1 or p > maxRow:
            return False
        
        cnt = self.set_seg_zero(0, 0, self.n - 1, p - 1)
        self.update_single(0, 0, self.n - 1, p, k - cnt)

        return True
''',
    call='''b = BookMyShow(2, 3)
out = [b.gather(2, 0), b.scatter(4, 1), b.gather(1, 1)]
out''',
    expect=[[0, 0], True, []],
    views=[
        dict(type='text', h=60, fn=lambda S: '`rest[i]` = 第 i 排剩余座位；线段树维护区间 `max_v`（最大值）和 `sum_v`（总和）'),
        dict(type='array', var='self.max_v', label='max_v（区间剩余座位最大值）', pointers={'now': 'blue'}, h=190, cell=60),
        dict(type='array', var='self.sum_v', label='sum_v（区间剩余座位总和）', pointers={'now': 'blue'}, h=190, cell=60),
        dict(type='calls', label='正在执行', h=170),
    ],
    watch=['k', 'maxRow', 'p', ('res', 'res', 'green'), ('cnt', 'cnt', 'cyan')],
    skip=['self.n = n', 'self.m = m', 'self.left = [-1]', 'self.right = [-1]', 'self.sum_v = [-1]', 'mid = (l + r) >> 1',
          'self.left[now] = now', 'self.right[now] = now', 'if l == r:', 'self.max_v[now] -= v',
          'self.max_v[now] = max('],
    max_steps=110,
    captions={
        'self.max_v = [-1]': '`max_v`、`sum_v`：线段树每个节点管一段区间的剩余座位最大值 / 总和（节点按 `2i+1`、`2i+2` 找儿子）',
        'self.build(0, 0, n - 1, m)': '建树：每个叶子 = 一排，一开始剩 `m = {m}` 个座位',
        'self.max_v[now] = self.sum_v[now] = v': '叶子（第 `{l}` 排）：`max_v = sum_v = {v}`',
        'self.sum_v[now] = self.sum_v[self.left[now]]': lambda S, B, ret: '节点 `{}` 的 `max_v` = 左右儿子最大者 = =={}==（`sum_v` = 两儿子之和 = =={}==）'.format(S.now, S.self.max_v[S.now], S.self.sum_v[S.now]),
        'p, node = self.find_max': '`gather({k}, {maxRow})`：先不管 `maxRow`，找最小的 `p` 使 `rest[p] >= {k}`，再检查 `p <= maxRow`',
        'if self.max_v[now] < v': lambda S, B, ret: ('`max_v = {}` < `{}`：这段里没有一排够坐 → 返回 `(-1, -1)`'.format(S.self.max_v[S.now], S.v) if S.self.max_v[S.now] < S.v
                                                    else '`max_v = {}` ≥ `{}`：这段里一定有一排够坐，继续往下找最靠左的'.format(S.self.max_v[S.now], S.v)),
        'if self.max_v[self.left[now]] >= v': lambda S, B, ret: ('左儿子 `max_v = {}` ≥ `{}` → ==最小的 p 在左边=='.format(S.self.max_v[S.self.left[S.now]], S.v) if S.self.max_v[S.self.left[S.now]] >= S.v
                                                                 else '左儿子 `max_v = {}` < `{}` → 左边没有，去右边'.format(S.self.max_v[S.self.left[S.now]], S.v)),
        'return l, now': '到叶子：第 `{l}` 排就是最小的 `p`',
        'if p == -1 or p > maxRow': lambda S, B, ret: ('`p = {}`：{}'.format(S.p, '没有够坐的一排 → 返回 `[]`' if S.p == -1 else '超出 `maxRow = {}` → 返回 `[]`'.format(S.maxRow)) if (S.p == -1 or S.p > S.maxRow)
                                                       else '`p = {}` ≤ `maxRow = {}`，可以安排'.format(S.p, S.maxRow)),
        'res = [p, self.m - self.max_v[node]]': '返回 `[排号 {p}, 起始座位 = m − 剩余 = {res[1]}]`',
        'self.update_single(0, 0, self.n - 1, p, k)': '第 `{B.p}` 排的剩余座位减去 `{B.k}`，沿路径回溯更新 `max_v` / `sum_v`',
        'self.sum_v[now] -= v': '叶子：剩余座位减 `{v}` → `max_v = sum_v = {self.sum_v[now]}`',
        'p = self.find_sum': '`scatter({k}, {maxRow})`：找最小的 `p` 使前缀和 `rest[0..p] >= {k}`（人可以分开坐）',
        'if self.sum_v[now] < v': lambda S, B, ret: ('`sum_v = {}` < `{}`：整段座位都不够 → 返回 -1'.format(S.self.sum_v[S.now], S.v) if S.self.sum_v[S.now] < S.v
                                                    else '`sum_v = {}` ≥ `{}`：座位够，继续找前缀和刚好够的位置'.format(S.self.sum_v[S.now], S.v)),
        'if self.sum_v[self.left[now]] >= v': lambda S, B, ret: ('左儿子 `sum_v = {}` ≥ `{}`：前缀在左边就凑够了 → 去左边'.format(S.self.sum_v[S.self.left[S.now]], S.v) if S.self.sum_v[S.self.left[S.now]] >= S.v
                                                                  else '左儿子 `sum_v = {}` < `{}`：左边全占满还不够 → 去右边，需求减去左边总和'.format(S.self.sum_v[S.self.left[S.now]], S.v)),
        'cnt = self.set_seg_zero': '把第 `0..p-1` 排全部坐满（置 0），记下它们原来的座位总数 `cnt`',
        'cnt = self.max_v[now]': '叶子原有 `{cnt}` 个座位，要被全部占用',
        'self.max_v[now] = self.sum_v[now] = 0': '这一排坐满：`max_v = sum_v = 0`',
        'self.max_v[self.left[now]] = self.sum_v': '`p` 在右边：左儿子整段都坐满，`cnt` += 左边总和',
        'self.update_single(0, 0, self.n - 1, p, k - cnt)': '剩下的 `k − cnt = {B.k - cnt}` 个人坐进第 `{B.p}` 排',
        'return True': '`scatter` 成功 → 返回 True',
        'return False': '返回 False',
        'return []': '返回 `[]`',
    },
    cards=dict(
        one_liner='排的状态只记剩余座位：线段树存 max_v 找连坐，sum_v 找分坐',
        complexity='每次操作 `O(log n)`；空间 `O(n)`',
        problem=['`gather(k, maxRow)`：前 `maxRow+1` 排里最小的一排能连坐 `k` 人，坐下并返回 `[排, 座位]`',
                 '`scatter(k, maxRow)`：`k` 人可分开坐，从前往后占空位，坐不下返回 False',
                 '本视频：`BookMyShow(2, 3)`，`gather(2,0)` `scatter(4,1)` `gather(1,1)`'],
        quote='座位安排总是从左到右进行，因此实际上并不需要关心每个座位的安排情况，而是使用每一行剩余的座位来表示每一行的状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['`gather`：找最小的 `p` 使 `rest[p] >= k`，线段树按 `max_v` 往左走；再检查 `p <= maxRow`',
              '`scatter`：找最小的 `p` 使前缀和 `>= k`，用 `sum_v` 二分；前 `p-1` 排置 0，余下的坐第 `p` 排',
              '置 0 是一次性的：被清零的区间之后不会再改'],
        summary=['每次操作 `O(log n)`，空间 `O(n)`（`4n` 个节点）',
                 '先不管 `maxRow` 找到最小 `p`，最后才判断 `p > maxRow`',
                 '`scatter` 把 `p` 左边全部置 0，`cnt` 记下占掉的座位数，余数放到第 `p` 排',
                 '原文是 Python 2 风格，本题代码无需改动'],
    ),
)
