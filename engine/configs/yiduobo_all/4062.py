
CASES = [([1, 2, 3], [0, 2, 4]), ([-5, -5], [-15, 5]), ([1, 2, 1], [0, 2, 5]), ([5, 0, 4], [3, 3, 3])]


def _ops(src, tgt):
    s = list(src)
    out = [list(s)]
    log = []
    for k in range(len(s) - 1):
        if s[k] != tgt[k]:
            i, j, d = k + 1, k, tgt[k]
            s[i] = s[i] + s[j] - d
            s[j] = d
            log.append(f'i={i}, j={j}, delta={d}：下标 {j} 变成 {d}，下标 {i} 变成 {s[i]}')
        else:
            log.append(f'下标 {k} 已经等于 {tgt[k]}：跳过，去掉它')
        out.append(list(s))
    return s, log


def _row(cv, x, y, arr, cell, T, label, color_fn=None):
    cv.text((x, y + cell / 2), label, 24, T['muted'], anchor='lm', bold=True)
    for k, v in enumerate(arr):
        X = x + 130 + k * (cell + 8)
        fill = (color_fn(k, v) if color_fn else None) or T['panel2']
        cv.rect((X, y, X + cell, y + cell), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, y + cell / 2), v, 28, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    src, tgt = S.get('source'), S.get('target')
    if not src or not tgt:
        cv.text((x0 + 18, y0 + 4), '把 source 变成 target：每次操作不改变总和', 22, T['muted'], bold=True)
        return
    n = len(src)
    cell = min(80, (x1 - x0 - 200) / n - 8)
    cv.text((x0 + 18, y0 + 4), '操作不改变总和：source 的和 = target 的和 则能变', 22, T['muted'], bold=True)
    _row(cv, x0 + 18, y0 + 60, src, cell, T, 'source', lambda k, v: T['blue'])
    _row(cv, x0 + 18, y0 + 60 + cell + 24, tgt, cell, T, 'target', lambda k, v: T['pink'])
    ss, st = sum(src), sum(tgt)
    live = S.get('_line') is not None and S.get('_line') >= 4
    y = y0 + 60 + 2 * cell + 70
    cv.text((x0 + 18, y), f'sum(source) = {ss}', 32, T['blue'], bold=True)
    cv.text((x0 + 18, y + 48), f'sum(target) = {st}', 32, T['pink'], bold=True)
    if live:
        ok = ss == st
        cv.text((x0 + 18, y + 100), ('相等 → true' if ok else '不相等 → false'), 34, T['green'] if ok else T['red'], bold=True)
        y2 = y + 170
        cv.text((x0 + 18, y2), '为什么够：逐个对齐，最后一个数自动对上', 22, T['muted'], bold=True)
        fin, log = _ops(src, tgt)
        for k, line in enumerate(log):
            cv.text((x0 + 18, y2 + 40 + k * 36), line, 22, T['text'])
        last = len(log)
        cv.text((x0 + 18, y2 + 48 + last * 36), f'剩下最后一个数：{fin[-1]}，target 末位 {tgt[-1]}', 24,
                T['green'] if fin[-1] == tgt[-1] else T['red'], bold=True)


CONFIG = dict(
    num=4062, title='成对操作转化数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='总和守恒 + delta 任意',
    tags=[],
    code='''
class Solution(object):
    def canTransform(self, source, target):
        
        return sum(source) == sum(target)
''',
    setup='CASES = [([1, 2, 3], [0, 2, 4]), ([-5, -5], [-15, 5]), ([1, 2, 1], [0, 2, 5]), ([5, 0, 4], [3, 3, 3])]',
    call='[Solution().canTransform(a, b) for a, b in CASES]',
    expect=[True, True, False, True],
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('source', 'sum(source)', 'blue'), ('target', 'sum(target)', 'pink')],
    captions={
        'return sum': lambda S, B, r: f'`sum(source) = {sum(S.source)}`，`sum(target) = {sum(S.target)}` → ' + ('==相同==，可以变' if sum(S.source) == sum(S.target) else '==不同==，不可能变'),
    },
    cards=dict(
        one_liner='delta 任意：能随心所欲定一个数，总和是唯一约束',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作选下标 `i, j` 和任意 `delta`，`source[i]` 变 `source[i]+source[j]-delta`，`source[j]` 变 `delta`',
                 '问能否把 `source` 变成 `target`',
                 '示例：`[-5,-5] → [-15,5]` 为 `true`'],
        quote='由于delta可以任意选择，因此每次操作可以在无视其中一个元素的前提下，使得另一个元素变为想要的目标元素。',
        quote_src='—— yiduobo 题解',
        idea=['`delta` 任选 → 一次操作能让一个元素直接变成想要的值',
              '但两个元素之和不变 → 总和永远不变',
              '分配完 n-1 个元素后，最后一个 = 总和 − 前 n-1 个，总和相同它就对得上'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：不要去模拟操作，直接比 `sum`',
                 '关键在两点：总和守恒 + 前 n-1 个可随意设定',
                 '原文代码已是 Python 3 可运行，未改动'],
    ),
)
