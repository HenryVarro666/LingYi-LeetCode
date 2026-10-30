def _bars(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    br = S['brackets']
    income = S['income']
    cv.text((x0 + 18, y0 + 4), f'数轴：收入 {income}，每一档只收「上一档上限 → 本档上限」这一段', 24, T['muted'], bold=True)
    top_v = max(b[0] for b in br)
    left, right = x0 + 40, x1 - 40
    sc = (right - left) / top_v
    y = y0 + 150
    live = 'last' in S
    last = S['last'] if live else 0
    cur = S.get('upper') if live else None
    cv.line([(left, y), (right, y)], T['border'], 3)
    prev = 0
    for k, (u, p) in enumerate(br):
        xa, xb = left + prev * sc, left + u * sc
        taxed_hi = min(u, income)
        done = live and u <= last
        is_cur = live and u == cur
        col = T['green'] if done else (T['yellow'] if is_cur else T['dim'])
        cv.rect((xa + 2, y - 46, xb - 2, y - 6), fill=col, alpha=150 if (done or is_cur) else 70, r=4)
        cv.text(((xa + xb) / 2, y - 26), f'{p}%', 24, T['text'], anchor='mm', bold=True)
        cv.text((xb, y + 12), u, 22, T['muted'], anchor='mt', mono=True)
        prev = u
    cv.text((left, y + 12), 0, 22, T['muted'], anchor='mt', mono=True)
    xi = left + income * sc
    cv.line([(xi, y - 80), (xi, y + 8)], T['pink'], 4)
    cv.text((xi, y - 88), f'income = {income}', 24, T['pink'], anchor='mb', bold=True)
    if live:
        xl = left + last * sc
        cv.tri_up(xl, y + 58, 10, T['blue'])
        cv.text((xl, y + 74), f'last = {last}', 22, T['blue'], anchor='mt', bold=True)


def _tax(S):
    if 'upper' not in S or 'res' not in S:
        return ''
    return f"累计税款 `res` = =={round(S['res'], 4)}=="


CONFIG = dict(
    num=2303, title='计算应缴税款总额', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · last 记上一档上限',
    tags=[],
    code='''
class Solution(object):
    def calculateTax(self, brackets, income):

        last = 0
        res = 0
        for upper, percent in brackets:
            if income > upper:
                res += (upper - last) * percent / 100.0
            else:
                res += (income - last) * percent / 100.0
                break
        
            last = upper

        return res
''',
    call='Solution().calculateTax([[3,50],[7,10],[12,25]], 10)',
    expect=2.65,
    views=[
        dict(type='custom', draw=_bars, h=330),
        dict(type='text', fn=_tax, size=34, h=90),
    ],
    watch=[('last', 'last', 'blue'), ('upper', 'upper', 'yellow'), ('percent', 'percent', 'cyan'), ('res', 'res', 'green')],
    captions={
        'last = 0': '`last` 记上一档的上限，第一档从 0 开始',
        'res = 0': '`res` 累计税款',
        'for upper, percent': '看这一档：上限 `{upper}`，税率 `{percent}%`',
        'if income > upper': lambda S, B, r: (f"`income = {S.income} > upper = {S.upper}`：收入越过了这一档 → ==整档都要交=="
                                               if S.income > S.upper else f"`income = {S.income} ≤ upper = {S.upper}`：收入停在这一档里 → ==只交到 income=="),
        'res += (upper - last)': '整档：`({upper} − {last}) × {percent}% = {(upper - last) * percent / 100.0}`，`res` → =={res}==',
        'res += (income - last)': '最后一档，只交到 income：`({income} − {last}) × {percent}% = {(income - last) * percent / 100.0}`，`res` → =={res}==',
        'break': '收入已经算完，后面的档位不用看了',
        'last = upper': '这一档交完，`last` 移到 `{upper}`，下一档从这里开始',
        'return res': '应缴税款总额 `{res}`',
    },
    cards=dict(
        one_liner='每个税级只收“上一档上限到本档上限”那一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`brackets[i] = [上限, 税率%]`，按上限递增；每一档只对落在这一档区间内的收入按该税率收税',
                 '给定总收入 `income`，求总税款',
                 '示例：`[[3,50],[7,10],[12,25]]`，`income=10` → `2.65`'],
        quote='使用一个变量last记录上一个税级上限，然后一趟遍历。若总收入大于当前遍历到的税级上限，那么就根据当前税级上限与last之差来计算税额并累加至答案，否则根据总收入与last之差计算税额，累加至答案后直接返回。',
        quote_src='—— yiduobo 题解原文',
        idea=['`last` = 上一档上限，本档收入段长度 = `upper − last`',
              '收入大于本档上限：整段都交，然后 `last = upper`',
              '否则只交 `income − last` 这一段，直接 `break`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：税率是 `percent / 100`，要用浮点数；原文写成 `/ 100.0`',
                 '易错：收入 ≤ 上限时是 `income − last`，别写成 `upper − last`',
                 '原文 `/ 100.0` 本身就是浮点除法，Python 3 下不用改，代码未改动'],
    ),
)
