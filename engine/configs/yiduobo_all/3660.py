def _fmt(v):
    return '·' if v is None else str(v)


def _rcol(S, i, v):
    return 'green' if v is not None else None


CONFIG = dict(
    num=3660, title='跳跃游戏 IX', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='向左最大下标 + 树状数组求向右最远 + 记忆化',
    tags=['灵神题单', '难度分 2187'],
    code='''
class Solution(object):
    def maxValue(self, nums):
        
        n = len(nums)

        left = [0]
        for index in range(1, n):
            if nums[index] >= nums[left[-1]]:
                left.append(index)
            else:
                left.append(left[-1])
        
        mapping = {}
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = len(mapping) + 1
        

        m = len(mapping)
        f = [-1] * (m + 1)

        def add(x, v):
            while x <= m:
                f[x] = max(f[x], v)
                x += x & -x
        
        def get(x):
            ma = -1
            while x:
                ma = max(ma, f[x])
                x -= x & -x
            return ma

        rightest = [-1]
        add(mapping[nums[-1]], n - 1)
        for index in range(n - 2, -1, -1):
            rightest.append(get(mapping[nums[index]] - 1))
            add(mapping[nums[index]], index)
        rightest.reverse()
        
        
        res = [None] * n
        
        def calc(index, res):
            if res[index] is None:
                p = left[index]
                if p != index:
                    res[index] = calc(p, res)
                elif rightest[index] == -1 or left[rightest[index]] == index:
                    res[index] = nums[index]
                else:
                    res[index] = calc(rightest[index], res)
            
            return res[index]

        for index in range(n):
            if res[index] is None:
                calc(index, res)
        
        return res
''',
    call='Solution().maxValue([2,3,1])',
    expect=[3,3,3],
    max_steps=90,
    skip=[14, 15, 25, 31, 36],
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums', cell=56, h=150),
        dict(type='array', var='left', label='left（前缀最大值的下标）', cell=56, h=120),
        dict(type='array', var='rightest', label='rightest（向右最远下标，-1 = 没有）', cell=56, h=120),
        dict(type='array', var='res', label='res（· = 还没算）', color=_rcol, cell=56, h=120),
        dict(type='calls', h=120),
    ],
    watch=['index', ('mapping', 'mapping'), ('f', 'f')],
    captions={
        6: '`left[i]`：`nums[0..i]` 里最大值的下标，向左跳时就跳到这里',
        8: lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` ≥ 当前前缀最大 `{S.nums[B.left[-1]]}`？' + ('成立：它成为新的最大' if S.nums[S.index] >= S.nums[B.left[-1]] else '不成立：最大值不变')),
        9: '新的前缀最大值 → `left` 记下 `{index}`（相等也取靠右）',
        11: '最大值没变 → `left` 沿用 `{left[-1]}`',
        14: '离散化：先把值从小到大排好，按顺序给每个不同的值编号（树状数组下标从 1 开始）',
        16: '`{v}` 的排名 = `{mapping[v]}`',
        19: '`m` = 不同取值个数 = {m}，树状数组大小 `m + 1`',
        20: '`f` 是树状数组，`f[x]` 存「排名区间内的最大下标」，初始 -1',
        23: lambda S, B, r: (f'`x = {S.x}` ≤ m：把下标 `{S.v}` 写进树状数组的第 `{S.x}` 格' if S.x <= S.m else f'`x = {S.x}` > m：已经越界，更新结束'),
        24: '`f[{x}]` 取较大的下标 → {f[x]}',
        25: '`x += x & -x`：跳到父结点 `{x}`',
        28: '`get(x)`：查排名 ≤ x 的最大下标，即「比当前值小」的数里下标最大的',
        29: lambda S, B, r: (f'`x = {S.x}` 非 0：还要查' if S.x else '`x = 0`：查完了'),
        30: '`ma = max(ma, f[{x}])` = {ma}',
        31: '`x -= x & -x`：跳到前一段 `{x}`',
        32: '查询结果 `{ret}`',
        34: '`rightest[i]` = 向右能跳到的最远下标；最后一位右边没有，记 -1',
        35: '最后一个数先放进树状数组：排名 `{mapping[nums[-1]]}`，下标 `{n - 1}`',
        36: lambda S, B, r: ('倒着扫完了' if 'index' not in S or (B.get('index') == S.get('index') and False) else f'倒着扫 `index = {S.index}`'),
        37: '`mapping[nums[index]] - 1` 之内都是更小的数，取其中下标最大的 → `rightest` 追加',
        38: '把 `nums[{index}]` 也放进树状数组，供更左边的数查询',
        39: '`rightest` 是倒着追加的，翻转后与下标对齐：`{rightest}`',
        42: '`res` 全为 None（·），用类似记忆化搜索的 `calc` 填',
        46: '`p = left[{index}] = {p}`：向左能跳到的最大值的下标',
        47: lambda S, B, r: (f'`p = {S.p}` ≠ `index = {S.index}`：向左跳能变大 → 答案和 `p` 一样，递归算 `p`' if S.p != S.index else f'`p = index = {S.index}`：向左无处可跳，试试向右'),
        48: '`res[index] = calc(p, res)`：递归求 `p` 的答案，直接拿来当自己的答案',
        49: lambda S, B, r: (f'`rightest[{S.index}] = {S.rightest[S.index]}`，`left[...] = {S.left[S.rightest[S.index]] if S.rightest[S.index] != -1 else "-"}`：右边没有可跳，或跳过去又只能回到 `{S.index}` → 不用反复横跳'
                             if (S.rightest[S.index] == -1 or S.left[S.rightest[S.index]] == S.index) else
                             f'`rightest[{S.index}] = {S.rightest[S.index]}`：向右跳到最远处，再从那里向左跳能到更大的数 → 递归'),
        50: '没法变得更大：`res[{index}] = nums[{index}] = {res[index]}`',
        52: '`res[index] = calc(rightest[index], res)`：递归求「向右最远位置」的答案，直接拿来用',
        54: '返回 `res[{index}] = {ret}`',
        57: lambda S, B, r: (f'`res[{S.index}]` 还没算 → 调用 `calc`' if S.res[S.index] is None else f'`res[{S.index}] = {S.res[S.index]}` 已经算好（记忆化）→ 跳过'),
        60: '全部算完 → `{ret}`',
    },
    cards=dict(
        one_liner='向左跳到前缀最大，向右跳到最远，反复横跳 + 记忆化',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['向后只能跳到==更小==的数，向前只能跳到==更大==的数',
                 '对每个下标求：跳任意多次能到达的==最大值==',
                 '示例：`[2,3,1]` → `[3,3,3]`'],
        quote='对于向左跳的操作，应该跳到目前可达的数值最大的位置……而对于向右跳的操作，则应该跳到最远而不是数值最小的位置，因为向右跳的目的是为了能通过向左跳到达数值更大的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心：先向左跳到最大值，再向右跳到==最远==，再向左…直到不再变大',
              '`left[i]`：前缀最大值的下标；`rightest[i]`：向右最远能跳到的下标（离散化 + 树状数组求）',
              '`calc` 记忆化：`left` 能跳就递归 `left`；否则看 `rightest`，无处可去就是自己'],
        summary=['时间 `O(n log n)`（树状数组），空间 `O(n)`',
                 '`rightest` 向右只看更小的值，所以树状数组查的是排名 `- 1` 的前缀',
                 '`calc` 里 `p != index` 必须先判断：能向左跳就一定先向左',
                 '原文无 Python 2 专有写法，未做修改',
                 '对比灵神：灵神用 `pre_max` 与 `suf_min` 的分界线 `O(n)` 解决；yiduobo 模拟跳跃路径'],
    ),
)
