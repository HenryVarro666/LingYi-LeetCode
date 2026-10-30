
def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n')
    t = S.get('k', S.get('target'))
    if n is None:
        return
    m = min(t // 2, n)
    show = ('m' in S or t <= 2)
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
    author='yiduobo', technique='复用 2829 的 O(1) 公式',
    tags=['灵神题单', '数学算法', '难度分 1409'],
    code='''
class Solution(object):
    def minimumPossibleSum(self, n, target):

        if target <= 2:
            return (1 + n) * n // 2

        m = target // 2
        if m >= n:
            return (1 + n) * n // 2
        else:
            return (1 + m) * m // 2 + (target + target + n - m - 1) * (n - m) // 2
''',
    call='[Solution().minimumPossibleSum(*a) for a in ((2, 3), (3, 3), (1, 1), (6, 4))]',
    expect=[4, 8, 1, 25],
    views=[dict(type='custom', draw=_draw, h=420)],
    watch=[('n', 'n', 'blue'), ('target', 'target', 'yellow'), ('m', 'm', 'green')],
    captions={
        'if target <= 2': '`target = {target}`：{"≤ 2，能凑出 target 的只有 1+1，而元素互不相同 → ==前 n 个正整数全能选==" if target <= 2 else "大于 2，存在配对（如 1 与 target-1），继续往下"}',
        'm = target': '`m = target // 2 = {m}`：`1..{m}` 每个数的配对 `target-x` 都比它大，选小的',
        'if m >= n': '`m = {m}`，`n = {n}`：{"m ≥ n，前 n 个正整数就够了" if m >= n else "m < n，只靠 1..m 不够，还要从 target 往后补"}',
        'return (1 + n)': '前 `n` 个正整数：`(1+{n})×{n}//2` = =={ret}==',
        'return (1 + m)': '`1..{m}` 的和 `{(1+m)*m//2}`，加上 `{target}..{target+n-m-1}`（共 `{n-m}` 个）的和 `{(target+target+n-m-1)*(n-m)//2}` = =={ret}==',
    },
    cards=dict(
        one_liner='和 2829 是同一道题，数据变大不影响 O(1) 公式',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['长度为 `n` 的互不相同正整数数组，任意两数之和不等于 `target`',
                 '求最小和（结果对 `10^9+7` 取模）',
                 '演示 `(2,3)`、`(3,3)`、`(1,1)`、`(6,4)`'],
        quote='本题与之前的2829题相同，不过数据范围大了不少，但数据规模的变化对之前O(1)的算法不会产生任何影响，直接套用就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`target <= 2`：没有配对限制，答案就是 `1+2+...+n`',
              '否则 `1..target//2` 里每个数只能留小的，`m = target//2`',
              '`m >= n` 就取前 n 个数；否则再从 `target` 起补 `n-m` 个，分两段求和'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '原文代码没有对 `10^9+7` 取模：题目要求取模，大数据会不通过（与灵神的写法不同）',
                 '`m >= n` 分支别漏：此时第二段为空'],
    ),
)
