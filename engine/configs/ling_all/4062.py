
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
    live = S.get('_line') is not None and S.get('_line') >= 3
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
    author='灵茶山艾府', technique='总和守恒',
    tags=[],
    code='''
class Solution:
    def canTransform(self, source: list[int], target: list[int]) -> bool:
        return sum(source) == sum(target)
''',
    setup='CASES = [([1, 2, 3], [0, 2, 4]), ([-5, -5], [-15, 5]), ([1, 2, 1], [0, 2, 5]), ([5, 0, 4], [3, 3, 3])]',
    call='[Solution().canTransform(a, b) for a, b in CASES]',
    expect=[True, True, False, True],
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('source', 'sum(source)', 'blue'), ('target', 'sum(target)', 'pink')],
    captions={
        'return sum': lambda S, B, r: f'操作前后总和不变，所以先比总和：`{sum(S.source)}` vs `{sum(S.target)}` → ' + ('==相等，能变==，返回 true' if sum(S.source) == sum(S.target) else '==不相等，必不能变==，返回 false'),
    },
    cards=dict(
        one_liner='操作不改变总和；总和相等就一定能变',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选两个不同下标 `i, j` 和任意 `delta`：`source[i] += source[j] - delta`，`source[j] = delta`',
                 '问能否把 `source` 变成 `target`',
                 '示例：`[1,2,3] → [0,2,4]` 为 `true`；`[1,2,1] → [0,2,5]` 为 `false`'],
        quote='两数之和仍然为 x+y，source 的总和仍然为 S。所以操作不改变 source 的总和。这个条件也是充分的，给出一个具体的操作方法即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['必要性：`x, y` 变成 `x+y-delta` 和 `delta`，两数之和不变 → 总和不变',
              '充分性：选 `i=1, j=0, delta=target[0]` 把下标 0 对齐，规模减 1',
              '一直对齐到只剩一个数：总和相等，最后一个数自然相等'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只需要比较总和，不用管每个位置',
                 '构造证明：每步固定一个下标，总和守恒保证最后一个也对上',
                 '演示用 4 组输入连续调用：3 个题面示例 + 1 个自拟'],
    ),
)
