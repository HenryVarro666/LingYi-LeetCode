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


def _clauses(S):
    a, b, c, d, e, f = S['a'], S['b'], S['c'], S['d'], S['e'], S['f']
    btw = lambda l, m, r: min(l, r) < m < max(l, r)
    return [
        a == e and (c != e or not btw(b, d, f)),
        b == f and (d != f or not btw(a, c, e)),
        c + d == e + f and (a + b != e + f or not btw(c, a, e)),
        c - d == e - f and (a - b != e - f or not btw(c, a, e)),
    ]


def _cond(S, B, r):
    a, b, c, d, e, f = S.a, S.b, S.c, S.d, S.e, S.f
    cl = _clauses(S)
    names = ['车同行', '车同列', '象同主斜线（c+d）', '象同副斜线（c-d）']
    if any(cl):
        k = cl.index(True)
        return f'==成立==：{names[k]}且中间没有被挡 → 一步直接吃到，返回 1'
    notes = []
    if a == e:
        notes.append('车和后同一行，但象夹在中间挡住了')
    if b == f:
        notes.append('车和后同一列，但象夹在中间挡住了')
    if c + d == e + f or c - d == e - f:
        notes.append('象和后同一斜线，但车夹在中间挡住了')
    why = '；'.join(notes) if notes else '车和象都不在后的攻击线上'
    return f'四种直接攻击都不成立：{why} → 走到下面返回 2'


CONFIG = dict(
    num=3001, title='捕获黑皇后需要的最少移动次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论：一步 or 两步',
    tags=['灵神题单', '难度分 1797'],
    code='''
class Solution:
    def minMovesToCaptureTheQueen(self, a: int, b: int, c: int, d: int, e: int, f: int) -> int:
        # m 在 l 和 r 之间（写不写等号都可以）
        def in_between(l: int, m: int, r: int) -> bool:
            return min(l, r) < m < max(l, r)

        # 车直接攻击到皇后 or 象直接攻击到皇后
        if a == e and (c != e or not in_between(b, d, f)) or \\
           b == f and (d != f or not in_between(a, c, e)) or \\
           c + d == e + f and (a + b != e + f or not in_between(c, a, e)) or \\
           c - d == e - f and (a - b != e - f or not in_between(c, a, e)):
            return 1
        return 2
''',
    call='Solution().minMovesToCaptureTheQueen(5, 1, 5, 3, 5, 6)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=50),
        dict(type='grid', var=_board, label='棋盘（蓝 = 车，绿 = 象，粉 = 黑后）', cell=62, color=_cell, h=520, index=False),
    ],
    watch=['a', 'b', 'c', 'd', 'e', 'f'],
    captions={
        'if a == e and': lambda S, B, r: (f'车 `a = {S.a}` 与后 `e = {S.e}` 同一行；象 `c = {S.c}` 也在这一行 → 要判断象是否夹在车和后的列之间，调用 `in_between`' if S.a == S.e and S.c == S.e
                                          else '车和后不同行 → 横向吃不到，看下一个条件'),
        'b == f and': lambda S, B, r: (f'`b = {S.b}`、`f = {S.f}`：车和后不在同一列 → 竖向吃不到' if S.b != S.f else '车和后同一列，看象是否夹在中间'),
        'c + d == e + f and': lambda S, B, r: (f'`c+d = {S.c + S.d}`、`e+f = {S.e + S.f}`：象和后不在同一副斜线' if S.c + S.d != S.e + S.f else '象和后同一副斜线，看车是否夹在中间'),
        'c - d == e - f and': lambda S, B, r: (f'`c-d = {S.c - S.d}`、`e-f = {S.e - S.f}`：象和后不在同一主斜线 → 四个条件全部不成立' if S.c - S.d != S.e - S.f else '象和后同一主斜线，看车是否夹在中间'),
        'return min(l, r)': lambda S, B, r: ('`min(l, r) < m < max(l, r)` 为 ==True==：象的位置夹在车和后之间 → 象挡住了车' if r else '`min(l, r) < m < max(l, r)` 为 ==False==：中间没有挡路的棋子'),
        'return 1': '一步就能吃掉黑后，返回 `1`',
        'return 2': '其余情况答案一定是 2：象挡路就「闪击」移开象，车不在线上就横竖各走一步（两条路至多被象挡一条）→ 返回 `2`',
    },
    cards=dict(
        one_liner='要么一步吃，要么两步一定吃得到',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 棋盘上有白车 `(a,b)`、白象 `(c,d)`、黑后 `(e,f)`',
                 '只能动白棋，车走直线，象走斜线，都不能越子，求吃掉黑后的最少步数',
                 '示例：`(1,1) (8,8) (2,3)` → `2`'],
        quote='如果车能攻击到皇后，但被象挡住，那么移走象，车就可以攻击到皇后，答案是 2。小知识：这在国际象棋中叫做「闪击」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['车能直接攻击（同行/同列且中间没象）→ 答案 `1`；象同理，中间不能有车',
              '其余情况一律是 `2`：被挡就移开挡路的棋子；车不在线上就横竖各一步，必有一条不被象挡',
              '判断「中间」：`in_between` 用 `min(l, r) < m < max(l, r)`',
              '本视频用车、象、后同一行的例子：象夹在中间，一步吃不到'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '象判斜线：`c+d == e+f`（副对角线）、`c-d == e-f`（主对角线）',
                 '被挡的条件要写在 `and (…)` 里：不同线，或者在线上但没人挡',
                 '另一种写法用 `(m-l)*(m-r) > 0` 表示 m 不在 l、r 之间'],
    ),
)
