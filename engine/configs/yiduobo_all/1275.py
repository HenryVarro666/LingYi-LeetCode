CONFIG = dict(
    num=1275, title='找出井字棋的获胜者', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟下棋 · 逐步检测',
    code='''
class Solution(object):
    def tictactoe(self, moves):
        
        g = [[None] * 3 for _ in range(3)]
        for index in range(len(moves)):
            x, y = moves[index]
            g[x][y] = index % 2
            if g[x][0] == g[x][1] and g[x][0] == g[x][2]:
                return chr(65 + index % 2)
            if g[0][y] == g[1][y] and g[0][y] == g[2][y]:
                return chr(65 + index % 2)
            if x + y == 2 and g[0][2] == g[1][1] and g[0][2] == g[2][0]:
                return chr(65 + index % 2)
            if x == y and g[0][0] == g[1][1] and g[0][0] == g[2][2]:
                return chr(65 + index % 2)
        
        if len(moves) == 9:
            return "Draw"
        
        return "Pending"
''',
    call='Solution().tictactoe([[0,0],[2,0],[1,1],[2,1],[2,2]])',
    expect='A',
    views=[
        dict(type='grid', var=lambda S: [['' if c is None else 'AB'[c] for c in r] for r in S['g']] if 'g' in S else None,
             label='棋盘 g（A 先手 = 偶数步，B 后手 = 奇数步；蓝框 = 刚落的子）', cell=110, h=420,
             cursors=[('x', 'y', 'blue')],
             color=lambda S, i, j, v: ('green' if v == 'A' else 'pink' if v == 'B' else None)),
        dict(type='text', h=80, size=30,
             fn=lambda S: (f"第 `{S['index']}` 步：=={'A' if S['index'] % 2 == 0 else 'B'}== 落子 `({S['x']}, {S['y']})`" if 'index' in S and 'x' in S else '')),
    ],
    watch=[('index', 'index'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    skip=['g = [[None]'],
    captions={
        'g = [[None]': '`3×3` 棋盘，`None` 表示空格',
        'x, y = moves': '第 `{index}` 步落在 `({x}, {y})`',
        'g[x][y] = index % 2': '偶数步是 A、奇数步是 B：`g[{x}][{y}] = {index % 2}`',
        'g[x][0] == g[x][1]': lambda S, B, r: (f"检查第 `{S.x}` 行是否三子相同 → ==成立=={chr(65 + S.index % 2)} 赢" if S.g[S.x][0] == S.g[S.x][1] == S.g[S.x][2]
                                              else f"检查第 `{S.x}` 行：`{S.g[S.x]}` 不是三子相同"),
        'g[0][y] == g[1][y]': lambda S, B, r: (f"检查第 `{S.y}` 列是否三子相同 → ==成立=={chr(65 + S.index % 2)} 赢" if S.g[0][S.y] == S.g[1][S.y] == S.g[2][S.y]
                                              else f"检查第 `{S.y}` 列：`{[S.g[k][S.y] for k in range(3)]}` 不是三子相同"),
        'x + y == 2': lambda S, B, r: (f"`x + y = {S.x + S.y}`，在反对角线上，要查它们是否一致" if S.x + S.y == 2
                                        else f"`x + y = {S.x + S.y} ≠ 2`：不在反对角线上，跳过"),
        'x == y and': lambda S, B, r: (f"`x == y`：落在主对角线上，检查三格是否一致 → ==成立=={chr(65 + S.index % 2)} 赢"
                                       if S.x == S.y and S.g[0][0] == S.g[1][1] == S.g[2][2]
                                       else (f"`x = {S.x}`、`y = {S.y}`：不在主对角线上，跳过" if S.x != S.y
                                             else '在主对角线上，但三格不一致')),
        'return chr': '这一步凑齐三连：返回 `{ret}`',
    },
    cards=dict(
        one_liner='每落一子，只检查这个子所在的行、列和对角线',
        complexity='时间 `O(n)`，空间 `O(1)`（棋盘固定 3×3）',
        problem=['`moves[i] = [行, 列]`，A 先手、B 后手，轮流在 3×3 棋盘落子',
                 '先在同一行/列/对角线连成三子者赢；返回 `A`、`B`、`Draw`（满盘）或 `Pending`（未下完）',
                 '示例：`[[0,0],[2,0],[1,1],[2,1],[2,2]]` → `A`'],
        quote='每一轮放置好棋子之后，都检测当前棋子所在的行、列上的棋子是否一样。另外，若当前位置在左右对角线上，则还需要额外检测对角线上的棋子是否一致。',
        quote_src='—— yiduobo 题解原文',
        idea=['新落的子只会影响它自己的行、列和（可能的）对角线',
              '偶数步写 0（A），奇数步写 1（B），连成三个相同就返回对应字母',
              '反对角线满足 `x + y == 2`，主对角线满足 `x == y`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先落子再检测，所以一行里至少有一个非 `None`，不会把三个空格误判成相等',
                 '都没赢时：9 步走完是 `Draw`，否则 `Pending`',
                 '`chr(65 + index % 2)` 把 0/1 变成 `A`/`B`'],
    ),
)
