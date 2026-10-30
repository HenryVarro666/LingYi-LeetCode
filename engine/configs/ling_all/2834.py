
def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    t = S.get('k', S.get('target'))
    if n is None:
        return
    m = min(t // 2, n)
    show = ('m' in S)
    N = 10
    cell = min(84, (x1 - x0 - 50) / N)
    sx = x0 + 25 + ((x1 - x0 - 50) - cell * N) / 2
    ys = y0 + 120
    cv.text((x0 + 18, y0 + 4), f'n={n}，target={t}：绿 = 从 1 起选的小数，蓝 = 从 {t} 起补的数，灰 = 被配对排除', 22, T['muted'], bold=True)
    low = set(range(1, m + 1))
    high = set(range(t, t + n - m))
    for v in range(1, N + 1):
        X = sx + (v - 1) * cell
        if show and v in low:
            fill, tc = T['green'], T['bg']
        elif show and v in high:
            fill, tc = T['blue'], T['bg']
        elif show and v < t:
            fill, tc = (52, 60, 72), T['dim']
        else:
            fill, tc = T['panel2'], T['muted']
        cv.rect((X + 4, ys, X + cell - 4, ys + cell), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + cell / 2), v, 32, tc, anchor='mm', bold=True, mono=True)
    if show:
        for a in range(1, t // 2 + 1):
            b = t - a
            if a != b and b <= N and a <= N:
                xa, xb = sx + (a - 1) * cell + cell / 2, sx + (b - 1) * cell + cell / 2
                yy = ys - 14 - 10 * a
                cv.line([(xa, ys - 4), (xa, yy), (xb, yy), (xb, ys - 4)], T['pink'] if a <= m else T['dim'], 2)
        cv.text((x0 + 25, ys + cell + 40), f'和 = 1+..+{m} 与 {t}..{t + n - m - 1} 两段：{sum(low)} + {sum(high)} = {sum(low) + sum(high)}', 28, T['text'], bold=True)
        cv.text((x0 + 25, ys + cell + 90), '粉色弧线 = 加起来等于 target 的一对，只能选一个', 22, T['pink'])


CONFIG = dict(
    num=2834, title='找出美丽数组的最小和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='配对 · 两段等差数列求和',
    tags=['灵神题单', '数学算法', '难度分 1409'],
    code='''
class Solution:
    def minimumPossibleSum(self, n: int, k: int) -> int:
        m = min(k // 2, n)
        return (m * (m + 1) + (k * 2 + n - m - 1) * (n - m)) // 2 % 1_000_000_007
''',
    call='[Solution().minimumPossibleSum(*a) for a in ((2, 3), (3, 3), (1, 1), (6, 4))]',
    expect=[4, 8, 1, 25],
    views=[dict(type='custom', draw=_draw, h=420),
           dict(type='text', fn=lambda S: (f"第一段 `1..{S['m']}` 和 `{S['m']}×{S['m']+1}/2` = =={S['m']*(S['m']+1)//2}==；第二段 `{S['k']}..{S['k']+S['n']-S['m']-1}` 共 `{S['n']-S['m']}` 个" if 'm' in S else ''), size=26)],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'yellow'), ('m', 'm', 'green')],
    captions={
        'm = min': '`x` 与 `{k}-x` 配对只能选一个，选小的 `x`，`x` 最多到 `k//2 = {k//2}`；再和 `n={n}` 取小：`m = {m}`',
        'return': '第一段 `1..{m}` 和 `{m*(m+1)//2}`，剩 `{n-m}` 个从 `{k}` 往后选，和 `{(k*2+n-m-1)*(n-m)//2}`，合计 =={ret}==（别忘了取模）',
    },
    cards=dict(
        one_liner='1 与 k-1 只能选一个：先选小的，不够再从 k 往后补',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['数组长 `n`，元素互不相同的正整数，任意两个不同元素之和都不等于 `target`',
                 '求这样的数组的最小和，结果对 `10^9+7` 取模',
                 '示例 `(2,3)` → `4`，`(3,3)` → `8`；另演示 `(1,1)`、`(6,4)`'],
        quote='1 和 k-1 只能选其中一个；2 和 k-2 只能选其中一个；……一直到 ⌊k/2⌋，无论 k 是奇数还是偶数，它都可以选。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`[1,k-1]` 里的数两两配对，每对只能取一个，当然取小的',
              '所以前 `m = min(k//2, n)` 个数 `1..m` 全选，和为 `m(m+1)/2`',
              '还差 `n-m` 个，只能从 `k` 起往后选：`k..k+n-m-1`，再等差求和'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`k` 为偶数时 `k/2` 与自己配对，但两个元素必须不同，所以可以选',
                 '`n` 小于 `k//2` 时 `m = n`，第二段为空',
                 '最后别忘了 `% (10^9+7)`；乘法结果要先整除 2 再取模'],
    ),
)
