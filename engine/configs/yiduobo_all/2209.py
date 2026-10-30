CONFIG = dict(
    num=2209, title='用地毯覆盖后的最少白色砖块', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='DP：用不用当前这条地毯 + 滚动数组',
    tags=['灵神题单', '动态规划', '难度分 2106'],
    code='''
class Solution(object):
    def minimumWhiteTiles(self, floor, numCarpets, carpetLen):

        n = len(floor)
        if numCarpets * carpetLen >= n:
            return 0
        
        f = [int(floor[0])]
        for index in range(1, n):
            f.append(f[-1] + int(floor[index]))
        
        for i in range(numCarpets):
            g = f[:]
            f = []
            for j in range(n):
                if j < carpetLen:
                    f.append(0)
                else:
                    f.append(min(f[j - 1] + int(floor[j]), g[j - carpetLen]))
        
        return f[-1]
''',
    call="Solution().minimumWhiteTiles('10110101', 2, 2)",
    expect=2,
    skip=['for j in range', 'for index in range'],
    views=[
        dict(type='string', var='floor', label='floor（1 = 白砖）', h=190, cell=76, pointers={'j': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('j') else None)),
        dict(type='array', var='g', label='g：上一轮（少一条地毯）的 f（黄 = 盖住时用到的 g[j-carpetLen]）', h=170, cell=76,
             color=lambda S, k, v: 'yellow' if S.get('j') is not None and 'g' in S and k == S['j'] - S['carpetLen'] and S.get('_line') == 19 else None),
        dict(type='array', var='f', label='f：这一轮正在算的结果', h=170, cell=76,
             color=lambda S, k, v: 'green' if k == len(S['f']) - 1 and S.get('i') is not None else None),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'blue'), ('carpetLen', 'carpetLen', 'orange')],
    captions={
        'n = len(floor)': '`n = {n}` 块砖',
        'if numCarpets * carpetLen >= n': lambda S, B, r: (f'`{S.numCarpets} × {S.carpetLen}` = {S.numCarpets * S.carpetLen} < `{S.n}`：盖不满，进入 DP'
                                                           if S.numCarpets * S.carpetLen < S.n else '地毯总长够盖满 → 答案必然是 0'),
        'f = [int(floor[0])]': '`f[j]`：0 块地毯时，`floor[0..j]` 的白砖数就是前缀和',
        'f.append(f[-1] + int': '前缀和：`f` = `{f}`',
        'for i in range': lambda S, B, r: (f'第 `{S.i + 1}` 条地毯：每一轮只依赖上一轮，所以先 `g = f[:]` 存下旧状态'
                                           if S.i != B.get('i') or 'g' not in B else '地毯都用完了'),
        'if j < carpetLen': lambda S, B, r: (f'`j = {S.j} < carpetLen = {S.carpetLen}`：不足一条地毯长，整段都能盖住' if S.j < S.carpetLen
                                             else f'`j = {S.j} >= carpetLen = {S.carpetLen}`：要比较「不用」和「用」这条地毯'),
        'g = f[:]': '`g` = 上一轮的 `f` = `{g}`',
        'f = []': '`f` 清空，这一轮重新算',
        'f.append(0)': '`j = {j} < carpetLen = {carpetLen}`：一条地毯就能盖住前 `j+1` 块 → `f[{j}] = 0`',
        'f.append(min': '`j = {j}`：不用地毯 `{f[j-1]} + {int(floor[j])}`，用地毯 `g[{j-carpetLen}] = {g[j-carpetLen]}` → 取小 =={f[j]}==',
        'return f[-1]': '`f[-1]` 就是最终答案 =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j]：前 i 条地毯盖前 j 块砖；用地毯就跳回 j − carpetLen',
        complexity='时间 `O(numCarpets · n)`，空间 `O(n)`',
        problem=['`floor` 里 `1` 是白砖，有 `numCarpets` 条长 `carpetLen` 的黑地毯',
                 '地毯可重叠，求没被盖住的白砖最少多少',
                 '示例：`"10110101"`，`2` 条、长 `2` → `2`'],
        quote='当 j >= carpetLen 时，有两种策略。如果不适用当前这块地毯，就有 f[i][j] = f[i][j - 1] + floor[j]。如果使用，那么就有 f[i][j] = f[i - 1][j - carpetLen]。',
        quote_src='—— yiduobo 题解原文',
        idea=['先特判：`numCarpets × carpetLen >= n` 时能全盖住，答案 0',
              '0 条地毯：`f` 是前缀和；之后每多一条，`j < carpetLen` 的位置直接是 0',
              '其余位置：不用 `f[j-1] + floor[j]`，用 `g[j-carpetLen]`，取最小'],
        summary=['时间 `O(numCarpets · n)`，空间 `O(n)`',
                 '原文先把 `f[i]` 看成二维，再用 `g = f[:]` 滚动掉地毯数这一维',
                 '`j < carpetLen` 时 `f[j] = 0`，别漏掉这个边界',
                 '代码在 Python 3 下无需修改即可运行',
                 '对比灵神：灵神从右往左想「选或不选」，并给出记忆化搜索的由来'],
    ),
)
