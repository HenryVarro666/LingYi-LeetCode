def _cur(S):
    d = S.get('cnt_dict')
    if not d:
        return {}
    idx = S.get('index')
    if idx is None or idx >= len(d):
        return d[-1] if S.get('_line', 0) < 38 else {}
    return d[idx]


def _txt(S):
    ln = S.get('_line', 0)
    if ln >= 47 and 'index' in S and 'n' in S:
        n = S['n']
        ms = list(S['cnt_dict'][S['index']].values())
        parts = ' × '.join(f'C({n}+{m}-1, {m})' for m in ms) or '1（k = 1，只有全 1 数组）'
        return f'第 {S["index"]} 个查询，`n = {n}`：答案 = `{parts}` = =={S["res"][S["index"]]}=='
    if ln >= 36:
        return '杨辉三角递推：`C(i, j) = C(i-1, j-1) + C(i-1, j)`，只需要 `j ≤ m`'
    if ln >= 22 and 'index' in S:
        return f'分解 `queries[{S["index"]}]` 的 `k`：取 `f[k]`（质因子），`k` 变成 `k // f[k]`'
    if ln >= 11 and 'now' in S:
        return f'筛法：`f[i]` 记录 `i` 的一个质因子；现在处理 `now = {S["now"]}`'
    return '步骤：筛出 `f` → 分解每个 `k` → 预处理组合数 `c` → 按质因子指数相乘'


