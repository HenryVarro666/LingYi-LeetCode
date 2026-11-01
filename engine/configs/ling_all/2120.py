CONFIG = dict(
    num=2120, title='执行所有后缀指令', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='枚举起点 + 暴力模拟（Go 原文转写）', tags=[],
    code='''
dirs = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

class Solution:
    def executeInstructions(self, n: int, startPos: List[int], s: str) -> List[int]:
        ans = [0] * len(s)
        for i in range(len(s)):
            ans[i] = len(s) - i
            x, y = startPos[0], startPos[1]
            for j, ch in enumerate(s[i:]):
                x += dirs[ch][0]
                y += dirs[ch][1]
                if x < 0 or x >= n or y < 0 or y >= n:
                    ans[i] = j
                    break
        return ans
''',
    call='Solution().executeInstructions(3, [0, 1], "RRDDLU")',
    expect=[1, 5, 4, 3, 1, 0],
    views=[
        dict(type='custom', h=330, draw=lambda cv, S, B, box, T: _draw(cv, S, B, box, T)),
        dict(type='string', var='s', label='s（蓝 = 起点 i，粉 = 当前执行的指令）', cell=70, h=140,
             pointers={'i': 'blue'}),
        dict(type='array', var='ans', label='ans', cell=70, h=140, pointers={'i': 'blue'}),
    ],
    skip=['x += dirs'],
    watch=[('i', 'i', 'blue'), ('(x, y)', '(x, y)', 'pink'), ('j', 'j'), ('ans', 'ans', 'green')],
    captions={
        'ans = [0]': '`ans` 存每个起点能执行的指令数',
        'for i in range': '枚举起点：从第 `{i}` 条指令开始，后缀 `{s[i:]}`',
        'ans[i] = len(s) - i': '先假设能全部执行完：`ans[{i}] = {len(s)} - {i} = {ans[i]}`；中途出界再改',
        'x, y = startPos': '回到起点 `({x}, {y})`，每个后缀都从头走',
        'for j, ch': '第 `{j}` 条指令 `{ch}`',
        'y += dirs': '`{ch}` 的偏移 `{dirs[ch]}` → 位置 `({x}, {y})`',
        'if x < 0': lambda S, B, r: f"位置 `({S.x}, {S.y})`，网格 `0..{S.n-1}` → " + ('==出界，停止==' if (S.x < 0 or S.x >= S.n or S.y < 0 or S.y >= S.n) else '还在界内，继续'),
        'ans[i] = j': '第 `{j}` 条指令会走出网格，之前只执行了 `{j}` 条：`ans[{i}] = {j}`',
        'break': '出界了，换下一个起点',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='枚举每个后缀起点，从头模拟，出界就记下步数',
        complexity='时间 `O(m^2)`，空间 `O(1)`（不计返回值）',
        problem=['`n×n` 网格，机器人在 `startPos`，指令串 `s`（L/R/U/D）',
                 '从第 `i` 条指令开始执行，出界前停止，求每个 `i` 能执行几条',
                 '示例：`n=3, startPos=[0,1], s="RRDDLU"` → `[1,5,4,3,1,0]`'],
        quote='ans[i] = len(s) - i ... if x < 0 || x >= n || y < 0 || y >= n { ans[i] = j; break }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['`m ≤ 500`，每个后缀直接模拟，`O(m^2)` 够快',
              '先默认能执行完 `len(s) - i` 条',
              '走出界时第 `j` 条指令不算，`ans[i] = j` 并 `break`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`dirs` 按字符索引的数组改成 dict，`range s[i:]` 改成 `enumerate(s[i:])`）',
                 '时间 `O(m^2)`，空间 `O(1)`',
                 '易错点：出界的那条指令不计入，所以是 `ans[i] = j` 而不是 `j + 1`',
                 '每个起点都要把 `x, y` 重置为 `startPos`'],
    ),
)

def _draw(cv, S, B, box, T):
    if 'n' not in S:
        return
    x0, y0, x1, y1 = box
    n = S['n']
    cell = min(80, (x1 - x0 - 40) / n, (y1 - y0 - 50) / n)
    sx = x0 + ((x1 - x0) - cell * n) / 2
    sy = y0 + 40
    cv.text((x0 + 18, y0 + 4), '网格（蓝 = 起点，粉 = 机器人当前位置，红 = 出界）', 22, T['muted'], bold=True)
    sp = S['startPos']
    for r in range(n):
        for c in range(n):
            fill = T['blue'] if [r, c] == list(sp) else (50, 56, 66)
            cv.rect((sx + c * cell + 2, sy + r * cell + 2, sx + (c + 1) * cell - 2, sy + (r + 1) * cell - 2), fill=fill, r=6, alpha=140)
            cv.text((sx + c * cell + cell / 2, sy + r * cell + cell / 2), f'{r},{c}', 18, T['dim'], anchor='mm', mono=True)
    if 'x' in S and 'y' in S:
        x, y = S['x'], S['y']
        if 0 <= x < n and 0 <= y < n:
            cv.rect((sx + y * cell + 10, sy + x * cell + 10, sx + (y + 1) * cell - 10, sy + (x + 1) * cell - 10), fill=T['pink'], r=cell / 2)
        else:
            cv.text((sx + n * cell + 20, sy + n * cell / 2), f'({x},{y}) 出界', 26, T['red'], anchor='lm', bold=True)
