BOARD = [[1, 1, 2], [3, 3, 4], [6, 6, 6]]
PATTERN = ["ab", "66"]


def _bcolor(S, i, j, v):
    if 'r' not in S or 'i' not in S or 'j' not in S:
        return None
    r, c, oi, oj = S['r'], S['c'], S['i'], S['j']
    if 'x' in S and 'y' in S and S['_line'] >= 17 and (i, j) == (oi + S['x'], oj + S['y']):
        return 'yellow'
    if oi <= i < oi + r and oj <= j < oj + c:
        return 'blue'
    return None


def _pcolor(S, x, y, v):
    if 'x' in S and 'y' in S and 'mapping' in S and S['_line'] >= 17 and (x, y) == (S['x'], S['y']):
        return 'yellow'
    return None


CONFIG = dict(
    num=3078, title='矩阵中的字母数字模式匹配 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力枚举左上角 + 哈希表映射',
    tags=[],
    code='''
class Solution(object):
    def findPattern(self, board, pattern):

        m = len(board)
        n = len(board[0])

        r = len(pattern)
        c = len(pattern[0])

        def check(i, j):
            mapping = {}
            mapped = set()
            for x in range(r):
                for y in range(c):
                    if 'a' <= pattern[x][y] <= 'z':
                        if pattern[x][y] not in mapping:
                            if board[x + i][y + j] in mapped:
                                return False
                            mapping[pattern[x][y]] = board[x + i][y + j]
                            mapped.add(board[x + i][y + j])
                        elif mapping[pattern[x][y]] != board[x + i][y + j]:
                            return False
                    elif int(pattern[x][y]) != board[x + i][y + j]:
                        return False
            return True

        for i in range(m - r + 1):
            for j in range(n - c + 1):
                if check(i, j):
                    return [i, j]
        
        return [-1, -1]
''',
    call=f'Solution().findPattern({BOARD}, {PATTERN})',
    expect=[1, 1],
    views=[
        dict(type='grid', var='board', label='board（蓝框 = 当前枚举的子矩阵，黄 = 正在比较的格子）', h=230, cell=70,
             color=_bcolor, cursors=[]),
        dict(type='grid', var=lambda S: [list(row) for row in S['pattern']], label='pattern（字母 = 要映射，数字 = 必须相等）', h=170, cell=70,
             color=_pcolor, cursors=[]),
        dict(type='map', var='mapping', label='mapping：pattern 字母 → board 数字', h=110, fmt=lambda k, v: f'{k} → {v}'),
        dict(type='set', var='mapped', label='mapped：已经被映射走的数字', h=100, fmt=lambda x: str(x)),
    ],
    watch=[('左上角', lambda S: (S.get('i'), S.get('j')) if 'j' in S else None, 'blue'),
           ('x,y', lambda S: (S.get('x'), S.get('y')) if 'y' in S and 'mapping' in S else None, 'yellow')],
    skip=['m = len', 'n = len', 'r = len', 'c = len', 'mapping = {}', 'mapped = set()', 'for x in range', 'for y in range',
          'for j in range', 'for i in range'],
    max_steps=70,
    captions={
        "if 'a' <= pattern": lambda S, B, r: (f"`pattern[{S.x}][{S.y}] = {S.pattern[S.x][S.y]}` 是"
                                              + ('字母 → 看它的映射' if 'a' <= S.pattern[S.x][S.y] <= 'z' else '数字 → 必须和 board 对应格相等')),
        'if pattern[x][y] not in mapping': lambda S, B, r: (f"字母 `{S.pattern[S.x][S.y]}` 还没映射过" if S.pattern[S.x][S.y] not in S.mapping
                                                           else f"字母 `{S.pattern[S.x][S.y]}` 已映射到 `{S.mapping[S.pattern[S.x][S.y]]}`，要检查是否一致"),
        'if board[x + i][y + j] in mapped': lambda S, B, r: (f"`board` 对应格是 `{S.board[S.x + S.i][S.y + S.j]}`，" +
                                                            ('它已被别的字母占用 → 不同字母不能映射到同一数字' if S.board[S.x + S.i][S.y + S.j] in S.mapped
                                                             else '没被占用，可以建立映射')),
        'mapping[pattern[x][y]] = board': '建立映射：`{pattern[x][y]} → {board[x + i][y + j]}`',
        'mapped.add': '把 `{board[x + i][y + j]}` 记进 `mapped`，以后别的字母不能再用',
        'elif mapping[pattern': lambda S, B, r: (f"`{S.pattern[S.x][S.y]}` 之前映射到 `{S.mapping[S.pattern[S.x][S.y]]}`，这格是 `{S.board[S.x + S.i][S.y + S.j]}` → "
                                                  + ('不一致，匹配失败' if S.mapping[S.pattern[S.x][S.y]] != S.board[S.x + S.i][S.y + S.j] else '一致，继续')),
        'elif int(pattern': lambda S, B, r: (f"数字 `{S.pattern[S.x][S.y]}` 对 board `{S.board[S.x + S.i][S.y + S.j]}` → "
                                             + ('不相等，匹配失败' if int(S.pattern[S.x][S.y]) != S.board[S.x + S.i][S.y + S.j] else '相等，继续')),
        'return False': '这个左上角匹配失败，换下一个位置',
        'return True': '`pattern` 每格都对上了 → 这个左上角匹配成功',
        'if check(i, j)': '检查以 `({i}, {j})` 为左上角的 `{r}×{c}` 子矩阵',
        'return [i, j]': '找到第一个匹配位置 =={[i, j]}==',
        'return [-1, -1]': '所有位置都失败 → 返回 `[-1, -1]`',
    },
    cards=dict(
        one_liner='枚举子矩阵左上角，用哈希表 + 集合检查字母是否一一映射',
        complexity='时间 `O(m·n·r·c)`，空间 `O(r·c)`',
        problem=['`board` 是整数矩阵，`pattern` 的每格是数字或小写字母',
                 '数字格：board 对应格必须等于它；字母格：同字母映射到同数字，不同字母映射到不同数字',
                 '返回匹配子矩阵的第一个左上角，没有则 `[-1, -1]`；示例 `[[1,1,2],[3,3,4],[6,6,6]]` 配 `["ab","66"]` → `[1,1]`'],
        quote='对于以(i, j)为左上角的子矩阵，遍历pattern中的每个字符，对于当前遍历到的pattern[x][y]，其在board中对应的字符应该是board[i + x][j + y]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`mapping` 记「字母 → 数字」，`mapped` 记「已被占用的数字」',
              '新字母遇到已被占用的数字 → 两个字母映射同一数字，失败',
              '老字母遇到不同数字 → 映射不一致，失败；数字格直接比较'],
        summary=['时间 `O(m·n·r·c)`，数据规模小，暴力足够',
                 '必须同时判断「字母 → 数字」和「数字 → 字母」唯一：所以才要 `mapped` 集合',
                 '数字格用 `int(pattern[x][y])` 转换后再比较',
                 '原文已是 Python 3 可运行的写法，无需改动',
                 '题面在库里缺失，题意按 LeetCode 3078 与 yiduobo 题解整理'],
    ),
)
