def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '每个约数 g 一棵树状数组 f[g]（下标 1..max//g）；右边 tot[g] = 元素都是 g 的倍数的严格递增子序列数', 21, T['muted'], bold=True)
    f, tot = S.get('f'), S.get('tot')
    if f is None or tot is None:
        return
    ma = len(f) - 1
    phase2 = 'res' in S
    hot = set()
    if not phase2 and 'g' in S.get('_inner', {}):
        hot.add(S['g'])
    elif not phase2 and 'v' in S and 'x' in S:
        hot.add(S['x'])
        if 'y' in S:
            hot.add(S['y'])
    row_h = min(70, (y1 - y0 - 60) / max(1, ma))
    for g in range(1, ma + 1):
        y = y0 + 52 + (g - 1) * row_h
        on = g in hot if not phase2 else g == S.get('v')
        if on:
            cv.rect((x0 + 14, y - 2, x1 - 14, y + row_h - 8), fill=T['panel2'], outline=T['yellow'], width=2, r=8)
        cv.text((x0 + 30, y + row_h / 2 - 4), f'f[{g}]', 24, T['yellow'] if on else T['muted'], anchor='lm', bold=True)
        cx = x0 + 120
        for k, v in enumerate(f[g]):
            if k == 0:
                continue
            cv.rect((cx, y + 4, cx + 62, y + row_h - 12), fill=T['panel2'], outline=T['border'], r=6)
            cv.text((cx + 31, y + row_h / 2 - 4), v, 22, T['green'] if v else T['dim'], anchor='mm', bold=True)
            cv.text((cx + 31, y + row_h - 10), k, 13, T['dim'], anchor='mm', mono=True)
            cx += 70
        cv.text((x1 - 30, y + row_h / 2 - 4), f'tot[{g}] = {tot[g]}', 24, T['green'] if tot[g] else T['dim'], anchor='rm', bold=True)


def _formula(S):
    if 'tot' not in S:
        return '用 `ma // g` 大小的树状数组，把元素按 g 的倍数分别统计'
    if 'res' in S:
        return '倒着看 `v`：`tot[v]` 减去所有 `2v, 3v, …` 的 `tot` → GCD ==恰好== 是 v'
    if 'g' in S.get('_inner', {}):
        return f'在 `f[{S["g"]}]` 这棵树状数组上操作，位置 `{S["x"]}`（查前缀 / 更新）'
    if 'v' in S:
        return f'`v = {S["v"]}`：对它的每个约数 `d`，更新 `d` 对应的树状数组'
    return '先建好 tot'


