def _hl(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = 从 `i` 步里选 `j` 步往回走的方案数 = `C(i, j)`'
    if j == 0 or j == i:
        return f'`f[{i}][{j}] = 1`：全不选 / 全选，只有一种'
    return f'`f[{i}][{j}] = f[{i - 1}][{j - 1}] + f[{i - 1}][{j}]` = =={S["f"][i][j]}=='


def _color(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 14:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if j not in (0, i) and (r, c) in ((i - 1, j - 1), (i - 1, j)):
        return 'blue'
    return None


CONFIG = dict(
    num=2400, title='恰好移动 k 步到达某一位置的方法数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='数学推导 + 递推求组合数 C(k, back)',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 1751'],
    code='''
class Solution(object):
    def numberOfWays(self, startPos, endPos, k):

        rest_step = k - (endPos - startPos)
        if rest_step < 0 or rest_step % 2 == 1:
            return 0
        
        back_step = rest_step // 2

        mod = 10 ** 9 + 7
        f = [[0] * (back_step + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            for j in range(min(back_step + 1, i + 1)):
                if j == 0 or j == i:
                    f[i][j] = 1
                else:
                    f[i][j] = (f[i - 1][j - 1] + f[i - 1][j]) % mod
        
        return f[k][back_step]
''',
    call='Solution().numberOfWays(1, 3, 6)',
    expect=15,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=_hl, size=26, h=70),
        dict(type='table', var='f', label='f[i][j] = C(i, j)（黄 = 正在算，蓝 = 它依赖的两格）', h=480, cell=64,
             rows=lambda S: [f'i={r}' for r in range(len(S['f']))], cols=lambda S: [f'j={c}' for c in range(len(S['f'][0]))],
             color=_color),
    ],
    watch=[('rest_step', 'rest_step', 'orange'), ('back_step', 'back_step', 'pink'), ('i', 'i', 'blue'), ('j', 'j', 'yellow')],
    captions={
        'rest_step = k': '先走直线：从 `{startPos}` 到 `{endPos}` 至少 `{endPos - startPos}` 步，多出 `rest_step = {k} − {endPos - startPos}` = =={rest_step}== 步',
        'if rest_step < 0': lambda S, B, r: (f'多出的 `{S.rest_step}` 步是偶数，而且步数够用 → ==能走到==，继续'
                                            if not (S.rest_step < 0 or S.rest_step % 2 == 1) else '步数不够，或者多出奇数步（回头要一来一回两趟）→ ==返回 0=='),
        'back_step = ': '多出的步数要“一来一回”消耗掉，所以往回走的步数 `back_step = {rest_step} // 2` = =={back_step}==',
        'mod = ': '答案取模：`mod = 10^9 + 7`',
        'f = [[0]': '`f[i][j]` 是 `C(i, j)`：`i` 步里选 `j` 步往回走；表 `{k + 1}` 行 × `{back_step + 1}` 列',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算 `C({S.i}, ·)`，要用到上一行 `i − 1`' if S.i != B.get('i') else '`i` 枚举完了，整张表算好'),
        'if j == 0 or j == i': lambda S, B, r: (f'`j = {S.j}`：一步都不回头，或每一步都回头 → 只有 ==1 种==，`f[{S.i}][{S.j}] = 1`'
                                                if S.j == 0 or S.j == S.i else f'`0 < j = {S.j} < i = {S.i}`：走递推公式'),
        'f[i][j] = 1': '`f[{i}][{j}] = 1`',
        'f[i][j] = (f[i - 1]': '杨辉三角：第 `{i}` 步要么回头（`f[{i-1}][{j-1}]` = {f[i-1][j-1]}），要么不回头（`f[{i-1}][{j}]` = {f[i-1][j]}）→ =={f[i][j]}==',
        'return f[k][back_step]': '`k` 步里选 `back_step` 步回头：`C({k}, {back_step})` = =={ret}==',
    },
    cards=dict(
        one_liner='多出的步数一半往回走，答案就是 C(k, back_step)',
        complexity='时间 `O(k · back_step)`，空间 `O(k · back_step)`',
        problem=['无限数轴上从 `startPos` 出发，每步向左或向右 1',
                 '求==恰好 k 步==走到 `endPos` 的不同走法数，对 `10^9 + 7` 取余',
                 '本视频：`startPos=1, endPos=3, k=6` → `15`'],
        quote='因为需要一来一回走两趟，那么当多出的步数是奇数时就无法刚好消耗掉所有的步数，也是直接返回-1，否则取多余步数的一半，记为back_step，也就是需要往回走的步数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先直线走到终点，要 `endPos − startPos` 步；剩下 `rest_step` 步必须成对抵消',
              '`rest_step` 为奇数或为负 → 0；否则往回走 `back_step = rest_step / 2` 步',
              '问题变成从 `k` 步里选 `back_step` 步 → 组合数 `C(k, back_step)`，用杨辉三角递推'],
        summary=['时间、空间都是 `O(k · back_step)`',
                 '易错：`rest_step` 为负要先判，奇偶判断不能漏；判断失败返回 ==0==（原文文字写“-1”，代码返回 0）',
                 '原文为 Python 2 写法，`back_step = rest_step / 2` 已改为 `//`',
                 '对比灵神：他用 `f(x, left)` 搜索走法；这里直接数学推出组合数'],
    ),
)
