TICKETS = [2, 4, 3, 1, 5, 2]
K = 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t = TICKETS
    k = K
    n = len(t)
    tk = t[k]
    cv.text((x0 + 18, y0 + 4), '每人要买的票（绿 = 第 k 人买完那一刻已买到的票，灰 = 来不及买）', 24, T['muted'], bold=True)
    cell = min(150, (x1 - x0 - 200) / n)
    sx = x0 + 120 + ((x1 - x0 - 200) - cell * n) / 2
    base, top = y1 - 110, y0 + 70
    scale = (base - top) / max(t)
    done = 'tk' in S
    for i, v in enumerate(t):
        X = sx + i * cell
        cap = tk if i <= k else tk - 1
        got = min(v, cap)
        bw = cell * 0.62
        bx0, bx1 = X + (cell - bw) / 2, X + (cell + bw) / 2
        for u in range(v):
            yb = base - u * scale
            if done and u < got:
                fill = T['orange'] if i == k else T['green']
            else:
                fill = (90, 96, 106)
            cv.rect((bx0, yb - scale + 3, bx1, yb - 1), fill=fill, r=4)
        cv.text((X + cell / 2, base - v * scale - 6), v, 24, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 8), f'i={i}', 20, T['orange'] if i == k else T['dim'], anchor='mt', mono=True)
        if done:
            cv.text((X + cell / 2, base + 40), f'+{got}', 26, T['green'], anchor='mt', bold=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if done:
        yk = base - tk * scale
        yk1 = base - (tk - 1) * scale
        cv.dashed((sx, yk), (sx + (k + 1) * cell, yk), T['cyan'], 3)
        cv.text((sx - 8, yk), f'tk={tk}', 22, T['cyan'], anchor='rm', bold=True)
        cv.dashed((sx + (k + 1) * cell, yk1), (sx + n * cell, yk1), T['pink'], 3)
        cv.text((sx + n * cell + 8, yk1), f'tk-1={tk - 1}', 22, T['pink'], anchor='lm', bold=True)


def _sumfn(S):
    if 'tk' not in S:
        return '先取出第 k 个人要买的票数 `tk`'
    tk = S['tk']
    parts = [f'min({v},{tk - (i > K)})' for i, v in enumerate(TICKETS)]
    tot = sum(min(v, tk - (i > K)) for i, v in enumerate(TICKETS))
    return '`' + ' + '.join(parts) + f'` = =={tot}=='


CONFIG = dict(
    num=2073, title='买票需要的时间', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='看「买完那一刻」每人买了几张',
    tags=['labuladong'],
    code='''
class Solution:
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        tk = tickets[k]
        return sum(min(t, tk - (i > k)) for i, t in enumerate(tickets))
''',
    call=f'Solution().timeRequiredToBuy({TICKETS}, {K})',
    expect=13,
    views=[
        dict(type='array', var='tickets', label='tickets（橙 = 第 k 人，绿 = 排他前面，粉 = 排他后面）', cell=90,
             color=lambda S, i, v: 'orange' if i == K else ('green' if i < K else 'pink')),
        dict(type='custom', draw=_draw, h=430),
        dict(type='text', fn=_sumfn, size=26, h=90),
    ],
    watch=[('k', 'k', 'orange'), ('tk', 'tk', 'cyan'), ('tk - 1', lambda S: S['tk'] - 1 if 'tk' in S else '', 'pink')],
    captions={
        'tk = tickets[k]': '第 k 个人要买 `tk = {tk}` 张：他买完第 `{tk}` 张的==那一刻==就是答案',
        'return sum(': lambda S, B, ret: (
            f'他前面（含自己）的人每人至多买 `tk = {S.tk}` 张，后面的人至多 `tk-1 = {S.tk - 1}` 张'
            f' → 累加 `min` = =={ret}== 秒'),
    },
    cards=dict(
        one_liner='别模拟排队：只看第 k 人买完那一刻，每人各买了几张',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 人排队，每次队首买 1 张票（1 秒），没买完就回到队尾',
                 '求第 `k` 个人买完所有票的时刻',
                 '示例：`tickets = [2,3,2], k = 2` → `6`',
                 '本视频：`[2,4,3,1,5,2], k = 2` → `13`'],
        quote='当第 k 个人买了 t_k 张票时：排在他前面的人，买的票不会超过 t_k，即 min(t_i, t_k)；排在他后面的人，买的票不会超过 t_k−1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每秒卖出一张票 → 答案 = ==那一刻为止卖出的总票数==',
              '前面的人和他同一轮买：至多 `tk` 张；后面的人这一轮还没轮到：至多 `tk-1` 张',
              '`tk - (i > k)`：布尔值当 0/1 用，一行搞定两种上限'],
        after=[dict(heading='灵神的思考题', lines=[
            '输入正整数 `q`，返回第 `q` 秒是谁在买票（保证队列里还有人）',
            '多组询问 `queries`，要求时间复杂度==与票数值域无关==',
            '提示：按 `tickets` 排序后，按「轮」分段统计人数'])],
        summary=['时间 `O(n)`，空间 `O(1)`，与票数大小无关',
                 '易错：排在 k ==后面==的人上限是 `tk-1`，不是 `tk`',
                 '易错：上限还要和自己的需求取 `min`，买完的人会离队',
                 '暴力模拟是 `O(n·max(t))`，这题数据小也能过'],
    ),
)
