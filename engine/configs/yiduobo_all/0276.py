CONFIG = dict(
    num=276, title='栅栏涂色', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='两个状态 f/g 滚动 DP',
    tags=[],
    code='''
class Solution(object):
    def numWays(self, n, k):

        f, g = 0, k
        for index in range(1, n):
            f, g = g, (f + g) * (k - 1) 
        
        return f + g
''',
    call='Solution().numWays(4, 3)',
    expect=66,
    max_steps=40,
    views=[
        dict(type='array', var=lambda S: [f'#{i + 1}' for i in range(S['n'])], label='栅栏（共 n 根；当前刚涂完前 index+1 根，蓝色 = 最后一根）',
             h=200, cell=110, pointers={'index': 'blue'},
             color=lambda S, i, v: ('blue' if i == S.get('index') else ('green' if i < S.get('index', -1) else None)) if 'index' in S else None),
        dict(type='text', size=30, h=80,
             fn=lambda S: (f"前 {S.get('index', 0) + 1} 根：最后两根同色 `f` = =={S['f']}== ，不同色 `g` = =={S['g']}==" if 'index' in S and 'f' in S
                           else (f"只有 1 根：`f` = {S['f']}，`g` = `k` = {S['g']}" if 'f' in S else ''))),
        dict(type='text', size=28, h=70,
             fn=lambda S: f"总方案数 = `f + g` = `{S['f']} + {S['g']}` = =={S['f'] + S['g']}==" if 'f' in S and 'index' in S else ''),
    ],
    watch=[('n', 'n', 'purple'), ('k', 'k', 'purple'), ('index', 'index', 'blue'), ('f', 'f', 'cyan'), ('g', 'g', 'pink')],
    captions={
        'f, g = 0, k': '只有 1 根栅栏：最后两根不可能同色，`f = 0`；不同色指这一根随便涂，`g = k = {g}`',
        'for index in range': lambda S, B, r: (f'开始涂第 `{S.index + 1}` 根' if 'index' in S and S.get('index') != B.get('index') else '全部涂完'),
        'f, g = g, (f + g)': '`f = 旧 g = {f}`：新栅栏和前一根同色，==前两根必须不同色==；`g = (旧f + 旧g) × (k-1) = {B.f} + {B.g}` × {k-1} = =={g}==，随便什么状态都能涂成不同色',
        'return f + g': '最后两根同色 + 不同色 = 总方案数 `{f} + {g}` = =={ret}==',
    },
    cards=dict(
        one_liner='只记最后两根栅栏是否同色，滚动递推',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 根栅栏、`k` 种颜色，每根涂一种颜色',
                 '==不允许连续三根==栅栏颜色相同，求涂法总数',
                 '本视频：`n=4`，`k=3` → `66`'],
        quote='令f[i]表示前i个栅栏，最后两个栅栏颜色相同时的涂色方案数，而g[i]则表示前i个栅栏，最后两个栅栏颜色不同时的涂色方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['同色：新栅栏只能抄前一根的颜色，所以前两根必须不同色：`f[i] = g[i-1]`',
              '不同色：前面怎样都行，新栅栏有 `k-1` 种选择：`g[i] = (f[i-1] + g[i-1]) × (k-1)`',
              '每轮只依赖上一轮，用两个变量滚动即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '初始是 1 根栅栏：`f = 0`，`g = k`；循环从第 2 根开始',
                 '`f, g = g, (f + g) * (k - 1)` 是同时赋值，右边用旧值',
                 '答案是 `f + g`，别漏掉任何一类'],
    ),
)
