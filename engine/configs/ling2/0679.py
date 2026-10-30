import sys as _sys

CARDS = [1, 2, 3, 4]


def _g(v):
    if isinstance(v, float):
        return f'{v:.3g}' if abs(v - round(v)) > 1e-9 else str(int(round(v)))
    return str(v)


def _frames():
    f = _sys._getframe(1)
    for _ in range(12):
        if f is None:
            return []
        st = f.f_locals.get('st')
        if isinstance(st, dict) and '_frames' in st:
            return st['_frames']
        f = f.f_back
    return []


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    frames = [fr for fr in _frames() if fr['name'] == 'judgePoint24']
    cv.text((x0 + 18, y0 + 4), '每层递归的牌（蓝 = x，粉 = y，绿 = 合并出的新牌）', 24, T['muted'], bold=True)
    rowh = 128
    for d, fr in enumerate(frames):
        L = fr['locals']
        cards = L.get('cards') or []
        i, j = L.get('i'), L.get('j')
        last = d == len(frames) - 1
        Y = y0 + 44 + d * rowh
        cv.text((x0 + 22, Y + 30), f'{len(cards)} 张', 22, T['yellow'] if last else T['muted'], anchor='lm', bold=True)
        cw = 78
        for k, v in enumerate(cards):
            X = x0 + 90 + k * (cw + 10)
            c = T['blue'] if k == i else (T['pink'] if k == j else T['panel2'])
            cv.rect((X, Y, X + cw, Y + 60), fill=c, r=10, outline=T['yellow'] if last else T['border'], width=2 if last else 1)
            s = _g(v)
            cv.text((X + cw / 2, Y + 30), s, 30 if len(s) < 4 else 22, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True)
        cand = L.get('candidates')
        res = L.get('res')
        if cand is not None and i is not None and j is not None:
            cx = x0 + 90 + 4 * (cw + 10) + 10
            cv.text((cx, Y + 4), f'{_g(L["x"])} 和 {_g(L["y"])} 的结果：', 20, T['muted'])
            xx = cx
            for v in cand:
                s = _g(v)
                w = cv.tlen(s, 22, mono=True) + 16
                on = res is not None and L.get('new_cards') is not None and abs(v - res) < 1e-12 and (d < len(frames) - 1 or S.get('_line') in (24, 25))
                cv.rect((xx, Y + 32, xx + w, Y + 62), fill=T['green'] if on else T['panel2'], r=6)
                cv.text((xx + w / 2, Y + 47), s, 22, T['bg'] if on else T['text'], anchor='mm', mono=True)
                xx += w + 6
        if d < len(frames) - 1:
            cv.text((x0 + 60, Y + 92), '↓ 递归', 20, T['dim'], anchor='lm')


def _cap_n1(S, B, ret):
    if S.n == 1:
        return f'只剩一张牌 `{_g(S.cards[0])}`：看它是不是 24'
    return f'有 `{S.n}` 张牌 `{[_g(v) for v in S.cards]}`：还要继续选两张合并'.replace("'", '')


def _cap_ret1(S, B, ret):
    v = _g(S.cards[0])
    return f'`|{v} − 24| < EPS` → ==True==，凑出 24 了！' if ret else f'`{v} ≠ 24` → False，回到上一层换个结果'


def _cap_res(S, B, ret):
    if B.get('res') == S.get('res') and 'res' in B and B.get('new_cards') == S.get('new_cards'):
        return '六种结果都试过了，换下一对牌'
    return f'试第 {S.candidates.index(S.res) + 1} 种结果：`res = {_g(S.res)}`'


