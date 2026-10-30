CUST = 'YYNYNNYY'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['customers']
    n = len(s)
    cv.text((x0 + 18, y0 + 4), 'customers（分割线从左往右移，N 把 penalty 加一，Y 减一）', 22, T['muted'], bold=True)
    live = 'penalty' in S and 'i' in S
    cur = 0
    if live:
        cur = S['i'] + 1 if (S['_line'] >= 5 or B.get('i') == S['i']) else S['i']
    cell = min(100, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    ys = y0 + 60
    ch = cell * 0.8
    for k, c in enumerate(s):
        X = sx + k * cell
        left = k < cur
        col = T['pink'] if c == 'N' else T['green']
        fill = col if left else T['panel2']
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), c, 36, T['bg'] if left else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 10), k, 18, T['dim'], anchor='mt', mono=True)
        if live and k == S['i'] and S['_line'] in (6, 7, 8):
            cv.rect((X, ys - 4, X + cell, ys + ch + 4), outline=T['blue'], width=5, r=12)
    # 折线：分割位置 j = 0..n 的 penalty（相对第一个点）
    vals = [0]
    for c in s:
        vals.append(vals[-1] + (1 if c == 'N' else -1))
    top, bot = ys + ch + 110, y1 - 90
    lo, hi = min(vals), max(vals)
    def py(v):
        return bot - (v - lo) / max(1, hi - lo) * (bot - top)
    def px(j):
        return sx + j * cell
    cv.text((x0 + 18, top - 66), 'penalty 随分割位置 j 的变化（j = 前 j 个字符在第一段）', 22, T['muted'], bold=True)
    cv.dashed((px(0), py(0)), (px(n), py(0)), T['border'], 2)
    cv.text((px(0) - 12, py(0)), '0', 20, T['dim'], anchor='rm', mono=True)
    if not live:
        return
    ans, mp = S.get('ans', 0), S.get('min_penalty', 0)
    shown = min(n, cur) + 1
    pts = [(px(j), py(vals[j])) for j in range(shown)]
    if len(pts) > 1:
        cv.line(pts, T['cyan'], 4)
    for j in range(shown):
        c = T['orange'] if j == ans else T['cyan']
        cv.rect((px(j) - 9, py(vals[j]) - 9, px(j) + 9, py(vals[j]) + 9), fill=c, r=9)
        cv.text((px(j), py(vals[j]) - 16), vals[j], 19, T['text'], anchor='mb', mono=True)
        cv.text((px(j), bot + 14), j, 18, T['dim'], anchor='mt', mono=True)
    cv.text((px(ans), bot + 44), f'目前最低 → 关门时间 {ans}', 20, T['orange'], anchor='mt', bold=True)


CONFIG = dict(
    num=2483, title='商店的最少代价', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 一次遍历（平移折线）',
    tags=['灵神题单', '动态规划', '难度分 1495'],
    code='''
class Solution:
    def bestClosingTime(self, customers: str) -> int:
        min_penalty = penalty = ans = 0
        for i, c in enumerate(customers):
            penalty += 1 if c == 'N' else -1
            if penalty < min_penalty:
                min_penalty = penalty
                ans = i + 1
        return ans
''',
    call=f'Solution().bestClosingTime("{CUST}")',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['i', ('c', 'c'), ('penalty', 'penalty', 'cyan'), ('min_penalty', 'min_penalty', 'orange'), ('ans', 'ans', 'green')],
    captions={
        3: '分割线在最左边：`penalty = 0`（只看相对变化，不必先数 Y 的个数）',
        'for i, c': lambda S, B, r: ('遍历结束，整条折线都走完了' if S.i == B.get('i', -1) else f"分割线右移，越过 `customers[{S.i}] = '{S.c}'`"),
        'penalty +=': lambda S, B, r: (f"`'N'`：开门却没人，代价 +1 → `penalty = {S.penalty}`" if S.c == 'N' else f"`'Y'`：这位顾客挪到第一段（开门）不再算代价 → `penalty = {S.penalty}`"),
        'if penalty <': lambda S, B, r: (f'`{S.penalty} < min_penalty = {S.min_penalty}` → ==更低了==' if S.penalty < S.min_penalty else f'`{S.penalty} < {S.min_penalty}` 不成立 → 不更新' + ('（==相等也不更新==，保证最早）' if S.penalty == S.min_penalty else '')),
        7: '`min_penalty` 更新为 =={min_penalty}==',
        'ans = i + 1': '`ans = i + 1 = {ans}`：`[0,{i}]` 是第一段，所以关门时间是 {ans}',
        'return ans': '折线最低点对应的分割位置：关门时间 =={ans}==',
    },
    cards=dict(
        one_liner='分割线从左往右移，折线最低点就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`customers[i]` 是 `Y` 表示第 `i` 小时有顾客，`N` 表示没有',
                 '开门时无人到达代价 +1，关门时有人到达代价 +1',
                 '求代价最小的最早关门时间；本视频：`"YYNYNNYY"` → `2`'],
        quote='把折线图往下平移（第一个点移到坐标零点），最低点的横坐标仍然不变。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分成两段：第一段数 `N`，第二段数 `Y`，代价 = `preN + sufY`',
              '分割线右移一格：遇到 `N` 代价 +1，遇到 `Y` 代价 −1',
              '起点平移到 0，只看相对变化，就省掉了先数 `Y` 的第一次遍历'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '更新用严格 `<`：代价相同保留更早的关门时间',
                 '`ans = i + 1`：分割线在 `customers[i]` 右边',
                 '优化前写法：先数 `Y` 的个数作初值（`min_penalty = penalty = customers.count(\'Y\')`），再遍历，思路相同，多一次遍历'],
    ),
)
