def _vals(S):
    """修正后的各前缀和（按下标 0..n）：从根到叶子路径上 f 之和"""
    f, n = S['f'], len(S['nums'])
    out = []
    for j in range(n + 1):
        now, l, r, tot = 0, 0, n, 0
        while True:
            tot += f[now]
            if l == r:
                break
            m = (l + r) // 2
            if j <= m:
                now, r = now + now + 1, m
            else:
                now, l = now + now + 2, m + 1
        out.append(tot)
    return out


def _idx(S):
    return S['_inner'].get('index', S.get('index'))


def _top(S):
    if 'index' not in S:
        return ''
    v = S['nums'][S['index']]
    return f"当前 `v = {v}`（{'偶数 +1' if v % 2 == 0 else '奇数 -1'}），已计数前缀和 `s = {S['s']}`，目标：找最早等于 s 的前缀位置"


CONFIG = dict(
    num=3719, title='最长平衡子数组 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 线段树区间修正 · 区间最值定位',
    tags=[],
    code='''
class Solution(object):
    def longestBalanced(self, nums):
        
        n = len(nums)
        ma = [0] * ((n + 1) * 4)
        mi = [0] * ((n + 1) * 4)
        f = [0] * ((n + 1) * 4)
        pre = {}
        res = 0

        def update(now, left, right, start, end, delta):
            if left == start and right == end:
                f[now] += delta
                return
            
            mid = (left + right) // 2
            if end <= mid:
                update(now + now + 1, left, mid, start, end, delta)
            elif start > mid:
                update(now + now + 2, mid + 1, right, start, end, delta)
            else:
                update(now + now + 1, left, mid, start, mid, delta)
                update(now + now + 2, mid + 1, right, mid + 1, end, delta)

            ma[now] = max(ma[now + now + 1] + f[now + now + 1], ma[now + now + 2] + f[now + now + 2])
            mi[now] = min(mi[now + now + 1] + f[now + now + 1], mi[now + now + 2] + f[now + now + 2])
        
        def get(now, left, right, v):
            if left == right:
                if mi[now] <= v <= ma[now]:
                    return left
                return None
            
            mid = (left + right) // 2
            if mi[now + now + 1] <= v - f[now + now + 1] <= ma[now + now + 1]:
                return get(now + now + 1, left, mid, v - f[now + now + 1])
            else:
                return get(now + now + 2, mid + 1, right, v - f[now + now + 2])

        s = 0
        for index, v in enumerate(nums):
            if v % 2 == 0:
                delta = 1
            else:
                delta = -1

            if v not in pre:
                update(0, 0, n, index + 1, n, delta)
                s += delta
            else:
                update(0, 0, n, pre[v], index, -delta)

            pre[v] = index + 1
            p = get(0, 0, n, s)
            if p is not None:
                res = max(res, index + 1 - p)
        
        return res
''',
    call='Solution().longestBalanced([1,2,3,2])',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=24, h=50),
        dict(type='array', var='nums', label='nums（蓝 = 当前 index）', cell=70, h=130,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var=_vals, label='修正后的前缀和（下标 0..n；黄 = 等于 s，绿 = 最左的 p）', cell=70, h=140,
             color=lambda S, i, v: 'green' if 'p' in S and i == S['p'] and S['_line'] >= 54 else ('yellow' if v == S.get('s') else None)),
        dict(type='map', var='pre', label='pre（值 → 上次出现的位置 + 1）', fmt=lambda k, v: f'{k}: {v}', h=110),
        dict(type='calls', h=190),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'pink'), 'p', ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '前缀和有 `n + 1` 个（下标 0..n），线段树就建在这些前缀位置上',
        'ma = [0]': '线段树建在前缀位置 `0..n` 上，`ma[x]`：区间最大值',
        'mi = [0]': '`mi[x]`：区间最小值',
        'f = [0]': '`f[x]`：打在这个区间上、==不下放==的整体加减量',
        'pre = {}': '`pre[v]` 记录 `v` 上一次出现的位置（+1，对应前缀下标）',
        'res = 0': '`res` 是最长平衡子数组的长度',
        'for index, v': lambda S, B, r: f"处理第 {S.index} 个元素 `v = {S.v}`：{'偶数当 +1' if S.v % 2 == 0 else '奇数当 -1'}（奇偶个数相等 ⇔ 和为零）",
        'if v % 2 == 0': lambda S, B, r: f"`v = {S.v}` 是{'偶数' if S.v % 2 == 0 else '奇数'}：奇数当 -1，偶数当 +1（和为零就是奇偶个数相等）",
        'delta = 1': '偶数 `delta = 1`',
        'delta = -1': '奇数 `delta = -1`',
        'if v not in pre': lambda S, B, r: (f'`{S.v}` 第一次出现 → 所有包含它的前缀（终点在 `[{S.index + 1}, {len(S.nums)}]`）都要把它计进去' if S.v not in S.pre else f'`{S.v}` 之前出现过（位置 {S.pre[S.v]}）→ 在新的子数组里它不再独一无二'),
        'update(0, 0, n, index + 1, n, delta)': '首次出现：区间 `[{index + 1}, {n}]` 的前缀和整体加 `{1 if nums[index] % 2 == 0 else -1}`，同时当前前缀和 `s` → `{s + (1 if nums[index] % 2 == 0 else -1)}`',
        's += delta': '`s` → {s}',
        'update(0, 0, n, pre[v], index, -delta)': '重复出现：上次位置 `pre[v]` 起的前缀已经含过它，现在要把它反向抵掉：区间 `[{pre[v]}, {index}]` 整体加 `{-1 if nums[index] % 2 == 0 else 1}`',
        'f[now] += delta': '区间刚好对上：只在这个节点记下 `f += {delta}`，不用下放',
        'ma[now] = max': '子区间改完后回溯：用 `子区间最大值 + 子区间 f` 更新本区间最大值 `ma = {ma[now]}`',
        'mi[now] = min': '同理更新最小值 `mi = {mi[now]}`',
        'pre[v] = index + 1': '记下 `v` 最近出现的位置：`pre[{v}] = {index + 1}`',
        'p = get(0, 0, n, s)': '记下 `pre[{v}] = {index + 1}`。查询：修正后的前缀和里，==最左边等于 s 的位置== p（子区间 [mi, ma] 包含 s 就往里走），找到 `p = {p}`',
        'if left == right': '到叶子了：检查 `mi <= v <= ma` 是否真的等于目标',
        'if mi[now + now + 1] <= v': '看左半区间：`v - f` 是否落在左区间 `[mi, ma]` 内？是就进左边（保证最左），否则去右边',
        'if p is not None': lambda S, B, r: ((f'找到 `p = {S.p}`：子数组 `nums[{S.p}..{S.index}]` 平衡，长度 `{S.index + 1 - S.p}`' if S.index + 1 > S.p else f'`p = {S.p}` 就是当前前缀自己：空子数组，长度 `0`') if S.p is not None else '没有前缀等于 s → 没有以当前位置结尾的平衡子数组'),
        'res = max': '`res = max({B.res}, {index + 1} - {p}) = {res}`',
        'return res': '最长平衡子数组长度 `{res}`',
    },
    skip=['return', 'if left == start', 'mid = ', 'if end <=', 'elif start', 'else:', 'ma[now] = max', 'mi[now] = min',
          'if left == right', 'if mi[now + now + 1]', 'if mi[now] <= v', 'delta = 1', 'delta = -1', 's += delta', 'if v % 2 == 0', 'pre[v] = index + 1'],
    max_steps=140,
    cards=dict(
        one_liner='奇偶当 ±1，去重靠线段树事后修正前缀和',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['子数组中==不同偶数==的个数等于==不同奇数==的个数就是平衡的，求最长平衡子数组',
                 '示例：`[1,2,3,2]` → `3`（`[2,3,2]`：偶数 {2}、奇数 {3}）',
                 '`n ≤ 1500`，本视频：`[1,2,3,2]`'],
        quote='对于首次出现的元素v，将终点在[index, n]之间的前缀和都加上v对应的值；若v不是首次出现，那么就将终点在[p, index - 1]之间的前缀和都减去v对应的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['不去重时：奇数 -1、偶数 +1，找和为零的最长子数组 = 前缀和 + 哈希表',
              '要去重：当前前缀和 `s` 好算（见过就不变），难的是被减去的那些旧前缀',
              '所以反过来==修正存好的前缀和==：用线段树做区间加，并记录区间最大/最小值',
              '前缀和相邻只差 ±1，`s` 落在 `[mi, ma]` 里就一定存在，据此往左优先下探找最左位置'],
        result='`[1,2,3,2]` 最长平衡子数组长度 `3` ✓',
        summary=['时间 `O(n log n)`（每个元素一次区间修改 + 一次查询），空间 `O(n)`',
                 '易错：修改只打在节点的 `f` 上不下放，查询时要一路减去 `f`',
                 '易错：重复出现时修正的区间是 `[pre[v], index]`，不是 `[index+1, n]`',
                 '原文已是 Python 3 兼容写法（整除用 `//`），无需修改',
                 '同一思路可以直接套用到 3721（II，数据更大）'],
    ),
)
