def _lines(S):
    ln = S.get('_line', 0)
    if 'cnt' not in S or ln < 20:
        return '`sum[mask]`：顾客集合 mask 一共需要多少个数'
    c = S.get('c')
    j, sub = S.get('j'), S.get('sub')
    if j is None or c is None:
        return '`dp[i][j]`：前 i 种数字能否满足顾客集合 j'
    q = len(S['quantity'])
    if sub is None or sub <= 0:
        return f'集合 j = `{j:0{q}b}`，当前这种数字有 c = {c} 个'
    return (f'试把 sub = `{sub:0{q}b}` 全分给这种数字：`sum[sub]` = {S["sum"][sub]}，c = {c}；'
            f'剩下 `{j ^ sub:0{q}b}` 要让前 i 种满足')


def _cur(S):
    i, j = S.get('i'), S.get('j')
    return (i + 1, j) if S.get('_line', 0) >= 22 and isinstance(i, int) and isinstance(j, int) else None


CONFIG = dict(
    num=1655, title='分配重复整数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 2307'],
    code='''
class Solution:
    def canDistribute(self, a: List[int], quantity: List[int]) -> bool:
        # 预处理 quantity 每个子集的子集和
        m = 1 << len(quantity)
        sum = [0] * m
        for i, v in enumerate(quantity):
            bit = 1 << i
            for j in range(bit):
                sum[bit | j] = sum[j] + v

        cnt = defaultdict(int)
        for v in a:
            cnt[v] += 1
        n = len(cnt)

        # dp[i][j] 表示 cnt 的前 i 个元素能否满足集合为 j 的顾客
        dp = [None] * (n + 1)
        for i in range(n + 1):
            dp[i] = [False] * m
            dp[i][0] = True
        i = 0
        for c in cnt.values():
            for j, ok in enumerate(dp[i]):
                if ok:
                    dp[i + 1][j] = True
                    continue
                sub = j
                while sub > 0:  # 枚举 j 的子集 sub
                    if sum[sub] <= c and dp[i][j ^ sub]:  # 判断这 c 个数能否全部分给 sub，并且除了 sub 以外的 j 中的顾客也满足
                        dp[i + 1][j] = True
                        break
                    sub = (sub - 1) & j
            i += 1
        return dp[n][m - 1]
''',
    call='Solution().canDistribute([1, 1, 1, 2, 2, 3], [2, 2])',
    expect=True,
    views=[
        dict(type='array', var=lambda S: S.get('sum'), label='sum[mask]：顾客集合 mask 需要的数的总数（蓝 = j，粉 = sub）', cell=70, h=200,
             pointers={'j': 'blue', 'sub': 'pink'}),
        dict(type='map', var='cnt', label='cnt：每种数字出现几次', h=100, font=24),
        dict(type='table', var=lambda S: [[int(x) for x in r] for r in S['dp']], values=True,
             label='dp[i][j]（1 = 前 i 种数字能满足顾客集合 j；行 i，列 j 为二进制）', cell=70, h=250,
             rows=lambda S: [f'i={k}' for k in range(len(S['dp']))], cols=lambda S: [f'{k:0{len(S["quantity"])}b}' for k in range(len(S['dp'][0]))],
             color=lambda S, i, j, v: 'green' if v else None,
             cursors=[(lambda S: (_cur(S) or (None,))[0], lambda S: (_cur(S) or (None, None))[1], 'yellow')]),
        dict(type='text', fn=_lines, size=24, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'orange'), ('j', 'j', 'blue'), ('sub', 'sub', 'pink'), ('n', 'n', 'cyan')],
    skip=['dp[i] = [False] * m', 'for j in range(bit)', 'dp = [None]', 'for i in range(n + 1)', 'dp[i][0] = True', 'for v in a:', 'cnt[v] += 1', 'i = 0', 'continue', 'sub = j', 'if ok:'],
    max_steps=80,
    captions={
        'm = 1 << len': '`m = 2^{len(quantity)} = {m}`：顾客集合共 `m` 种（用二进制表示）',
        'sum = [0] * m': '`sum[mask]` 先全为 0，下面递推填',
        'for i, v in enumerate': lambda S, B, r: (f'第 `{S.i}` 位顾客需要 `{S.v}` 个' if S.get('i') != B.get('i') or S.get('v') != B.get('v')
                                                   else '顾客都处理完，`sum` 填好了'),
        'bit = 1 << i': '`bit = {bit}`：只含第 {i} 位顾客的集合',
        'sum[bit | j] = sum[j] + v': '`sum[{bit | j}] = sum[{j}] + {v}` = =={sum[bit | j]}==：集合加入顾客 {i}',
        'cnt = defaultdict': '统计每种数字出现的次数',
        'dp[i + 1][j] = True': lambda S, B, r: (f'`dp[{S.i}][{S.j}]` 已成立 → `dp[{S.i + 1}][{S.j}]` 直接 ==True==' if S._line == 25
                                                else f'`dp[{S.i + 1}][{S.j}]` = ==True=='),
        'n = len(cnt)': '`cnt` = {dict(cnt)}，一共 `n = {n}` 种不同的数字；`dp[i][0] = True`（没有顾客要满足，总成立），其余先 False',
        'for c in cnt.values()': lambda S, B, r: (f'处理第 `{S.i}` 种数字，它有 `c = {S.c}` 个' if S.i < S.n else '所有数字都处理完'),
        'for j, ok in enumerate': lambda S, B, r: (f'枚举顾客集合 `j = {S.j:0{len(S.quantity)}b}`，`dp[{S.i}][j]` = {S.ok}' + ('' if S.ok else '：不成立，要枚举 j 的子集 sub 分给这种数字')
                                                    if S.get('j') != B.get('j') or S.get('ok') != B.get('ok') else '这个集合 j 枚举完了'),
        'while sub > 0': lambda S, B, r: (f'`sub = {S.sub:0{len(S.quantity)}b}` > 0，继续枚举' if S.sub > 0 else '子集枚举完，dp[i+1][j] 保持 False'),
        'if sum[sub] <= c': lambda S, B, r: (f'`sum[sub]` = {S.sum[S.sub]} {"≤" if S.sum[S.sub] <= S.c else ">"} c = {S.c}；'
                                              f'`dp[{S.i}][j^sub]` = {S.dp[S.i][S.j ^ S.sub]} → '
                                              + ('==可以分配==' if S.sum[S.sub] <= S.c and S.dp[S.i][S.j ^ S.sub] else '不行')),
        'sub = (sub - 1) & j': '`(sub-1) & j`：下一个更小的子集 → `sub = {sub:b}`',
        'break': '找到一种分法，不用再试了',
        'i += 1': '第 {i} 种数字处理完，`i` → =={i}==',
        'return dp[n][m - 1]': '前 `n` 种数字能否满足==所有顾客==（集合 `m-1`）：=={ret}==',
    },
    cards=dict(
        one_liner='把「每个顾客分给哪种数字」压成子集，逐种数字做状压 DP',
        complexity='时间 `O(n · 3^m)`，空间 `O(n · 2^m)`',
        problem=['`nums` 至多 50 种不同的值，`quantity[i]` 是第 i 位顾客要的个数',
                 '每位顾客要的数必须==恰好 quantity[i] 个且全相同==',
                 '示例：`nums=[1,1,2,2]`，`quantity=[2,2]` → `true`'],
        quote='dp[i][j] 表示 cnt 的前 i 个元素能否满足集合为 j 的顾客。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先算出每个顾客子集的需求总和 `sum[mask]`；`cnt` 统计每种数字个数',
              '`dp[i][j]`：前 i 种数字能否满足顾客集合 j',
              '第 i 种数字 `c` 个：枚举 j 的子集 `sub` 全分给它，其余 `j^sub` 看 `dp[i]`'],
        summary=['时间 `O(n · 3^m)`（枚举子集的子集），`m ≤ 10`，`n ≤ 50`',
                 '原文为 Go，已按原逻辑逐行转写为 Python：`for sub := j; sub > 0; ...` 改写成 `while`，Go 的 `map` 用 `defaultdict`',
                 '易错点：`sub` 要枚举 j 的非空子集，`(sub - 1) & j`；`dp[i][0] = True` 作为起点',
                 '同类题：子集状压 DP（§9.4）'],
    ),
)
