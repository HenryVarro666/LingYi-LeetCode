QUEENS = [[0, 0], [1, 1], [2, 2], [3, 4], [3, 5], [4, 4], [4, 5]]
KING = [3, 3]


def _board(S):
    b = [['' for _ in range(8)] for _ in range(8)]
    for qx, qy in QUEENS:
        b[qx][qy] = '后'
    b[KING[0]][KING[1]] = '王'
    return b


def _color(S, i, j, v):
    if v == '王':
        return 'yellow'
    if 'ans' in S and [i, j] in S['ans']:
        return 'green'
    if v == '后':
        return 'pink'
    return None


def _ray(S, B, r):
    x, y = B.x, B.y
    if not (0 <= x < 8 and 0 <= y < 8):
        return f'`({x},{y})` 出了棋盘：这个方向没有皇后能攻击到国王'
    if (x, y) in B.s:
        return f'`({x},{y})` 有皇后 → 射线==首次遇到皇后==，它能攻击国王'
    return f'`({x},{y})` 是空格 → 射线继续前进'


CONFIG = dict(
    num=1222, title='可以攻击国王的皇后', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='国王视角发射八条射线',
    tags=[],
    code='''
class Solution:
    def queensAttacktheKing(self, queens: List[List[int]], king: List[int]) -> List[List[int]]:
        s = set(map(tuple, queens))
        ans = []
        for dx, dy in (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1):
            x, y = king[0] + dx, king[1] + dy  # 国王朝 (dx,dy) 方向发射一条射线
            while 0 <= x < 8 and 0 <= y < 8:
                if (x, y) in s:  # 射线首次遇到皇后
                    ans.append([x, y])
                    break
                x += dx
                y += dy  # 射线没有遇到皇后，继续往前走
        return ans
''',
    call=f'Solution().queensAttacktheKing({QUEENS}, {KING})',
    expect=[[4, 4], [3, 4], [2, 2]],
    views=[
        dict(type='grid', var=_board, label='棋盘（黄 = 国王，粉 = 皇后，绿 = 能攻击国王，蓝框 = 射线当前位置）',
             cell=58, h=500, color=_color, cursors=[('x', 'y', 'blue')]),
        dict(type='text', fn=lambda S: (f"射线方向 `({S['dx']}, {S['dy']})`，已找到 =={len(S['ans'])}== 个" if 'dx' in S else '')),
    ],
    watch=[('dx', 'dx', 'blue'), ('dy', 'dy', 'blue'), ('x', 'x'), ('y', 'y'), ('ans', 'ans', 'green')],
    skip=['ans = []', 'x += dx'],
    max_steps=90,
    captions={
        's = set(': '皇后坐标放进集合 `s`，判断某格有没有皇后是 `O(1)`',
        'for dx, dy': '换一个方向 `(dx, dy) = ({dx}, {dy})`：国王朝这个方向发射射线',
        'x, y = king': '射线从国王旁边第一格出发：`({x}, {y})`',
        'while 0 <= x': lambda S, B, r: (f'`({S.x},{S.y})` 还在棋盘内，继续检查' if 0 <= S.x < 8 and 0 <= S.y < 8
                                         else f'`({S.x},{S.y})` 出界：这条射线结束，换下一个方向'),
        'if (x, y) in s': _ray,
        'ans.append': '这个皇后是该方向上最近的，==挡住了后面所有皇后==：加入答案 `{ans}`',
        'break': '该方向只会被最近的皇后攻击，不用再往前看',
        'y += dy': '没遇到皇后，沿方向前进一格：`({x}, {y})`',
        'return ans': '八个方向都看完，能攻击国王的皇后：`{ans}`',
    },
    cards=dict(
        one_liner='站在国王视角，向八个方向发射射线，首个遇到的皇后就是答案',
        complexity='时间 `O(m+n)`，空间 `O(m)`',
        problem=['`8×8` 棋盘上有若干黑皇后和一个白国王',
                 '返回所有==能直接攻击国王==的皇后坐标（可任意顺序）',
                 '示例：皇后 `[[0,0],[1,1],[2,2],[3,4],[3,5],[4,4],[4,5]]`，国王 `[3,3]`',
                 '→ `[[2,2],[3,4],[4,4]]`'],
        quote='更加巧妙的做法是，站在国王的视角，计算有哪些皇后能被国王「看到」。想象成从国王的位置发射八个方向的射线，记录每条射线首次遇到的皇后。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能攻击：同行、同列或同斜线，且中间没有别的皇后挡住',
              '枚举皇后要判断「有没有被挡」，麻烦',
              '反过来从国王出发：每个方向最多一个答案，就是==第一个遇到的皇后=='],
        summary=['时间 `O(m+n)`：建集合 `O(m)`，八条射线各走至多 8 步',
                 '空间 `O(m)`：集合存皇后',
                 '易错：遇到皇后后要 `break`，否则会把被挡住的皇后也加进答案',
                 '另一种思路：枚举每个皇后，判断是否同线且无遮挡，更繁琐'],
    ),
)
