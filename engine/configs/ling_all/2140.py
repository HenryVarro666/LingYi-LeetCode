def _txt(S):
    if 'point' not in S or S.get('_line') not in (6, 7, 8):
        return '`f[i]` = 在「能解决第 `i` 题」时，前面题目能拿到的最高分'
    i, j, p, f = S['i'], S.get('j'), S['point'], S['f']
    if S['_line'] == 6:
        return f'跳过第 `{i}` 题：`f[{i+1}]` 至少是 `f[{i}]` = =={f[i+1]}=='
    if S['_line'] == 7:
        return f'解决第 `{i}` 题后，下一个能做的是 `j = {j}`'
    return f'解决：`f[{j}] = max(.., f[{i}] + {p})` = =={f[j]}=='


CONFIG = dict(
    num=2140, title='解决智力问题', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='刷表法递推',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1709'],
    code='''
class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        n = len(questions)
        f = [0] * (n + 1)
        for i, (point, brainpower) in enumerate(questions):
            f[i + 1] = max(f[i + 1], f[i])
            j = min(i + brainpower + 1, n)
            f[j] = max(f[j], f[i] + point)
        return f[n]
''',
    call='Solution().mostPoints([[1,1],[2,2],[3,3],[4,4],[5,5]])',
    expect=7,
    views=[
        dict(type='array', var=lambda S: [f'{p}分/{b}' for p, b in S['questions']], label='questions：分数 / 脑力（蓝 = 当前题 i，粉 = 解决后下一个能做的 j）', h=200, cell=110,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='array', var='f', label='f[k]：能解决第 k 题时，前面最多拿多少分（f[n] 是答案）', h=200, cell=100,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=['n', ('i', 'i', 'blue'), ('j', 'j', 'pink'), 'point', 'brainpower'],
    captions={
        'n = len': '`n = {n}`，再加一个虚拟的第 `n` 题，作为终点',
        'f = [0]': '`f[0] = 0`：还没做任何题，得分为 0',
        'for i, (point': lambda S, B, r: ('所有题都处理完，`f[n]` 里就是答案' if B.get('i') == S.i else f'轮到第 `{S.i}` 题：`point = {S.point}`，`brainpower = {S.brainpower}`'),
        'f[i + 1] = max': '==不解决==：第 `{i+1}` 题仍可做，用 `f[{i}] = {f[i]}` 更新 `f[{i+1}]` → {f[i+1]}',
        'j = min': '==解决==：接下来 `{brainpower}` 题不能做，下一个能做的是 `min({i}+{brainpower}+1, {n}) = {j}`',
        'f[j] = max': '`f[{j}] = max({B.f[j]}, f[{i}] + {point})` = =={f[j]}==',
        'return f[n]': '终点 `f[{n}]` 就是最高分 = =={ret}==',
    },
    cards=dict(
        one_liner='选了就跳到 i+脑力+1，用当前状态去更新未来状态',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['按顺序决定每题「解决」或「跳过」，解决第 `i` 题得 `points` 分',
                 '但接下来 `brainpower` 道题都不能做',
                 '示例：`[[1,1],[2,2],[3,3],[4,4],[5,5]]` → `7`（做第 1、4 题）'],
        quote='从左往右递推的困难之处在于，并不好确定该从哪里转移过来……对于这种知道该去哪，但不好知道该从哪来的 DP，可以用刷表法：用当前状态，更新未来的（右边的）状态。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` = 能做第 `i` 题时，前面拿到的最高分',
              '不选：能做第 `i+1` 题，更新 `f[i+1]`',
              '选：跳到 `j = min(i+脑力+1, n)`，用 `f[i]+分数` 更新 `f[j]`'],
        after=[dict(heading='另外两种写法', lines=['题解先写记忆化搜索 `dfs(i)`，再 1:1 翻译成倒序递推', '倒序是查表法 `f[i]=max(f[i+1], f[j]+points)`', '这里演示的是最后的刷表法'])],
        summary=['时间、空间都是 `O(n)`',
                 '`j` 要和 `n` 取最小，越界的都当成终点',
                 '`brainpower=1` 时就是打家劫舍'],
    ),
)
