def _info(S):
    if 'g' not in S:
        return '`g[j][k]`：已处理颜色里，盒子一放 j 个球、颜色数差为 k − n 的方案数'
    n = S['n']
    i = S.get('i')
    t = f'处理第 `{i}` 种颜色（共 `{S["balls"][i]}` 个球），前 `{i+1}` 种共 `{S["now_s"]}` 个' if i is not None and 'now_s' in S else ''
    j, k = S.get('j'), S.get('k')
    if j is not None and k is not None and S.get('_line', 0) >= 17:
        t += f'；算 `f[{j}][{k}]`（盒子一 {j} 个球，颜色差 {k - n}）'
    return t


def _color(S, r, c, v):
    j, k = S.get('j'), S.get('k')
    if j is not None and k is not None and (r, c) == (j, k) and S.get('_line', 0) >= 17:
        return 'yellow'
    return None


CONFIG = dict(
    num=1467, title='两个盒子中球的颜色数相同的概率', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='计数 DP · 按颜色差分类（滚动数组）',
    tags=[],
    code='''
class Solution(object):
    def getProbability(self, balls):

        n = len(balls)
        s = sum(balls)
        g = [[0] * (n + n + 1) for _ in range(s // 2 + 1)]
        g[0][n] = 1
        now_s = 0

        fact = [1]
        for index in range(1, s + 1):
            fact.append(fact[-1] * index)

        for i in range(n):
            now_s += balls[i]
            f = [[0] * (n + n + 1) for _ in range(s // 2 + 1)]
            for j in range(s // 2 + 1):
                for k in range(n + n + 1):
                    f[j][k] = 0
                    p = 1
                    for choose in range(balls[i] + 1):
                        if choose == 0:
                            if k + 1 <= n + n:
                                f[j][k] += g[j][k + 1] * fact[now_s - j] // fact[now_s - j - balls[i]] // fact[balls[i]]
                        elif j >= choose:
                            if choose == balls[i]:
                                if k - 1 >= 0:
                                    f[j][k] += g[j - choose][k - 1] * fact[j] // fact[j - balls[i]] // fact[balls[i]]
                            else:
                                f[j][k] += g[j - choose][k] * fact[j] // fact[j - choose] // fact[choose] * fact[now_s - j] // fact[now_s - j - balls[i] + choose] // fact[balls[i] - choose]

            g = f[:]

        return f[-1][n] * 1.0 / sum(f[-1])
''',
    call='Solution().getProbability([1, 1])',
    expect=1.0,
    max_steps=80,
    skip=['p = 1', 'f[j][k] = 0', 'fact.append', 'for k in range', 'for choose in range', 'if k + 1 <= n + n', 'elif j >= choose', 'if k - 1 >= 0', 'if choose == 0', 'if choose == balls[i]'],
    views=[
        dict(type='array', var='balls', label='balls[i]：第 i 种颜色的球数', h=150, cell=90,
             color=lambda S, k, v: 'blue' if S.get('i') == k else None),
        dict(type='text', fn=_info, size=24, h=70),
        dict(type='table', var='g', label='g[j][k]（上一轮）：行 = 盒子一球数 j，列 = 颜色差 k − n', h=250, cell=70,
             rows=lambda S: [f'j={r}' for r in range(len(S['g']))] if 'g' in S else [],
             cols=lambda S: [str(c - S['n']) for c in range(2 * S['n'] + 1)] if 'n' in S else [],
             color=lambda S, r, c, v: 'green' if v else None),
        dict(type='table', var='f', label='f[j][k]（本轮，黄 = 正在算）', h=250, cell=70,
             rows=lambda S: [f'j={r}' for r in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [str(c - S['n']) for c in range(2 * S['n'] + 1)] if 'n' in S else [], color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'purple'), ('choose', 'choose', 'orange'), ('now_s', 'now_s', 'green')],
    captions={
        'n = len(balls)': '一共 `n = {n}` 种颜色',
        's = sum(balls)': '球总数 `s = {s}`，每个盒子装 `s // 2 = {s // 2}` 个',
        'g = [[0]': '`g[j][k]`：盒子一有 j 个球、两盒颜色数之差为 `k − n` 的方案数；`k` 加 `n` 的偏移，避免负下标',
        'g[0][n] = 1': '起点：一种颜色都没放，`j = 0`、差 0（下标 `{n}`）只有 ==1 种==',
        'for index in range': '预处理阶乘 `fact`：后面插空组合要用',
        'fact[-1] * index': '`fact[{index}] = {fact[-1]}`',
        'for i in range(n)': lambda S, B, r: (f'开始处理第 `{S.i}` 种颜色，`balls[{S.i}] = {S.balls[S.i]}`' if S.get('i') != B.get('i') else '所有颜色处理完'),
        'now_s += balls[i]': '前 `{i + 1}` 种颜色共 `now_s = {now_s}` 个球',
        'f = [[0]': '新建本轮 `f`，只依赖上一轮 `g`（滚动数组，去掉 i 这一维）',
        'for j in range': lambda S, B, r: f'`j = {S.j}`：盒子一放 {S.j} 个球，盒子二放 {S.now_s - S.j} 个',
        'if choose == 0': lambda S, B, r: ('`choose = 0`：第 i 种球==全放盒子二==，颜色差多一种 → 从 `g[j][k+1]` 转移' if S.choose == 0
                                        else f'`choose = {S.choose}`：这种颜色放 {S.choose} 个到盒子一，其余放盒子二'),
        'if k + 1 <= n + n': '下标不越界才能从 `g[j][k+1]` 转移',
        'f[j][k] += g[j][k + 1]': '`choose = 0`：这种颜色==全放盒子二==，颜色差多一种，从 `g[{j}][{k+1}]` 转移 × 插入方案数 → `f[{j}][{k}] = {f[j][k]}`',
        'elif j >= choose': '盒子一至少要有 `choose` 个球，才能放',
        'if choose == balls[i]': lambda S, B, r: ('`choose = balls[i]`：这种颜色==全放盒子一==，颜色差少一种 → 从 `g[j-choose][k-1]` 转移' if S.choose == S.balls[S.i]
                                                  else '`choose` 在 1..balls[i]-1：两个盒子都有这种颜色，颜色差不变 → 从 `g[j-choose][k]` 转移'),
        'if k - 1 >= 0': '下标不越界才能从 `k − 1` 转移',
        'g[j - choose][k - 1]': '`choose = {choose}` = `balls[i]`：这种颜色==全放盒子一==，颜色差少一种，从 `g[{j-choose}][{k-1}]` 转移 × 插入方案数 → `f[{j}][{k}] = {f[j][k]}`',
        'g[j - choose][k] *': '`choose = {choose}`：两盒都有这种颜色，颜色差不变，从 `g[{j-choose}][{k}]` 转移；盒子一插 `choose` 个、盒子二插 `balls[i]-choose` 个，两边方案数相乘 → `f[{j}][{k}] = {f[j][k]}`',
        'g = f[:]': '本轮算完，`g` 换成 `f`，进入下一种颜色',
        'return f[-1][n]': '`f[-1][n]`：盒子一恰有 `s//2` 个球且颜色差 0 的方案数 ÷ 所有方案数 `sum(f[-1])` = =={ret}==',
    },
    cards=dict(
        one_liner='状态里只记「盒子一球数、两盒颜色差」，逐种颜色滚动转移',
        complexity='时间约 `O(n · s · n · 球数)`，空间 `O(s · n)`',
        problem=['`balls[i]` 是第 `i` 种颜色的球数，总数 `2n` 个偶数；把球打乱后前一半放盒子一、后一半放盒子二',
                 '求==两个盒子里颜色种数相同==的概率（同色球不可区分前的排列等可能）',
                 '示例：`balls = [1,1]` → `1.0`；`[2,1,1]` → `0.66667`'],
        quote='这里其实并不需要关心具体拿球的方案，而只需要知道两个盒子中球颜色的差值，那么可以重新设定状态为f[i][j][k]表示从前i中颜色的球中拿出j个放入盒子一，剩下的放入盒子二，且两个盒子中球的颜色数相差为k时所有的方案数',
        quote_src='—— yiduobo 题解原文',
        idea=['每种颜色三种放法：全放盒子二（颜色差 +1）、全放盒子一（差 −1）、拆开（差不变）',
              '方案数用「插入」计数：把新球插进已有排列，再除以同色球的重复',
              '最后 `f[-1][n]` 是颜色差为 0 的方案数，除以总数就是概率',
              '滚动数组去掉 `i`；下标加偏移 `n`，避免 Python 负下标'],
        summary=['时间 `O(n · s · n · max(balls))`，`n ≤ 8`，`s ≤ 48`，可过',
                 '易错：颜色差带负数，要加偏移 `n`；分母是 `sum(f[-1])`，不是总排列数',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（含 `s // 2`、阶乘比值）',
                 '视频为控制长度只演示 `balls = [1, 1]`'],
    ),
)
