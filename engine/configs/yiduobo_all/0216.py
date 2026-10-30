def _bound(S, B, ret):
    n, k = S.n, S.k
    mx = (9 + 9 - k + 1) * k // 2
    top = ' + '.join(str(9 - t) for t in range(k)) if k > 0 else '0'
    if mx < n:
        return f'最大 `{top} = {mx}` < 还差的 `{n}` → ==凑不够，回溯=='
    if n < 0:
        return f'`n = {n}` 已经是负数，但 `{mx}` < `{n}` 不成立 → ==这个剪枝拦不住==，只能继续枚举'
    return f'最大 `{top} = {mx}` ≥ 还差的 `{n}`：有希望，继续'


def _n0(S, B, ret):
    if S.n == 0:
        return f'`n == 0`：和已经凑够了，再看个数 `k = {S.k}`'
    return f'`n = {S.n}` ≠ 0，和还没凑够'


def _for(S, B, ret):
    if S.get('num') is not None and S.num != B.get('num'):
        return f'试 `num = {S.num}`（从 `now[-1] + 1` 起，==递增==不重复）'
    return '`num` 枚举到 9，这一层结束'


def _color(S, i, v):
    now = S.get('now') or []
    return 'green' if v in now[1:] else None


def _dim(S, i, v):
    now = S.get('now') or []
    return bool(now) and v <= now[-1] and v not in now[1:]


CONFIG = dict(
    num=216, title='组合总和 III', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='搜索回溯 · 递增枚举 + 最大和剪枝',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def combinationSum3(self, k, n):

        res = []
        self.dfs(n, k, [0], res)

        return res

    def dfs(self, n, k, now, res):
        if n == 0:
            if k == 0:
                res.append(now[1:])
            return

        if (9 + 9 - k + 1) * k // 2 < n:
            return

        for num in range(now[-1] + 1, 10):
            now.append(num)
            self.dfs(n - num, k - 1, now, res)
            now.pop()
''',
    call='Solution().combinationSum3(2, 16)',
    expect=[[7, 9]],
    skip=[4, 10, 16, 19],
    views=[
        dict(type='array', var=lambda S: list(range(1, 10)), label='数字 1..9（绿 = 已选进 now，暗 = 不大于 now[-1]，不能再选）',
             cell=80, index=False, color=_color, dim=_dim, h=150),
        dict(type='array', var='now', label='now（now[0] = 0 是哨兵，方便写 now[-1] + 1）', cell=80, h=150,
             dim=lambda S, i, v: i == 0),
        dict(type='calls', h=220, hide=('res', 'now')),
        dict(type='stack', var='res', label='res', h=100),
    ],
    watch=[('n（还差）', lambda S: S['_inner'].get('n'), 'pink'), ('k（还要选）', lambda S: S['_inner'].get('k'), 'yellow'),
           ('num', lambda S: S['_inner'].get('num'), 'blue')],
    captions={
        'self.dfs(n, k, [0], res)': '`now = [0]`：放一个哨兵 0，第一个数从 `1` 开始枚举',
        'if n == 0': _n0,
        'if k == 0': lambda S, B, ret: ('`n == 0` 和凑够了，`k == 0` 个数也刚好 → ==找到一个解==' if S.k == 0
                                        else f'`n == 0` 但 `k = {S.k}` ≠ 0：个数不对，不是解'),
        'res.append(now[1:])': '记录 `now[1:] = {res[-1]}`（去掉哨兵）',
        13: '这条路径结束，返回上一层',
        'if (9 + 9 - k + 1) * k // 2 < n': _bound,
        16: '剪枝：回溯到上一层',
        'for num in range': _for,
        'now.append(num)': '选 `{num}`：`now = {now}`',
        'self.dfs(n - num, k - 1': lambda S, B, ret: f'`now = {S.now}`：还差 `{B.n - B.num}`，还要 `{B.k - 1}` 个',
        'now.pop()': '回溯：弹出 `{B.now[-1]}`',
        'return res': '搜索结束，返回 `{ret}`',
    },
    max_steps=72,
    cards=dict(
        one_liner='每次从 now[-1]+1 枚举到 9，最大的 k 个数都凑不够就回溯',
        complexity='时间 `O(k·C(9,k))` 量级，空间 `O(k)`',
        problem=['从 `1..9` 中选 `k` 个==不同==的数，使它们的和为 `n`，返回所有组合',
                 '示例：`k = 3, n = 7` → `[[1,2,4]]`',
                 '本视频：`k = 2, n = 16` → `[[7,9]]`'],
        quote='每次枚举当前选取数中最后一个数==now[-1] + 1至9==，选择之后加入now然后继续搜索，直到sum(now) = n且len(now) = k，或者==剩下的数满足不了答案==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 里的数严格递增 → 每个组合只会被枚举一次',
              '剩下 `k` 个数最大是 `9, 8, …, 9-k+1`，和为 `(9 + 9-k+1)·k / 2`',
              '这个和都 `< n` 就不可能凑够，直接返回'],
        summary=['递增枚举避免重复组合；`now[0] = 0` 哨兵让第一个数从 1 开始',
                 '剪枝只管「凑不够」：`n` 变负数时不会被这个条件剪掉，`n` 越小搜索越多',
                 '`n == 0` 但 `k != 0` 时也要返回，不能继续往下选',
                 '原文为 Python 2 写法，整数除法 `/ 2` 已改为 `// 2`',
                 '原文也提到可用 DP：`f[i][j][k]` 表示和为 i、取 j 次、最大取到 k 的所有解'],
    ),
)
