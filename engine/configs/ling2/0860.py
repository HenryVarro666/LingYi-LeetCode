BILLS = [5, 5, 5, 10, 20, 5, 5, 20]

# 只用于可视化：让列表记住 for 循环走到了第几位顾客（代码本身不变）
SETUP = '''
class TLSnap(list):
    pos = -1

class TL(list):
    pos = -1
    def __iter__(self):
        for i in range(len(self)):
            self.pos = i
            yield list.__getitem__(self, i)
    def __deepcopy__(self, memo):
        snap = TLSnap(list.__iter__(self))
        snap.pos = self.pos
        return snap
'''

CODE = '''
class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        five = ten = 0
        for b in bills:
            if b == 5:  # 无需找零
                five += 1
            elif b == 10:  # 返还 5
                five -= 1
                ten += 1
            elif ten > 0:  # 此时 b=20，优先用 10 美元，返还 10+5
                five -= 1
                ten -= 1
            else:  # 此时 b=20，返还 5+5+5
                five -= 3
            if five < 0:  # 无法正确找零
                return False
        return True
'''
_LINES = CODE.strip('\n').split('\n')
FIVE_M1 = [i + 1 for i, s in enumerate(_LINES) if 'five -= 1' in s]       # [10 美元分支, 20 美元分支]


def _pos(S):
    p = getattr(S.get('bills'), 'pos', -1)
    return p if isinstance(p, int) and p >= 0 else None


def _bill(cv, x, y, val, T, w=78, h=44):
    c = {5: T['green'], 10: T['blue'], 20: T['purple']}[val]
    cv.rect((x, y, x + w, y + h), fill=c, r=8, outline=T['bg'], width=2)
    cv.text((x + w / 2, y + h / 2), f'${val}', 22, T['bg'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '钱箱（20 美元不能用来找零，不用统计）', 24, T['muted'], bold=True)
    five, ten = S.get('five'), S.get('ten')
    if five is None:
        cv.text((x0 + 40, y0 + 60), '（尚未开张）', 24, T['dim'])
        return
    for row, (name, cnt, val, bc) in enumerate((('five', five, 5, B.get('five')), ('ten', ten, 10, B.get('ten')))):
        y = y0 + 56 + row * 96
        changed = bc is not None and bc != cnt
        cv.text((x0 + 40, y + 22), f'{name} = {cnt}', 30, T['red'] if cnt < 0 else (T['yellow'] if changed else T['text']),
                anchor='lm', bold=True, mono=True)
        for k in range(max(0, cnt)):
            _bill(cv, x0 + 250 + k * 88, y, val, T)
        if cnt < 0:
            cv.text((x0 + 250, y + 22), f'欠 {-cnt} 张 → 找不开！', 28, T['red'], anchor='lm', bold=True)


def _cap_for(S, B, ret):
    p = _pos(S)
    if 'b' in B and B.get('b') is not None and _pos(B) == p:
        return '所有顾客都处理完了'
    return f'第 `{p}` 位顾客付了 `{S.b}` 美元'


def _cap_ten(S, B, ret):
    if S.b == 10:
        return '付 10 美元：要==返还 5=='
    return '`b = 20`：要返还 15'


def _cap_t(S, B, ret):
    if S.ten > 0:
        return f'手里有 `ten = {S.ten}` 张 10 美元 → ==优先用 10==（10 只能给 20 找零，5 更通用）'
    return '手里没有 10 美元 → 只能返还 5+5+5'


CONFIG = dict(
    num=860, title='柠檬水找零', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='分类讨论 · 优先用 10 美元找零',
    tags=['字节30天'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().lemonadeChange(TL({BILLS}))',
    expect=True,
    views=[
        dict(type='array', var=lambda S: list(list.__iter__(S['bills'])) if 'bills' in S else BILLS,
             label='bills（顾客按顺序付款，蓝 = 当前顾客）', cell=96,
             pointers={_pos: 'blue'}, pointer_labels={_pos: 'b'},
             color=lambda S, i, v: {5: 'green', 10: 'blue', 20: 'purple'}[v] if _pos(S) is not None and i == _pos(S) else None,
             dim=lambda S, i, v: _pos(S) is not None and i < _pos(S)),
        dict(type='custom', draw=_draw, h=260),
        dict(type='text', fn=lambda S: '找零规则：`5` 不找；`10` 找 5；`20` ==先试 10+5==，不行再 5+5+5', h=60, size=26),
    ],
    watch=[('b', 'b', 'blue'), ('five', 'five', 'green'), ('ten', 'ten', 'cyan')],
    captions={
        'five = ten = 0': '一开始手里==没有零钱==：`five = ten = 0`',
        'for b in bills': _cap_for,
        'if b == 5': lambda S, B, ret: ('付 5 美元：==无需找零==' if S.b == 5 else f'`b = {S.b}`，不是 5'),
        'five += 1': '收下 5 美元：`five` → {five}',
        'elif b == 10': _cap_ten,
        FIVE_M1[0]: '返还 5：`five` → {five}',
        'ten += 1': '收下 10 美元：`ten` → {ten}',
        'elif ten > 0': _cap_t,
        FIVE_M1[1]: '返还 10 + 5：先用掉一张 5，`five` → {five}',
        'ten -= 1': '再用掉一张 10，`ten` → {ten}',
        'five -= 3': '返还 5+5+5：`five` → {five}',
        'if five < 0': lambda S, B, ret: ('`five < 0`：5 美元不够了 → ==无法正确找零==' if S.five < 0
                                          else f'`five = {S.five} ≥ 0`：这位顾客找零成功'),
        'return False': '返回 `False`',
        'return True': '中途没有返回 False → 每位顾客都找零成功，返回 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='10 美元只能给 20 找零，5 美元更通用 → 能用 10 就先用 10',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['柠檬水 5 美元一杯，顾客按顺序付 `5`、`10` 或 `20` 美元，一开始没有零钱',
                 '能否给每位顾客正确找零？',
                 '示例：`[5,5,5,10,20]` → `true`；`[5,5,10,10,20]` → `false`',
                 '本视频：`[5,5,5,10,20,5,5,20]` → `true`'],
        quote='10 美元钞票只能用于 20 美元的找零，而 5 美元钞票既可以用于 20 美元的找零，又可以用于 10 美元的找零，==更加通用==……所以如果可以用 10 美元，应当优先用 10 美元。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`five`、`ten` 记录手里 5、10 美元的张数',
              '`b = 5`：`five + 1`；`b = 10`：`five − 1`，`ten + 1`',
              '`b = 20`：有 10 就 `five − 1`、`ten − 1`，否则 `five − 3`',
              '简洁写法：先扣钱，==统一判断== `five < 0` 就返回 False'],
        result='每位顾客都找开了 → `True` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '贪心：20 美元优先返还 10+5；若先用 5+5+5，之后来 10 美元可能找不开',
                 '简洁之处：`b = 10` 时不先判断 `five > 0`，扣完再统一看 `five < 0`',
                 '`ten` 不会变负：只在 `ten > 0` 时才减'],
    ),
)