CONFIG = dict(
    num=679, title='24 点游戏', difficulty='Hard', category='回溯',
    author='灵茶山艾府', technique='每次合并两张牌，递归',
    tags=['字节30天'],
    code='''
from typing import Union
EPS = 1e-9

class Solution:
    def judgePoint24(self, cards: List[Union[int, float]]) -> bool:
        n = len(cards)
        if n == 1:
            return abs(cards[0] - 24) < EPS

        # 选两张牌 x=cards[i] 和 y=cards[j]
        for i, x in enumerate(cards):
            for j in range(i + 1, n):
                y = cards[j]

                # 六种情况：加减乘除，其中减和除都有两种不同的顺序
                candidates = [x + y, x - y, y - x, x * y]
                if abs(y) > EPS:  # 保证分母不为 0
                    candidates.append(x / y)
                if abs(x) > EPS:  # 保证分母不为 0
                    candidates.append(y / x)

                new_cards = cards[:j] + cards[j + 1:]  # 删除 j
                for res in candidates:
                    new_cards[i] = res  # 覆盖 i
                    if self.judgePoint24(new_cards):
                        return True
        return False
''',
    call=f'Solution().judgePoint24({CARDS})',
    expect=True,
    skip=['n = len(cards)', 'y = cards[j]', 'if abs(y) > EPS', 'candidates.append', 'if abs(x) > EPS'],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green'), ('new_cards', 'new_cards')],
    captions={
        'if n == 1': _cap_n1,
        'return abs(cards[0] - 24)': _cap_ret1,
        'for i, x in enumerate': lambda S, B, r: f'第一张牌选 `x = cards[{S.i}] = {_g(S.x)}`',
        'for j in range(i + 1, n)': lambda S, B, r: f'第二张牌选 `y = cards[{S.j}] = {_g(S.cards[S.j])}`（`j > i`，避免重复选同一对）',
        'candidates = [': lambda S, B, r: (f'六种情况：`x+y, x−y, y−x, x·y` = `{", ".join(_g(v) for v in S.candidates)}`，'
                                           f'分母不为 0 时再加 `x/y`、`y/x`'),
        'new_cards = cards[:j]': lambda S, B, r: (f'删除第 j 张，剩下 `{", ".join(_g(v) for v in S.new_cards)}`；'
                                                  f'第 i 个位置一会儿放合并结果'),
        'for res in candidates': _cap_res,
        'new_cards[i] = res': lambda S, B, r: (f'用结果覆盖第 i 张：`new_cards = [{", ".join(_g(v) for v in S.new_cards)}]`，'
                                               f'少了一张牌'),
        'if self.judgePoint24': lambda S, B, r: f'用这 `{len(B.new_cards)}` 张牌==递归==：问题规模减一',
        'return True': '下一层凑出了 24 → 一路返回 ==True==',
        'return False': '所有组合都凑不出 24 → 返回 False',
    },
    cards=dict(
        one_liner='不管表达式长什么样，总能先算其中两个数：每次合并两张牌，递归到只剩一张',
        complexity='时间 `O(n! · 6^n)`，空间 `O(n^2)`（本题 n = 4）',
        problem=['给 4 张牌，每张是 `[1, 9]` 的数字',
                 '用 `+ − × /`（实数除法）和括号组成表达式，问能否==得到 24==',
                 '不能把数字拼在一起，`−` 不能当一元负号',
                 '示例：`[4,1,8,7]` → `true`：`(8−4) × (7−1)`；`[1,2,1,2]` → `false`'],
        quote='无论表达式是什么样的，我们总是可以==从中选两个数最先计算==。计算后，变成包含三个数字的表达式。同样地，这个表达式也可以从中选两个数最先计算，依此类推。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每次从剩余牌中取两张，算出结果，==合并成一张新牌==，牌数减一',
              '两数 x、y 至多六种结果：`x+y, x−y, y−x, x·y, x/y, y/x`（分母非 0）',
              '递归到只剩一张牌，判断它是否等于 24；浮点误差用 `EPS = 1e-9`'],
        result='`1 + 2 = 3`，`3 + 3 = 6`，`6 × 4 = 24` → `True`',
        summary=['时间 `O(n! · 6^n)`：每层选一对牌、六种结果；空间 `O(n^2)`',
                 '易错：除法要判分母非 0；实数比较要用 `abs(a − b) < EPS`',
                 '易错：减法、除法有两种顺序，都要试',
                 '原文还给了 `Fraction` 分数类写法，彻底避免浮点误差',
                 '为在本地运行，代码开头补了 `from typing import Union`（LeetCode 已预置）'],
    ),
)
