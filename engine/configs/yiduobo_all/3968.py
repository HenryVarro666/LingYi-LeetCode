def _pos(S):
    m = S.get('moves')
    if m is None or 'c' not in S or not all(n in S for n in ('v', 'h', 'space')):
        return -1
    cur = (S['v'], S['h'], S['space'])
    st = [0, 0, 0]
    pre = []
    for c in m:
        pre.append(tuple(st))
        if c == 'U': st[0] += 1
        elif c == 'D': st[0] -= 1
        elif c == 'L': st[1] -= 1
        elif c == 'R': st[1] += 1
        else: st[2] += 1
    pre.append(tuple(st))
    for k, c in enumerate(m):
        if c == S['c'] and cur == pre[k]:
            return k
    for k, c in enumerate(m):
        if c == S['c'] and cur == pre[k + 1] and S.get('_line', 0) in (9, 11, 13, 15, 17):
            return k
    return -1


def _color(S, i, v):
    return 'blue' if i == _pos(S) else None


def _txt(S):
    if 'v' not in S:
        return ''
    return f"竖直 `v = {S['v']}`，水平 `h = {S['h']}`，`'_'` 个数 `space = {S['space']}`"


CONFIG = dict(
    num=3968, title='移动后的最大曼哈顿距离', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='水平竖直互不影响 · 数 _ 的个数', tags=[],
    code='''
class Solution(object):
    def maxDistance(self, moves):
        
        v = 0
        h = 0
        space = 0
        for c in moves:
            if c == 'U':
                v += 1
            elif c == 'D':
                v -= 1
            elif c == 'L':
                h -= 1
            elif c == 'R':
                h += 1
            else:
                space += 1
        
        return abs(v) + abs(h) + space
''',
    call='Solution().maxDistance("LDU_R_L_")',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='string', var='moves', label='moves（蓝 = 当前字符）', cell=90, color=_color, h=200),
        dict(type='text', fn=lambda S: (f"`abs(v) + abs(h) + space = {abs(S['v'])} + {abs(S['h'])} + {S['space']}` = =={abs(S['v'])+abs(S['h'])+S['space']}==" if S.get('_line', 0) >= 19 else '遍历一趟，只记三个数'), size=28),
    ],
    watch=[('v', 'v', 'blue'), ('h', 'h', 'pink'), ('space', 'space', 'orange')],
    captions={
        'v = 0': '`v`：竖直方向上 U 比 D 多几个',
        'h = 0': '`h`：水平方向上 R 比 L 多几个',
        'space = 0': '`space`：`_` 的数量',
        'for c in moves': lambda S, B, ret: (f"取 `moves[{_pos(S)}]` = `'{S.c}'`" if _pos(S) >= 0 else '遍历完 moves'),
        "c == 'U'": lambda S, B, ret: f"`c = '{S.c}'`，是 U 吗？" + ('是' if S.c == 'U' else '不是'),
        "c == 'D'": lambda S, B, ret: f"`c = '{S.c}'`，是 D 吗？" + ('是' if S.c == 'D' else '不是'),
        "c == 'L'": lambda S, B, ret: f"`c = '{S.c}'`，是 L 吗？" + ('是' if S.c == 'L' else '不是'),
        "c == 'R'": lambda S, B, ret: f"`c = '{S.c}'`，是 R 吗？" + ('是' if S.c == 'R' else '不是'),
        'v += 1': '向上，`v` → {v}',
        'v -= 1': '向下，`v` → {v}',
        'h -= 1': '向左，`h` → {h}',
        'h += 1': '向右，`h` → {h}',
        'space += 1': '`_` 先不动，记数 `space` → {space}',
        'return': '`|{v}| + |{h}| + {space}` = =={ret}==：`_` 顺着较多的方向继续远离原点，每个多走 1',
    },
    cards=dict(
        one_liner='水平、竖直互不影响：不算 _ 的距离，再加上 _ 的个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`moves` 由 `U D L R _` 组成，`_` 可换成任意方向',
                 '问走完所有步后，离原点最大的曼哈顿距离',
                 '本视频：`"LDU_R_L_"` → `4`'],
        quote='题目需要计算的是距离原点的最大曼哈顿距离，那么就意味着水平和竖直方向上的移动互不影响。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟遍历，算出水平、竖直方向两种移动的数量之差 `h`、`v`',
              '不考虑 `_`，答案是 `abs(v) + abs(h)`',
              '`_` 顺着较多的那个方向继续远离原点，所以再加 `space`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`h`、`v` 是差值，可正可负，最后分别取绝对值',
                 '`_` 不必真的选方向，数个数就够了',
                 '对比灵神：灵神用 x、y、free，思路相同，yiduobo 先讲清水平竖直互相独立'],
    ),
)
