CONFIG = dict(
    num=3248, title='矩阵中的蛇', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='直接模拟坐标',
    tags=[],
    code='''
class Solution:
    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        i = j = 0
        for s in commands:
            if s[0] == 'U': i -= 1
            elif s[0] == 'D': i += 1
            elif s[0] == 'L': j -= 1
            else: j += 1
        return i * n + j
''',
    call="Solution().finalPositionOfSnake(4, ['RIGHT', 'DOWN', 'DOWN', 'LEFT', 'RIGHT', 'RIGHT'])",
    expect=10,
    views=[
        dict(type='text', h=70, fn=lambda S: f"蛇在 `({S['i']}, {S['j']})`，编号 `i * n + j` = =={S['i'] * 4 + S['j']}==" if 'i' in S and 'j' in S else '格子编号 = `i * n + j`，蛇从 0 号格 `(0, 0)` 出发'),
        dict(type='grid', label='矩阵（格内是编号）', var=[[r * 4 + c for c in range(4)] for r in range(4)], cursors=[('i', 'j', 'yellow', '蛇')], h=330),
        dict(type='array', var='commands', pointers={}, label='commands', h=130, cell=110),
    ],
    watch=['i', 'j', ('s', 's', 'cyan'), ('n', 'n')],
    captions={
        3: '蛇从 `(0, 0)` 出发，`i` 是行、`j` 是列',
        4: '取下一条指令 `s = {s}`，只看首字母 `{s[0]}` 就能区分四个方向',
        5: lambda S, B, r: (f"首字母 `U` → 向上，行 `i` 减 1 → ==i = {S.i}==" if S.s[0] == 'U' else "不是 `U`，看下一个分支"),
        6: lambda S, B, r: (f"首字母 `D` → 向下，行 `i` 加 1 → ==i = {S.i}==" if S.s[0] == 'D' else "不是 `D`，看下一个分支"),
        7: lambda S, B, r: (f"首字母 `L` → 向左，列 `j` 减 1 → ==j = {S.j}==" if S.s[0] == 'L' else "不是 `L`，看 else 分支"),
        8: 'else 就是 `R`（题目保证只有四种）→ 向右，列 `j` 加 1 → ==j = {j}==',
        9: '最终位置 `({i}, {j})`，编号 `{i} * {n} + {j}` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='按指令移动坐标，最后返回 i·n + j',
        complexity='时间 `O(m)`（m 为指令数），空间 `O(1)`',
        problem=['`n × n` 矩阵，格子 `(i, j)` 的编号是 `i * n + j`',
                 '蛇从 0 号格出发，按 `commands` 上下左右走，保证不出界',
                 '示例：`n = 2, ["RIGHT","DOWN"]` → `3`'],
        quote='初始化 i=j=0，按题意要求上下左右移动即可，注意题目保证不会出界。最后返回 i·n+j。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用真的建矩阵，只记行 `i` 和列 `j`',
              '指令只看首字母 `s[0]`：`U` 行减 1，`D` 行加 1，`L` 列减 1，其余是 `R`，列加 1',
              '走完用 `i * n + j` 换算回编号'],
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '易错点：向上是 `i -= 1`（行号变小），不是加；最后乘的是 `n`，不是 `n - 1`',
                 '题解还给了 Python 3.10 的 `match s[0]` 写法二，逻辑相同'],
    ),
)
