BILLS = [5, 5, 5, 10, 20, 10, 20]

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
class Solution(object):
    def lemonadeChange(self, bills):
        cnt5 = cnt10 = 0
        for bill in bills:
            if bill == 5:
                cnt5 += 1
            elif bill == 10:
                if cnt5 == 0:
                    return False
                cnt5 -= 1
                cnt10 += 1
            else:
                if cnt10 > 0 and cnt5 > 0:
                    cnt10 -= 1
                    cnt5 -= 1
                elif cnt5 >= 3:
                    cnt5 -= 3
                else:
                    return False

        return True
'''
_LINES = CODE.strip('\n').split('\n')
CNT5_M1 = [i + 1 for i, s in enumerate(_LINES) if 'cnt5 -= 1' in s]      # [10 美元分支, 20 美元分支]
RET_F = [i + 1 for i, s in enumerate(_LINES) if 'return False' in s]
L_IF20 = [i + 1 for i, s in enumerate(_LINES) if 'if cnt10 > 0 and cnt5 > 0' in s][0]


def _pos(S):
    p = getattr(S.get('bills'), 'pos', -1)
    return p if isinstance(p, int) and p >= 0 else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '手里的零钱', 24, T['muted'], bold=True)
    c5, c10 = S.get('cnt5'), S.get('cnt10')
    if c5 is None:
        return
    for row, (name, cnt, val, col, bc) in enumerate((('cnt5', c5, 5, T['green'], B.get('cnt5')),
                                                      ('cnt10', c10, 10, T['blue'], B.get('cnt10')))):
        y = y0 + 52 + row * 92
        changed = bc is not None and bc != cnt
        cv.text((x0 + 40, y + 22), f'{name} = {cnt}', 30, T['yellow'] if changed else T['text'], anchor='lm', bold=True, mono=True)
        for k in range(cnt):
            X = x0 + 270 + k * 88
            cv.rect((X, y, X + 78, y + 44), fill=col, r=8)
            cv.text((X + 39, y + 22), f'${val}', 22, T['bg'], anchor='mm', bold=True)
    # 当前这张 20 / 10 需要的组合（只在判断那几行显示，用判断时的值）
    b = S.get('bill')
    ln = S.get('_line', 0)
    b5, b10 = B.get('cnt5'), B.get('cnt10')
    if b == 20 and ln in (L_IF20, L_IF20 + 3, RET_F[1]) and b5 is not None:
        ok1 = b10 > 0 and b5 > 0
        ok2 = b5 >= 3
        cv.rich(x0 + 40, y0 + 236, '找 15：`10+5` 需要 `cnt10>0 且 cnt5>0` → ' + ('==可以==' if ok1 else '不行'), x1 - x0 - 60, size=24)
        if not ok1:
            cv.rich(x0 + 40, y0 + 280, '　　　 `5+5+5` 需要 `cnt5 ≥ 3` → ' + ('==可以==' if ok2 else '不行'), x1 - x0 - 60, size=24)
    elif b == 10 and ln in (L_IF20 - 5, RET_F[0]) and b5 is not None:
        cv.rich(x0 + 40, y0 + 236, '找 5：需要 `cnt5 > 0` → ' + ('==可以==' if b5 > 0 else '不行'), x1 - x0 - 60, size=24)


def _cap_for(S, B, ret):
    p = _pos(S)
    if B.get('bill') is not None and _pos(B) == p:
        return '所有顾客都处理完了'
    return f'第 `{p}` 位顾客付 `{S.bill}` 美元'


def _cap20(S, B, ret):
    c5, c10 = S.cnt5, S.cnt10
    if c10 > 0 and c5 > 0:
        return f'付 20：先试 ==10+5==（`cnt10 = {c10}`，`cnt5 = {c5}`）→ 可以'
    if c10 > 0:
        return f'付 20：有 10 美元，但 `cnt5 = 0`，==凑不出 10+5==；再试 5+5+5'
    return '付 20：没有 10 美元 → 试 5+5+5'


CONFIG = dict(
    num=860, title='柠檬水找零', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='贪心：先找 10+5，再找 5+5+5',
    tags=['字节30天'],
    code=CODE,
    setup=SETUP,
    call=f'Solution().lemonadeChange(TL({BILLS}))',
    expect=False,
    views=[
        dict(type='array', var=lambda S: list(list.__iter__(S['bills'])) if 'bills' in S else BILLS,
             label='bills（蓝箭头 = 当前顾客）', cell=96, pointers={_pos: 'blue'}, pointer_labels={_pos: 'bill'},
             color=lambda S, i, v: {5: 'green', 10: 'blue', 20: 'purple'}[v] if _pos(S) is not None and i == _pos(S) else None,
             dim=lambda S, i, v: _pos(S) is not None and i < _pos(S)),
        dict(type='custom', draw=_draw, h=340),
    ],
    watch=[('bill', 'bill', 'blue'), ('cnt5', 'cnt5', 'green'), ('cnt10', 'cnt10', 'cyan')],
    captions={
        'cnt5 = cnt10 = 0': '两个变量分别统计手上 5 块和 10 块的数量，开始都是 0',
        'for bill in bills': _cap_for,
        'if bill == 5': lambda S, B, ret: ('付 5 块：不用找零' if S.bill == 5 else f'`bill = {S.bill}`，要找零'),
        'cnt5 += 1': '`cnt5` → {cnt5}',
        'elif bill == 10': lambda S, B, ret: ('付 10 块：==只有找 5 块这一种选择==' if S.bill == 10 else '付 20 块'),
        'if cnt5 == 0': lambda S, B, ret: ('一张 5 块都没有 → 找不开' if S.cnt5 == 0 else f'`cnt5 = {S.cnt5}`，找得开'),
        CNT5_M1[0]: '找出一张 5 块：`cnt5` → {cnt5}',
        'cnt10 += 1': '收下 10 块：`cnt10` → {cnt10}',
        'if cnt10 > 0 and cnt5 > 0': _cap20,
        'cnt10 -= 1': '找出一张 10 块：`cnt10` → {cnt10}',
        CNT5_M1[1]: '再找出一张 5 块：`cnt5` → {cnt5}',
        'elif cnt5 >= 3': lambda S, B, ret: (f'`cnt5 = {S.cnt5} ≥ 3` → 找 5+5+5' if S.cnt5 >= 3
                                             else f'`cnt5 = {S.cnt5} < 3`：5+5+5 也凑不出'),
        'cnt5 -= 3': '找出三张 5 块：`cnt5` → {cnt5}',
        RET_F[0]: '无法找零 → 返回 `False`',
        RET_F[1]: '两种组合都凑不出 15 → ==无法找零==，返回 `False`',
        'return True': '每位顾客都找零成功 → 返回 `True`',
    },
    max_steps=60,
    cards=dict(
        one_liner='手握两张 5 块总比一张 10 块好：20 块先找 10+5，不行再找 5+5+5',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['柠檬水 5 美元一杯，顾客依次付 `5`、`10` 或 `20` 美元，开始时没有零钱',
                 '能否给每位顾客正确找零？',
                 '示例：`[5,5,5,10,20]` → `true`',
                 '本视频：`[5,5,5,10,20,10,20]` → `false`'],
        quote='对于20块而言，可以明确的是在任何情况下，==手握两张5块都是比只有一张10块更好的选择==，因此应该首先尝试找零10+5的组合，如果不行再尝试5+5+5的组合。',
        quote_src='—— yiduobo 题解',
        idea=['面值只有 5、10、20，只需考虑给 10 块和 20 块找零',
              '10 块：只能找 5 块；没有 5 块就失败',
              '20 块：先试 10+5，再试 5+5+5；都不行就失败'],
        result='最后一位顾客的 20 块：有 10 没有 5，也凑不出 5+5+5 → `False` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：10+5 要同时满足 `cnt10 > 0` ==且== `cnt5 > 0`',
                 '对比灵神：yiduobo 先判断够不够再找零；灵神先扣钱，再统一判断 `five < 0`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
