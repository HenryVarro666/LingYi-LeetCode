def _draw(cv, S, B, box, T):
    if 'n' not in S:
        return
    x0, y0, x1, y1 = box
    n = S['n']
    cell = min(80, (x1 - x0 - 40) / n, (y1 - y0 - 50) / n)
    sx = x0 + ((x1 - x0) - cell * n) / 2
    sy = y0 + 40
    cv.text((x0 + 18, y0 + 4), '网格（蓝 = 起点，粉 = 机器人当前位置）', 22, T['muted'], bold=True)
    sp = S['startPos']
    for r in range(n):
        for c in range(n):
            fill = T['blue'] if [r, c] == list(sp) else (50, 56, 66)
            cv.rect((sx + c * cell + 2, sy + r * cell + 2, sx + (c + 1) * cell - 2, sy + (r + 1) * cell - 2), fill=fill, r=6, alpha=140)
            cv.text((sx + c * cell + cell / 2, sy + r * cell + cell / 2), f'{r},{c}', 18, T['dim'], anchor='mm', mono=True)
    if 'nowx' in S and 'nowy' in S:
        x, y = S['nowx'], S['nowy']
        if 0 <= x < n and 0 <= y < n:
            cv.rect((sx + x * cell + 10, sy + y * cell + 10, sx + (x + 1) * cell - 10, sy + (y + 1) * cell - 10), fill=T['pink'], r=cell / 2)
        else:
            cv.text((sx + n * cell + 20, sy + n * cell / 2), f'(行{y}, 列{x}) 出界', 26, T['red'], anchor='lm', bold=True)


CONFIG = dict(
    num=2120, title='执行所有后缀指令', difficulty='Medium', category='网格图',
    author='yiduobo', technique='枚举起点 + 直接模拟', tags=[],
    code='''
class Solution(object):
    def executeInstructions(self, n, startPos, s):

        m = len(s)
        res = []
        for start_index in range(m):
            nowy, nowx = startPos
            cnt = 0
            for index in range(start_index, m):
                if s[index] == 'L':
                    nowx -= 1
                elif s[index] == 'R':
                    nowx += 1
                elif s[index] == 'U':
                    nowy -= 1
                else:
                    nowy += 1
                
                if nowx < 0 or nowx > n - 1 or nowy < 0 or nowy > n - 1:
                    break

                cnt += 1
            
            res.append(cnt)
        
        return res
''',
    call='Solution().executeInstructions(3, [0, 1], "RRDDLU")',
    expect=[1, 5, 4, 3, 1, 0],
    views=[
        dict(type='custom', h=330, draw=_draw),
        dict(type='string', var='s', label='s（蓝 = 起点 start_index，粉 = 当前指令 index）', cell=70, h=140,
             pointers={'start_index': 'blue', 'index': 'pink'}),
        dict(type='array', var='res', label='res', cell=70, h=140),
    ],
    watch=[('start_index', 'start_index', 'blue'), ('index', 'index', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    skip=["nowx -= 1", "nowx += 1", "nowy -= 1", "nowy += 1", "elif s[index]"],
    captions={
        'm = len': 'm 很小（≤ 500），直接枚举每个后缀',
        'res = []': '`res` 依次存每个起点的答案',
        'for start_index': '枚举起点：从第 `{start_index}` 条指令开始，后缀 `{s[start_index:]}`',
        'nowy, nowx = startPos': '每个后缀都从头出发：`(行 {nowy}, 列 {nowx})`',
        'cnt = 0': '`cnt` 记录这个后缀已执行的指令数',
        'for index': '执行第 `{index}` 条指令 `{s[index]}`',
        "if s[index] == 'L'": '指令 `{s[index]}`：L 列−1，R 列+1，U 行−1，D 行+1，按指令移动机器人',
        'else:': '指令 `{s[index]}`（D）：行 +1',
        'if nowx < 0': lambda S, B, r: f"位置 `(行 {S.nowy}, 列 {S.nowx})`，合法范围 `0..{S.n-1}` → " + ('==出界，停止==' if (S.nowx < 0 or S.nowx > S.n - 1 or S.nowy < 0 or S.nowy > S.n - 1) else '还在界内'),
        'break': '出界：这条指令不算，已执行 `{cnt}` 条',
        'cnt += 1': '没出界，这条指令成功执行：`cnt` → =={cnt}==',
        'res.append': '起点 `{start_index}` 的答案是 `{cnt}`：`res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='m 很小：枚举每个后缀，模拟到出界为止',
        complexity='时间 `O(m^2)`，空间 `O(1)`（不计返回值）',
        problem=['`n×n` 网格，机器人在 `startPos`，指令串 `s`（L/R/U/D）',
                 '从第 `i` 条指令开始执行，出界前停止，求每个 `i` 能执行几条',
                 '示例：`n=3, startPos=[0,1], s="RRDDLU"` → `[1,5,4,3,1,0]`'],
        quote='由于题目中m的规模很小，因此直接枚举每一种后缀指令然后模拟执行就行了。模拟的过程中需要注意不要走出边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层 `start_index` 枚举起点，内层 `index` 逐条执行',
              '每条指令先移动，再检查是否出界；出界就 `break`',
              '没出界才 `cnt += 1`，所以出界那条不计数'],
        summary=['时间 `O(m^2)`，空间 `O(1)`',
                 '`startPos = [行, 列]`，所以 `nowy, nowx = startPos`',
                 '每个起点都要把 `nowy, nowx` 重置；先判出界，再 `cnt += 1`',
                 '作者提到可能有 `O(m)` 做法，但情况较多，原文没有展开',
                 '代码与原文一致，Python 3 下可直接运行（无需修改）'],
    ),
)
