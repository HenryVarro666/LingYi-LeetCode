BOARD = [['X', 'X', '.', 'X'],
         ['.', '.', '.', 'X'],
         ['X', '.', '.', 'X']]


def _head(b, r, c):
    return b[r][c] == 'X' and (c == 0 or b[r][c - 1] != 'X') and (r == 0 or b[r - 1][c] != 'X')


def _seen(S, r, c):
    """(r, c) 是否已经判断完"""
    if 'j' not in S:
        return False
    i, j = S['i'], S['j']
    if (r, c) < (i, j):
        return True
    return (r, c) == (i, j) and S.get('_line') in (8,)


def _color(S, r, c, v):
    if 'j' not in S:
        return None
    b = S['board']
    i, j = S['i'], S['j']
    if _seen(S, r, c) and _head(b, r, c):
        return 'green'                      # 已数过的战舰头部
    if (r, c) == (i, j):
        return None
    if b[i][j] == 'X' and ((r, c) == (i, j - 1) or (r, c) == (i - 1, j)):
        return 'purple'                     # 正在检查的左邻 / 上邻
    if _seen(S, r, c) and v == 'X':
        return 'blue'                       # 战舰身体（不计数）
    return None


def _info(S):
    if 'j' not in S:
        return '绿 = 战舰头部（计数），蓝 = 战舰身体，紫 = 正在检查的左邻 / 上邻'
    i, j, b = S['i'], S['j'], S['board']
    if b[i][j] != 'X':
        return f'`({i},{j})` 是空位'
    left = 'X' if j and b[i][j - 1] == 'X' else '非 X'
    up = 'X' if i and b[i - 1][j] == 'X' else '非 X'
    return f'`({i},{j})` 是 X：左边 `{left}`，上边 `{up}`' + ('　→ ==头部==' if _head(b, i, j) else '　→ 不是头部')


def _if(S, B, r):
    i, j, c, row, b = S.i, S.j, S.c, S.row, S.board
    if c != 'X':
        return f'`board[{i}][{j}]` 是 `.`，不是战舰，跳过'
    if j > 0 and row[j - 1] == 'X':
        return f'左边 `({i},{j - 1})` 是 X → 它是横向战舰的==中间或尾部==，不是头部'
    if i > 0 and b[i - 1][j] == 'X':
        return f'上边 `({i - 1},{j})` 是 X → 它是竖向战舰的==中间或尾部==，不是头部'
    return f'是 X，且左边、上边都不是 X → `({i},{j})` 是==战舰头部=='


CONFIG = dict(
    num=419, title='棋盘上的战舰', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='一次遍历 · 枚举战舰起点',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def countBattleships(self, board: List[List[str]]) -> int:
        ans = 0
        for i, row in enumerate(board):
            for j, c in enumerate(row):
                if c == 'X' and (j == 0 or row[j - 1] != 'X') and \\
                                (i == 0 or board[i - 1][j] != 'X'):
                    ans += 1
        return ans
''',
    call=f'Solution().countBattleships({BOARD})',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=28, h=80),
        dict(type='grid', var='board', cursors=[('i', 'j', 'yellow', '(i,j)')], color=_color, cell=110, h=480),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'c', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '战舰个数 = 战舰「头部」个数：只数头部',
        'for i, row in enumerate': lambda S, B, r: ('所有行都看完了' if 'i' in B and B.i == S.i and 'j' in S
                                                    else f'第 `{S.i}` 行'),
        'for j, c in enumerate': lambda S, B, r: (f'第 `{S.i}` 行看完' if B.get('i') == S.i and B.get('j') == S.j and S.get('_inner', {}).get('j') == B.get('j') and B.get('_line') != 5
                                                  else f'看 `board[{S.i}][{S.j}] = {S.c!r}`'),
        "if c == 'X'": _if,
        'ans += 1': '数到一艘新战舰：`ans` → =={ans}==',
        'return ans': '一共 =={ans}== 艘战舰',
    },
    cards=dict(
        one_liner='战舰的个数 = 战舰头部的个数',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`board` 中 `X` 是战舰、`.` 是空位；横着或竖着==连续的 X== 是一艘战舰',
                 '战舰互不相邻，统计战舰数；进阶：一次扫描、`O(1)` 空间、不改 board',
                 '本视频：3×4 棋盘，一横、一竖、一个单格 → `3`'],
        quote='战舰的个数，等于战舰「头部」的个数。如果位于 (i,j) 的格子是战舰的头部，那么左边和上边的相邻格子不能是 X。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每艘战舰只有==一个==头部：横向战舰的最左格 / 竖向战舰的最上格',
              '头部条件：是 X，且 `j == 0` 或左边不是 X，且 `i == 0` 或上边不是 X',
              '只看左邻、上邻 → 不用 DFS、不用 visited、不改 board'],
        summary=['时间 `O(mn)`，空间 `O(1)`，满足进阶要求',
                 '`j == 0 or ...` 写在前面：==短路求值==避免 `row[-1]` 取到行尾',
                 '能这么做是因为题目保证战舰互不相邻、只有横竖两种形状',
                 '通用做法：网格图 DFS/BFS 数连通块（200. 岛屿数量）'],
    ),
)
