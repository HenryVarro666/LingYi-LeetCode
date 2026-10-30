A = [1, 2, 3, -9, 4, 1]


def _cap_f(S, B, ret):
    i = S.i
    ws = [(S.f[i + k], i + k) for k in (1, 2, 3)]
    m = min(ws)
    return (f'后手最少能拿 `min(f[{i+1}], f[{i+2}], f[{i+3}])` = `min({S.f[i+1]}, {S.f[i+2]}, {S.f[i+3]})` = {m[0]}；'
            f'先手 = 后缀和 `{S.suf_sum}` − {m[0]} = =={S.f[i]}==')


def _fcolor(S, i, v):
    if 'i' not in S or S.get('_line') not in (8, 9):
        return None
    if i == S['i']:
        return 'yellow'
    if i in (S['i'] + 1, S['i'] + 2, S['i'] + 3):
        return 'blue'
    return None


def _formula(S):
    if 'i' not in S or 'suf_sum' not in S:
        return '`f[i]` = 剩下后缀 `[i, n-1]` 里，先手最多拿到的分数'
    i = S['i']
    return f'后缀 `[{i}, {len(S["stoneValue"])-1}]` 总和 `{S["suf_sum"]}`：先手拿的 + 后手拿的 = {S["suf_sum"]}'


CONFIG = dict(
    num=1406, title='石子游戏 III', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='博弈 DP · 先手得分最大化',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2027'],
    code='''
class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        f = [0] * (n + 3)
        suf_sum = 0  # stoneValue 的后缀和
        for i in range(n - 1, -1, -1):
            suf_sum += stoneValue[i]
            f[i] = suf_sum - min(f[i + 1], f[i + 2], f[i + 3])

        diff = f[0] - (suf_sum - f[0])
        if diff == 0:
            return "Tie"
        return "Alice" if diff > 0 else "Bob"
''',
    call=f'Solution().stoneGameIII({A!r})',
    expect='Alice',
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='array', var='stoneValue', label='stoneValue', h=200, cell=90, pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i < S['i']),
        dict(type='array', var='f', label='f[i]：先手最多拿多少（黄 = 正在算，蓝 = 后手的三种选择）', h=240, cell=90,
             pointers={'i': 'yellow'}, color=_fcolor),
    ],
    watch=[('i', 'i', 'blue'), ('suf_sum', 'suf_sum', 'cyan'), ('f[i]', 'f[i]', 'green'), ('diff', 'diff', 'orange')],
    captions={
        'n = len': '`n = {n}`',
        'f = [0] * (n + 3)': '`f[i]` = 后缀 `[i, n-1]` 里先手最多得分；多开 3 格 0，让 `i = n-1` 时 `f[i+1..i+3]` 不越界（没石子 = 0 分）',
        'suf_sum = 0': '`suf_sum` 记录后缀和',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：从后往前算，`f[i]` 只依赖更靠后的 `f[i+1..i+3]`' if S.get('i') != B.get('i') else '后缀都算完了'),
        'suf_sum +=': '后缀和加上 `stoneValue[{i}] = {stoneValue[i]}` → `suf_sum = {suf_sum}`',
        'f[i] = suf_sum': _cap_f,
        'diff = f[0]': '先手总分 `f[0] = {f[0]}`，后手 = `{suf_sum} - {f[0]}` = {suf_sum - f[0]}，差 =={diff}==',
        'if diff == 0': lambda S, B, r: '差为 0 → 平局' if S.diff == 0 else f'差 `{S.diff}` ≠ 0，不是平局',
        'return "Alice"': '`diff = {diff}`：{"> 0 → Alice 赢" if diff > 0 else "< 0 → Bob 赢"}',
    },
    skip=[],
    cards=dict(
        one_liner='先手拿得越多，后手剩得越少：f[i] = 后缀和 − 后手最少能拿的',
        complexity='时间 `O(nK)`，`K = 3`；空间 `O(n)`',
        problem=['石子排成一行，两人轮流从左边拿 1、2 或 3 堆，拿完为止，分高者赢',
                 '双方都最优，返回 `"Alice"` / `"Bob"` / `"Tie"`',
                 '示例：`[1,2,3,7]` → `"Bob"`；本视频：`[1,2,3,-9,4,1]` → `"Alice"`'],
        quote='自己的得分 + 对手的得分 = 元素总和。……所以，也可以定义 f[i] 表示当剩余整数为 a 的后缀 [i,n-1] 时，先手得分的最大值。',
        quote_src='—— 灵茶山艾府题解 · 另一种状态定义',
        idea=['先手拿完后，后手变成新的先手，他最多拿 `f[j+1]`',
              '后手拿得越少，先手越多：`f[i] = 后缀和 - min(f[i+1], f[i+2], f[i+3])`',
              '最后比较 `f[0]` 和 `总和 - f[0]`'],
        summary=['时间 `O(n)`（`K` 是常数），空间 `O(n)`',
                 '`f` 开 `n+3`，省去 `i` 靠近末尾时的边界判断',
                 '灵神还给了：差值定义 `dfs(i) = max(s - dfs(j+1))`、三变量滚动、单调队列优化',
                 '同类题：博弈 DP 题单（石子游戏系列）'],
    ),
)
