def _line(S):
    if 'right_boundary' not in S:
        return None
    return list(range(S['right_boundary'] + 1))


def _color(S, i, v):
    if 'forbidden_pos' not in S:
        return None
    if i in S['forbidden_pos']:
        return 'red'
    if 'now_pos' in S and i == S['now_pos']:
        return 'blue'
    if i == S['x']:
        return 'yellow'
    if i in S['used']:
        return 'green'
    return None


def _txt(S):
    if 'q' not in S:
        return ''
    if 'next_pos' in S and 'delta' in S and 'now_pos' in S and S.get('_line', 0) >= 24:
        d = '右跳' if S['delta'] > 0 else '左跳'
        return f"从 `{S['now_pos']}` {d} `{abs(S['delta'])}` 到 ==`{S['next_pos']}`==（红 = forbidden，黄 = x，绿 = 去过）"
    return '红 = forbidden，黄 = x，绿 = 已用右跳到过的位置'


CONFIG = dict(
    num=1654, title='到家的最少跳跃次数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='bfs · 状态带上一步方向 · 限定右边界',
    tags=['图论算法', '动态规划'],
    code='''
class Solution(object):
    def minimumJumps(self, forbidden, a, b, x):

        if x == 0:
            return 0

        forbidden_pos = set(forbidden)

        if a >= b:
            right_boundary = x + b
        else:
            right_boundary = max(forbidden) + a + b

        q = [[0, 2]]
        d = [a, -b]
        l = 0
        r = 1
        used = set([0])
        step = 0
        while l < r:
            step += 1
            for now_pos, last_direct in q[l : r]:
                for index, delta in enumerate(d[:last_direct]):
                    next_pos = now_pos + delta
                    if next_pos == x:
                        return step
                    if next_pos >= 0 and next_pos <= right_boundary and next_pos not in forbidden_pos and (delta < 0 or next_pos not in used):
                        if index == 0:
                            used.add(next_pos)
                        q.append([next_pos, 2 - index])

            l, r = r, len(q)

        return -1
''',
    call='Solution().minimumJumps([5], 2, 3, 3)',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=_line, pointers={'now_pos': 'blue', 'x': 'yellow'}, color=_color, label='数轴位置 0 ~ right_boundary', h=170),
        dict(type='queue', var='q', fmt=lambda p: f'{p[0]}{"←" if p[1] == 1 else ""}', label='队列 q（位置，带 ← 表示刚向左跳，不能再左跳）', h=170),
    ],
    watch=[('step', 'step', 'yellow'), 'now_pos', 'delta', 'next_pos', ('right_boundary', 'right_boundary', 'pink'), ('x', 'x', 'green')],
    max_steps=64,
    captions={
        'if x == 0': '`x = {x}`，不是 0，需要跳；（`x = 0` 时本来就在家，直接返回 0）',
        'forbidden_pos = set': '把 `forbidden` 放进集合，判断是否禁止 O(1)',
        'if a >= b': lambda S, B, r: ('`a >= b`：每个「右跳 + 左跳」组合都不会往回走，越跳越靠右' if S.a >= S.b else '`a < b`：右跳加左跳可以净向左，所以可能先跳很远再退回来'),
        'right_boundary = x + b': '`a >= b`：位置超过 `x + b` 就回不来了，右边界 = ==`{right_boundary}`==',
        'right_boundary = max': '`a < b`：位置不小于 `max(forbidden) + b + 1` 后左跳不会踩禁点；边界 = `{max(forbidden)} + {a} + {b}` = ==`{right_boundary}`==',
        'q = [[0, 2]]': '队列元素 `[位置, 上一步方向]`：2 表示起点，左右都能跳',
        'd = [a, -b]': '`d[0] = a` 右跳，`d[1] = -b` 左跳',
        'used = set': '`used` 只记录右跳到达的位置',
        'step += 1': '新的一层：再多跳一次，现在是第 ==`{step}`== 跳',
        'for index, delta': lambda S, B, r: (f'`d[:{S.last_direct}]`：' + ('上一步是右跳，左右都能跳' if S.last_direct == 2 else '上一步是左跳，只能右跳') + f'；现在 `delta = {S.delta}`'
                                             if B.get('delta') != S.get('delta') or 'delta' not in B else '这个位置的跳法枚举完了'),
        'next_pos = now_pos + delta': '`next_pos = {now_pos} + ({delta}) = {next_pos}`',
        'if next_pos == x': lambda S, B, r: (f'`next_pos = {S.next_pos}` 就是 `x` → 答案 ==`step = {S.step}`==' if S.next_pos == S.x
                                             else f'`next_pos = {S.next_pos}` 不是 `x = {S.x}`'),
        'if next_pos >= 0': lambda S, B, r: ((f'`{S.next_pos}` 在 0~{S.right_boundary}、不是禁点、' + ('左跳不用去重' if S.delta < 0 else '右跳也没来过') + ' → 入队')
                                             if (0 <= S.next_pos <= S.right_boundary and S.next_pos not in S.forbidden_pos and (S.delta < 0 or S.next_pos not in B.used))
                                             else f'`{S.next_pos}` 越界、是禁点或右跳重复 → 不入队'),
        'if index == 0': '只有右跳（`index == 0`）才记入 `used`',
        'used.add': '`used` 加入 `{next_pos}`',
        'q.append': '入队 `[{next_pos}, {2 - index}]`：{"右跳到的，下一步左右都行" if index == 0 else "左跳到的，下一步只能右跳"}',
        'l, r = r, len(q)': '这一层处理完，新一层是 `q[{l}:{r}]`',
        'return step': '返回 ==`{step}`==',
        'return -1': '队列空了仍到不了 → `-1`',
    },
    cards=dict(
        one_liner='bfs 的状态 = 位置 + 上一步方向，右边界靠推导确定',
        complexity='时间 `O(right_boundary)`，空间 `O(right_boundary)`',
        problem=['从 `0` 出发，每次右跳 `a` 或左跳 `b`，不能连续左跳，不能到负数或 `forbidden`',
                 '求到达 `x` 的最少跳数，到不了返回 `-1`',
                 '本视频：`forbidden=[5], a=2, b=3, x=3` → `4`（如 0 → 2 → 4 → 1 → 3）'],
        quote='若当前位置now大于某个right_boundary时，就再也不可能跳到x上来了。很明显，x + b就是一个right_boundary。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a >= b` 时每个「右跳 + 左跳」只会往右走，边界取 `x + b`',
              '`a < b` 时可以净向左，边界取 `max(forbidden) + a + b`',
              '右跳位置去重；左跳位置不进 `used`，因为从那里不能再左跳，状态不同'],
        summary=['时间、空间都是 `O(right_boundary)`',
                 '易错点：不能连续左跳，所以队列里要带上一步方向',
                 '易错点：左跳到的位置不能进 `used`，否则会漏掉「右跳后再左跳」的状态',
                 '`x == 0` 要先单独返回 0；`a < b` 时 `max(forbidden)` 要求 `forbidden` 非空（题目保证）'],
    ),
)
