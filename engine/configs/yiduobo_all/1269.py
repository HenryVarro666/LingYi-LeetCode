CONFIG = dict(
    num=1269, title='停在原地的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按步数递推 + 滚动数组',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numWays(self, steps, arrLen):

        if arrLen > steps // 2 + 1:
            arrLen = steps // 2 + 1
        
        f = [0] * arrLen
        g = [0] * arrLen
        f[0] = 1
        mod = 10 ** 9 + 7
        for i in range(1, steps + 1):
            for j in range(arrLen):
                g[j] = f[j]
                if j > 0:
                    g[j] += f[j - 1]
                    g[j] %= mod
                if j < arrLen - 1:
                    g[j] += f[j + 1]
                    g[j] %= mod

            f = g[:]

        return f[0]
''',
    call='Solution().numWays(3, 4)',
    expect=4,
    views=[
        dict(type='array', var='f', label='f：上一轮，走 i-1 步后停在各位置的方案数', h=190, cell=110,
             pointers={'j': 'blue'}, color=lambda S, k, v: 'green' if k == 0 and S.get('_line', 0) > 0 and False else None),
        dict(type='array', var='g', label='g：这一轮，走 i 步后停在各位置的方案数', h=190, cell=110,
             pointers={'j': 'pink'}, color=lambda S, k, v: 'yellow' if k == S.get('j') and v else None),
        dict(type='text', size=26, h=70,
             fn=lambda S: (f'`g[{S["j"]}]` = ==停在原地 f[{S["j"]}]== + 从左来 `f[{S["j"]-1}]` + 从右来 `f[{S["j"]+1}]`'
                           if S.get('j') is not None and S.get('i') is not None else '每走一步：停在原地、向左、向右，三选一')),
    ],
    watch=[('i（步数）', 'i', 'blue'), ('j（位置）', 'j', 'pink'), ('arrLen', 'arrLen', 'cyan')],
    captions={
        'if arrLen > steps': lambda S, B, r: (f'走 `{S.steps}` 步最远只能到 `{S.steps // 2}`，再远回不来 → 只需 ==`arrLen = {S.arrLen}`== 个位置'
                                              if S.arrLen != B.arrLen else f'`arrLen = {S.arrLen}` 已经够小，不用缩'),
        'arrLen = steps': '数组长度压到 `steps // 2 + 1` = {arrLen}',
        'f = [0] * arrLen': '`f[j]`：上一轮停在位置 j 的方案数',
        'g = [0] * arrLen': '`g` 存这一轮的结果',
        'f[0] = 1': '走 0 步：只有 ==位置 0== 一种方案，`f[0] = 1`',
        'mod = ': '答案对 `10^9 + 7` 取模',
        'for i in range': '第 `{i}` 步：由上一轮 `f` 推出这一轮 `g`',
        'g[j] = f[j]': '`g[{j}]` 先取 `f[{j}]` = =={g[j]}==（这一步选择不动）',
        'g[j] += f[j - 1]': '加上从左边 `{j-1}` 走过来的 `f[{j-1}]` = {f[j-1]} → `g[{j}] = {g[j]}`',
        'g[j] += f[j + 1]': '加上从右边 `{j+1}` 走过来的 `f[{j+1}]` = {f[j+1]} → `g[{j}] = {g[j]}`',
        'g[j] %= mod': '取模，防止溢出',
        'f = g[:]': '这一轮算完，`g` 复制成下一轮的 `f` = {f}',
        'return f[0]': '走完 `{steps}` 步回到位置 0 的方案数 = =={ret}==',
    },
    skip=['g[j] %= mod', 'mod ='],
    max_steps=90,
    cards=dict(
        one_liner='f[i][j] = 走 i 步停在 j：只能从 j-1、j、j+1 过来',
        complexity='时间 `O(steps * min(steps, arrLen))`，空间 `O(min(steps, arrLen))`',
        problem=['数组长度 `arrLen`，指针从下标 0 出发，每步左移 / 右移 / 不动，不能出界',
                 '恰好走 `steps` 步，求回到下标 0 的方案数，对 `10^9+7` 取模',
                 '本视频：`steps = 3, arrLen = 4` → `4`（数组实际只用前 2 格）'],
        quote='令f[i][j]表示走i步，最后停在位置j的方案数。初始情况下f[0][0] = 1，其他f[0][k] = 0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 来自上一轮的 `j-1`（向右走）和 `j+1`（向左走），再加上原地不动的 `j`',
              '每一轮只依赖上一轮，用 `f` 和 `g` 两个数组滚动，省掉 `i` 这一维',
              '走 `steps` 步最远只到 `steps // 2`，所以数组长度可以压到 `steps // 2 + 1`'],
        summary=['时间 `O(steps * min(steps, arrLen))`，空间 `O(min(steps, arrLen))`',
                 '易错：回到 0 的路程要走回来，所以最远只能到 `steps // 2`',
                 '边界：位置 0 没有左邻，位置 `arrLen-1` 没有右邻',
                 '原文为 Python 2 写法，`steps / 2 + 1` 已改为 `steps // 2 + 1`',
                 'yiduobo 提到矩阵乘法可行但矩阵规模 O(n)，不划算'],
    ),
)
