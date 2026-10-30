def _ph2(S):
    return S.get('_line', 0) >= 15 and 'index' in S


def _bidx(S):
    """匹配阶段：当前这对相邻元素在 b 中的下标"""
    return S['index'] - 1 if _ph2(S) else None


def _bcolor(S, k, v):
    i, p, ln = _bidx(S), S.get('p', 0), S.get('_line', 0)
    if i is None or not p:
        return None
    if ln <= 25:
        return 'green' if i - p <= k <= i - 1 else None
    return 'green' if i - p + 1 <= k <= i else None


def _b(S):
    n = S['nums']
    return [(n[i + 1] > n[i]) - (n[i + 1] < n[i]) for i in range(len(n) - 1)]


def _ncolor(S, k, v):
    if not _ph2(S):
        return None
    if k == S['index']:
        return 'blue'
    if k == S['index'] - 1:
        return 'pink'
    return None


def _top(S):
    if _ph2(S) and S['_line'] >= 16 and 'v' in S:
        i, n = S['index'], S['nums']
        r = '>' if n[i] > n[i - 1] else '<' if n[i] < n[i - 1] else '=='
        return f"`nums[{i}] = {n[i]}` {r} `nums[{i-1}] = {n[i-1]}` → 相邻关系 `v = {S['v']}`"
    return '先把相邻元素的大小关系变成 1 / 0 / -1，再做标准的 kmp 模式匹配'


