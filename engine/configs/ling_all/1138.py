BOARD = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"]

CONFIG = dict(
    num=1138, title='字母板上的路径', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='曼哈顿距离 · 直角拐弯',
    tags=[],
    code='''
class Solution:
    def alphabetBoardPath(self, target: str) -> str:
        ans = []
        x = y = 0
        for c in target:
            nx, ny = divmod(ord(c) - ord('a'), 5)  # 目标位置
            v = "UD"[nx > x] * abs(nx - x)  # 竖直
            h = "LR"[ny > y] * abs(ny - y)  # 水平
            ans.append((v + h if c != 'z' else h + v) + "!")
            x, y = nx, ny
        return ''.join(ans)
''',
    call='Solution().alphabetBoardPath("leet")',
    expect="DDR!UURRR!!DDD!",
    views=[
        dict(type='grid', var=lambda S: BOARD, label='字母板（蓝框 = 当前位置 (x,y)，绿 = 要去的目标字母）', cell=84, h=330,
             color=lambda S, i, j, v: 'green' if ('nx' in S and (i, j) == (S['nx'], S['ny'])) else None,
             cursors=[('x', 'y', 'blue')]),
        dict(type='string', var='target', label='target（当前处理的字母 c）', cell=70, h=120,
             color=lambda S, i, v: 'green' if 'c' in S and i == S['target'].index(S['c']) and False else None),
        dict(type='array', var='ans', label='ans（每个字母的指令段）', cell=150, h=130),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'blue'), 'c', 'nx', 'ny', 'v', 'h'],
    captions={
        'for c in target': lambda S, B, r: ('`target` 的字母都处理完，循环结束' if len(S.ans) == len(S.target) else f'取下一个字母 `c = {S.c}`，已经收集了 `{len(S.ans)}` 段指令'),
        'ans = []': '`ans` 收集每个字母对应的指令段',
        'x = y = 0': '从左上角 `(0,0)` 出发，`x` 是行、`y` 是列',
        'nx, ny = divmod': '字母 `{c}` 是第 `{ord(c) - 97}` 个 → 行 `{nx}`、列 `{ny}`：目标位置 `({nx},{ny})`',
        'v = "UD"': lambda S, B, r: (f'竖直：`nx={S.nx}` 在 `x={S.x}` 的下面 → `D` × `{abs(S.nx - S.x)}` = `{S.v!r}`' if S.nx > S.x
                                     else f'竖直：`nx={S.nx}` 不在 `x={S.x}` 下面 → `U` × `{abs(S.nx - S.x)}` = `{S.v!r}`（0 步则为空）'),
        'h = "LR"': lambda S, B, r: (f'水平：`ny={S.ny}` 在 `y={S.y}` 右边 → `R` × `{abs(S.ny - S.y)}` = `{S.h!r}`' if S.ny > S.y
                                     else f'水平：`ny={S.ny}` 不在 `y={S.y}` 右边 → `L` × `{abs(S.ny - S.y)}` = `{S.h!r}`（0 步则为空）'),
        'ans.append': lambda S, B, r: (f'去 `z` 必须==先水平再竖直==（`z` 下面只有它一格）：`{S.h}` + `{S.v}` + `!`' if S.c == 'z'
                                       else f'直角拐弯：先竖直 `{S.v}` 再水平 `{S.h}`，最后 `!` 拾取 `{S.c}` → `{S.ans[-1]}`'),
        'x, y = nx, ny': '移到目标位置，下一个字母从 `({nx},{ny})` 出发',
        "return ''.join": '拼起来：`{ret}`',
    },
    cards=dict(
        one_liner='字母转坐标，先竖后横走直角，去 z 时反过来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母板 `abcde / fghij / ... / uvwxy / z`，从 `(0,0)` 出发',
                 '`U D L R` 移动一格，`!` 把当前字母加入答案',
                 '求让答案等于 `target` 的最短指令序列，返回任意一个',
                 '示例：`leet` → `DDR!UURRR!!DDD!`'],
        quote='用「直角拐弯」来移动，比如从 (0,0) 到 (2,3)，可以先往下走 2 步，然后往右走 3 步。例外情况是，如果要移动到 z，必须先水平移动，再竖直移动。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字母 ASCII 连续：`ord(c) - ord("a")` 是第几个，`divmod(…, 5)` 直接得到行和列',
              '最短步数就是曼哈顿距离 `|nx-x| + |ny-y|`，直角拐弯正好走满',
              '`"UD"[nx > x]` 用布尔值当下标选方向，再乘以距离'],
        summary=['时间 `O(n)`，空间 `O(1)`，返回值不计入',
                 '易错：`z` 单独占第 5 行，去 `z` 先水平，否则会踩到不存在的格子',
                 '易错：`nx == x` 时 `"UD"[False] * 0` 是空串，不用特判',
                 '`x, y = nx, ny` 别忘了更新当前位置'],
    ),
)
