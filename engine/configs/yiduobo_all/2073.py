TICKETS = [2, 4, 3, 1, 5, 2]
K = 2

CODE = '''
class Solution(object):
    def timeRequiredToBuy(self, tickets, k):

        n = len(tickets)
        res = n * (tickets[k] - 1) + k + 1

        for index in range(k):
            if tickets[index] < tickets[k]:
                res -= tickets[k] - tickets[index]

        for index in range(k + 1, n):
            if tickets[index] < tickets[k] - 1:
                res -= tickets[k] - 1 - tickets[index]

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return [i + 1 for i, s in enumerate(_LINES) if sub in s][0]


L_FOR1, L_FOR2, L_RET = _ln('for index in range(k):'), _ln('for index in range(k + 1'), _ln('return res')


def _done(S, i):
    ln = S.get('_line')
    if 'res' not in S:
        return False
    if ln == L_RET or i == K:
        return True
    idx = S.get('index')
    if idx is None:
        return False
    if ln > L_FOR2 or ln == L_FOR2:
        if i < K:
            return True
    if i < idx:
        return True
    return i == idx and ln not in (L_FOR1, L_FOR2)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t = TICKETS
    n = len(t)
    tk = t[K]
    cv.text((x0 + 18, y0 + 4), '虚线格 = 先假设每人都买够的票；红 = 实际票不够、要从 res 减掉的', 24, T['muted'], bold=True)
    cell = min(150, (x1 - x0 - 200) / n)
    sx = x0 + 120 + ((x1 - x0 - 200) - cell * n) / 2
    base, top = y1 - 110, y0 + 80
    scale = (base - top) / max(tk, 1) / 1.15
    started = 'res' in S
    cur = S.get('index') if S.get('_line') not in (L_RET,) else None
    for i, v in enumerate(t):
        X = sx + i * cell
        cap = tk if i <= K else tk - 1
        bw = cell * 0.62
        bx0, bx1 = X + (cell - bw) / 2, X + (cell + bw) / 2
        done = _done(S, i)
        for u in range(cap):
            yb = base - u * scale
            r = (bx0, yb - scale + 3, bx1, yb - 1)
            if not started:
                continue
            if u < v:
                cv.rect(r, fill=T['orange'] if i == K else T['blue'], r=4)
            elif done:
                cv.rect(r, fill=T['red'], alpha=150, r=4)
                cv.text(((bx0 + bx1) / 2, yb - scale / 2), '−1', 22, T['bg'], anchor='mm', bold=True)
            else:
                cv.rect(r, outline=T['muted'], width=2, r=4)
        if started:
            cv.text((X + cell / 2, base - cap * scale - 6), f'需 {v}', 22, T['text'], anchor='mb', bold=True)
        col = T['orange'] if i == K else (T['yellow'] if (cur == i and S.get('_line') != L_RET) else T['dim'])
        cv.text((X + cell / 2, base + 8), f'i={i}', 20, col, anchor='mt', mono=True, bold=cur == i)
        if cur == i and S.get('_line') != L_RET:
            cv.tri_up(X + cell / 2, base + 40, 10, T['yellow'])
            cv.text((X + cell / 2, base + 56), 'index', 20, T['yellow'], anchor='mt', bold=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if started:
        yk = base - tk * scale
        yk1 = base - (tk - 1) * scale
        cv.dashed((sx, yk), (sx + (K + 1) * cell, yk), T['cyan'], 3)
        cv.text((sx - 8, yk), f'{tk} 轮', 22, T['cyan'], anchor='rm', bold=True)
        cv.dashed((sx + (K + 1) * cell, yk1), (sx + n * cell, yk1), T['pink'], 3)
        cv.text((sx + n * cell + 8, yk1), f'{tk - 1} 轮', 22, T['pink'], anchor='lm', bold=True)


def _if1(S, B, ret):
    i, a, b = S.index, S.tickets[S.index], S.tickets[K]
    if a < b:
        return f'第 {i} 人只要 `{a}` 张 < `{b}`：前面按 `{b}` 张算==多算了 {b - a} 秒=='
    return f'第 {i} 人要 `{a}` 张 ≥ `{b}`：第 k 人买完前他一直在排队，没多算'


def _if2(S, B, ret):
    i, a, b = S.index, S.tickets[S.index], S.tickets[K] - 1
    if a < b:
        return f'第 {i} 人只要 `{a}` 张 < `{b}`：在他后面按 `{b}` 张算==多算了 {b - a} 秒=='
    return f'第 {i} 人要 `{a}` 张 ≥ `tk-1 = {b}`：没多算'


CONFIG = dict(
    num=2073, title='买票需要的时间', difficulty='Easy', category='模拟',
    author='yiduobo', technique='先按票够多算，再减去差值',
    tags=['labuladong'],
    code=CODE,
    call=f'Solution().timeRequiredToBuy({TICKETS}, {K})',
    expect=13,
    views=[
        dict(type='array', var='tickets', label='tickets（橙 = 第 k 个人，黄 = 当前 index）', cell=90,
             color=lambda S, i, v: 'orange' if i == K else ('yellow' if S.get('index') == i and S.get('_line') != L_RET else None)),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('n', 'n'), ('tickets[k]', lambda S: S['tickets'][K], 'orange'), ('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len': '一共 `n = {n}` 个人',
        'res = n *': '假设大家票都够：先买满 `{tickets[k]}-1` 轮（`{n}×{tickets[k]-1}`），再由前 `k+1` 人买一轮 → `res = {res}`',
        'for index in range(k):': lambda S, B, r: (f'看第 {S.index} 人：排在第 k 人==前面==，要和 `tickets[k] = {S.tickets[K]}` 比'
                                                   if B.get('index') != S.index else '前面的人都检查完了'),
        'if tickets[index] < tickets[k]:': _if1,
        'res -= tickets[k] - tickets[index]': '减去差值 `{tickets[k]} − {tickets[index]}` → `res = {res}`',
        'for index in range(k + 1, n):': lambda S, B, r: (f'看第 {S.index} 人：排在第 k 人==后面==，要和 `tickets[k] - 1 = {S.tickets[K] - 1}` 比'
                                                          if B.get('index') != S.index else '后面的人也检查完了'),
        'if tickets[index] < tickets[k] - 1:': _if2,
        'res -= tickets[k] - 1 - tickets[index]': '减去差值 `{tickets[k]-1} − {tickets[index]}` → `res = {res}`',
        'return res': '扣掉所有多算的时间，答案 =={res}== 秒',
    },
    skip=[],
    cards=dict(
        one_liner='先当所有人票都够多算出时间，再把多算的差值减掉',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 人排队，每次队首买 1 张票（1 秒），没买完就回到队尾',
                 '求第 `k` 个人买完所有票的时刻',
                 '示例：`tickets = [2,3,2], k = 2` → `6`',
                 '本视频：`[2,4,3,1,5,2], k = 2` → `13`'],
        quote='一共是n个人先买tickets[k] - 1轮票，然后第0到第k个人再买一轮票后第k个人才能买到全部的票，此时需要的时间就是n * (tickets[k] - 1) + k + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 k 人在==第 tickets[k] 轮==买完：前面整轮 `n` 人，最后一轮只到第 k 人',
              '票不够的人会提前离队：前面的人少于 `tickets[k]`，后面的人少于 `tickets[k]-1`',
              '把这些==差值从 res 里减掉==即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：最后一轮只有第 `0..k` 人，所以是 `+ k + 1`',
                 '易错：k 后面的人对比的是 `tickets[k] - 1`，不是 `tickets[k]`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神直接累加 `min(t, tk - (i > k))`，这里是「先多算再扣」'],
    ),
)
