N = 10


def _draw(cv, S, B, box, T):
    """只有一行代码：把 n = 10 时每一轮切换了哪些灯泡画成一张表"""
    x0, y0, x1, y1 = box
    n = N
    cv.text((x0 + 18, y0 + 4), f'n = {n}：第 r 轮切换所有 r 的倍数号灯泡（■ = 这一轮被切换）', 24, T['muted'], bold=True)
    lab_w = 120
    cw = min(80, (x1 - x0 - 40 - lab_w) / n)
    rh = 36
    sx = x0 + 20 + lab_w
    sy = y0 + 50
    sq = {k * k for k in range(1, n + 1)}
    # 表头：灯泡编号
    cv.text((x0 + 20, sy + rh / 2), '灯泡', 22, T['muted'], anchor='lm', bold=True)
    for j in range(1, n + 1):
        X = sx + (j - 1) * cw
        cv.text((X + cw / 2, sy + rh / 2), j, 24, T['yellow'] if j in sq else T['text'], anchor='mm', bold=True)
    # 每一轮
    for r in range(1, n + 1):
        Y = sy + r * rh
        cv.text((x0 + 20, Y + rh / 2), f'第 {r} 轮', 20, T['muted'], anchor='lm')
        for j in range(1, n + 1):
            X = sx + (j - 1) * cw
            if j % r == 0:
                cv.rect((X + 6, Y + 4, X + cw - 6, Y + rh - 4), fill=T['yellow'] if j in sq else T['blue'], r=5)
            else:
                cv.rect((X + 6, Y + 4, X + cw - 6, Y + rh - 4), outline=T['border'], width=1, r=5)
    # 约数个数
    Y = sy + (n + 1) * rh + 8
    cv.text((x0 + 20, Y + rh / 2), '切换次数', 20, T['muted'], anchor='lm', bold=True)
    for j in range(1, n + 1):
        X = sx + (j - 1) * cw
        cnt = sum(1 for d in range(1, j + 1) if j % d == 0)
        cv.text((X + cw / 2, Y + rh / 2), cnt, 24, T['yellow'] if cnt % 2 else T['muted'], anchor='mm', bold=True)
    # 最终状态
    Y += rh + 6
    cv.text((x0 + 20, Y + 24), '最终', 20, T['muted'], anchor='lm', bold=True)
    for j in range(1, n + 1):
        X = sx + (j - 1) * cw + cw / 2
        on = j in sq
        rad = 17
        cv.d.ellipse((X - rad, Y + 24 - rad, X + rad, Y + 24 + rad), fill=T['yellow'] if on else (40, 45, 53),
                     outline=T['yellow'] if on else T['border'], width=2)
        cv.text((X, Y + 24), '亮' if on else '灭', 18, T['bg'] if on else T['dim'], anchor='mm', bold=True)
    # 完全平方数列框
    for k in range(1, n + 1):
        j = k * k
        if j > n:
            break
        X = sx + (j - 1) * cw
        cv.rect((X + 1, sy, X + cw - 1, Y + 50), outline=T['yellow'], width=2, r=8)
    cv.rich(x0 + 24, Y + 64, f'亮着的：`1, 4, 9` = `1², 2², 3²` → 共 `floor(sqrt({n}))` = =={int(n ** 0.5)}== 个', x1 - x0 - 40, size=26)


CONFIG = dict(
    num=319, title='灯泡开关', difficulty='Medium', category='数学',
    author='yiduobo', technique='约数个数的奇偶 → 完全平方数',
    tags=['字节30天'],
    code='''
class Solution(object):
    def bulbSwitch(self, n):
        return int(sqrt(n))
''',
    setup='from math import sqrt',  # 原文直接调用 sqrt（依赖力扣环境的预导入），这里补上导入，代码本身不改
    call=f'Solution().bulbSwitch({N})',
    expect=3,
    views=[dict(type='custom', draw=_draw, h=630)],
    watch=[('n', 'n')],
    captions={
        'return int(sqrt': '`1..{n}` 里的完全平方数只有 `1², 2², …, k²`（`k² ≤ n`）→ 个数就是 `int(sqrt({n}))` = =={ret}==',
    },
    cards=dict(
        one_liner='第 k 个灯泡亮着 ⇔ k 有奇数个约数 ⇔ k 是完全平方数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 个灯泡初始都是关的；第 `i` 轮，每 `i` 个灯泡切换第 `i` 个的开关',
                 '（第 1 轮全打开，第 2 轮关掉偶数号，……，第 `n` 轮只切最后一个）',
                 '求 `n` 轮后亮着的灯泡数。示例：`n = 3` → `1`；`n = 0` → `0`'],
        before=[dict(heading='第 k 个灯泡被切换了几次？', lines=[
            '第 `r` 轮切换的是 `r` 的倍数号灯泡',
            '灯泡 `k` 在第 `r` 轮被切换 ⇔ ==r 是 k 的约数==',
            '所以切换次数 = `k` 的约数个数；==奇数次==最后亮着'])],
        quote='考察第k个灯泡，那么如果在1到k之间有奇数个数是k的约数，那么k最后就是亮着的……而对于一个数而言，==只有当这个数是完全平方数时，才会具有奇数个约数==。',
        quote_src='—— yiduobo 题解',
        idea=['经典的数学题：模拟要 `O(n log n)`，`n` 到 `10⁹` 会超时',
              '题目变成：`1` 到 `n` 之间有多少个完全平方数',
              '`1², 2², …, k² ≤ n` → 答案是 `k = int(sqrt(n))`'],
        result='`n = 10` → 灯泡 1、4、9 亮着，返回 `3` ✓',
        after=[dict(heading='为什么只有完全平方数有奇数个约数？', lines=[
            '约数总是==成对==出现：`d` 和 `k / d`',
            '`12`：`1×12`、`2×6`、`3×4` → 6 个（偶数）',
            '`9`：`1×9`、`3×3` → `3` 和自己配对，只算一次 → 3 个（奇数）',
            '只有 `d = k / d`，即 `k = d²` 时，才会多出一个落单的约数'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '难点在转化：切换次数 = 约数个数 → 奇数 ⇔ 完全平方数',
                 '浮点开方在大数时可能有误差；Python 3.8+ 可以用 `isqrt(n)` 精确求整数平方根',
                 '原文直接调用 `sqrt`（依赖力扣环境的预导入），本视频运行前补了 `from math import sqrt`',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