CONFIG = dict(
    num=3036, title='匹配模式数组的子数组数目 II', difficulty='Hard', category='字符串',
    author='yiduobo', technique='比较相邻元素 + kmp 匹配 pattern',
    tags=['灵神题单', '字符串', '难度分 1895'],
    code='''
class Solution(object):
    def countMatchingSubarrays(self, nums, pattern):

        f = [0]
        p = 0
        for index in range(1, len(pattern)):
            while p and pattern[p] != pattern[index]:
                p = f[p - 1]
            if pattern[p] == pattern[index]:
                p += 1
            f.append(p)
        
        res = 0
        p = 0
        for index in range(1, len(nums)):
            if nums[index] > nums[index - 1]:
                v = 1
            elif nums[index] < nums[index - 1]:
                v = -1
            else:
                v = 0
            
            while p and v != pattern[p]:
                p = f[p - 1]
            if pattern[p] == v:
                p += 1
                if p == len(pattern):
                    res += 1
                    p = f[p - 1]
        
        return res
''',
    call='Solution().countMatchingSubarrays([1,2,3,4,5,6], [1,1])',
    expect=4,
    views=[
        dict(type='text', size=26, h=60, fn=_top),
        dict(type='array', var='nums', label='nums（粉 = nums[index-1]，蓝 = nums[index]）', cell=76, h=190, color=_ncolor),
        dict(type='array', var=_b, label='相邻关系 b（绿 = 当前匹配上的部分）', cell=76, h=190, color=_bcolor),
        dict(type='array', var='pattern', label='pattern（蓝箭头 = p 已匹配长度）', cell=76, h=200,
             pointers={'p': 'blue', 'index if _line < 13 else None': 'pink'}, pointer_labels={'index if _line < 13 else None': 'index'}),
        dict(type='array', var='f', label='f：pattern 的 next 数组', cell=76, h=130),
    ],
    watch=[('index', 'index', 'pink'), ('p', 'p', 'blue'), ('v', 'v'), ('f', 'f', 'green'), ('res', 'res', 'green')],
    captions={
        'f = [0]': '`f` 是 pattern 的 kmp next 数组，`f[0] = 0`',
        'p = 0': '`p` 是当前已经匹配上的长度',
        'for index in range(1, len(pattern))': lambda S, B, r: (
            f"`index = {S.index}`：看 `pattern[{S.index}]` 能不能接在前缀 `pattern[:p]` 后面" if B.get('index') is None or S.index != B.index
            else 'pattern 处理完了，`f` 建好了'),
        'while p and pattern[p] != pattern[index]': lambda S, B, r: (
            f"`pattern[{S.p}] = {S.pattern[S.p]}` ≠ `pattern[{S.index}] = {S.pattern[S.index]}`：失配，`p` 退到 `f[{S.p-1}] = {S.f[S.p-1]}`" if S.p and S.pattern[S.p] != S.pattern[S.index]
            else ('`p = 0`，没得退了' if not S.p else '已经相等，不用回退')),
        'p = f[p - 1]': lambda S, B, r: f'借助 `f` 回退：`p` → {S.p}',
        'if pattern[p] == pattern[index]': lambda S, B, r: (
            f"`pattern[{S.p}]` == `pattern[{S.index}]` = {S.pattern[S.index]} → 匹配长度加一" if S.pattern[S.p] == S.pattern[S.index]
            else f"`pattern[{S.p}] = {S.pattern[S.p]}` ≠ `pattern[{S.index}] = {S.pattern[S.index]}` → 没匹配上"),
        'p += 1': '`p` → {p}',
        'f.append(p)': '`f` 追加 `{p}`，现在 `f = {f}`',
        'res = 0': '`res` 统计匹配次数',
        'for index in range(1, len(nums))': lambda S, B, r: (
            f"`index = {S.index}`：比较 `nums[{S.index}]` 和 `nums[{S.index-1}]`" if 'v' not in B or S.index != B.index
            else 'nums 扫完了'),
        'if nums[index] > nums[index - 1]': lambda S, B, r: (
            f"`{S.nums[S.index]} > {S.nums[S.index-1]}` → 上升" if S.nums[S.index] > S.nums[S.index - 1] else f"`{S.nums[S.index]} > {S.nums[S.index-1]}` 不成立"),
        'elif nums[index] < nums[index - 1]': '`{nums[index]} < {nums[index-1]}` 成立 → 下降',
        'v = 1': '上升，`v = 1`',
        'v = -1': '下降，`v = -1`',
        'v = 0': '相等，`v = 0`',
        'while p and v != pattern[p]': lambda S, B, r: (
            f"`pattern[{S.p}] = {S.pattern[S.p]}` ≠ `v = {S.v}`：失配，`p` 退到 `f[{S.p-1}] = {S.f[S.p-1]}`，不用回头重扫 nums" if S.p and S.v != S.pattern[S.p]
            else ('`p = 0`，没得退了' if not S.p else '已经相等，不用回退')),
        'if pattern[p] == v': lambda S, B, r: (
            f"`pattern[{S.p}] = {S.pattern[S.p]}` == `v = {S.v}` → 匹配长度加一" if S.pattern[S.p] == S.v
            else f"`pattern[{S.p}] = {S.pattern[S.p]}` ≠ `v = {S.v}` → 这一位没匹配上"),
        'if p == len(pattern)': lambda S, B, r: (f'`p = {S.p} == len(pattern)` → ==整段匹配成功==' if S.p == len(S.pattern)
                                                 else f'`p = {S.p} < {len(S.pattern)}`，继续'),
        'res += 1': '找到一个子数组：`res` → {res}',
        'p = f[p - 1]': '匹配满后借助 `f` 回退：`p` → {p}，后面的匹配可以与前一个重叠',
        'return res': '共 `{res}` 个子数组匹配 pattern',
    },
    cards=dict(
        one_liner='先转成 -1/0/1 的关系序列，再套 kmp 模板',
        complexity='时间 `O(n + m)`，空间 `O(m)`',
        problem=['`pattern` 只含 `1`、`0`、`-1`，长 `m`；统计 `nums` 中长为 `m+1` 的子数组，其相邻元素的关系依次是 升 / 平 / 降',
                 '示例：`nums = [1,2,3,4,5,6]`，`pattern = [1,1]` → `4`',
                 '第二题（3036）数据规模更大，需要 `O(n)` 的 kmp'],
        quote='如果现根据题目中nums数组相邻元素的大小关系将其转化成由-1、0、1构成的数组，那么问题就变成了非常标准的模式匹配问题，直接套用kmp算法就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻元素比较：大于记 `1`，小于记 `-1`，相等记 `0`',
              '问题变成：这个序列里有几段等于 `pattern`——模式匹配',
              '先对 `pattern` 建 next 数组 `f`，再扫一遍 `nums`，边比较边匹配；匹配满了计数并用 `f` 回退'],
        summary=['时间 `O(n + m)`，空间 `O(m)`',
                 '匹配满后 `p = f[p - 1]`，允许相邻的匹配重叠（如本例 `[1,2,3]` 与 `[2,3,4]`）',
                 '`index` 从 1 开始比较 `nums[index]` 和 `nums[index - 1]`，共 `n - 1` 个关系',
                 '对比灵神：灵神用 `pairwise` 配合 `(y > x) - (y < x)` 一行算出关系；yiduobo 用 if/elif/else 写开'],
    ),
)
