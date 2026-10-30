S0 = [1, 4, 2]
T0 = [1, 2, 4]


def _j(S):
    return S.get('j') if S.get('_line', 0) >= 7 else None


def _formula(S):
    if 'y' not in S or 'j' not in S:
        return '`f[j]` = 当前这行 `x` 之前的数字与 `t[0..j-1]` 的最大连线数'
    x, y, j = S['x'], S['y'], S['j']
    if x == y:
        return f'`x = {x}` == `y = {y}` → 都选：`pre + 1` = {S["pre"] + 1}'
    return f'`x = {x}` ≠ `y = {y}` → 不连：`max(f[{j + 1}], f[{j}])`'


CONFIG = dict(
    num=1035, title='不相交的线', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='LCS · 一维空间优化',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1806'],
    code='''
class Solution:
    def maxUncrossedLines(self, s: List[int], t: List[int]) -> int:
        f = [0] * (len(t) + 1)
        for x in s:
            pre = 0  # f[0]
            for j, y in enumerate(t):
                tmp = f[j + 1]
                f[j + 1] = pre + 1 if x == y else max(f[j + 1], f[j])
                pre = tmp
        return f[-1]
''',
    call=f'Solution().maxUncrossedLines({S0}, {T0})',
    expect=2,
    max_steps=90,
    skip=['pre = tmp'],
    views=[
        dict(type='array', var='s', label='s（蓝 = 当前行的 x）', h=140, cell=70,
             color=lambda S, i, v: 'blue' if S.get('x') == v else None),
        dict(type='array', var='t', label='t（粉 = 当前 y）', h=150, cell=70,
             color=lambda S, i, v: 'pink' if S.get('j') == i and S.get('_line', 0) >= 7 else None),
        dict(type='array', var='f', label='f[j]：s 前缀与 t[0..j-1] 的最大连线数', h=200, cell=70,
             color=lambda S, i, v: ('yellow' if S.get('j') is not None and i == S['j'] + 1 and S.get('_line', 0) >= 8 else
                                    'green' if S.get('j') is not None and i == S['j'] and S.get('_line', 0) >= 8 else None)),
        dict(type='text', fn=_formula, size=26, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('j', 'j', 'pink'), ('y', 'y', 'pink'), ('pre', 'pre', 'green'), ('tmp', 'tmp', 'yellow')],
    captions={
        'f = [0]': '`f[j]` 表示用 `s` 的前几个数、`t` 的前 `j` 个数，最多能画几条线；一开始全是 `{f}`',
        'for x in s': '取 `s` 的下一个数当 `x`，把 `f` 从上一行滚动更新成这一行；取完就结束',
        'pre = 0': '`pre` 保存「左上角」`f[i][j]`（被覆盖之前的 `f[j]`），这一行开头是 `f[0] = 0`',
        'tmp = f[j + 1]': '先把还没被覆盖的 `f[{j + 1}] = {tmp}` 存进 `tmp`，等这格算完再赋给 `pre`，当作下一格的「左上角」',
        'f[j + 1] =': lambda S, B, r: (f'`x = {S.x}` == `y = {S.y}`：两条线能连 → 左上角 `pre + 1` = =={S.f[S.j + 1]}=='
                                       if S.x == S.y else
                                       f'`x = {S.x}` ≠ `y = {S.y}`：连不了 → 取 `max(f[{S.j + 1}]={B.f[S.j + 1]}, f[{S.j}]={S.f[S.j]})` = =={S.f[S.j + 1]}=='),
        'pre = tmp': '`pre` 更新成刚存的旧值 `{pre}`，留给下一格当左上角',
        'return f[-1]': '最后一格 `f[-1]` 就是 `s`、`t` 全部考虑后的最大连线数 = =={ret}==',
    },
    cards=dict(
        one_liner='不交叉连线 = 最长公共子序列',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['两行数字 `nums1`、`nums2`，相等的数字可以连线，连线==不能交叉、不能共用端点==',
                 '求最多能连几条线',
                 '示例：`[1,4,2]` 和 `[1,2,4]` → `2`；本视频就用它'],
        quote='上面的思考过程和 1143. 最长公共子序列 是一模一样的……当 s[i]=t[j] 时，只需要考虑==都选==的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不交叉 = 连线两端下标同时递增 = ==公共子序列==',
              '`s[i] == t[j]` 就都选，来自左上角 `+1`；否则 `max(上, 左)`',
              '算一行只用到上一行 → 去掉第一维，用 `pre` 记住被覆盖的左上角'],
        summary=['时间 `O(nm)`，空间优化后 `O(m)`',
                 '易错：`s[i] != t[j]` 时来源 `f[j]` 就是被覆盖后的值，==不需要 pre==',
                 '`pre` 必须在覆盖 `f[j+1]` 之前用 `tmp` 保存',
                 '题解还给了记忆化搜索和二维递推两种写法，这里演示最后的一维版本'],
    ),
)
