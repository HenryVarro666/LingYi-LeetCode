def _board(S):
    if 'a' not in S:
        return None
    g = [[''] * 8 for _ in range(8)]
    g[S['a'] - 1][S['b'] - 1] = '车'
    g[S['c'] - 1][S['d'] - 1] = '象'
    g[S['e'] - 1][S['f'] - 1] = '后'
    return g


def _cell(S, i, j, v):
    return {'车': 'blue', '象': 'green', '后': 'pink'}.get(v)


def _txt(S):
    if 'a' not in S:
        return ''
    return f"车 `({S['a']},{S['b']})`　象 `({S['c']},{S['d']})`　黑后 `({S['e']},{S['f']})`（行, 列）"


CONFIG = dict(
    num=3001, title='捕获黑皇后需要的最少移动次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先判一步到位，否则两步',
    tags=['灵神题单', '难度分 1797'],
    code='''
class Solution(object):
    def minMovesToCaptureTheQueen(self, a, b, c, d, e, f):

        if a == e and (c != a or d < min(b, f) or d > max(b, f)):
            return 1
        
        if b == f and (d != b or c < min(a, e) or c > max(a, e)):
            return 1
        
        if e - f == c - d and (a - b != c - d or a < min(c, e) or a > max(c, e)):
            return 1
        
        if e + f == c + d and (a + b != c + d or a < min(c, e) or a > max(c, e)):
            return 1
        
        return 2
''',
    call='Solution().minMovesToCaptureTheQueen(1, 1, 3, 1, 6, 4)',
    expect=1,
    views=[
        dict(type='text', fn=_txt, h=50),
        dict(type='grid', var=_board, label='棋盘（蓝 = 车，绿 = 象，粉 = 黑后）', cell=62, color=_cell, h=520, index=False),
    ],
    watch=['a', 'b', 'c', 'd', 'e', 'f'],
    captions={
        'if a == e': lambda S, B, r: (f'车 `a = {S.a}` 和后 `e = {S.e}` 不在同一行 → 车不能横向直接吃' if S.a != S.e
                                      else '车和后同一行，再看象是否夹在中间'),
        'if b == f': lambda S, B, r: (f'车 `b = {S.b}` 和后 `f = {S.f}` 不在同一列 → 车不能竖向直接吃' if S.b != S.f
                                      else '车和后同一列，再看象是否夹在中间'),
        'if e - f == c - d': lambda S, B, r: (f'`e-f = {S.e - S.f}`、`c-d = {S.c - S.d}`：象和后在同一条斜线，且 `a-b = {S.a - S.b}` 不在这条线上 → 车不挡路，象一步吃到'
                                              if (S.e - S.f == S.c - S.d and S.a - S.b != S.c - S.d) else
                                              ('象和后同一斜线，再看车是否夹在中间' if S.e - S.f == S.c - S.d else '`e-f != c-d`：不在同一条主斜线')),
        'if e + f == c + d': lambda S, B, r: (f'`e+f = {S.e + S.f}`、`c+d = {S.c + S.d}`：不在同一条副斜线' if S.e + S.f != S.c + S.d else '象和后同一副斜线，再看车是否夹在中间'),
        'return 1': '车或象有一个能一步直接吃到后 → 答案 `1`',
        'return 2': '一步到不了：车一定能先横后竖（或先竖后横），两条路不交叉，象至多挡一条 → 答案 `2`',
    },
    cards=dict(
        one_liner='能一步吃就一步，不能的话车横竖两步必到',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 棋盘：白车 `(a,b)`、白象 `(c,d)`、黑后 `(e,f)`',
                 '只能动白棋，车走直线，象走斜线，不能越子，求吃掉黑后的最少步数',
                 '本视频：车 `(1,1)`、象 `(3,1)`、后 `(6,4)` → `1`'],
        quote='如果不满足上面的条件，那么车是一定可以通过一次水平的移动加上一次竖直的移动到达皇后的位置的，在这里可以先水平后竖直，或者先竖直后水平。由于这两条路径没有交叉，也就意味着象最多挡住其中的一条路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['一步到位：车与后同行/同列，且象不在两者之间；或象与后同斜线，且车不在两者之间',
              '四个 `if` 分别对应：同行、同列、主斜线、副斜线',
              '都不满足：车横竖各走一步，先横后竖或先竖后横，两条路径不交叉',
              '象最多挡住一条，另一条畅通 → 答案 `2`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '「夹在中间」用 `min/max` 判断，等于不算在中间时才放行',
                 '同斜线两种：`e - f == c - d` 和 `e + f == c + d`',
                 '对比灵神：灵神一个大 `if` 用 `or` 连起来；yiduobo 拆成四个 `if`，更好读'],
    ),
)
