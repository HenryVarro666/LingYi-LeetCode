def _board(S):
    s = S['source']
    t = S['target']
    return [['象' if [r, c] == s else '目标' if [r, c] == t else '' for c in range(1, 9)] for r in range(1, 9)]


def _bcolor(S, i, j, v):
    r, c = i + 1, j + 1
    sr, sc = S['source']
    tr, tc = S['target']
    if [r, c] == [sr, sc]:
        return 'blue'
    if [r, c] == [tr, tc]:
        return 'pink'
    if r + c == sr + sc or r - c == sr - sc:
        return 'cyan'
    return None


CONFIG = dict(
    num=4034, title='象到达目标格子的最少移动步数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='颜色奇偶 + 对角线判断', tags=[],
    code='''
class Solution:
    def minBishopMoves(self, source: list[int], target: list[int]) -> int:
        sx, sy = source
        tx, ty = target

        # 颜色不同
        if (sx + sy) % 2 != (tx + ty) % 2:
            return -1

        # 两点之间的直线，如果斜率是 -1 或者 1，那么两点可以直接到达，否则要走两步
        return 1 if sx + sy == tx + ty or sx - sy == tx - ty else 2
''',
    call='Solution().minBishopMoves([4, 2], [1, 3])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"象 `({S['sx']},{S['sy']})`  目标 `({S['tx']},{S['ty']})`：坐标和 `{S['sx']+S['sy']}` / `{S['tx']+S['ty']}`，坐标差 `{S['sx']-S['sy']}` / `{S['tx']-S['ty']}`" if 'ty' in S else '蓝 = 象，粉 = 目标，青 = 象一步能到的格子'), size=26),
        dict(type='grid', var=_board, rows=list(range(1, 9)), cols=list(range(1, 9)), color=_bcolor, cell=64, h=560,
             label='8×8 棋盘（行、列从 1 开始）'),
    ],
    watch=[('source', 'source', 'blue'), ('target', 'target', 'pink')],
    captions={
        'sx, sy = source': '拆出象的位置 `(sx, sy) = ({sx}, {sy})`',
        'tx, ty = target': '拆出目标位置 `(tx, ty) = ({tx}, {ty})`',
        'if (sx + sy) % 2 != (tx + ty) % 2': '象走对角线不换色，坐标和奇偶不变：`{sx+sy} % 2 = {(sx+sy)%2}`，`{tx+ty} % 2 = {(tx+ty)%2}` → ==颜色相同，有解==',
        'return 1 if': '同一条对角线？和 `{sx+sy}` vs `{tx+ty}`，差 `{sx-sy}` vs `{tx-ty}`，都不等 → ==需要两步==，返回 `{ret}`',
    },
    cards=dict(
        one_liner='象不换色：异色无解，同色最多两步',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 棋盘，象每步可沿对角线走任意格',
                 '求从 `source` 到 `target` 的最少步数，到不了返回 `-1`',
                 '示例：`[4,2] → [1,3]` 答案 `2`；`[1,1] → [3,4]` 答案 `-1`'],
        quote='由于象移动后不改变所在格子的颜色，所以如果两个象的格子颜色不同，那么无解。',
        quote_src='—— 灵茶山艾府题解',
        idea=['异色格子永远到不了：返回 `-1`',
              '同色且斜率为 `±1`（和相等或差相等）：一步到',
              '否则必有一个中转格同时在两条对角线上：两步到'],
        after=[dict(heading='为什么最多两步', lines=['同色两点 `A`、`B`：从 `A` 画斜率 `+1` 的线，从 `B` 画斜率 `-1` 的线', '两条线的交点和 `A`、`B` 同色，必在棋盘内或能换另一对线', '所以 `A → 交点 → B`，两步一定够', '再看示例 3：`[1,1]` 和 `[3,4]` 坐标和奇偶不同，直接 `-1`'])],
        summary=['时间、空间都是 `O(1)`',
                 '判断颜色用坐标和的奇偶，判断对角线用 `x+y` 或 `x-y` 相等',
                 '一步可达的条件不要漏掉 `x - y` 相等的那条对角线',
                 '本题没有真正的搜索，是纯结论题'],
    ),
)
