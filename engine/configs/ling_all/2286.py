CONFIG = dict(
    num=2286, title='以组为单位订音乐会的门票', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='线段树二分（min + sum）',
    tags=['难度分 2471'],
    code='''
class BookMyShow:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.min = [0] * (2 << n.bit_length())  # 相比 4n 空间更小
        self.sum = [0] * (2 << n.bit_length())

    # 线段树：把下标 i 上的元素值增加 val
    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            self.min[o] += val
            self.sum[o] += val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.min[o] = min(self.min[o * 2], self.min[o * 2 + 1])
        self.sum[o] = self.sum[o * 2] + self.sum[o * 2 + 1]

    # 线段树：返回区间 [L,R] 内的元素和
    def query_sum(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.sum[o]
        res = 0
        m = (l + r) // 2
        if L <= m:
            res = self.query_sum(o * 2, l, m, L, R)
        if R > m:
            res += self.query_sum(o * 2 + 1, m + 1, r, L, R)
        return res

    # 线段树：返回区间 [0,R] 中 <= val 的最靠左的位置，不存在时返回 -1
    def find_first(self, o: int, l: int, r: int, R: int, val: int) -> int:
        if self.min[o] > val:
            return -1  # 整个区间的元素值都大于 val
        if l == r:
            return l
        m = (l + r) // 2
        if self.min[o * 2] <= val:
            return self.find_first(o * 2, l, m, R, val)
        if R > m:
            return self.find_first(o * 2 + 1, m + 1, r, R, val)
        return -1

    def gather(self, k: int, maxRow: int) -> List[int]:
        # 找第一个能倒入 k 升水的水桶
        r = self.find_first(1, 0, self.n - 1, maxRow, self.m - k)
        if r < 0:  # 没有这样的水桶
            return []
        c = self.query_sum(1, 0, self.n - 1, r, r)
        self.update(1, 0, self.n - 1, r, k)  # 倒水
        return [r, c]

    def scatter(self, k: int, maxRow: int) -> bool:
        # [0,maxRow] 的接水量之和
        s = self.query_sum(1, 0, self.n - 1, 0, maxRow)
        if s > self.m * (maxRow + 1) - k:
            return False  # 水桶已经装了太多的水
        # 从第一个没有装满的水桶开始
        i = self.find_first(1, 0, self.n - 1, maxRow, self.m - 1)
        while k:
            left = min(self.m - self.query_sum(1, 0, self.n - 1, i, i), k)
            self.update(1, 0, self.n - 1, i, left)  # 倒水
            k -= left
            i += 1
        return True
''',
    call='''b = BookMyShow(2, 3)
out = [b.gather(2, 0), b.scatter(3, 1), b.gather(2, 1)]
out''',
    expect=[[0, 0], True, []],
    views=[
        dict(type='text', h=60, fn=lambda S: '把「座位」换成水桶：每个水桶容量 `m`，线段树存==接水量==的 `min` 和 `sum`（节点编号从 1 开始）'),
        dict(type='array', var='self.min', label='self.min（区间接水量的最小值）', pointers={'o': 'blue'}, h=200, cell=64),
        dict(type='array', var='self.sum', label='self.sum（区间接水量之和）', pointers={'o': 'blue'}, h=200, cell=64),
        dict(type='calls', label='正在执行', h=170),
    ],
    watch=['k', 'maxRow', 'r', 'i', ('s', 's', 'cyan'), ('left', 'left', 'green')],
    skip=['if l == r:', 'self.min[o] += val', 'self.min[o] = min(', 'if L <= m', 'if i <= m', 13, 30, 25, 'return res', 'm = (l + r) // 2', 'self.n = n', 'self.m = m', 'res = 0'],
    max_steps=140,
    captions={
        'self.min = [0]': '`min`：每个区间的接水量最小值，数组比 `4n` 更省',
        'self.sum = [0]': '`sum`：区间接水量之和，一开始桶都是空的',
        'if l == r:': lambda S, B, ret: ('区间长度为 1，到叶子了' if S.l == S.r else '区间还很长，继续二分'),
        'self.sum[o] += val': '到叶子 `o={o}`：接水量增加 `{val}` → `min = sum = {self.min[o]}`',
        'if i <= m': '要改的下标 `{i}`，中点 `{m}` → ' + '{"去左半" if i <= m else "去右半"}',
        'self.sum[o] = self.sum': '回溯：节点 `{o}` 的 `min` = 左右儿子较小者 =={self.min[o]}==，`sum` = 之和 =={self.sum[o]}==',
        'if self.min[o] > val': lambda S, B, ret: ('区间 `min = {}` > `{}`：整段都装不下 → 返回 -1'.format(S.self.min[S.o], S.val) if S.self.min[S.o] > S.val
                                                   else '区间 `min = {}` ≤ `{}`：这段里有桶放得下，继续'.format(S.self.min[S.o], S.val)),
        'return l': '找到叶子：第 `{l}` 号桶是最靠左的放得下的桶',
        'if self.min[o * 2] <= val': lambda S, B, ret: ('左半 `min = {}` ≤ `{}` → ==答案在左半==，往左走'.format(S.self.min[S.o * 2], S.val) if S.self.min[S.o * 2] <= S.val
                                                       else '左半 `min = {}` > `{}`：左边没有，去右边看看'.format(S.self.min[S.o * 2], S.val)),
        'if R > m': '右半区间 `[{m+1}, {r}]` 是否在 `maxRow = {R}` 范围内：{"在，往右走" if R > m else "不在，没有答案"}',
        'if L <= l and r <= R': lambda S, B, ret: ('`[{}, {}]` 完全落在 `[{}, {}]` 里 → 直接返回 `sum`'.format(S.l, S.r, S.L, S.R) if S.L <= S.l and S.r <= S.R
                                                   else '`[{}, {}]` 只有一部分在查询区间 `[{}, {}]` 内，要往下拆'.format(S.l, S.r, S.L, S.R)),
        'return self.sum[o]': '整段在范围内：返回 `sum[{o}] = {self.sum[o]}`',
        'self.find_first(1, 0, self.n - 1, maxRow, self.m - k)': '`gather({k}, {maxRow})`：接水量 ≤ `m−k = {self.m - k}` 的桶才放得下 `{k}` 升，线段树二分找最靠左的桶',
        'if r < 0:': lambda S, B, ret: ('`r = {}`：前 `maxRow+1` 个桶都放不下 → 返回空列表'.format(S.r) if S.r < 0 else '`r = {}`：找到了第 {} 号桶'.format(S.r, S.r)),
        52: '查这个桶倒水前已有 `c = {c}` 升',
        'self.update(1, 0, self.n - 1, r, k)': '往 `{B.r}` 号桶倒 `{B.k}` 升（单点修改，沿路径回溯更新 min/sum）',
        'return [r, c]': '返回 `[桶号 {r}, 倒前水量 {c}]`',
        58: '`scatter({k}, {maxRow})`：前 `{maxRow+1}` 个桶已有水量总和 `s = {s}`',
        'if s > self.m *': lambda S, B, ret: ('`s = {}` > `m×(maxRow+1) − k = {}`：剩余空间不够 `{}` 升 → 返回 False'.format(S.s, S.self.m * (S.maxRow + 1) - S.k, S.k) if S.s > S.self.m * (S.maxRow + 1) - S.k
                                              else '`s = {}` ≤ `m×(maxRow+1) − k = {}`：剩余空间够，可以倒'.format(S.s, S.self.m * (S.maxRow + 1) - S.k)),
        62: '线段树二分：第一个==没装满==（接水量 ≤ m−1）的桶 `i = {i}`',
        'while k:': lambda S, B, ret: ('还剩 `{}` 升没倒完，继续'.format(S.k) if S.k else '`k = 0`，全倒完了'),
        'left = min(': '这个桶本次倒 `left = min(m − 已有, k) = {left}` 升',
        'k -= left': '还剩 `k = {k}` 升',
        'i += 1': '换下一个桶 `i = {i}`',
        'return True': '全部倒完 → 返回 True',
        'return False': '返回 False，不改动任何桶',
        'return []': '返回 `[]`',
    },
    cards=dict(
        one_liner='线段树同时存区间 min 和 sum：min 做二分找桶，sum 判断总量够不够',
        complexity='`gather` `O(log n)`；`scatter` 均摊 `O(log n)`；空间 `O(n)`',
        problem=['`gather(k, maxRow)`：前 `maxRow+1` 排里，找第一排能连坐 `k` 人的',
                 '`scatter(k, maxRow)`：`k` 人可分散坐，从前往后填空位，坐不下返回 False',
                 '本视频：`BookMyShow(2, 3)`，依次 `gather(2,0)` `scatter(3,1)` `gather(2,1)`'],
        quote='线段树维护每个区间的接水量的最小值 min，以及每个区间的接水量之和 sum。……如果左半区间 min≤m−k，则答案在左半区间中，递归左半区间。',
        quote_src='—— 灵茶山艾府题解',
        idea=['座位 = 水桶，维护每个桶==已接水量==；放得下 `k` 升 ⇔ 接水量 `≤ m−k`',
              '`gather`：线段树二分，左半 `min` 够小就往左，否则往右',
              '`scatter`：先看 `sum` 够不够，够就从第一个没装满的桶逐个倒'],
        summary=['`gather` 是树高 `O(log n)`；`scatter` 填满的桶不再遍历，均摊 `O(log n)`',
                 '只有单点修改，不需要懒标记；数组开 `2 << n.bit_length()` 就够',
                 '易错点：`find_first` 的 `R` 只在往右走时检查；`scatter` 先判 sum 再动手',
                 '原文把座位换成水桶讲，思路等价；代码未改动'],
    ),
)
