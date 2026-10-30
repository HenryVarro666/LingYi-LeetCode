COST = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]


def _text(S):
    f, i = S.get('f'), S.get('i')
    if f is None:
        return '`f[i]`：从 0 或 1 ==爬到台阶 i== 的最小花费；楼顶是台阶 `n`，不是 `n-1`'
    if i is None:
        return '`f[0] = f[1] = 0`：一开始就站在 0 或 1 上，不用花钱'
    c = S['cost']
    a, b = f[i - 1] + c[i - 1], f[i - 2] + c[i - 2]
    return (f'`f[{i}] = min(f[{i - 1}] + cost[{i - 1}], f[{i - 2}] + cost[{i - 2}])`'
            f' = `min({f[i - 1]} + {c[i - 1]}, {f[i - 2]} + {c[i - 2]})` = `min({a}, {b})` = =={min(a, b)}==')


def _fcolor(S, k, v):
    i = S.get('i')
    if i is None:
        return 'green' if k <= 1 else None
    if k == i:
        return 'yellow'
    if k in (i - 1, i - 2):
        return 'blue'
    return 'green' if k < i else None


def _fdim(S, k, v):
    i = S.get('i')
    return i is not None and k > i


def _cost_color(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    return 'pink' if k in (i - 1, i - 2) else None


def _stairs(cv, S, B, box, T):
    """台阶示意：和下面的 f 数组同列对齐；黄 = 台阶 i，绿箭头 = 更省的最后一步"""
    x0, y0, x1, y1 = box
    n = len(S['cost'])
    width = x1 - x0 - 40
    cell = min(80, width / (n + 1))
    sx = x0 + 20 + (width - cell * (n + 1)) / 2
    base, hstep = y1 - 8, (y1 - y0 - 70) / (n + 1)
    i = S.get('i')
    for k in range(n + 1):
        X = sx + k * cell
        top = base - (k + 1) * hstep
        c = T['yellow'] if k == i else ((52, 60, 72) if i is None or k < i else (34, 39, 47))
        cv.rect((X + 1, top, X + cell - 1, base), fill=c, r=3)
    cv.text((sx + n * cell + cell / 2, base - (n + 1) * hstep - 6), '楼顶', 20, T['yellow'], anchor='mb', bold=True)
    cv.text((x0 + 18, y0 + 4), '台阶 0..n（楼顶 = n）', 22, T['muted'], bold=True)
    if i is None or 'f' not in S:
        return
    f, c = S['f'], S['cost']
    one, two = f[i - 1] + c[i - 1], f[i - 2] + c[i - 2]
    for src, val, other in ((i - 1, one, two), (i - 2, two, one)):
        good = val <= other
        p0 = (sx + src * cell + cell / 2, base - (src + 1) * hstep - 4)
        p1 = (sx + i * cell + cell / 2 - 4, base - (i + 1) * hstep - 4)
        mid = cv.arc_arrow(p0, p1, 10 + 32 * (i - src), T['green'] if good else T['dim'], 3, 11)
        cv.text((mid[0], mid[1] - 4), f'+{c[src]}', 19, T['green'] if good else T['dim'], anchor='mb', bold=True)


def _cap_for(S, B, ret):
    if 'i' in B and B.i == S.i:
        return f'`f` 填完了：`f[{len(S.f) - 1}]` 就是爬到楼顶的最小花费'
    i = S.i
    return f'算 `f[{i}]`：最后一步要么从 `{i - 1}` 爬 1 级，要么从 `{i - 2}` 爬 2 级'


def _cap_f(S, B, ret):
    i, f, c = S.i, S.f, S.cost
    a, b = f[i - 1] + c[i - 1], f[i - 2] + c[i - 2]
    if a < b:
        how = f'从 `{i - 1}` 爬 1 级更省（`{a} < {b}`）'
    elif b < a:
        how = f'从 `{i - 2}` 爬 2 级更省（`{b} < {a}`）'
    else:
        how = f'两种一样（都是 `{a}`）'
    return f'{how} → `f[{i}] =` =={f[i]}=='


CONFIG = dict(
    num=746, title='使用最小花费爬楼梯', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='从记忆化搜索到递推',
    tags=['字节30天'],
    code='''
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        f = [0] * (n + 1)
        for i in range(2, n + 1):
            f[i] = min(f[i - 1] + cost[i - 1], f[i - 2] + cost[i - 2])
        return f[n]
''',
    call=f'Solution().minCostClimbingStairs({COST})',
    expect=6,
    views=[
        dict(type='text', fn=_text, h=96, size=26),
        dict(type='custom', draw=_stairs, h=190),
        dict(type='array', var='cost', label='cost[i]：从台阶 i 往上爬要付的钱（粉 = 这一步可能付的）', cell=80,
             color=_cost_color, h=170),
        dict(type='array', var='f', label='f[i]：爬到台阶 i 的最小花费（黄 = 正在算，蓝 = 依赖的两个状态）', cell=80,
             pointers={'i': 'yellow'}, color=_fcolor, dim=_fdim, h=230),
    ],
    watch=[('n', 'n'), ('i', 'i', 'yellow'), ('f[i]', 'f[i]', 'green'), ('f[n]', 'f[n]', 'green')],
    captions={
        'n = len': '`n = {n}`：台阶编号 `0..{n}`，==楼顶是 {n}==',
        'f = [0] * (n + 1)': '`f` 开 `n + 1 = {n + 1}` 个：`f[0] = f[1] = 0` 翻译自递归边界 `dfs(0) = dfs(1) = 0`',
        'for i in range': _cap_for,
        'f[i] = min(': _cap_f,
        'return f[n]': '答案 `f[{n}]` 翻译自递归入口 `dfs(n)`：返回 =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一步爬了 1 级还是 2 级，把问题缩小成子问题',
        complexity='时间 `O(n)`，空间 `O(n)`（可优化到 `O(1)`）',
        problem=['`cost[i]` 是从第 `i` 级台阶向上爬要付的钱，付完可以爬 ==1 级或 2 级==',
                 '可以从下标 0 或 1 出发，求爬到==楼顶（下标 n）==的最小花费',
                 '示例：`cost = [1,100,1,1,1,100,1,1,100,1]` → `6`'],
        quote='枚举最后一步爬了几个台阶，分类讨论……这两种情况都会把原问题变成一个==和原问题相似的、规模更小的子问题==，所以可以用递归解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i)`：从 0 或 1 爬到 `i` 的最小花费',
              '最后一步爬 1 级：`dfs(i-1) + cost[i-1]`；爬 2 级：`dfs(i-2) + cost[i-2]`，取 min',
              '记忆化搜索 ==1:1 翻译成递推==：`dfs` 换成数组 `f`，边界 `f[0] = f[1] = 0`'],
        summary=['时间 `O(n)`，空间 `O(n)`；只依赖前两个状态 → 可滚动成 `f0, f1`，空间 `O(1)`',
                 '易错：楼顶是下标 `n`（数组外面），`f` 要开 `n + 1` 个',
                 '`f[0] = f[1] = 0`：起点不花钱，钱是==离开==台阶时付的',
                 '题解的完整路线：递归（`O(2^n)` 超时）→ `@cache` 记忆化 → 递推 → 空间优化'],
    ),
)
