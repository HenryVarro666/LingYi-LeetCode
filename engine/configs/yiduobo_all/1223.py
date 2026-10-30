def _cell(S, r, c, v):
    j, k = S.get('j'), S.get('k')
    if j is None or r != j:
        return None
    if S.get('_line', 0) >= 17:
        return 'yellow' if c == 1 else None
    if k is not None and c == k:
        return 'yellow'
    if k is not None and c == k - 1:
        return 'blue'
    return None


def _formula(S):
    j, k, ln = S.get('j'), S.get('k'), S.get('_line', 0)
    if 'last_s' not in S or j is None or 'i' not in S:
        return '`f[j][k]`：最后一次掷出 j+1，且末尾连续 k 次都是 j+1 的方案数'
    if ln in (14, 15, 16) and k is not None:
        return f'k = {k} > 1：`f[{j}][{k}] = f[{j}][{k-1}]`，上一轮末尾连续 {k-1} 个 {j+1}，再接一个'
    if ln >= 17:
        return f'k = 1：`f[{j}][1] = sum(last_s) − last_s[{j}]` = {sum(S["last_s"])} − {S["last_s"][j]}'
    return '`f[j][k]`：最后一次掷出 j+1，且末尾连续 k 次都是 j+1 的方案数'


CONFIG = dict(
    num=1223, title='掷骰子模拟', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[点数][连续次数] 滚动数组',
    tags=['其他线性 DP', '难度分 2008'],
    code='''
class Solution(object):
    def dieSimulator(self, n, rollMax):

        mod = 10 ** 9 + 7
        f = [[0] * (max(rollMax) + 1) for _ in range(6)]
        f[0][1] = 1
        f[1][1] = 1
        f[2][1] = 1
        f[3][1] = 1
        f[4][1] = 1
        f[5][1] = 1
        last_s = [1, 1, 1, 1, 1, 1]
        for i in range(2, n + 1):
            s = [0, 0, 0, 0, 0, 0]
            for j in range(6):
                for k in range(min(i, rollMax[j]), 1, -1):
                    f[j][k] = f[j][k - 1]
                    s[j] += f[j][k]
                    s[j] %= mod
                f[j][1] = (sum(last_s) - last_s[j]) % mod
                s[j] += f[j][1]
                s[j] %= mod
        
            last_s = s[:]

        return sum(last_s) % mod
''',
    call='Solution().dieSimulator(4, [1, 1, 2, 2, 2, 3])',
    expect=1072,
    skip=['f[0][1] = 1', 'f[1][1] = 1', 'f[2][1] = 1', 'f[3][1] = 1', 'f[4][1] = 1', 'mod = ', 's[j] %= mod', 'for k in range', 'for j in range'],
    max_steps=48,
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[j][k]（行 = 最后点数，列 = 末尾连续次数；黄 = 正在写，蓝 = 来源）', h=330, cell=80,
             rows=lambda S: [f'点{j+1}' for j in range(6)], cols=lambda S: [f'k={c}' for c in range(len(S['f'][0]))],
             color=_cell),
        dict(type='array', var='last_s', label='last_s[j]：上一轮「最后点数是 j」的合法总数', h=150, cell=90,
             pointers={'j': 'pink'}),
        dict(type='array', var='s', label='s[j]：本轮累计', h=150, cell=90, pointers={'j': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'f[5][1] = 1': '掷 1 次：每个点数各 1 种，连续 1 次',
        'last_s = [1': '`last_s`：上一轮每个点数结尾的方案总数，初始全是 1',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算掷 `{S.i}` 次的方案' if S.get('i') != B.get('i') else '所有轮次完成'),
        's = [0, 0': '本轮的 `s` 清零',
        'f[j][k] = f[j][k - 1]': '`k = {k} > 1`：上一轮末尾已连续 `{k-1}` 个 `{j+1}`，再接一个 → `f[{j}][{k}] = f[{j}][{k-1}]` = =={f[j][k]}==。从大到小遍历，避免覆盖',
        's[j] += f[j][k]': '`s[{j}]` 累加 → {s[j]}',
        'f[j][1] = (sum': '`k = 1`：上一轮结果只要不是 `{j+1}` 都行 → `sum(last_s) − last_s[{j}]` = {sum(last_s)} − {last_s[j]} = =={f[j][1]}==',
        's[j] += f[j][1]': '`s[{j}]` 再加上 `f[{j}][1]` → =={s[j]}==',
        'last_s = s[:]': '这一轮结束，`last_s` 更新为 `{last_s}`',
        'return sum': '掷 `{n}` 次，所有点数结尾的方案相加 = =={ret}==',
    },
    cards=dict(
        one_liner='f[j][k]：末尾连续 k 个 j，k>1 直接继承，k=1 取别的点数之和',
        complexity='时间 `O(6·n·max(rollMax))`，空间 `O(6·max(rollMax))`',
        problem=['掷 `n` 次骰子，连续掷出点数 `i` 的次数不能超过 `rollMax[i]`',
                 '求不同点数序列的个数，对 `10^9 + 7` 取模',
                 '本视频：`n=4, rollMax=[1,1,2,2,2,3]` → `1072`'],
        quote='令f[i][j][k]表示掷i次骰子，最后一次的结果为j，且最后连续k轮的结果都是j。……当k大于1时，说明上一次的结果也是j。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k > 1`：上一轮末尾就有 `k-1` 个 j，`f[j][k] = f[j][k-1]`',
              '`k = 1`：上一轮结尾不是 j 的都行，`sum(last_s) - last_s[j]`',
              '只依赖上一轮，去掉 `i` 维；`k` 从大到小更新避免覆盖'],
        summary=['时间 `O(n·6·max(rollMax))`，空间 `O(6·max(rollMax))`',
                 '`k` 必须从大到小：`f[j][k]` 要用旧的 `f[j][k-1]`',
                 '`k` 上限是 `min(i, rollMax[j])`：次数既不能超限也不能超过轮数',
                 '原文已是 Python 3 写法，无需修改；视频跳过了 6 行初始化赋值的单独步骤'],
    ),
)
