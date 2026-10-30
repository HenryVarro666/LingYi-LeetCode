def _txt(S):
    if 'sum_l' not in S:
        return 'L 存「出现次数最多的前 x 种」的二元组 (次数, 值)，sum_l 是它们的 次数×值 之和'
    L, R = S['L'], S['R']
    return f'L（前 x 种）{len(L)} 个　R（其余）{len(R)} 个　`sum_l = {S["sum_l"]}`　（比较时先比次数，次数相同比值）'


def _fmt(p):
    return f'{p[1]}×{p[0]}'


CONFIG = dict(
    num=3321, title='计算子数组的 x-sum II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='滑动窗口 · 对顶有序集合',
    tags=['常用数据结构', '难度分 2598'],
    code='''
class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        cnt = defaultdict(int)
        L = SortedList()  # 保存 tuple (出现次数，元素值)
        R = SortedList()
        sum_l = 0  # L 的元素和

        def add(val: int) -> None:
            if cnt[val] == 0:
                return
            p = (cnt[val], val)
            if L and p > L[0]:  # p 比 L 中最小的还大
                nonlocal sum_l
                sum_l += p[0] * p[1]
                L.add(p)
            else:
                R.add(p)

        def remove(val: int) -> None:
            if cnt[val] == 0:
                return
            p = (cnt[val], val)
            if p in L:
                nonlocal sum_l
                sum_l -= p[0] * p[1]
                L.remove(p)
            else:
                R.remove(p)

        def l2r() -> None:
            nonlocal sum_l
            p = L[0]
            sum_l -= p[0] * p[1]
            L.remove(p)
            R.add(p)

        def r2l() -> None:
            nonlocal sum_l
            p = R[-1]
            sum_l += p[0] * p[1]
            R.remove(p)
            L.add(p)

        ans = [0] * (len(nums) - k + 1)
        for r, in_ in enumerate(nums):
            # 添加 in_
            remove(in_)
            cnt[in_] += 1
            add(in_)

            l = r + 1 - k
            if l < 0:
                continue

            # 维护大小
            while R and len(L) < x:
                r2l()
            while len(L) > x:
                l2r()
            ans[l] = sum_l

            # 移除 out
            out = nums[l]
            remove(out)
            cnt[out] -= 1
            add(out)
        return ans
''',
    # 原文第一行 from sortedcontainers import SortedList：这里用 list 子类写一个最小替代
    setup='''
class SortedList(list):
    def add(self, v):
        bisect.insort(self, v)
    def remove(self, v):
        del self[bisect.bisect_left(self, v)]
''',
    call='Solution().findXSum([1,1,2,3], 3, 2)',
    expect=[4, 5],
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [l, r]）', pointers={'r': 'blue'},
             window=(lambda S: max(0, S['r'] - 2) if 'r' in S else None, 'r'), h=185),
        dict(type='queue', var='L', label='L：前 x 种（值×次数）', fmt=_fmt, h=105),
        dict(type='queue', var='R', label='R：其余', fmt=_fmt, h=105),
        dict(type='map', var='cnt', label='cnt 窗口内出现次数', h=100),
        dict(type='array', var='ans', label='ans', h=155),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=[('r', 'r', 'blue'), ('in_', 'in_', 'orange'), ('sum_l', 'sum_l', 'green'), ('val', 'val', 'orange'), 'p'],
    skip=['cnt = defaultdict', 'L = SortedList', 'R = SortedList', 'sum_l = 0', 'def ', 'nonlocal', 'ans = [0]', 'remove(in_)', 'add(in_)', 'remove(out)', 'add(out)', 'continue', 'l = r + 1 - k', 'p = (cnt[val], val)', 10, 21],
    captions={
        'for r, in_ in enumerate': lambda S, B, rt: ('遍历结束' if B.get('r') == S.r and B.get('in_') == S.in_ and S.r == len(S.nums) - 1 else f'`r = {S.r}`，`in_ = {S.in_}` 进入窗口：次数要变了，==先删旧二元组，改次数，再加新二元组=='),
        'cnt[in_] += 1': '`cnt[{in_}]` 加一 → =={cnt[in_]}==',
        'if cnt[val] == 0': lambda S, B, r: (f'`cnt[{S.val}] = 0`：窗口里没有它，不用处理，直接返回' if S.cnt[S.val] == 0 else f'`cnt[{S.val}] = {S.cnt[S.val]}`，二元组 `p = ({S.cnt[S.val]}, {S.val})`（先比次数，次数相同比数值）'),
        'p = (cnt[val], val)': '二元组 `p = {p}`：先比出现次数，次数相同比数值（题目规则：同次数数值大的更重要）',
        'if L and p > L[0]': lambda S, B, r: (f'`L` 为空，放进 R' if not S.L else
                                              f'`p = {S.p} > L 里最小的 {S.L[0]}` → ' + ('比它大，应该在前 x 种里，放进 L，`sum_l` 加上 `{0}×{1}`'.format(*S.p) if S.p > S.L[0] else '不比它大，放进 R')),
        'L.add(p)': '`p` 进 L，`sum_l` → {sum_l}',
        'R.add(p)': '`p` 进 R（候选区）',
        'sum_l += p[0] * p[1]': '`sum_l` += `{p[0]}×{p[1]}` → {sum_l}',
        'if p in L': lambda S, B, r: (f'`p = {S.p}` 在 L 里 → 从 L 删，同时 `sum_l` 减掉它' if S.p in S.L else f'`p = {S.p}` 不在 L 里 → 从 R 删'),
        'sum_l -= p[0] * p[1]': '`sum_l` −= `{p[0]}×{p[1]}` → {sum_l}',
        'L.remove(p)': '把 `p` 从 L 删掉',
        'R.remove(p)': '把 `p` 从 R 删掉',
        'if l < 0': lambda S, B, r: (f'`l = r+1−k = {S.l} < 0`：窗口还没长到 k，先不算答案' if S.l < 0 else f'`l = r+1−k = {S.l}`：窗口 `[{S.l}, {S.r}]` 长度为 k，可以算答案了'),
        'while R and len(L) < x': lambda S, B, r: (f'`len(L) = {len(S.L)} < x = {S.x}` 且 R 非空 → L 不够，从 R 里补' if (S.R and len(S.L) < S.x) else f'`len(L) = {len(S.L)}`，不用补'),
        'while len(L) > x': lambda S, B, r: (f'`len(L) = {len(S.L)} > x = {S.x}` → L 太多，把最弱的挪回 R' if len(S.L) > S.x else f'`len(L) = {len(S.L)}` ≤ x，大小刚好'),
        'p = R[-1]': 'R 里最大的 `{p}` 是候选里最强的，准备挪进 L',
        'p = L[0]': 'L 里最小的 `{p}` 是前 x 种里最弱的，准备挪走',
        'R.remove(p)\n            L.add(p)': None,
        'ans[l] = sum_l': '窗口 `[{l}, {r}]` 的 x-sum = `sum_l` = =={ans[l]}==',
        'out = nums[l]': '窗口左端 `nums[{l}] = {out}` 要离开了',
        'cnt[out] -= 1': '`cnt[{out}]` 减一 → =={cnt[out]}==，之后用新次数把它加回去（次数为 0 就不加）',
        'return ans': '所有窗口的 x-sum：`{ans}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='把「值」换成「(次数, 值)」二元组，对顶有序集合维护前 x 大',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['窗口内每种数按出现次数排序，次数相同数值大的更靠前，只保留前 `x` 种，求保留元素之和',
                 '对每个长为 `k` 的子数组求 x-sum',
                 '本视频：`[1,1,2,3]`，`k=3`，`x=2` → `[4,5]`；次数相同时数值大的优先（3 比 1 强）'],
        quote='本题要维护前 x 大的二元组 (cnt[x], x)，以及 cnt[x]·x 的总和。……其余逻辑同 3013 题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`L` 保存前 `x` 大的 `(次数, 值)`，`R` 保存其余；`sum_l` 是 `L` 里 次数×值 之和',
              '元素进出窗口：==先删旧二元组，改次数，再加新二元组==，同时维护 `sum_l`',
              '每个窗口末尾：`R` 太强就 `r2l`，`L` 太多就 `l2r`，再记录 `sum_l`'],
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '原文 `from sortedcontainers import SortedList` 在这里用 `list` 子类 + `bisect` 写了最小替代（演示用）',
                 '易错点：次数变化前必须先 `remove` 旧二元组，否则找不到；次数为 0 的值不放进集合',
                 '二元组比较天然满足「次数相同比数值」',
                 '前置题：295、480、3013'],
    ),
)
