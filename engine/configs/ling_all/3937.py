NUMS = [1, 1, 1]
K = 3


def _flat(a):
    return isinstance(a, list) and all(isinstance(v, int) for v in a)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a, k = S.get('a'), S.get('k')
    cv.text((x0 + 18, y0 + 4), '断环成数轴：x 和 x+k 是同一个位置（蓝 = a，青 = 复制出来的 a+k）', 22, T['muted'], bold=True)
    if k is None or a is None:
        return
    if not _flat(a):   # minOperations 阶段：偶数 / 奇数下标分开存
        for r, name in enumerate(('偶数下标', '奇数下标')):
            vals = a[r] if r < len(a) else []
            cv.text((x0 + 30, y0 + 90 + r * 80), f'{name}的数（模 {k} 之后）：{vals}', 30, T['text'], bold=True)
        return
    n = S.get('n', len(a))
    line = S.get('_line', 0)
    loc = S.get('_inner', {})
    t, i, j = loc.get('target'), loc.get('i'), loc.get('j')
    lo, hi = 0, 2 * k
    ax0, ax1 = x0 + 60, x1 - 60
    ay = y0 + 250

    def X(v):
        return ax0 + (ax1 - ax0) * (v - lo) / (hi - lo)

    if t is not None:
        h = k // 2
        cv.rect((X(t), ay - 200, X(t + h), ay + 4), fill=T['green'], alpha=34, r=8)
        cv.rect((X(t + h), ay - 200, X(t + k), ay + 4), fill=T['orange'], alpha=34, r=8)
        cv.text(((X(t) + X(t + h)) / 2, ay - 196), '往下减', 20, T['green'], anchor='mt', bold=True)
        cv.text(((X(t + h) + X(t + k)) / 2, ay - 196), '往上加到 target+k', 20, T['orange'], anchor='mt', bold=True)
        cv.line([(X(t), ay - 200), (X(t), ay + 30)], T['yellow'], 4)
        cv.dashed((X(t + k), ay - 200), (X(t + k), ay + 30), T['yellow'], 3)
        cv.text((X(t), ay + 62), f'target={t}', 22, T['yellow'], anchor='mt', bold=True)
        cv.text((X(t + k), ay + 62), f'target+k={t + k}', 22, T['yellow'], anchor='mt', bold=True)
    elif loc.get('x') in range(hi + 1) and 20 <= line <= 28:
        cv.line([(X(loc['x']), ay - 200), (X(loc['x']), ay + 30)], T['yellow'], 3)
        cv.text((X(loc['x']), ay + 62), f"x={loc['x']}", 22, T['yellow'], anchor='mt', bold=True)
    cv.line([(ax0 - 14, ay), (ax1 + 14, ay)], T['muted'], 3)
    for v in range(lo, hi + 1):
        cv.line([(X(v), ay - 7), (X(v), ay + 7)], T['muted'], 2)
        cv.text((X(v), ay + 12), v, 20, T['dim'], anchor='mt', mono=True)
    seen = {}
    for idx, v in enumerate(a):
        c = T['blue'] if idx < n else T['cyan']
        dim = False
        if t is not None and i is not None:
            if i <= idx < i + n:
                if j is not None:
                    c = T['green'] if idx < j else T['orange']
            else:
                dim = True
        if dim:
            c = (58, 64, 74)
        m = seen.get(v, 0)
        seen[v] = m + 1
        cx, cy = X(v), ay - 30 - m * 44
        cv.rect((cx - 19, cy - 19, cx + 19, cy + 19), fill=c, r=19)
        cv.text((cx, cy), idx, 22, T['bg'] if not dim else T['dim'], anchor='mm', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 34), '圆内数字 = a 的下标；绿 / 橙 = 这一步要移动的人，灰 = 不在这一圈里', 20, T['dim'])


def _formula(S):
    line = S.get('_line', 0)
    loc = S.get('_inner', {})
    t = loc.get('target')
    if t is not None:
        n, k, pre = S['n'], S['k'], S.get('pre')
        i = loc.get('i')
        if i is None:
            return f'`calc_op({t})`：看看围着 `{t}` 转一圈的所有人，各自该往哪边走'
        j = loc.get('j')
        if j is None:
            return f'`i = {i}`：从 `a[{i}]` 起的 `n = {n}` 个数 `a[{i}..{i + n - 1}]`，就是围着 target 转一圈的所有人'
        if 's1' not in loc or line == 12:
            return (f'`a[{i}..{j - 1}]` 共 {j - i} 个数落在 `[{t}, {t + k // 2}]` 内 → 往==下==减；'
                    f'`a[{j}..{i + n - 1}]` 共 {n - j + i} 个数 → 往==上==加到 `{t + k}`')
        s1 = loc['s1']
        if 's2' not in loc or line == 13:
            return f'`s1 = (pre[{j}] − pre[{i}]) − {j - i}×{t}` = ({pre[j]} − {pre[i]}) − {(j - i) * t} = =={s1}=='
        s2 = loc['s2']
        if line == 14:
            return f'`s2 = {n - j + i}×({t}+{k}) − (pre[{i + n}] − pre[{j}])` = {(n - j + i) * (t + k)} − ({pre[i + n]} − {pre[j]}) = =={s2}=='
        return f'`s1 + s2` = {s1} + {s2} = =={s1 + s2}=='
    if 'mn' in S and 'best_x' in S:
        return f'目前：最小 `mn = {S["mn"]}`，次小 `mn2 = {S["mn2"]}`，最小对应的位置 `best_x = {S["best_x"]}`'
    if 'min1y' in S:
        return (f'偶数下标：最小 {S["min1x"]}（位置 {S["best_x"]}），次小 {S["min2x"]}；'
                f'奇数下标：最小 {S["min1y"]}（位置 {S["best_y"]}），次小 {S["min2y"]}')
    if 'min1x' in S:
        return f'偶数下标：最小 `{S["min1x"]}`（位置 {S["best_x"]}），次小 `{S["min2x"]}`'
    return '不考虑 `x ≠ y`：偶数下标、奇数下标互相独立，分别求「集中到一点」的最小代价'


