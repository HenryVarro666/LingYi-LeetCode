def _tgt(S):
    return S['x'] * S['v'] % S['k'] if 'x' in S and 'v' in S else None


CONFIG = dict(
    num=3524, title='求出数组的 X 值 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='以 nums[i] 结尾的子数组 DP · 滚动数组',
    tags=['灵神题单', '动态规划', '难度分 2008'],
    code='''
class Solution(object):
    def resultArray(self, nums, k):
        
        f = [0] * k
        res = [0] * k
        for v in nums:
            g = f[:]
            f = [0] * k
            f[v % k] += 1
            for x, pre in enumerate(g):
                f[x * v % k] += pre
        
            for x in range(k):
                res[x] += f[x]

        return res
''',
    call='Solution().resultArray([1,2,3,4], 3)',
    expect=[6, 2, 2],
    skip=['for x, pre', 'for x in range', 'res = [0] * k'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前元素 v）', h=130, cell=80,
             color=lambda S, i, x: 'blue' if 'v' in S and x == S['v'] else None),
        dict(type='text', size=26, h=56, fn=lambda S: (
            f"`g[{S['x']}] = {S['pre']}` 个子数组接上 `{S['v']}`：余数 `{S['x']}×{S['v']} mod {S['k']} = {_tgt(S)}` → 累加到 `f[{_tgt(S)}]`"
            if S.get('_line') == 11 and 'x' in S else
            '`f[x]` = 以当前元素结尾、乘积模 k 余 x 的子数组数量')),
        dict(type='array', var='g', label='g（上一轮 f[index-1]）', h=130, cell=90,
             color=lambda S, i, x: 'pink' if S.get('_line') == 11 and i == S.get('x') else None),
        dict(type='array', var='f', label='f（这一轮 f[index]）', h=130, cell=90,
             color=lambda S, i, x: 'yellow' if S.get('_line') in (9, 11) and i == (_tgt(S) if S.get('_line') == 11 else S['v'] % S['k']) else None),
        dict(type='array', var='res', label='res（逐轮累加 f）', h=130, cell=90,
             color=lambda S, i, x: 'green' if S.get('_line') == 14 and i == S.get('x') else None),
    ],
    watch=[('v', 'v', 'blue'), ('x', 'x', 'pink'), ('pre', 'pre', 'cyan'), ('k', 'k', 'orange')],
    captions={
        4: '`f[x]`：以 `nums[index]` 结尾的子数组中，乘积模 k 余 x 的个数；先全 0',
        'for v in nums': '处理下一个元素 `v = {v}`，它是新的子数组结尾',
        'g = f[:]': '把上一轮的 `f` 备份成 `g`：`g = {g}`，下面要读它、写新的 `f`',
        8: '新一轮 `f` 先初始化为 0',
        'f[v % k] += 1': '`{v}` 单独成子数组，余数 `{v} % {k} = {v % k}` → `f[{v % k}]` 加 1',
        'f[x * v % k] += pre': '把 `{pre}` 个余数为 `{x}` 的旧子数组末尾接上 `{v}`：余数变 `{x} × {v} % {k} = {x * v % k}`，`f[{x * v % k}]` 加 {pre}',
        'res[x] += f[x]': '以 `{v}` 结尾的子数组计入答案：`res[{x}] += {f[x]}` → =={res}==',
        'return res': '`res[x]` 就是积模 k 余 x 的子数组总数 = =={ret}==',
    },
    cards=dict(
        one_liner='子数组 = 取走前后缀剩下的部分，按结尾元素做 DP',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['移除任意不重叠的前缀和后缀，剩下的就是==一个子数组==',
                 '问有多少个子数组的乘积模 `k` 余 `x`，对每个 `x` 输出',
                 '示例：`nums = [1,2,3,4,5], k = 3` → `[9,2,4]`（视频用 `[1,2,3,4]`）'],
        quote='题目中描述的操作，实际上就是取出nums中的某个子数组，因此题目实际上问的是nums中有多少个子数组，其乘积模k的结果为x。由于题目中k的取值范围不大，因此可以直接使用动态规划进行求解。',
        quote_src='—— yiduobo 题解',
        idea=['`f[index][x]`：以 `nums[index]` 结尾、乘积模 k 余 x 的子数组数',
              '先加上 `nums[index]` 单独成的子数组；再把 `f[index-1][x]` 接上它，累加到 `f[index][x*nums[index]%k]`',
              '`f` 只依赖上一轮，用 `g` 备份 + 新 `f` 滚动掉 `index` 这一维'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '易错：必须先备份 `g = f[:]` 再清空 `f`，否则读到的是新值',
                 '`nums[index]` 单独成子数组别漏，余数是 `v % k`',
                 '`res` 是每一轮 `f` 的累加，不是最后一轮的 `f`'],
    ),
)
