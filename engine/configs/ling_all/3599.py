N0 = [2, 3, 3, 2]
K0 = 3


def _on(S):
    return S.get('_line') in (11, 12, 13, 14) and 'l' in S and 'j' in S


def _txt(S):
    if 'i' not in S:
        return '`f[j]`：把前 `j` 个数分成 `i` 段，==最大段异或==的最小值（滚动数组，当前段数 `i`）'
    if _on(S):
        return (f'最后一段 `nums[{S["l"]}..{S["j"] - 1}]` 异或 `s = {S["s"]}`；'
                f'前面 `f[{S["l"]}] = {S["f"][S["l"]] if S["f"][S["l"]] != float("inf") else "inf"}`')
    return f'第 `{S["i"]}` 段：算 `f[j]`，==j 倒序==，避免覆盖还要用的旧值'


CONFIG = dict(
    num=3599, title='划分数组得到最小 XOR', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 空间优化',
    tags=['灵神核心路线', '灵神题单·图论算法', '难度分 1955'],
    code='''
# 另见【Python3 更快写法】，避免函数调用，减少赋值次数
min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

class Solution:
    def minXor(self, nums: List[int], k: int) -> int:
        n = len(nums)
        f = [0] + [inf] * n
        for i in range(1, k + 1):
            for j in range(n - (k - i), i - 1, -1):
                res = inf
                s = 0
                for l in range(j - 1, i - 2, -1):
                    s ^= nums[l]
                    res = min(res, max(f[l], s))
                f[j] = res
        return f[n]
''',
    call=f'Solution().minXor({N0!r}, {K0})',
    expect=2,
    skip=['min = lambda', 'max = lambda', 'n = len(nums)', 'res = inf', 's = 0'],
    views=[
        dict(type='array', var='nums', label='nums（粉 = 最后一段 nums[l..j-1]）', h=190, cell=90,
             pointers={'l': 'pink'},
             color=lambda S, i, v: ('pink' if _on(S) and S['l'] <= i < S['j'] else None)),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='f', label='f[j]（下标 j = 前缀长度；第 i 段滚动更新）', h=230, cell=100,
             pointers={'j': 'blue'},
             color=lambda S, i, v: ('yellow' if 'j' in S and i == S['j'] and S.get('_line') == 15 else 'blue' if _on(S) and i == S['l'] else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('l', 'l', 'pink'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [0] + [inf]': '`f[0] = 0`（空前缀分 0 段），其余是 `inf`：==无法把非空数组分成 0 段==',
        'for i in range(1, k + 1)': lambda S, B, r: (f'现在分成 `i = {S.i}` 段' if S.get('i') != B.get('i') else '`k` 段都算完了'),
        'for j in range(n - (k - i)': lambda S, B, r: (
            f'前缀长度 `j = {S.j}`：下界 `i`，上界 `n-(k-i) = {len(S.nums) - (S.k - S.i)}`，给后面 `{S.k - S.i}` 段留数；==倒序==保护旧值'
            if S.get('j') != B.get('j') else f'`i = {S.i}` 这一层的 `f[j]` 都更新完了'),
        'for l in range': lambda S, B, r: (f'枚举最后一段的左端点 `l = {S.l}`，==倒着==枚举，`s` 才能 O(1) 更新' if not (S.get('l') == B.get('l') and S.get('s') == B.get('s')) else '左端点枚举完毕'),
        's ^= nums[l]': '最后一段 `nums[{l}..{j-1}]` 的异或：`s ^= nums[{l}]` → =={s}==',
        'res = min(res, max(': '这种分法：前面 `f[{l}]` = `{f[l]}`，最后一段 `s = {s}` → 最大段取大 `{max(f[l], s)}`，所有分法取小 → `res` = =={res}==',
        'f[j] = res': '`f[{j}] = {res}`：前 `{j}` 个数分 `{i}` 段的最优',
        'return f[n]': '前 `{n}` 个数分 `{k}` 段，最大异或和最小 = =={ret}==',
    },
    cards=dict(
        one_liner='划分型 DP：枚举最后一段，前面最大与这段取大，再取小',
        complexity='时间 `O(k(n-k)^2)`，空间 `O(n)`',
        problem=['把数组 `nums` 分成 `k` 个非空连续子数组，每段取按位 XOR',
                 '求 ==各段 XOR 的最大值== 的 ==最小值==',
                 '示例：`nums = [2,3,3,2], k = 3` → `2`（`[2] [3,3] [2]`）'],
        quote='和「§5.3 约束划分个数」是一个套路：把数组分成恰好 k 个连续子数组，计算与这些子数组有关的最优值。……为什么要倒着枚举？这样可以一边枚举，一边 O(1) 计算子数组异或和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]`：前 `j` 个数分 `i` 段的最优；枚举最后一段左端点 `L`',
              '`f[i][j] = min(max(f[i-1][L], s(L,j)))`，`s` 是最后一段的异或',
              '只依赖上一层 → 像 0-1 背包去掉第一维，`j` ==倒序=='],
        summary=['时间 `O(k(n-k)^2)`，空间 `O(n)`',
                 '`f[0] = 0`、其余 `inf`：无法把非空数组分成 0 段',
                 '`j` 的范围要给前后的段预留空间：`i ≤ j ≤ n-(k-i)`',
                 '另有 2D 版本、记忆化搜索、二分答案 + 位运算 DP、Dijkstra（边权取 max）等写法，本视频演示空间优化版',
                 '异或没有单调性，二分答案仍要写 DP，不如直接 DP'],
    ),
)
