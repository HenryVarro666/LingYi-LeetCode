def _t(S):
    if 's' not in S or 'f' not in S:
        return ''
    n = len(S['nums'])
    return f"当前前缀和 `s = {S['s']}`；树状数组下标 = s + n + 1 = =={S['s'] + n + 1}==（前缀和平移到正数）"


CONFIG = dict(
    num=3739, title='统计主要元素子数组数目 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='±1 前缀和 + 树状数组',
    tags=['前缀和与哈希表', '难度分 2090'],
    code='''
class Solution(object):
    def countMajoritySubarrays(self, nums, target):
        
        n = len(nums)
        f = [0] * (n + n + 2)
        s = 0
        res = 0

        def get(x):
            res = 0
            while x > 0:
                res += f[x]
                x -= x & -x
            return res
        
        def add(x):
            while x <= n + n + 1:
                f[x] += 1
                x += x & -x

        add(n + 1)
        for v in nums:
            if v == target:
                s += 1
            else:
                s -= 1
            
            res += get(s + n)
            add(s + n + 1)
        
        return res
''',
    call='Solution().countMajoritySubarrays([1,2,2,3], 2)',
    expect=5,
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums（== target 记 +1，其余 −1）', h=170, cell=100,
             color=lambda S, i, v: 'green' if v == S['target'] else None),
        dict(type='array', var='f', label='f：树状数组（下标 1 起；各下标 = 前缀和 + n + 1）', h=230, cell=80,
             pointers={'x': 'blue'}),
        dict(type='text', h=110, size=28, fn=_t),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'cyan'), ('x', 'x', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'f = [0]': '树状数组 `f` 长 `2n+2 = {len(f)}`，下标从 1 用起',
        6: '`s` 是当前前缀和',
        7: '`res` 累计答案',
        10: '`get` 里的局部 `res` 从 0 开始累加',
        'def get': '`get(x)`：查下标 ≤ x 的前缀个数（树状数组前缀查询）',
        'def add': '`add(x)`：下标 x 个数 +1，并向上更新',
        'while x > 0': lambda S, B, r: (f'`x = {S.x} > 0`，继续累加' if S.x > 0 else '`x = 0`，查询结束'),
        'res += f[x]': '累加 `f[{x}] = {f[x]}` → `{res}`',
        'x -= x & -x': '去掉 x 的最低位 1：`x = {x}`',
        'while x <= n + n + 1': lambda S, B, r: (f'`x = {S.x}` 没越界，继续更新' if S.x <= 2 * S.n + 1 else f'`x = {S.x}` 越界，更新结束'),
        'f[x] += 1': '`f[{x}]` 加一 → `{f[x]}`',
        'x += x & -x': '加上最低位 1，更新上一层：`x = {x}`',
        'add(n + 1)': '先放入空前缀（和 0）：下标 `n + 1 = {n + 1}`',
        'for v in nums': lambda S, B, r: (f'取下一个数 `v = {S.v}`' if S.f[1 << ((2 * S.n + 1).bit_length() - 1)] <= S.n else '遍历结束'),
        'if v == target': lambda S, B, r: (f'`{S.v} == {S.target}`：记 +1' if S.v == S.target else f'`{S.v} ≠ {S.target}`：记 −1'),
        's += 1': '`s = {s}`',
        's -= 1': '`s = {s}`',
        'res += get': '查之前前缀和 ≤ `s − 1` 的个数 `get(s + n) = {get(s + n)}`，它们都满足 `s[j] − s[i] > 0` → `res = {res}`',
        'add(s + n + 1)': '把当前前缀和 `s = {s}` 记进树状数组（下标 `{s + n + 1}`）',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='target 记 +1、其余 −1，树状数组数「比 s 小的前缀」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['主要元素：在子数组中出现次数 ==严格大于== 长度的一半',
                 '求以 `target` 为主要元素的子数组个数，`n` 可达 `10^5`',
                 '示例：`[1,2,2,3], target = 2` → `5`'],
        quote='对于本题，需要计算的是对于每个前缀和s，其左侧所有小于s的前缀和的数目，因此在这里不能继续使用哈希表，而是需要使用树状数组来处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['转成 ±1 数组后，要的是子数组和 `> 0`，不是恰好等于 0',
              '“恰好等于”能用哈希表；“小于 s 的个数”要树状数组',
              '前缀和范围 `[−n, n]`，整体加 `n + 1` 变成树状数组下标'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：下标偏移——查询用 `s + n`（即 ≤ s−1），插入用 `s + n + 1`',
                 '起始要先 `add(n + 1)` 放入空前缀',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神利用 s 每次只变 1，用 f 增量维护做到 O(n)'],
    ),
)
