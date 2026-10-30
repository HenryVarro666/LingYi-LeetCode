N0 = 5


def _lr(S):
    I = S['_inner']
    return I.get('l'), I.get('r'), I.get('cut_pos')


def _cell(S, i, j, v):
    l, r, cp = _lr(S)
    if l is None or r is None:
        return None
    return 'yellow' if (i, j) == (l, r) else None


def _formula(S, B):
    l, r, cp = _lr(B)
    if l is None or r is None:
        return '`f[l][r]` = 猜 `l+1 .. r+1` 里的数，最坏情况下的最少花费'
    ln = B.get('_line')
    if l >= r:
        return f'区间 `[{l}, {r}]`：只剩一个数（或没有），不用猜 → ==0=='
    if l == r - 1:
        return f'区间 `[{l}, {r}]` 只剩两个数 `{l + 1}, {r + 1}`：猜小的 `{l + 1}` → =={l + 1}=='
    if ln == 17 and cp is not None:
        return f'区间 `[{l}, {r}]` 猜 `{cp + 1}`：`{cp + 1}` + `max(f[{l}][{cp - 1}], f[{cp + 1}][{r}])`'
    if ln == 15:
        return f'区间 `[{l}, {r}]` 先假设猜 `{l + 2}`：`{l + 2}` + `f[{l + 2}][{r}]`'
    return f'区间 `[{l}, {r}]`（数字 `{l + 1} .. {r + 1}`）'


CONFIG = dict(
    num=375, title='猜数字大小 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP（记忆化搜索，最坏情况取 max、枚举取 min）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def getMoneyAmount(self, n):

        f = [[None] * (n) for _ in range(n)]

        return self.dfs(0, n - 1, f)

    def dfs(self, l, r, f):
        if f[l][r] is None:
            if l >= r:
                f[l][r] = 0
            elif l == r - 1:
                f[l][r] = l + 1
            else:
                f[l][r] = l + 2 + self.dfs(l + 2, r, f)
                for cut_pos in range(l + 1, r):
                    f[l][r] = min(f[l][r], cut_pos + 1 + max(self.dfs(l, cut_pos - 1, f), self.dfs(cut_pos + 1, r, f)))

        return f[l][r]
''',
    call=f'Solution().getMoneyAmount({N0})',
    expect=6,
    skip=['for cut_pos in range', 'f = [[None]', 'return self.dfs(0'],
    max_steps=80,
    views=[
        dict(type='text', fn=_formula, size=24, h=80),
        dict(type='table', var='f', label='f[l][r]（黄 = 当前正在算的区间，· = 还没算）', h=330, cell=66,
             rows=lambda S: [str(k + 1) for k in range(N0)], cols=lambda S: [str(k + 1) for k in range(N0)],
             color=_cell),
        dict(type='calls', h=200),
    ],
    watch=[('l', lambda S: S['_inner'].get('l'), 'blue'), ('r', lambda S: S['_inner'].get('r'), 'pink'),
           ('cut_pos', lambda S: S['_inner'].get('cut_pos'), 'cyan')],
    captions={
        'if f[l][r] is None': lambda S, B, r: (f'`f[{S.l}][{S.r}]` 还没算过 → 进来算' if S.f[S.l][S.r] is None
                                               else f'`f[{S.l}][{S.r}] = {S.f[S.l][S.r]}` 已经算过 → 直接用（记忆化）'),
        'f[l][r] = 0': '`l >= r`：区间里最多一个数，直接猜中，花费 ==0==',
        'f[l][r] = l + 1': '只有两个数 `{l+1}, {r+1}`：猜小的 `{l+1}`，错了答案必是另一个 → ==`{l+1}`==',
        'f[l][r] = l + 2 + self.dfs': '先假设猜第二小的数 `{B.l+2}`：最坏落在右边 `[{B.l+2}, {B.r}]`（左边只有 1 个数，花 0）→ `{B.l+2} + f[{B.l+2}][{B.r}]`，先递归算右边',
        'f[l][r] = min(': '枚举猜 `{B.cut_pos+1}`：花 `{B.cut_pos+1}`，最坏取左 `f[{B.l}][{B.cut_pos-1}]`、右 `f[{B.cut_pos+1}][{B.r}]` ==较大==的一边；当前最小 `f[{B.l}][{B.r}] = {B.f[B.l][B.r]}` → 先递归算两边',
        'self.dfs(': '进入子区间，先把它的最少花费算出来',
        'return f[l][r]': '区间 `[{l}, {r}]` 的最少花费 `f[{l}][{r}]` = =={ret}==',
    },
    cards=dict(
        one_liner='每次猜一个数，最坏情况取大边，再在所有猜法里取最小',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['我从 `1` 到 `n` 中选一个数，你来猜；猜错我会告诉你大了还是小了',
                 '每次猜 `x` 猜错要付 `x` 元，求==保证获胜所需的最少现金==',
                 '示例：`n = 10` → `16`；本视频：`n = 5` → `6`'],
        quote='虽然二分法可以保证猜中所需的次数最少，但是这里每次猜测代价不同，次数最少并不意味着代价最低。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[l][r]`：在 `l..r` 里猜，==最坏情况==下的最少代价',
              '猜 `cut_pos`：代价 = `cut_pos` + 左右两边==较大==的那个（最坏）',
              '所有 `cut_pos` 里取==最小==；`l == r - 1` 时猜小的；下标从 0 开始，猜的数要 +1'],
        summary=['时间 `O(n^3)`：`O(n^2)` 个区间 × 枚举猜的数 `O(n)`',
                 '易错：下标从 0 开始，`cut_pos` 对应的数是 `cut_pos + 1`',
                 '易错：外层 `min`、内层 `max`（最坏情况），不能用二分',
                 '原文先令 `f = l + 2 + dfs(l+2, r)` 当初值（猜第二小的数），再枚举 `cut_pos` 取小',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
