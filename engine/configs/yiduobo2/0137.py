import math

NUMS = [2, 2, 3, 2]
BITS = 2

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''

NAMES = ['模3余0', '模3余1', '模3余2']
SUB = ['(0,0)', '(1,0)', '(0,1)']


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _state(once, twice, j):
    o, t = once >> j & 1, twice >> j & 1
    return 1 if o else (2 if t else 0)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    once, twice = S.get('once'), S.get('twice')
    if once is None or twice is None:
        cv.text((x0 + 18, y0 + 4), '每一位都是一个三状态自动机：来一个 1 就往下走一格', 24, T['muted'], bold=True)
        return
    line = S.get('_line')
    num = S.get('num') if _k(S) is not None else None
    nxt = None
    if line == 8 and num is not None:
        nxt = (S['next_once'], S['next_twice'])
    cv.text((x0 + 18, y0 + 4), '每一位一个三状态自动机，括号里是 (once, twice) 这一位的值；来 1 走一格', 23, T['muted'], bold=True)
    W = (x1 - x0) / BITS
    for col, j in enumerate(range(BITS - 1, -1, -1)):
        cx = x0 + W * col + W / 2
        cy = y0 + 252
        R = 120
        pos = [(cx, cy - R), (cx + R * math.cos(math.pi / 6), cy + R * 0.5), (cx - R * math.cos(math.pi / 6), cy + R * 0.5)]
        cur = _state(once, twice, j)
        nb = num >> j & 1 if num is not None else None
        head = f'第 {j} 位' + (f'：num 这一位 = {nb}' if nb is not None else '')
        cv.text((cx, y0 + 52), head, 24, T['blue'] if nb else T['text'], anchor='mt', bold=True)
        tgt = _state(nxt[0], nxt[1], j) if nxt else None
        for s in range(3):
            p0, p1 = pos[s], pos[(s + 1) % 3]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            hot = tgt is not None and s == cur and tgt != cur
            cv.arrow((p0[0] + ux * 48, p0[1] + uy * 48), (p1[0] - ux * 50, p1[1] - uy * 50),
                     T['yellow'] if hot else T['border'], width=5 if hot else 3, head=16 if hot else 12)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            ox, oy = -uy * 22, ux * 22
            cv.text((mx - ox, my - oy), '1', 20, T['yellow'] if hot else T['muted'], anchor='mm', bold=True)
        for s in range(3):
            X, Y = pos[s]
            on = s == cur
            fill = T['green'] if on else T['panel2']
            outline = T['yellow'] if (tgt is not None and s == tgt) else T['border']
            cv.d.ellipse((X - 44, Y - 44, X + 44, Y + 44), fill=fill, outline=outline, width=5 if outline == T['yellow'] else 2)
            cv.text((X, Y - 8), NAMES[s], 20, T['bg'] if on else T['text'], anchor='mm', bold=True)
            cv.text((X, Y + 18), SUB[s], 18, T['bg'] if on else T['muted'], anchor='mm')
        if tgt is not None:
            msg = '不变（来的是 0）' if tgt == cur else f'{NAMES[cur]} → {NAMES[tgt]}'
            cv.text((cx, cy + R * 0.5 + 64), msg, 22, T['yellow'], anchor='mt', bold=True)


def _bits(v):
    return format(v & ((1 << BITS) - 1), f'0{BITS}b')


def _cap_next_once(S, B, ret):
    return (f'`next_once = ~twice & (once ^ num)` = `~{_bits(S.twice)} & ({_bits(S.once)} ^ {_bits(S.num)})` = =={_bits(S.next_once)}=='
            + ('：余 0 来 1、或余 1 来 0 时为 1' if _k(S) == 0 else ''))


def _cap_next_twice(S, B, ret):
    moves = []
    for j in range(BITS - 1, -1, -1):
        a, b = _state(S.once, S.twice, j), _state(S.next_once, S.next_twice, j)
        moves.append(f'第{j}位 ' + (f'{NAMES[a][-2:]}→{NAMES[b][-2:]}' if a != b else '不变'))
    return f'`next_twice = (once ^ twice) & (twice ^ num)` = =={_bits(S.next_twice)}==：' + '，'.join(moves)


