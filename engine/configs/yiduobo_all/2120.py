def _cell(S, i, j, v):
    if 'nowx' in S and (i, j) == (S['nowy'], S['nowx']):
        return 'blue'
    if 'startPos' in S and [i, j] == list(S['startPos']):
        return 'green'
    return None


CONFIG = dict(
    num=2120, title='执行所有后缀指令', difficulty='Medium', category='模拟',
    author='yiduobo', technique='枚举起点 + 直接模拟',
    tags=[],
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
    call="Solution().executeInstructions(2, [1, 1], 'LURD')",
    expect=[4, 1, 0, 0],
    skip=['m = len', 'res = []'],
    views=[
        dict(type='grid', var=lambda S: [[0] * S['n'] for _ in range(S['n'])], label='网格（绿 = 起点，蓝 = 机器人当前位置）', cell=120, h=300,
             values=False, color=_cell),
        dict(type='string', var='s', label='s（蓝框 = 本轮起点之后的后缀，黄 = 正在执行的指令）', cell=100, h=190,
             window=('start_index', 'm - 1'),
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] and S['_line'] >= 12 else None),
        dict(type='array', var='res', label='res（每个起点能执行的指令数）', cell=80, h=130),
    ],
    watch=[('start_index', 'start_index', 'blue'), ('index', 'index', 'yellow'), ('(nowy, nowx)', '(nowy, nowx)', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'for start_index': '枚举从第 `{start_index}` 条指令开始的后缀（m 很小，直接模拟）',
        'nowy, nowx = startPos': '每个后缀都从起点出发：`(nowy, nowx) = ({nowy}, {nowx})`',
        'cnt = 0': '已成功执行的指令数清零',
        'for index in range': '依次执行 `s[{start_index}:]` 的指令',
        "if s[index] == 'L'": '看指令 `{s[index]}`',
        'nowx -= 1': '`L` 向左：列 `nowx` → {nowx}',
        'nowx += 1': '`R` 向右：列 `nowx` → {nowx}',
        'nowy -= 1': '`U` 向上：行 `nowy` → {nowy}',
        'nowy += 1': '`D` 向下：行 `nowy` → {nowy}',
        'if nowx < 0': lambda S, B, r: (f'位置 `({S.nowy}, {S.nowx})` 出了 `{S.n}×{S.n}` 网格 → 这条指令不能执行，停止' if (S.nowx < 0 or S.nowx > S.n - 1 or S.nowy < 0 or S.nowy > S.n - 1)
                                         else f'位置 `({S.nowy}, {S.nowx})` 还在网格内，可以执行'),
        'break': '出界，不再往后：本后缀共执行 `{cnt}` 条',
        'cnt += 1': '这条指令执行成功：`cnt` → {cnt}',
        'res.append': '起点 `{start_index}` 能执行 `{cnt}` 条，`res` = {res}',
        'return res': '全部后缀处理完：`{ret}`',
    },
    cards=dict(
        one_liner='m 很小：枚举每个后缀，逐条模拟到出界',
        complexity='时间 `O(m²)`，空间 `O(1)`（不计答案）',
        problem=['`n×n` 网格，机器人从 `startPos` 出发，指令串 `s` 含 `L R U D`',
                 '从第 `i` 条指令开始执行，出界前能执行几条？返回长度为 `m` 的数组',
                 '示例：`n=2, startPos=[1,1], s="LURD"` → `[4,1,0,0]`'],
        quote='由于题目中m的规模很小，因此直接枚举每一种后缀指令然后模拟执行就行了。模拟的过程中需要注意不要走出边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个起点 `start_index` 都把机器人放回 `startPos` 重新走',
              '每走一步先移动再判出界：出界就 `break`，没出界 `cnt += 1`',
              '原文提到：理论上有 `O(m)` 做法，但情况较多，没有继续展开'],
        summary=['时间 `O(m²)`，`m ≤ 500` 完全够用',
                 '易错点：先移动再判断出界，出界那一步不计入 `cnt`',
                 '`nowy, nowx = startPos`：行在前、列在后，别写反',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
