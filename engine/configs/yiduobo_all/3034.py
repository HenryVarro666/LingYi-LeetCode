NUMS = [1, 4, 4, 1, 3, 5, 5, 3]
PAT = [1, 0, -1]


def _diff(S):
    n = S.get('nums')
    if not n:
        return None
    return [(n[k] > n[k - 1]) - (n[k] < n[k - 1]) for k in range(1, len(n))]


def _pat_color(S, i, v):
    if S['_line'] >= 13 and 'p' in S and i < S['p']:
        return 'green'
    return None


CONFIG = dict(
    num=3034, title='匹配模式数组的子数组数目 I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='差分转 -1/0/1 + KMP',
    tags=[],
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
    call=f'Solution().countMatchingSubarrays({NUMS}, {PAT})',
    expect=2,
    skip=['f = [0]', 'res = 0', 'p = 0'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前比较的 nums[index]）', cell=70, h=170,
             pointers={'index': 'blue'}, index=True),
        dict(type='array', var=_diff, label='相邻关系（1 升 / 0 平 / -1 降），蓝 = 当前这一对', cell=70, h=130,
             color=lambda S, i, v: 'blue' if S['_line'] >= 15 and 'index' in S and i == S['index'] - 1 else None),
        dict(type='array', var='pattern', label='pattern（绿 = 已匹配前缀，p = 下一个要匹配的位置）', cell=70, h=190,
             pointers={'p': 'blue'}, color=_pat_color),
        dict(type='array', var='f', label='f：最长相同前后缀（失配时 p 回退到 f[p-1]）', cell=70, h=130),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'blue'), ('v', 'v', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for index in range(1, len(pattern))': lambda S, B, r: ('`f` 建好了：`' + str(S.f) + '`' if getattr(B, 'index', None) == S.index else f'先对 `pattern` 建 f 数组（KMP 的 next），`index = {S.index}`'),
        'while p and pattern[p] != pattern[index]': lambda S, B, r: (
            f'`p = {B.p}`：`pattern[{B.p}]={B.pattern[B.p]}` 与 `pattern[{B.index}]={B.pattern[B.index]}` 不等 → ==p 回退到 f[p-1]=={B.f[B.p-1]}'
            if B.p and B.pattern[B.p] != B.pattern[B.index] else
            ('`p = 0`，无法再回退' if not B.p else '相等，不用回退')),
        'if pattern[p] == pattern[index]': lambda S, B, r: (
            f'`pattern[{B.p}]={B.pattern[B.p]}` == `pattern[{B.index}]={B.pattern[B.index]}` → 前缀能再延长一位'
            if B.pattern[B.p] == B.pattern[B.index] else f'`pattern[{B.p}]={B.pattern[B.p]}` ≠ `pattern[{B.index}]={B.pattern[B.index]}` → 这一位的前后缀长度保持 `{B.p}`'),
        'f.append(p)': '`f[{index}] = {p}`',
        'for index in range(1, len(nums))': lambda S, B, r: ('`nums` 扫完了' if getattr(B, 'index', None) == S.index and B.index == len(S.nums) - 1 else f'把 `nums` 相邻两项比大小，当作模式串里的字符送进 KMP：`index = {S.index}`'),
        'if nums[index] > nums[index - 1]': lambda S, B, r: (f'`nums[{B.index}]={B.nums[B.index]}` 比 `nums[{B.index-1}]={B.nums[B.index-1]}` '
                                                           + ('大 → 记为 `1`' if B.nums[B.index] > B.nums[B.index-1] else '不大，再看是不是更小')),
        'elif nums[index] < nums[index - 1]': lambda S, B, r: (f'`nums[{B.index}]={B.nums[B.index]}` 比前一项 `{B.nums[B.index-1]}` 小 → 记为 `-1`' if B.nums[B.index] < B.nums[B.index-1] else f'`nums[{B.index}]={B.nums[B.index]}` 与前一项相等 → 记为 `0`'),
        'v = 1': '升：`v = 1`',
        'v = -1': '降：`v = -1`',
        'v = 0': '相等：`v = 0`',
        'while p and v != pattern[p]': lambda S, B, r: (
            f'`v={B.v}` 与 `pattern[{B.p}]={B.pattern[B.p]}` 不匹配，已匹配 `{B.p}` 个 → ==用 f 回退：p = {B.f[B.p-1]}=='
            if B.p and B.v != B.pattern[B.p] else ('`p = 0`，没有已匹配的前缀可退了' if not B.p else f'`v={B.v}` 与 `pattern[{B.p}]` 相同，不用回退')),
        'if pattern[p] == v': lambda S, B, r: (
            f'`pattern[{B.p}]={B.pattern[B.p]}` == `v={B.v}` → ==匹配 +1=='
            if B.pattern[B.p] == B.v else f'`pattern[{B.p}]={B.pattern[B.p]}` ≠ `v={B.v}` → 这一位对不上，`p` 保持 {B.p}'),
        'if p == len(pattern)': lambda S, B, r: (f'`p = {S.p}`：等于 `len(pattern) = {len(S.pattern)}`，==整个模式匹配完==' if S.p == len(S.pattern) else f'`p = {S.p}`，还没匹配完整个模式'),
        'res += 1': '找到一个匹配的子数组，`res = {res}`',
        'return res': '`nums` 扫完，一共 `{res}` 个子数组匹配',
    },
    cards=dict(
        one_liner='先把 nums 变成 -1/0/1 的升降序列，再套 KMP 模式匹配',
        complexity='时间 `O(n + m)`，空间 `O(m)`',
        problem=['`pattern` 只含 `-1/0/1`，规定相邻两项 `nums[i+k+1]` 与 `nums[i+k]` 的大小关系',
                 '数一数 `nums` 中有多少个长度为 `m+1` 的子数组匹配 `pattern`',
                 '示例：`nums=[1,4,4,1,3,5,5,3]`，`pattern=[1,0,-1]` → `2`'],
        quote='如果现根据题目中nums数组相邻元素的大小关系将其转化成由-1、0、1构成的数组，那么问题就变成了非常标准的模式匹配问题，直接套用kmp算法就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻两项比大小，得到由 `1/0/-1` 组成的序列',
              '匹配条件正好是：这个序列里出现 `pattern` 作为连续子串',
              '先对 `pattern` 建 `f`（最长相同前后缀），再扫 `nums`，失配时 `p = f[p-1]`'],
        summary=['时间 `O(n + m)`，每个下标最多进出一次；第 II 题数据更大，同样适用',
                 '易错：匹配完整后要 `p = f[p - 1]`，让重叠的子数组也能被统计',
                 '易错：`nums` 下标从 `1` 开始，比较的是相邻两项，所以序列长度是 `n - 1`',
                 '原文为 Python 2 风格，仅删去类型说明，代码未改'],
    ),
)
