def _fcol(S, k, v):
    j, L = S.get('j'), S.get('carpetLen')
    if j is None or 'nf' not in S or S.get('_line') not in (12,):
        return None
    return 'yellow' if k == j - L else None


def _ncol(S, k, v):
    j = S.get('j')
    if j is None:
        return None
    if k == j:
        return 'green'
    if k == j - 1 and S.get('_line') in (12,):
        return 'blue'
    return None


CONFIG = dict(
    num=2209, title='用地毯覆盖后的最少白色砖块', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（选或不选 + 滚动数组）',
    tags=['灵神题单', '动态规划', '难度分 2106'],
    code='''
class Solution:
    def minimumWhiteTiles(self, floor: str, numCarpets: int, carpetLen: int) -> int:
        m = len(floor)
        if numCarpets * carpetLen >= m:
            return 0

        floor = list(map(int, floor))
        f = list(accumulate(floor))
        for i in range(1, numCarpets + 1):
            nf = [0] * m
            for j in range(carpetLen * i, m):
                nf[j] = min(nf[j - 1] + floor[j], f[j - carpetLen])
            f = nf
        return f[-1]
''',
    call="Solution().minimumWhiteTiles('10110101', 2, 2)",
    expect=2,
    skip=['for j in range'],
    views=[
        dict(type='array', var='floor', label='floor（1 = 白砖，要尽量盖住）', h=190, cell=76, pointers={'j': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('j') else None)),
        dict(type='array', var='f', label='f：已有 i-1 条地毯时的答案（黄 = 选覆盖时用到的 f[j-carpetLen]）', h=170, cell=76, color=_fcol),
        dict(type='array', var='nf', label='nf：用 i 条地毯的答案（蓝 = nf[j-1]，绿 = 正在算的 nf[j]）', h=170, cell=76, color=_ncol),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'blue'), ('carpetLen', 'carpetLen', 'orange'), ('nf[j]', 'nf[j]', 'green')],
    captions={
        'm = len(floor)': '`m = {m}` 块砖',
        'if numCarpets * carpetLen >= m': lambda S, B, r: (f'`{S.numCarpets} × {S.carpetLen} = {S.numCarpets * S.carpetLen}` < `{S.m}`：地毯盖不完，需要 DP'
                                                           if S.numCarpets * S.carpetLen < S.m else '地毯总长够盖满所有砖 → 直接返回 0'),
        'floor = list(map': '字符串转成 0/1 数组，白砖 = 1，方便直接累加',
        'f = list(accumulate': '0 条地毯：每块白砖都留着，答案就是前缀和 → `f = {f}`',
        'for i in range': '`i = {i}`：多用一条地毯，`nf` 只依赖上一轮的 `f`',
        'nf = [0] * m': '新数组 `nf` 全 0：前 `carpetLen × i` 块砖可以被全部盖住，不用算',
        'nf[j] = min': '`j = {j}`：不盖这块 `{nf[j-1]} + {floor[j]}`，盖住就是 `f[{j-carpetLen}] = {f[j-carpetLen]}` → 取小 =={nf[j]}==',
        'f = nf': '第 `{i}` 条地毯算完，`nf` 变成新的 `f`',
        'return f[-1]': '用满 `{numCarpets}` 条地毯，最少剩 =={ret}== 块白砖',
    },
    cards=dict(
        one_liner='从右往左看最后一块砖：不盖加它自己，盖就用掉一条地毯跳过 carpetLen 块',
        complexity='时间 `O(numCarpets·m)`，空间 `O(m)`',
        problem=['`floor` 的 `1` 是白砖、`0` 是黑砖，有 `numCarpets` 条长 `carpetLen` 的黑地毯',
                 '地毯可以互相重叠，求没被盖住的白砖最少有几块',
                 '示例：`"10110101"`，`2` 条，长 `2` → `2`'],
        quote='考虑 floor[j] 是否覆盖（选或不选）……覆盖（选）：如果 i>0，接下来要解决的问题是，用 i-1 条地毯覆盖下标在 [0,j-carpetLen] 中的砖。',
        quote_src='—— 灵茶山艾府题解（二、状态定义与状态转移方程）',
        idea=['`dfs(i, j)`：用 `i` 条地毯处理 `floor[0..j]` 的最少白砖数',
              '不盖：`dfs(i, j-1) + floor[j]`；盖：`dfs(i-1, j-carpetLen)`，两者取小',
              '1:1 翻译成递推后，`f[i]` 只用到 `f[i-1]`，用两个数组滚动'],
        summary=['时间 `O(numCarpets·m)`，空间 `O(m)`',
                 '题解先给记忆化搜索、再 1:1 翻成二维递推，最后滚动数组；这里演示最后一种',
                 '先特判 `numCarpets × carpetLen >= m`，直接返回 0',
                 '`j` 从 `carpetLen × i` 开始：更小的 `j` 本来就能全部盖住，值为 0',
                 '同类划分型 DP：§6.3 约束划分个数'],
    ),
)