CONFIG = dict(
    num=1735, title='生成乘积数组的方案数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='筛法分解质因数 + 插板法',
    tags=['数论', '组合数学', '难度分 2500'],
    code='''
class Solution(object):
    def waysToFillArray(self, queries):

        maxn = maxk = 0
        len_q = len(queries)
        res = [1] * len_q
        for n, k in queries:
            maxn = max(maxn, n)
            maxk = max(maxk, k)
        
        f = list(range(maxk + 1))
        now = 2
        while now * now <= maxk:
            if f[now] == now:
                tmp = now + now
                while tmp <= maxk:
                    f[tmp] = now
                    tmp += now
            
            now += 1
        
        cnt_dict = [{} for _ in range(len_q)]
        m = 0
        for index in range(len_q):
            k = queries[index][1]
            while k > 1:
                cnt_dict[index][f[k]] = cnt_dict[index].get(f[k], 0) + 1
                k //= f[k]

            if cnt_dict[index]:
                m = max(m, max(cnt_dict[index].values()))

        if m == 0:
            return res

        c = [[0] * (m + 1) for _ in range(m + maxn)]
        mod = 10 ** 9 + 7
        for i in range(1, m + maxn):
            for j in range(min(i, m) + 1):
                if i == 1 or j == 0:
                    c[i][j] = 1
                else:
                    c[i][j] = c[i - 1][j - 1] + c[i - 1][j]
                    if c[i][j] >= mod:
                        c[i][j] -= mod

        for index in range(len_q):
            n = queries[index][0]
            for m in cnt_dict[index].values():
                res[index] = (res[index] * c[n + m - 1][m]) % mod
        
        return res
''',
    call='Solution().waysToFillArray([[2, 6], [3, 1], [3, 8]])',
    expect=[4, 1, 10],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='f', label='f[i]：i 的一个质因子（筛出来的）', cell=64,
             color=lambda S, i, v: 'blue' if 'now' in S and S.get('_line', 99) <= 21 and i == S['now'] else None, h=120),
        dict(type='map', var=_cur, label='cnt_dict[index]：质因子 → 次数', fmt=lambda k, v: f'{k}^{v}', h=100),
        dict(type='table', var='c', label='c[i][j] = C(i, j)（插板法要用的组合数）', cell=72, h=250),
        dict(type='array', var='res', label='res（每个查询的答案）', cell=90, index=False, color=lambda S, i, v: 'green', h=100),
    ],
    watch=['maxn', 'maxk', ('now', 'now', 'blue'), 'k', 'm'],
    skip=['len_q = len', 'tmp += now', 'for i in range(1, m + maxn)', 'for j in range', 'if c[i][j] >= mod', 'if i == 1 or j == 0', 'maxn = max', 'maxk = max', 'if cnt_dict[index]', 'mod = 10', 'now += 1', 'while tmp <= maxk', 'while k > 1', 'for index in range(len_q)'],
    max_steps=90,
    captions={
        'maxn = maxk = 0': '先扫一遍查询，找出最大的 `n` 和最大的 `k`，后面预处理只做到这个范围',
        'res = [1] * len_q': '`res[i]` 先全部设为 1，之后按质因子乘上去',
        'for n, k in queries': lambda S, B, r: (f'看查询 `n = {S.n}`，`k = {S.k}`：`maxn = {S.maxn}`，`maxk = {S.maxk}`' if 'n' in S and not (B.get('n') == S.n and B.get('k') == S.k) else f'扫完了：`maxn = {S.maxn}`，`maxk = {S.maxk}`'),
        'f = list(range': '`f[i] = i` 起步：先假设每个数的质因子是自己（原文 `f = range(...)`，Python 3 需转成 list）',
        'now = 2': '从 `now = 2` 开始筛，只需筛到 `sqrt(maxk)`',
        'while now * now <= maxk': lambda S, B, r: (f'`{S.now}² = {S.now * S.now} ≤ {S.maxk}`，继续' if S.now * S.now <= S.maxk else f'`{S.now}² > {S.maxk}`：筛完了，`f` 就绪'),
        'if f[now] == now': lambda S, B, r: (f'`f[{S.now}] = {S.now}`，没被更小的数改过 → ==质数==，筛它的倍数' if S.f[S.now] == S.now else f'`f[{S.now}] = {S.f[S.now]} ≠ {S.now}`：合数，跳过'),
        'tmp = now + now': '从 `{tmp}` 开始，筛 `{now}` 的倍数',
        'while tmp <= maxk': '`tmp = {tmp}` ≤ `{maxk}`？{"是，继续" if tmp <= maxk else "否，这个质数筛完了"}',
        'f[tmp] = now': '`f[{tmp}] = {now}`：`{tmp}` 是 `{now}` 的倍数',
        'now += 1': '`now` → {now}',
        'cnt_dict = [': '每个查询一个哈希表，记录质因子出现次数',
        'm = 0': '`m` 记录所有查询里质因子的最大指数',
        'for index in range(len_q)': lambda S, B, r: ('处理下一个查询' if 'index' in S else '逐个查询'),
        'k = queries[index][1]': '取出 `k = {k}`，开始分解',
        'while k > 1': lambda S, B, r: (f'`k = {S.k} > 1`，还有质因子' if S.k > 1 else '`k = 1`，分解完毕'),
        'cnt_dict[index][f[k]]': '`f[{B.k}] = {f[B.k]}` 是质因子 → 次数加一：`{cnt_dict[index]}`',
        'k //= f[k]': '`k` 除以 `{B.f[B.k]}` → {k}（原文 `/=`，Python 3 改为 `//=`）',
        'if cnt_dict[index]': '`m` 要涵盖这个查询里最大的指数',
        'm = max(m': '`m = {m}`',
        'if m == 0': '`m = {m}`：{"所有 k 都是 1，答案全是 1" if m == 0 else "有质因子，需要组合数"}',
        'c = [[0]': '`c` 有 `m + maxn = {m + maxn}` 行、`m + 1 = {m + 1}` 列：指数最大才 `m`，列数很少（原题 `m ≤ 13`）',
        'mod = 10': '`mod = 10^9 + 7`',
        'for i in range(1, m + maxn)': '`C(i, ·)` 这一行',
        'for j in range': '`j` 从 0 到 `min(i, m)`',
        'if i == 1 or j == 0': lambda S, B, r: ('边界：`C(i, 0) = 1`（以及 `C(1, 1)`）' if (S.i == 1 or S.j == 0) else f'`C({S.i}, {S.j})` 要用递推公式'),
        'c[i][j] = 1': '边界：`C({i}, {j}) = 1`（`j = 0` 或 `i = 1`）',
        'c[i][j] = c[i - 1][j - 1] + c[i - 1][j]': '`C({i},{j}) = C({i-1},{j-1}) + C({i-1},{j}) = {c[i][j]}`：选或不选第 i 个，==不用逆元==',
        'if c[i][j] >= mod': '取模：`{c[i][j]}` {"≥" if c[i][j] >= mod else "<"} `mod`',
        'c[i][j] -= mod': '超过 mod 就减一次',
        'n = queries[index][0]': '第 `{index}` 个查询 `n = {n}`',
        'for m in cnt_dict[index].values()': '每个质因子的指数 `m` 单独算一份方案',
        'res[index] = (': lambda S, B, r: f'`C(n+m-1, m) = C({S.n + S.m - 1}, {S.m}) = {S.c[S.n + S.m - 1][S.m]}`，乘到 `res[{S.index}]` → =={S.res[S.index]}==',
        'return res': '全部答案：`{ret}`',
    },
    cards=dict(
        one_liner='把 k 拆成质因子，每个质因子的指数用「插板法」分给 n 个位置',
        complexity='筛法 `O(maxk log log maxk)`，组合数 `O((m+maxn)·m)`',
        problem=['每个查询 `[n, k]`：长为 `n`、元素为正整数、乘积为 `k` 的数组有几个',
                 '答案对 `10^9+7` 取余；`n, k ≤ 10^4`，最多 `10^4` 个查询',
                 '示例：`[2,6]` → 4：`[1,6] [2,3] [3,2] [6,1]`',
                 '本视频：`[[2,6],[3,1],[3,8]]` → `[4,1,10]`'],
        quote='将这m[i]个p[i]分配给这n个数……m个小球放入n个盒子，每个盒子可以放多个小球，也可以一个都不放……最终就是C(n + m[i] - 1, m[i])。',
        quote_src='—— yiduobo 题解原文（节选）',
        idea=['乘积 = 各质因子的幂相乘，不同质因子互不影响 → 分别讨论',
              '`p^m` 要分给 `n` 个数：`m` 个球放进 `n` 个盒子，加 `n` 个假球用隔板法',
              '总方案 `C(n+m-1, m)`，所有质因子的结果相乘',
              '`2^14 > 10000`，指数 `m ≤ 13`，组合数表很小，用杨辉三角递推（不需要逆元）'],
        summary=['先找 `maxn`、`maxk`，筛法和组合数只做到需要的范围',
                 '原文为 Python 2 写法，已改为：`f = range(...)` → `list(range(...))`，`k /= f[k]` → `k //= f[k]`',
                 '筛法里 `f[i]` 被不断覆盖，最终存的是 `i` 的一个质因子，不断除就能分解',
                 '易错：`m == 0`（所有 `k = 1`）要提前返回，否则组合数表为空',
                 '对比灵神：灵神每个查询直接试除到 `√k`，yiduobo 先批量筛再分解'],
    ),
)