def _long(S):
    """第一次 calc 里第一次 calc_op：讲全套解释；之后只报数"""
    return 'min1x' not in S and 'op' not in S


def _cap_for(S, B, r):
    bi, si = B.get('_inner', {}), S.get('_inner', {})
    if 'x' in bi and si.get('x') == bi['x']:
        return '`a` 里不同的位置都枚举完了'
    if 'min1x' in S:
        return '枚举集中位置 `x = {}`'.format(si.get('x'))
    return '枚举集中位置 `x = {}`：最优位置一定在某个 `a[i]` 上（中位数贪心），用 `set` 去重'.format(si.get('x'))


def _cap_if(S, B, r):
    if S.op < B.mn:
        return '`op = {} < mn = {}`：刷新最小值，原来的最小值退为次小'.format(S.op, B.mn if B.mn != inf else '∞')
    return '`op = {} ≥ mn = {}`：不是新的最小值，再看是不是次小'.format(S.op, B.mn)


CONFIG = dict(
    num=3937, title='使数组变为模交替数组的最少操作次数 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='断环 + 二分 + 前缀和 · 维护最小 / 次小操作次数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def calc(self, a: list[int], k: int) -> tuple[int, int, int]:
        n = len(a)
        a.sort()
        a += [x + k for x in a]

        pre = list(accumulate(a, initial=0))

        # 都变成 target 的最小操作次数
        def calc_op(target: int) -> int:
            i = bisect_left(a, target, 0, n)
            j = bisect_right(a, target + k // 2, i, i + n)
            s1 = (pre[j] - pre[i]) - (j - i) * target  # [i, j) 中的数都减小到 target
            s2 = (n - j + i) * (target + k) - (pre[i + n] - pre[j])  # [j, i+n) 中的数都增大到 target+k
            return s1 + s2

        mn = mn2 = inf
        best_x = 0

        for x in set(a[:n]):
            op = calc_op(x)
            # 维护最小次小操作次数
            if op < mn:
                mn2 = mn
                mn = op
                best_x = x
            elif op < mn2:
                mn2 = op

        # 还可以都变成 best_x-1 或者 best_x+1
        mn2 = min(mn2, calc_op((best_x - 1) % k), calc_op((best_x + 1) % k))

        return mn, mn2, best_x

    def minOperations(self, nums: list[int], k: int) -> int:
        if len(nums) == 1:
            return 0

        a = [[], []]
        for i, x in enumerate(nums):
            a[i % 2].append(x % k)

        min1x, min2x, best_x = self.calc(a[0], k)
        min1y, min2y, best_y = self.calc(a[1], k)

        if best_x != best_y:
            return min1x + min1y
        return min(min1x + min2y, min2x + min1y)
''',
    call=f'Solution().minOperations({NUMS}, {K})',
    expect=1,
    skip=['n = len(a)', 'mn = mn2 = inf', 'best_x = 0', 'mn2 = mn', 'for i, x in enumerate(nums)'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_formula, size=24, h=100),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('target', lambda S: S['_inner'].get('target'), 'yellow'), ('i', lambda S: S['_inner'].get('i') if 'target' in S['_inner'] else None, 'blue'),
           ('j', lambda S: S['_inner'].get('j'), 'pink'), ('mn', 'mn', 'green'), ('mn2', 'mn2', 'orange'),
           ('best_x', lambda S: S.get('best_x') if 'mn' in S else None, 'cyan')],
    max_steps=80,
    captions={
        'a.sort()': '`a` = 这组下标的数模 `k` 之后的值，先从小到大排序',
        'a += [x + k for x in a]': '复制一份、每个数加 `k` 接在后面：==把环断开==成普通数组（模 `k` 下 `x` 与 `x+k` 同位置）',
        'pre = list(accumulate': '`pre`：`a` 的前缀和，一段数的和 `O(1)` 就能算',
        'for x in set(a[:n])': _cap_for,
        'op = calc_op(x)': lambda S, B, r: ('`calc_op({})`：所有数都集中到位置 `{}`，最少要几步'.format(S.x, S.x) if 'min1x' not in S
                                            else '`calc_op({})`'.format(S.x)),
        'i = bisect_left': lambda S, B, r: ('`i` = 第一个 `≥ target` 的下标：从这里起的 `n` 个数 = 围着 `target` 转一圈的人' if _long(S)
                                            else '`i = {}`'.format(S['_inner']['i'])),
        'j = bisect_right': lambda S, B, r: ('`target + k//2` 是「正对面」：左边那段的人往==下==走到 target 更近，右边那段的人往==上==走到 `target + k` 更近' if _long(S)
                                             else '`j = {}`'.format(S['_inner']['j'])),
        's1 =': lambda S, B, r: ('一边是等差求和：每人走 `x − target` 步，合起来 = ==和 − 人数×target==' if _long(S)
                                 else '`s1 = {}`'.format(S['_inner']['s1'])),
        's2 =': lambda S, B, r: ('另一边每人走 `(target + k) − x` 步：==人数×(target+k) − 和==' if _long(S)
                                 else '`s2 = {}`'.format(S['_inner']['s2'])),
        'return s1 + s2': lambda S, B, r: ('两边相加，就是集中到 `target` 的总步数 =={}=='.format(r) if _long(S)
                                           else '`calc_op({})` = =={}=='.format(S['_inner']['target'], r)),
        'if op < mn:': _cap_if,
        'mn = op': '`mn` = =={mn}==：新的最小操作次数',
        'best_x = x': '记下它对应的位置 `best_x = {best_x}`',
        'elif op < mn2:': lambda S, B, r: ('`op = {} < mn2 = {}`：刷新次小值'.format(S.op, B.mn2) if S.op < B.mn2
                                            else '`op = {}` 也不比次小值 {} 小，不更新'.format(S.op, B.mn2)),
        'mn2 = op': '`mn2` = =={mn2}==：新的次小操作次数',
        'mn2 = min(mn2, calc_op': '次小值也可能来自 `best_x ± 1`（不一定是 `a` 里的数），额外算这两个位置',
        'return mn, mn2, best_x': '返回：最小 `{mn}`、次小 `{mn2}`、最小对应的位置 `{best_x}`',
        'if len(nums) == 1': '只有一个数，没有「偶数下标 / 奇数下标取不同余数」的限制，不用操作',
        'a = [[], []]': '偶数下标、奇数下标的数分开存：不考虑 `x ≠ y` 时两边互相独立',
        'a[i % 2].append(x % k)': '`nums[{i}] = {x}`，模 {k} 得 `{x % k}`，放进 `a[{i % 2}]`',
        'self.calc(a[0], k)': '先算偶数下标：`calc` 返回「最小操作次数、次小操作次数、最优位置」',
        'self.calc(a[1], k)': '偶数下标算完了；再用同样的方法算奇数下标',
        'if best_x != best_y': lambda S, B, r: ('`best_x = {}`、`best_y = {}` ==相同==，但题目要求 `x ≠ y`，必须让一边退而求其次'.format(S.best_x, S.best_y)
                                                if S.best_x == S.best_y else '两边最优位置不同，各取最优'),
        'return min1x + min1y': '两边最优位置不同：直接相加',
        'return min(min1x + min2y, min2x + min1y)': '`min({min1x}+{min2y}, {min2x}+{min1y})` = =={ret}==：偶数取最小 + 奇数取次小，或者反过来，取较小者',
    },
    cards=dict(
        one_liner='把环断开成数组：哪些数往下走、哪些往上走，前缀和一次算清',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每步可把任意元素 `±1`；偶数下标的数模 `k` 都等于 `x`，奇数下标的都等于 `y`，且 `x ≠ y`',
                 '求最少操作次数',
                 '示例：`nums=[1,4,2,8]`，`k=3` → `2`',
                 f'本视频：`nums={NUMS}`，`k={K}` → `1`（`x = y` 冲突的情形）'],
        quote='想象有一个长为 k 的环，上面有一些人……把这些人集中到环上的哪个位置，可以让总移动距离之和最小？……在 x 对面的那段弧是没人经过的，那么断开这段弧，变成一个普通数组问题。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['不考虑 `x ≠ y`：偶数、奇数下标独立；模 `k` 后把每个数看成环上的一个人',
              '集中位置取在某个 `a[i]` 上（中位数贪心）：右边 `k/2` 内的往下走，其余的往上走到 `x+k`',
              '复制 `a+k` 展平成数组，二分切开两段，前缀和求步数；同时记最小、次小值',
              '若两边最优位置相同（`x = y`），一边退到次小：`min(最小+次小, 次小+最小)`'],
        summary=['时间 `O(n log n)`（排序 + 二分），空间 `O(n)`',
                 '易错：次小值不一定来自 `a` 里的数，还要试 `best_x ± 1`',
                 '易错：`n = 1` 直接返回 0；`best_x == best_y` 时才用次小',
                 '方法一：暴力枚举 `x, y`，每个数代价 `min(d, k−d)`，`O(nk²)`'],
    ),
)
