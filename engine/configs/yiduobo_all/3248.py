CONFIG = dict(
    num=3248, title='矩阵中的蛇', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟蛇的行动',
    tags=[],
    code='''
class Solution(object):
    def finalPositionOfSnake(self, n, commands):

        x, y = 0, 0
        for c in commands:
            if c == 'UP':
                x -= 1
            elif c == 'DOWN':
                x += 1
            elif c == 'LEFT':
                y -= 1
            else:
                y += 1
        
        return x * n + y
''',
    call="Solution().finalPositionOfSnake(4, ['RIGHT', 'DOWN', 'DOWN', 'LEFT', 'RIGHT', 'RIGHT'])",
    expect=10,
    views=[
        dict(type='text', h=70, fn=lambda S: f"蛇在 `({S['x']}, {S['y']})` → 编号 `x * n + y` = =={S['x'] * 4 + S['y']}==" if 'x' in S and 'y' in S else '编号 = `x * n + y`'),
        dict(type='grid', label='矩阵（格内是编号）', var=[[r * 4 + c for c in range(4)] for r in range(4)], cursors=[('x', 'y', 'yellow', '蛇')], h=330),
        dict(type='array', var='commands', label='commands', h=130, cell=110),
    ],
    watch=['x', 'y', ('c', 'c', 'cyan'), ('n', 'n')],
    captions={
        'x, y = 0, 0': '蛇一开始在 0 号格，坐标 `(0, 0)`，`x` 是行、`y` 是列',
        'for c in commands': '按顺序取指令 `c = {c}`',
        "c == 'UP'": lambda S, B, r: ('指令是 `UP` → 向上走一格' if S.c == 'UP' else '不是 `UP`，继续判断'),
        "c == 'DOWN'": lambda S, B, r: ('指令是 `DOWN` → 向下走一格' if S.c == 'DOWN' else '不是 `DOWN`，继续判断'),
        "c == 'LEFT'": lambda S, B, r: ('指令是 `LEFT` → 向左走一格' if S.c == 'LEFT' else '不是 `LEFT`，剩下只能是 `RIGHT`'),
        'x -= 1': '向上：行号变小 → `x = {x}`',
        'x += 1': '向下：行号变大 → `x = {x}`',
        'y -= 1': '向左：列号变小 → `y = {y}`',
        'y += 1': '向右：列号变大 → `y = {y}`',
        'return x * n + y': '最后位置 `({x}, {y})`，换算成编号 `{x} * {n} + {y}` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='模拟蛇的坐标，最后换算成单元格编号',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['`n * n` 矩阵，第 `i` 行第 `j` 列的编号是 `i * n + j`',
                 '蛇从 0 号格出发，按指令 up/down/left/right 各走一格，保证不出界',
                 '本视频：`n = 4`，6 条指令 → `10`'],
        quote='蛇一开始处于坐标(0, 0)，接下来只需根据commands模拟蛇在矩阵中的行动，得到蛇最终的下标，然后计算出下标对应的单元格编号即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['记蛇的坐标 `(x, y)`，从 `(0, 0)` 开始',
              '逐条指令改坐标：UP/DOWN 改 `x`，LEFT/RIGHT 改 `y`',
              '结束后用 `x * n + y` 还原成编号'],
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '易错点：UP 是 `x -= 1`，坐标 `x` 是行；编号乘的是 `n`',
                 '最后的 `else` 就是 RIGHT，题目保证指令只有四种',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
