CONFIG = dict(
    num=3737, title='统计主要元素子数组数目 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='±1 前缀和 + 树状数组', tags=[],
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
    call='Solution().countMajoritySubarrays([1,2,2], 2)',
    expect=4,
    skip=['while x > 0', 'while x <= n + n + 1', 'res = 0'],
    views=[
        dict(type='array', var='nums', h=190, label='nums（绿 = 等于 target，记 +1；其余记 −1）',
             color=lambda S, i, v: 'green' if v == S['target'] else 'pink'),
        dict(type='array', var='f', h=250, label='树状数组 f：下标 x 处统计前缀和（偏移后）出现次数'),
        dict(type='text', fn=lambda S: f"前缀和 `s = {S['s']}`，查询 `get(s+n)` 统计偏移后 ≤ s 的旧前缀数" if 's' in S else '', size=30, h=90),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    max_steps=110,
    captions={
        'f = [0]': '树状数组 `f`：下标 `1..2n+1`，代表前缀和 `−n..n` 偏移后的位置',
        'add(n + 1)': '先放入空前缀（和为 0，偏移后下标 `n+1`）',
        'if v == target': lambda S, B, r: f'`{S.v}` {"==" if S.v == S.target else "≠"} `{S.target}` → ' + ('这个数记 ==+1==' if S.v == S.target else '这个数记 ==−1=='),
        'x -= x & -x': '`x` 去掉最低位 1，跳到上一段：`x = {x}`',
        'x += x & -x': '`x` 加上最低位 1，跳到覆盖它的下一段：`x = {x}`',
        'res += f[x]': '累加 `f[{x}] = {f[x]}`',
        'res += get': '查询：左边有多少个前缀和 `< s = {s}`？它们到当前位置的子数组和都 `> 0`，进入 `get({s + n})` 统计',
        'f[x] += 1': '把当前前缀和（偏移后下标 `{x}`）的计数 `+1`',
        'add(s + n + 1)': '当前前缀和入树状数组，供后面的位置查询',
        14: '查询结果：左边严格更小的前缀和共 `{res}` 个 → 以当前位置结尾的主要元素子数组有 `{res}` 个',
        31: '遍历完毕，累计 `{res}` 个以 `target` 为主要元素的子数组',
    },
    cards=dict(
        one_liner='等于 target 记 +1，否则 −1：子数组和 > 0 就是主要元素',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`target` 在子数组中出现次数 ==严格大于长度的一半== 才算主要元素',
                 '求以 `target` 为主要元素的子数组个数',
                 '示例：`nums = [1,2,2,3], target = 2` → `5`',
                 '本视频用 `[1,2,2]`，`target = 2` → `4`'],
        quote='将nums中所有等于target的元素视为1，不等于target的元素视为-1，那么问题就转化成了……问子数组和大于0的子数组数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['出现次数 > 一半 ⇔ 「+1 的个数」多于「−1 的个数」⇔ 区间和 `> 0`',
              '区间和 = 前缀和之差，所以对每个 `s` 数左边有多少前缀和 `< s`',
              '这不是「相等」，哈希表不够用 → 改用 ==树状数组== 做计数前缀和'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；II 数据 `10^5` 也能过',
                 '前缀和范围 `[−n, n]`，要加偏移 `n`（再 +1，树状数组下标从 1 开始）',
                 '`get(s+n)` 查的是前缀和 `≤ s−1`，即严格小于 `s`',
                 '本题 n ≤ 1000，O(n²) 暴力也行，yiduobo 直接给了可扩展到 II 的解法'],
    ),
)
