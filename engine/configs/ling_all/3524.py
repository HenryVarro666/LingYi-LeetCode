def _tgt(S):
    return S['y'] * S['v'] % S['k'] if 'y' in S and 'v' in S else None


CONFIG = dict(
    num=3524, title='求出数组的 X 值 I', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='子数组 DP · 刷表法 · 滚动数组',
    tags=['灵神题单', '动态规划', '难度分 2008'],
    code='''
class Solution:
    def resultArray(self, nums: List[int], k: int) -> List[int]:
        ans = [0] * k
        f = [0] * k
        for v in nums:
            nf = [0] * k
            nf[v % k] = 1
            for y, c in enumerate(f):
                nf[y * v % k] += c
            f = nf
            for x, c in enumerate(f):
                ans[x] += c
        return ans
''',
    call='Solution().resultArray([1,2,3,4], 3)',
    expect=[6, 2, 2],
    skip=['for y, c', 'for x, c', 'ans = [0] * k'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前右端点 v）', h=130, cell=80,
             color=lambda S, i, x: 'blue' if 'v' in S and x == S['v'] else None),
        dict(type='text', size=26, h=56, fn=lambda S: (
            f"右端点 `v = {S['v']}`：旧状态 `f[{S['y']}]` 的 {S['c']} 个子串乘上 v → 余数 `{S['y']}×{S['v']} mod {S['k']} = {_tgt(S)}`"
            if S.get('_line') == 9 and 'y' in S else
            '`f[x]` = 以当前元素结尾、乘积模 k 余 x 的子数组个数')),
        dict(type='array', var='f', label='f（上一轮：右端点 i-1）', h=130, cell=90,
             color=lambda S, i, x: 'pink' if S.get('_line') == 9 and i == S.get('y') else None),
        dict(type='array', var='nf', label='nf（这一轮：右端点 i，刷表法写入）', h=130, cell=90,
             color=lambda S, i, x: 'yellow' if S.get('_line') in (8, 9) and i == (_tgt(S) if S.get('_line') == 9 else S['v'] % S['k']) else None),
        dict(type='array', var='ans', label='ans（累加每个右端点的 f）', h=130, cell=90,
             color=lambda S, i, x: 'green' if S.get('_line') == 12 and i == S.get('x') else None),
    ],
    watch=[('v', 'v', 'blue'), ('y', 'y', 'pink'), ('c', 'c', 'cyan'), ('k', 'k', 'orange')],
    captions={
        ' f = [0] * k': '`f[x]`：右端点为 i-1、元素积模 k 等于 x 的子数组个数，一开始没有子数组',
        'for v in nums': '枚举右端点，新元素 `v = {v}`',
        'nf = [0] * k': '新开一行 `nf`，装右端点为 i 的子数组',
        'nf[v % k] = 1': '`v` 自己单独成一个子数组，积模 k 是 `{v} % {k} = {v % k}` → `nf[{v % k}] = 1`',
        'nf[y * v % k] += c': '刷表法：`{c}` 个余数为 `{y}` 的子数组乘上 `{v}` → 余数 `{y} × {v} % {k} = {y * v % k}`，`nf[{y * v % k}]` 加 {c}',
        ' f = nf': '这一轮成了下一轮的“上一轮”：`f = {nf}`',
        'ans[x] += c': '右端点为 i 的所有子数组计入答案：`ans[{x}] += {c}` → =={ans}==',
        'return ans': '每个余数 x 对应的子数组个数 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举右端点：旧余数乘上新元素，刷表到新余数',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['去掉任意不重叠的前缀和后缀，剩下的是一个==非空子数组==',
                 '对每个 `x`，统计有多少个子数组的元素积模 `k` 等于 `x`',
                 '示例：`nums = [1,2,3,4,5], k = 3` → `[9,2,4]`（视频里用 `[1,2,3,4]`）'],
        quote='要计算右端点为 i 的、元素积模 k 等于 x 的子数组的个数，需要知道右端点为 i-1 的、元素积模 k 等于 y 的子数组的个数。',
        quote_src='—— 灵茶山艾府题解（寻找子问题）',
        idea=['类比 53 题最大子数组和：右端点 `i-1` 的子数组拼上 `nums[i]` 就是右端点 `i`',
              '只关心积模 k，用 `(a·b) mod k = ((a mod k)·b) mod k` 边乘边取模',
              '==刷表法==：枚举 `y`，更新 `nf[y·v % k]`；`v` 自己再加一个子数组'],
        summary=['时间 `O(nk)`，空间 `O(k)`（原先 `f` 是 `n+1` 行，滚动后只留一行）',
                 '易错：别忘了 `v` 单独成子数组 `nf[v % k] = 1`',
                 '`ans` 是每个右端点的 `f` 逐项累加，不是只取最后一行',
                 '空间优化前的二维 `f[i+1][...]` 写法思路完全一样；相似题：3448'],
    ),
)
