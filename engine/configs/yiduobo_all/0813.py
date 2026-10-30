A0 = [9, 1, 2, 3, 9]
K0 = 3


def _cell(S, r, c, v):
    I = S.get('_inner', S)
    now, K = I.get('now'), I.get('K')
    if now is None or K is None:
        return None
    if (r, c) == (now, K):
        return 'yellow'
    if v is not None:
        return 'green'
    return None


def _seg(S):
    I = S.get('_inner', S)
    now, K, idx = I.get('now'), I.get('K'), I.get('index')
    A = S.get('A')
    if now is None or A is None:
        return ''
    if idx is None or K == 0:
        return f'`dfs({now}, {K})`：从第 {now} 个数起分 {K + 1} 组'
    return f'当前这组 `A[{now}..{idx}]` = {A[now:idx + 1]}，平均 =={sum(A[now:idx + 1]) / (idx - now + 1):.2f}==，后面 `dfs({idx + 1}, {K - 1})` 分 {K} 组'


def _win(S):
    return None


CONFIG = dict(
    num=813, title='最大平均值和的分组', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='记忆化搜索 + 前缀和',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def largestSumOfAverages(self, A, K):

        n = len(A)
        s = [A[0]]
        for index in range(1, n):
            s.append(s[-1] + A[index])
        
        f = [[None] * K for _ in range(n)]
        return self.dfs(0, K - 1, A, n, s, f)
    
    def dfs(self, now, K, A, n, s, f):
        if f[now][K] is None:
            if K == 0:
                if now == 0:
                    f[now][K] = s[-1] * 1.0 / n
                else:
                    f[now][K] = (s[-1] - s[now - 1]) * 1.0 / (n - now)
            else:
                f[now][K] = 0
                for index in range(now, n - K):
                    if now == 0:
                        part_avg = s[index] * 1.0 / (index + 1)
                    else:
                        part_avg = (s[index] - s[now - 1]) * 1.0 / (index - now + 1)

                    f[now][K] = max(f[now][K], self.dfs(index + 1, K - 1, A, n, s, f) + part_avg)
        
        return f[now][K]
''',
    call=f'Solution().largestSumOfAverages({A0!r}, {K0})',
    expect=20.0,
    skip=['s = [A[0]]', 's.append', 'for index in range(1, n)', 'n = len(A)'],
    views=[
        dict(type='array', var='A', label='A', h=170, cell=80,
             color=lambda S, i, v: ('blue' if S.get('_inner', S).get('index') is not None and S['_inner'].get('now', 0) <= i <= S['_inner']['index'] else None)),
        dict(type='text', fn=_seg, size=26, h=60),
        dict(type='table', var=lambda S: [[None if v is None else round(v, 1) for v in r] for r in S['f']], label='f[now][K]（行 = now，列 = K；黄 = 当前，绿 = 已算）',
             h=300, cell=110, rows=lambda S: [f'{i}' for i in range(len(S['A']))], cols=lambda S: [f'{j}' for j in range(S['f'] and len(S['f'][0]))],
             color=_cell),
        dict(type='calls', h=230),
    ],
    max_steps=56,
    watch=[('now', 'now', 'blue'), ('K', 'K', 'pink'), ('index', 'index', 'cyan'), ('part_avg', 'part_avg', 'yellow'), ('f[now][K]', 'f[now][K]', 'green')],
    captions={
        'f = [[None]': '`f[now][K]` 记忆表，`None` 表示还没算过；`K` 是==还要再切几刀==（组数 − 1）',
        'return self.dfs(0': '分成 `{len(f[0])}` 组 = 还要切 `{len(f[0]) - 1}` 刀，从 `dfs(0, {len(f[0]) - 1})` 开始',
        'if f[now][K] is None': lambda S, B, r: (f'`f[{S.now}][{S.K}]` 还没算过 → 开始计算' if S.f[S.now][S.K] is None
                                                  else f'`f[{S.now}][{S.K}]` = {S.f[S.now][S.K]:.2f} 已经算过 → ==直接返回==，不用重复搜索'),
        'if K == 0': lambda S, B, r: ('`K == 0`：不能再切了，剩下的数==全分到一组==' if S.K == 0
                                      else f'`K = {S.K} > 0`：还要切，枚举这一组的末尾 `index`'),
        'f[now][K] = s[-1]': '整段平均：`{s[-1]} / {n}` = =={f[now][K]:.2f}==',
        'f[now][K] = (s[-1]': '后缀平均：`({s[-1]} − {s[now-1]}) / {n - now}` = =={f[now][K]:.2f}==',
        'f[now][K] = 0': '先置 0，再取各个 `index` 的最大值',
        'for index in range(now, n - K)': '`index` 最多到 `n-K-1 = {n-K-1}`：后面要留 `{K}` 个数给 `{K}` 个组',
        'part_avg = s[index] *': '这一组 `A[0..{index}]` 的平均 = `{s[index]}/{index+1}` = =={part_avg:.2f}==',
        'part_avg = (s[index] -': '这一组 `A[{now}..{index}]` 的平均 = `({s[index]}−{s[now-1]})/{index-now+1}` = =={part_avg:.2f}==',
        'f[now][K] = max(f[now][K], self': lambda S, B, r: f'这组平均 `{S.part_avg:.2f}` + 后面最优 `{S.f[S.now][S.K] if False else (S.f[S.index + 1][S.K - 1]):.2f}`，和之前取大 → `f[{S.now}][{S.K}]` = =={S.f[S.now][S.K]:.2f}==',
        'return f[now][K]': '`f[{now}][{K}]` = =={ret:.2f}==，返回给上一层',
    },
    cards=dict(
        one_liner='枚举这一组的末尾，剩下的交给子问题',
        complexity='时间 `O(n^2·K)`，空间 `O(n·K)`',
        problem=['把数组 `A` 分成最多 `K` 个相邻的非空组，分数 = 每组平均值之和',
                 '求最大分数（组数越多越好，因此恰好 `K` 组）',
                 '示例：`A = [9,1,2,3,9], K = 3` → `20`（`[9] [1,2,3] [9]`）'],
        quote='令f[i][j]表示从第i个数开始到末尾，分为j组可以得到的最大平均值和……我在这里采用的是记忆化搜索的写法，对于边界条件的判断相对方便一点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`j = 1`：剩下的数全分一组，平均值 = 后缀和 / 个数',
              '`j > 1`：枚举这一组的末尾 `index`，`平均值 + f[index+1][j-1]`',
              '区间和用前缀和 `s` 一步得到'],
        summary=['时间 `O(n^2·K)`，空间 `O(n·K)`',
                 '易错：`index` 上界是 `n - K`，要给后面的组留够数',
                 '`now == 0` 时没有 `s[now-1]`，单独处理',
                 '原文已是 Python 3 可运行写法，`* 1.0` 用来得到浮点除法，无需修改'],
    ),
)
