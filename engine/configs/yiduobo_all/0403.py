STONES = [0, 1, 3, 5, 6, 8, 12, 17]


def _f(S):
    f = S.get('f')
    if f is None:
        return None
    return [['·' if v is None else 'F' for v in row] for row in f]


def _cur(S):
    inner = S.get('_inner', {})
    if 'prev_pos' in inner and 'now' in inner:
        return inner['prev_pos'], inner['now']
    return None


def _txt(S):
    inner = S.get('_inner', {})
    if 'now' not in inner:
        return '`f[i][j]`：这一步从石头 i 跳到石头 j，后面能不能到终点（· = 还没算，F = 确定不行）'
    st = S['stones']
    a, b = inner['prev_pos'], inner['now']
    k = st[b] - st[a]
    return f'上一跳 `{st[a]} → {st[b]}`（步长 {k}），这一跳可以跳 `{k - 1}`、`{k}`、`{k + 1}`'


CONFIG = dict(
    num=403, title='青蛙过河', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='记忆化搜索 · f[i][j] = 从 i 跳到 j 后能否到终点',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def canCross(self, stones):

        if stones[1] != 1:
            return False

        pos_dict = {}
        for index, pos in enumerate(stones):
            pos_dict[pos] = index

        f = [[None] * len(stones) for _ in range(len(stones))]
        return self.dfs(0, 1, f, stones, pos_dict)

    def dfs(self, prev_pos, now, f, stones, pos_dict):
        if now == len(stones) - 1:
            return True

        if f[prev_pos][now] is not None:
            return False

        prev_len = stones[now] - stones[prev_pos]
        for k in range(-1, 2):
            next_pos = pos_dict.get(stones[now] + prev_len + k, 0)
            if next_pos > now and self.dfs(now, next_pos, f, stones, pos_dict):
                return True

        f[prev_pos][now] = False
        return False
''',
    call=f'Solution().canCross({STONES})',
    expect=True,
    views=[
        dict(type='array', var=lambda S: S['_inner'].get('stones') or S.get('stones'),
             label='stones（石头位置；蓝 = 上一块，粉 = 当前所在）', cell=96,
             pointers={'prev_pos': 'blue', 'now': 'pink'}, h=250),
        dict(type='table', var=_f, label='f[prev][now]（· 未算，F = 从这里出发走不到终点）', cell=46, h=330,
             cursors=[(lambda S: (_cur(S) or (None, None))[0], lambda S: (_cur(S) or (None, None))[1], 'pink')],
             color=lambda S, i, j, v: 'red' if v == 'F' else None),
        dict(type='calls', h=130, hide=('f', 'stones', 'pos_dict')),
    ],
    watch=[('prev_pos', 'prev_pos', 'blue'), ('now', 'now', 'pink'), 'prev_len', ('k', 'k', 'yellow')],
    captions={
        'if stones[1] != 1': lambda S, B, r: ('第一跳固定是 1 步（上一步长 0 → 只能跳 1），`stones[1] = %d` == 1，可以出发' % S.stones[1]
                                              if S.stones[1] == 1 else '第一块石头不在 1 处 → 第一跳就到不了，直接 False'),
        'pos_dict[pos] = index': '`pos_dict[{pos}] = {index}`：位置 → 石头编号，之后 O(1) 判断某位置有没有石头',
        'f = [[None]': '先用 `pos_dict` 建好「位置 → 石头编号」（O(1) 判断落点有没有石头）；`f[i][j]` 初始 `None`：还没算过',
        'return self.dfs(0, 1': '从「0 号石头跳到 1 号石头」出发，递归 `dfs(0, 1)`',
        'if now == len(stones) - 1': lambda S, B, r: (f'`now = {S.now}` 已经是最后一块石头 → ==到达终点==，返回 True' if S.now == len(S.stones) - 1
                                                      else f'`now = {S.now}` 还不是终点（共 {len(S.stones)} 块）→ 继续跳'),
        'if f[prev_pos][now] is not None': lambda S, B, r: ('这个状态算过了且是 False → 直接返回 False，不再重复搜索'
                                                            if S.f[S.prev_pos][S.now] is not None else '这个状态没算过，继续往下展开'),
        'prev_len = stones': '上一跳长度 `prev_len = {stones[now]} − {stones[prev_pos]} = {prev_len}` → 这一跳只能是 `{prev_len-1}`、`{prev_len}`、`{prev_len+1}`',
        'if next_pos > now and': lambda S, B, r: (
            f"落点 `{B.stones[B.now] + B.prev_len + B.k}`（步长 {B.prev_len + B.k}）→ 是 {B.next_pos} 号石头，在 `now = {B.now}` 前方 → 跳过去，递归 `dfs({B.now}, {B.next_pos})`"
            if B.next_pos > B.now else
            f"落点 `{B.stones[B.now] + B.prev_len + B.k}`（步长 {B.prev_len + B.k}）→ " + ('没有石头' if B.next_pos == 0 else f'是 {B.next_pos} 号石头但不在前方') + '，这个步长不行'),
        25: '下游有一条路能到终点 → 这一状态也为 True，层层返回',
        16: '`now` 就是终点 → 返回 True',
        'f[prev_pos][now] = False': '三种步长都试过，没有一个能到终点 → `f[{prev_pos}][{now}] = False`，以后不再展开',
        19: '这个状态已经算过（且是 False）→ 返回 False',
        28: '这个状态走不到终点 → 返回 False，回溯到上一层',
    },
    skip=['pos_dict = {}', 'for index, pos in enumerate', 'pos_dict[pos] = index', 'for k in range(-1, 2)', 'next_pos = pos_dict.get'],
    cards=dict(
        one_liner='f[i][j]：从石头 i 跳到 j 之后，还能不能到终点',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['一排石头的位置 `stones`（升序），青蛙从第 0 块出发，第一跳固定 1 步',
                 '上一跳 `k` 步，这一跳只能跳 `k-1`、`k`、`k+1` 步，且只能往前',
                 '问能否到达最后一块石头',
                 '示例：`[0,1,3,5,6,8,12,17]` → `True`'],
        quote='用f[i][j]表示如果这一步从石头i跳到了石头j，那么最后是否可能到达终点。……判断在这些位置上是否存在石头next，如果存在的话，那么递归计算f[j][next]。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态是「上一块石头 + 当前石头」：由它们就能算出上一跳的步长',
              '从 j 起跳枚举 `k-1, k, k+1`，用 `pos_dict` 判断落点有没有石头',
              '只要有一个落点能到终点就是 True；全不行就记 `f[i][j] = False`'],
        summary=['时间 `O(n²)`：状态 `(prev, now)` 最多 `n²` 个，每个只展开一次',
                 '易错：必须 `next_pos > now`，否则会跳回头或原地不动（`pos_dict.get` 默认 0 也被它过滤）',
                 '`f` 里只有 `None` / `False` 两种值：`True` 会直接返回，不需要记忆',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