CONFIG = dict(
    num=3671, title='子序列美丽值求和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='每个约数一棵树状数组 + 倒序容斥',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def totalBeauty(self, nums):

        ma = max(nums)
        f = [[] for _ in range(ma + 1)]
        for g in range(1, ma + 1):
            f[g] = [0] * (ma // g + 1)

        mod = 10 ** 9 + 7

        def get(g, x):
            s = 0
            while x > 0:
                s += f[g][x]
                if s >= mod:
                    s -= mod
                x -= x & -x
            return s
        
        def add(g, x, v):
            while x < len(f[g]):
                f[g][x] += v
                if f[g][x] >= mod:
                    f[g][x] -= mod
                x += x & -x

        tot = [0] * (ma + 1)
        for v in nums:
            x = 1
            while x * x <= v:
                if v % x == 0:
                    y = v // x
                    end_y = get(x, y - 1) + 1
                    add(x, y, end_y)
                    tot[x] += end_y
                    if tot[x] >= mod:
                        tot[x] -= mod
                    if x != y:
                        end_x = get(y, x - 1) + 1
                        add(y, x, end_x)
                        tot[y] += end_x
                        if tot[y] >= mod:
                            tot[y] -= mod
                x += 1
        
        res = 0
        for v in range(ma, 0, -1):
            for x in range(v + v, ma + 1, v):
                tot[v] -= tot[x]
                if tot[v] < 0:
                    tot[v] += mod
            delta = tot[v] * v % mod
            res += delta
            if res >= mod:
                res -= mod
        
        return res
''',
    call='Solution().totalBeauty([2,4])',
    expect=8,
    views=[
        dict(type='text', fn=_formula, size=24, h=56),
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='tot', label='tot[g]（容斥前是「g 的倍数」，容斥后变成「恰好 g」）', h=170, cell=80, pointers={'x if "g" not in _inner else None': 'blue'}, pointer_labels={'x if "g" not in _inner else None': 'x'}),
    ],
    watch=[('end_y', 'end_y', 'cyan'), ('end_x', 'end_x', 'cyan'), ('delta', 'delta', 'yellow'), ('res', 'res', 'green')],
    captions={
        'tot = [0]': '`tot[d]` 记「元素都是 d 的倍数」的严格递增子序列数；每个 d 有自己的树状数组 `f[d]`（已全 0）',
        'x = 1': '枚举 `v = {v}` 的约数：只扫到 `sqrt(v)`，`x` 和 `v // x` 成对出现',
        'y = v // x': '`{x}` 整除 `{v}` → 约数对 `({x}, {y})`',
        'end_y = get': '对约数 `{B.x}`：在树 `f[{B.x}]` 里数「比 `{B.y}` 小的数结尾」的序列数，`+1` 是 `{B.v}` 单独一个 → 以 `{B.v}` 结尾的个数',
        'add(x, y, end_y)': '以 `{B.v}` 结尾的严格递增子序列有 `end_y = {B.end_y}` 个 → 记进 `f[{B.x}]` 的位置 `{B.y}`',
        'tot[x] += end_y': '`tot[{x}]` 累加 `{end_y}` → =={tot[x]}==',
        'if x != y': lambda S, B, r: (f'`{S.x} != {S.y}`：另一个约数 `{S.y}` 也要更新' if S.x != S.y else f'`x == y = {S.x}`：同一个约数，不能算两遍'),
        'end_x = get': '对约数 `{B.y}`：在树 `f[{B.y}]` 里数比 `{B.x}` 小的数结尾的序列数 `+1`',
        'add(y, x, end_x)': '以 `{B.v}` 结尾有 `end_x = {B.end_x}` 个 → 记进 `f[{B.y}]` 的位置 `{B.x}`',
        'tot[y] += end_x': '`tot[{y}]` 累加 `{end_x}` → =={tot[y]}==',
        'res = 0': '统计完毕。接下来 ==从大到小== 容斥：`v` 减去它的所有更大倍数',
        'tot[v] -= tot[x]': '`{x}` 是 `{v}` 的倍数：GCD 是 `{x}` 的子序列被多算了 → 减 `tot[{x}]`，`tot[{v}]` = =={tot[v]}==',
        'delta = tot[v] * v': '恰好 GCD 为 `{v}` 的有 `{tot[v]}` 个，美丽值 `{v} × {tot[v]} = {delta}`',
        'res += delta': '累加：`res` → =={res}==',
        'return res': '所有美丽值之和 = =={ret}==',
    },
    skip=[4, 5, 6, 7, 9, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 36, 37, 42, 43, 44, 50, 51, 54, 55],
    cards=dict(
        one_liner='每个约数一棵树状数组，从大到小减去倍数，得到「恰好」',
        complexity='时间约 `O(R·log m)`（`R` 为所有元素约数总数），空间 `O(m log m)`',
        problem=['对每个正整数 `g`，数 GCD ==恰好为 g== 的严格递增子序列个数，乘以 `g` 后全部相加，对 `10^9+7` 取模','`n <= 10^4`，`nums[i] <= 7×10^4`','本视频：`[2,4]` → `8`（`[2]`、`[4]`、`[2,4]` 的 GCD 分别是 2、4、2）'],
        quote='使用以v为公约数的合法子序列数目，减去所有以2v、3v、...、kv为最大公约数的合法子序列数目，就是以v为最大公约数的合法子序列数目了。',
        quote_src='—— yiduobo 题解原文',
        idea=['参考 3312 题：先数「公约数是 v 的倍数」的子序列，再从大到小减去 `2v、3v、…`','数严格递增子序列用「按值域的树状数组」：以 `x` 结尾的个数 = `1 + 比 x 小的各值个数之和`','不为每个约数单独建数组，而是直接建 `ma // g` 大小的树，遍历 `nums` 时对每个约数的树做更新'],
        summary=['时间约 `O(R·log m)`，`R` 是所有元素的约数总数；找约数还有 `O(n·sqrt(m))`','`get` 和 `add` 里每一步都取模；容斥减法后用 `if tot[v] < 0: += mod` 保持非负','`x != y` 判断防止完全平方数的约数被算两遍','视频里把树状数组内部循环折叠了，只展示每次更新后的各棵树','原文本身是 Python 3 可运行的写法，代码未做修改；灵神把元素除以 `g` 后做同样的事']
    ),
)
