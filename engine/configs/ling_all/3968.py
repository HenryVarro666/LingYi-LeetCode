def _pos(S, ch='ch', names=('x', 'y', 'free')):
    """当前正在处理 moves 的哪个下标（-1 = 还没开始 / 已结束）"""
    m = S.get('moves')
    if m is None or ch not in S or not all(n in S for n in names):
        return -1
    cur = tuple(S[n] for n in names)
    st = [0, 0, 0]
    pre = []
    for c in m:
        pre.append(tuple(st))
        if c == 'L': st[0] -= 1
        elif c == 'R': st[0] += 1
        elif c == 'D': st[1] -= 1
        elif c == 'U': st[1] += 1
        else: st[2] += 1
    pre.append(tuple(st))
    for k, c in enumerate(m):
        if c == S[ch] and cur == pre[k]:
            return k
    return -1


def _color(S, i, v):
    k = _pos(S)
    if k < 0:
        return 'green' if 'x' in S and S.get('_line', 0) >= 11 else None
    if i == k:
        return 'blue'
    return None


def _txt(S):
    if 'x' not in S:
        return ''
    return f"水平 `x = {S['x']}`，竖直 `y = {S['y']}`，自由步 `free = {S['free']}`"


CONFIG = dict(
    num=3968, title='移动后的最大曼哈顿距离', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='分开统计 · 万能步全往远处走', tags=[],
    code='''
class Solution:
    def maxDistance(self, moves: str) -> int:
        x = y = free = 0

        for ch in moves:
            if ch == 'L': x -= 1
            elif ch == 'R': x += 1
            elif ch == 'D': y -= 1
            elif ch == 'U': y += 1
            else: free += 1

        return abs(x) + abs(y) + free
''',
    call='Solution().maxDistance("LLU_R_D_")',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='string', var='moves', label='moves（蓝 = 当前这一步）', cell=90, color=_color, h=200),
        dict(type='text', fn=lambda S: (f"`|x| + |y| + free = {abs(S['x'])} + {abs(S['y'])} + {S['free']}` = =={abs(S['x'])+abs(S['y'])+S['free']}==" if S.get('_line', 0) >= 11 else '先统计，再一起算距离'), size=28),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('free', 'free', 'orange')],
    captions={
        'x = y = free': '`x`、`y` 是不含 `_` 时的坐标，`free` 是 `_` 的个数，都从 0 开始',
        'for ch in moves': lambda S, B, ret: (f"取 `moves[{_pos(S)}]` = `'{S.ch}'`" if _pos(S) >= 0 else '遍历完 moves'),
        "ch == 'L'": lambda S, B, ret: f"`ch = '{S.ch}'`，是 L 吗？" + ('是，==向左==，`x` 减 1' if S.ch == 'L' else '不是'),
        "ch == 'R'": lambda S, B, ret: f"`ch = '{S.ch}'`，是 R 吗？" + ('是，==向右==，`x` 加 1' if S.ch == 'R' else '不是'),
        "ch == 'D'": lambda S, B, ret: f"`ch = '{S.ch}'`，是 D 吗？" + ('是，==向下==，`y` 减 1' if S.ch == 'D' else '不是'),
        "ch == 'U'": lambda S, B, ret: f"`ch = '{S.ch}'`，是 U 吗？" + ('是，==向上==，`y` 加 1' if S.ch == 'U' else '不是'),
        'x -= 1': '向左一步，`x` → {x}',
        'x += 1': '向右一步，`x` → {x}',
        'y -= 1': '向下一步，`y` → {y}',
        'y += 1': '向上一步，`y` → {y}',
        'free += 1': '`_` 想往哪走都行：先记下来，`free` → {free}',
        'return': '`|{x}| + |{y}| + {free}` = =={ret}==：每个 `_` 都朝远离原点的方向走，各贡献 1',
    },
    cards=dict(
        one_liner='每个 `_` 都朝远离原点的方向走，答案是 |x|+|y|+free',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`moves` 由 `U D L R _` 组成，`_` 可以换成任意一个方向',
                 '从原点出发走完全部步，求离原点最大的曼哈顿距离',
                 '示例：`"L_D_"` → `4`；本视频 `"LLU_R_D_"` → `4`'],
        quote='本题是 2833. 距离原点最远的点 的二维版本，思路是一样的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先不管 `_`：只统计 `L R U D` 得到 `x`、`y`',
              '`x` 为负就让 `_` 继续向左，`x` 为正就向右，竖直同理',
              '每个 `_` 都能让 `|x|` 或 `|y|` 恰好多 1，所以直接加 `free`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`_` 不用真的替换成哪个方向，数个数就够了',
                 '易错：先取绝对值再加，不要对 `x + y` 取绝对值',
                 '类似题：2833 距离原点最远的点（一维）、3443 K 次修改后的最大曼哈顿距离'],
    ),
)