CONFIG = dict(
    num=137, title='只出现一次的数字 II', difficulty='Medium', category='技巧',
    author='yiduobo', technique='位运算 + 自动机 · once / twice',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def singleNumber(self, nums):
        once = 0
        twice = 0

        for num in nums:
            next_once = ~twice & (once ^ num)
            next_twice = (once ^ twice) & (twice ^ num)
            once = next_once
            twice = next_twice

        return once
''',
    setup=TRACK,
    call=f'Solution().singleNumber(TList({NUMS}))',
    expect=3,
    skip=['once = next_once'],
    views=[
        dict(type='array', var=lambda S: [f'{v}={v:02b}' for v in S['nums']] if 'nums' in S else None,
             label='nums（二进制）', cell=110, h=215, pointers={_k: 'blue'}, pointer_labels={_k: 'num'},
             dim=lambda S, i, v: _k(S) is not None and i < _k(S) or (_k(S) is None and 'once' in S and S.get('_line') == 12)),
        dict(type='custom', draw=_draw, h=415),
    ],
    watch=[('num', 'num', 'blue'), ('once', 'once', 'green'), ('twice', 'twice', 'purple'),
           ('next_once', 'next_once'), ('next_twice', 'next_twice')],
    captions={
        'once = 0': '`once` 的第 i 位为 1：第 i 位上 1 的个数==模 3 余 1==',
        'twice = 0': '`twice` 的第 i 位为 1：第 i 位上 1 的个数==模 3 余 2==；都为 0 表示余 0',
        'for num in nums': lambda S, B, ret: (f'新来 `num = {S.num}`（二进制 `{S.num:02b}`）：每一位按自动机转移一步'
                                              if _k(S) is not None else '所有数处理完：出现 3 次的数在每一位上都转回了「余 0」'),
        'twice = next_twice': '`once = {once:02b}`、`twice = {twice:02b}`：状态转移完成（都用旧值算好再赋值）',
        'next_once = ': _cap_next_once,
        'next_twice = ': _cap_next_twice,
        'return once': '每一位要么余 0 要么余 1，余 1 的位就是答案的 1 → 返回 `once` = =={ret}==',
    },
    cards=dict(
        one_liner='每一位的 1 的个数模 3 只有三种状态，用 once / twice 两个变量做自动机',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `nums` 中，除某个元素只出现==一次==外，其余每个元素都恰好出现==三次==',
                 '找出只出现一次的元素；要求==线性时间、常数空间==',
                 '示例：`[2,2,3,2]` → `3`'],
        quote='将每一位上1出现的次数归到三种状态中，分别为模3等于0，模3等于1以及模3等于2。==对于每个新来的1，这个状态都会往下一个状态移动==。',
        quote_src='—— yiduobo 题解',
        idea=['二进制 `[10],[10],[11],[10]`：第 1 位有 4 个 1，第 0 位有 1 个 1',
              '各自模 3 都剩 1 → 答案 `[11]` = 3',
              '用 `once`、`twice` 两个变量的每一位记录这一位处于哪个状态'],
        after=[dict(heading='转移公式怎么来的？列出 6 种情况', lines=[
            '`(once, twice, x)`：`(0,0,1)→(1,0)`，`(1,0,1)→(0,1)`，`(0,1,1)→(0,0)`；`x = 0` 时不变',
            '`next_once = 1`：`(0,0,1)` 或 `(1,0,0)` → `~twice & (once ^ x)`',
            '`next_twice = 1`：`(1,0,1)` 或 `(0,1,0)` → `(once ^ twice) & (twice ^ x)`',
            '同样的方法可以解决出现 5 次、7 次……只需设计更多状态'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '要先用旧值算出 `next_once`、`next_twice`，再一起赋值',
                 '原文提到：若用 zero/once 表示，zero 初值要全 1，边界麻烦，所以选 once/twice',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改',
                 '对比灵神：灵神先算 b 再用新 b 算 a，省掉了临时变量'],
    ),
)
