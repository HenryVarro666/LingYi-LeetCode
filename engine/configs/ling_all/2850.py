G0 = [[2, 2, 2], [1, 0, 0], [0, 1, 1]]


def _cell(S, i, j, v):
    if 'x1' in S and (i, j) == (S['x1'], S['y1']) and S.get('_line') in (15, 16):
        return 'pink'
    if 'x2' in S and (i, j) == (S['x2'], S['y2']) and S.get('_line') in (15, 16):
        return 'green'
    if v > 1:
        return 'orange'
    if v == 0:
        return 'cyan'
    return None


def _txt(S):
    if 'x1' in S and S.get('_line') in (15, 16):
        return f"这一对：`({S['x1']},{S['y1']}) → ({S['x2']},{S['y2']})`，距离 `|{S['x1']}-{S['x2']}| + |{S['y1']}-{S['y2']}|` = =={abs(S['x1']-S['x2'])+abs(S['y1']-S['y2'])}==；累计 `total = {S['total']}`"
    if 'total' in S and 'ans' in S:
        return f"当前排列总距离 `{S['total']}`，目前最小 `ans = {S['ans']}`"
    return '橙 = 石头过多（要移走多余的），青 = 空格（要移入）'


def _lst(S, k, note):
    if k not in S:
        return ''
    return f"`{k}` = {str(list(S[k])).replace(' ', '')}　{note}"


CONFIG = dict(
    num=2850, title='将石头分散到网格图的最少移动次数', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='枚举全排列匹配',
    tags=['图论算法', '动态规划', '难度分 2001'],
    code='''
class Solution:
    def minimumMoves(self, grid: List[List[int]]) -> int:
        from_ = []
        to = []
        for i, row in enumerate(grid):
            for j, cnt in enumerate(row):
                if cnt > 1:
                    from_.extend([(i, j)] * (cnt - 1))
                elif cnt == 0:
                    to.append((i, j))

        ans = inf
        for from2 in permutations(from_):
            total = 0
            for (x1, y1), (x2, y2) in zip(from2, to):
                total += abs(x1 - x2) + abs(y1 - y2)
            ans = min(ans, total)
        return ans
''',
    call=f'Solution().minimumMoves({G0!r})',
    expect=4,
    skip=['total = 0'],
    views=[
        dict(type='grid', var='grid', label='grid（石头数）', h=260, cell=70, color=_cell),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='text', fn=lambda S: _lst(S, 'from_', '要移走的石头'), size=24, h=56),
        dict(type='text', fn=lambda S: _lst(S, 'to', '空格（要移入）'), size=24, h=56),
        dict(type='text', fn=lambda S: _lst(S, 'from2', '当前排列，与 to 按位置配对'), size=24, h=56),
    ],
    watch=['total', ('ans', 'ans', 'green')],
    captions={
        'from_ = []': '`from_` 记录要移走的石头坐标（可重复）',
        'to = []': '`to` 记录要移入的空格坐标',
        'if cnt > 1': lambda S, B, r: (f'`({S.i},{S.j})` 有 `{S.cnt}` 个石头，多于 1 个' if S.cnt > 1 else f'`cnt = {S.cnt}`，不大于 1，再看是不是 0'),
        'from_.extend': '多出 `{cnt - 1}` 个石头要移走：`({i},{j})` 加入 `from_` {cnt - 1} 次',
        'elif cnt == 0': '`cnt = {cnt}`：{"是空格，要移入一个石头" if cnt == 0 else "恰好 1 个，不用管"}',
        'to.append': '空格 `({i},{j})` 加入 `to`',
        'ans = inf': '`ans` 记录所有配对方案里总距离的最小值',
        'for from2 in permutations': lambda S, B, r: ('枚举 `from_` 的下一个排列 `from2`，和 `to` 按位置一一配对' if 'from2' in S else '排列都枚举完了'),
        'for (x1, y1)': lambda S, B, r: ('这个排列的所有配对都累加完了' if ('x1' in B and (S.x1, S.y1, S.x2, S.y2) == (B.x1, B.y1, B.x2, B.y2)) else f'取一对：石头从 `({S.x1},{S.y1})` 移到空格 `({S.x2},{S.y2})`'),
        'total += ': '这一对要走曼哈顿距离 `{abs(x1 - x2) + abs(y1 - y2)}`（每步只能走一格）→ `total = {total}`',
        'ans = min': lambda S, B, r: (f'`total = {S.total}` < 之前最小 `{B.ans}` → 更新 `ans` = =={S.ans}==' if S.total < B.ans else f'`total = {S.total}` ≥ 当前最小 `{B.ans}` → `ans` 不变'),
        'return ans': '所有配对方案里最少的总移动次数 =={ret}==',
    },
    cards=dict(
        one_liner='多余的石头配给空格，枚举所有配对取最小总距离',
        complexity='时间 `O(mn·(mn)!)`，空间 `O(mn)`',
        problem=['`3×3` 网格共 9 个石头，每步把一个石头移到相邻格',
                 '要让每个格子恰好 1 个石头，求最少移动次数',
                 '示例：`[[1,3,0],[1,0,0],[1,0,3]]` → `4`'],
        quote='移走的石子个数等于移入的石子个数（即 0 的个数），把移走的石子坐标记到 from，移入的记到 to。枚举 from 的所有排列，与 to 匹配，累加曼哈顿距离，最小值就是答案。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['石头总数 = 格子数，所以多出的石头数 = 空格数',
              '一个石头从 A 走到 B 至少要曼哈顿距离那么多步，路上不会互相妨碍',
              '于是问题变成「多余石头 ↔ 空格」的最小代价匹配：排列全枚举'],
        summary=['时间 `O(mn·(mn)!)`；`3×3` 最多 8 个待配对，很快',
                 '易错：一个格子有 `cnt` 个石头只需移走 `cnt - 1` 个，所以坐标要重复 `cnt - 1` 次',
                 '方法二：最小费用最大流，`10×10` 网格也能做；相似题 1947、1349、1879、2172'],
    ),
)
