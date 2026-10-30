def _txt(S):
    if 'index' not in S or S.get('_line') not in (10, 11, 12, 13, 14, 15):
        return '`f[i]` = 处理第 `i` 题到第 `n-1` 题的最大收益，从后往前算'
    i, q, f = S['index'], S['questions'], S['f']
    t = i + q[i][1] + 1
    if t < len(q):
        return f'解决第 `{i}` 题：跳到第 `{t}` 题，`f[{t}] + {q[i][0]}` = {f[t] + q[i][0]}；跳过：`f[{i+1}]` = {f[i + 1]}'
    return f'解决第 `{i}` 题后后面全做不了：只得 `{q[i][0]}` 分；跳过：`f[{i+1}]` = {f[i + 1]}'


CONFIG = dict(
    num=2140, title='解决智力问题', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='从后往前线性 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1709'],
    code='''
class Solution(object):
    def mostPoints(self, questions):

        n = len(questions)
        f = [0] * n
        f[-1] = questions[-1][0]
        for index in range(n - 2, -1, -1):
            f[index] = f[index + 1]
            if index + questions[index][1] + 1 < n:
                f[index] = max(f[index], f[index + questions[index][1] + 1] + questions[index][0])
            else:
                f[index] = max(f[index], questions[index][0])

        return f[0]
''',
    call='Solution().mostPoints([[1,1],[2,2],[3,3],[4,4],[5,5]])',
    expect=7,
    views=[
        dict(type='array', var=lambda S: [f'{p}分/{b}' for p, b in S['questions']], label='questions：分数 / 脑力（蓝 = 当前题）', h=190, cell=110,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var='f', label='f[i]：从第 i 题做到最后的最大收益', h=200, cell=100,
             pointers={'index': 'blue'}),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=['n', ('index', 'index', 'blue')],
    captions={
        'n = len': '`n = {n}`',
        'f = [0] * n': '`f[i]` 表示处理第 `i` 题到第 `n-1` 题的最大收益',
        'f[-1] = ': '边界：最后一题，解决它就得 `{f[-1]}` 分，后面没题了',
        'for index in range': lambda S, B, r: ('从后往前都算完了，答案是 `f[0]`' if B.get('index') == S.index else f'轮到第 `{S.index}` 题，`f[{S.index}]` 由后面的 `f` 算出'),
        'f[index] = f[index + 1]': '==跳过==第 `{index}` 题：直接继承 `f[{index+1}] = {f[index]}`',
        'if index + ': lambda S, B, r: (f'`{S.index}+{S.questions[S.index][1]}+1 = {S.index + S.questions[S.index][1] + 1}` ' + ('< n：解决后还有题可做' if S.index + S.questions[S.index][1] + 1 < S.n else '≥ n：解决后后面全做不了')),
        'f[index] = max(f[index], f[': '解决：`max({B.f[B.index]}, f[{index + questions[index][1] + 1}] + {questions[index][0]})` = =={f[index]}==',
        'f[index] = max(f[index], questions': '解决后后面全不能做：`max({B.f[B.index]}, {questions[index][0]})` = =={f[index]}==',
        'return f[0]': '最高分 = `f[0]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 表示做第 i 题到最后的最大收益，从后往前推',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['按顺序决定每题「解决」或「跳过」，解决第 `i` 题得 `points` 分',
                 '但接下来 `brainpower` 道题都不能做',
                 '示例：`[[1,1],[2,2],[3,3],[4,4],[5,5]]` → `7`'],
        quote='由于题目的要求是解决了某个问题后之后不能再解决后续的若干问题，因此本题的状态表示应该是 f[i] 表示处理从第 i 题到第 n - 1 题的最大收益。',
        quote_src='—— yiduobo 题解',
        idea=['边界：`f[n-1]` = 最后一题的分数',
              '跳过：`f[i] = f[i+1]`；解决：`f[i+brainpower+1] + points`',
              '如果 `i+brainpower+1 ≥ n`，后面全不能做，解决就只得 `points`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '要从后往前算，因为 `f[i]` 依赖右边的状态',
                 '越界要单独判断，不要偷懒取 `f[n]`；灵神的写法多开一格 `f[n]=0` 省掉分支'],
    ),
)
