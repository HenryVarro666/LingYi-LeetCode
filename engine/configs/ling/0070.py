def _legend(cv, box, T, items):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in items:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 36


def _f_color(S, i, v):
    if 'i' not in S:
        return 'green' if i <= 1 and S.get('f', [0, 0])[1] == 1 else None
    if i == S['i']:
        return 'green'
    if i == S['i'] - 1:
        return 'blue'
    if i == S['i'] - 2:
        return 'cyan'
    return None


def _stairs(cv, S, B, box, T):
    f = S.get('f')
    if not f:
        return
    x0, y0, x1, y1 = box
    n = len(f) - 1
    cur = S.get('i')
    done = cur if cur is not None else (1 if f[1] == 1 else -1)
    cv.text((x0 + 18, y0 + 4), '楼梯：到第 i 阶 = 从 i-1 爬 1 阶 + 从 i-2 爬 2 阶', 24, T['muted'], bold=True)
    w = (x1 - x0 - 80) / (n + 1)
    hh = (y1 - y0 - 120) / max(1, n)
    base = y1 - 30

    def top(i):
        return base - 12 - i * hh

    for i in range(n + 1):
        X = x0 + 40 + i * w
        c = T['panel2']
        if cur is not None and i == cur:
            c = T['green']
        elif cur is not None and i == cur - 1:
            c = T['blue']
        elif cur is not None and i == cur - 2:
            c = T['cyan']
        cv.rect((X, top(i), X + w, base), fill=c, outline=T['border'], width=1, r=4)
        cv.text((X + w / 2, base + 4), f'{i}', 18, T['dim'], anchor='mt', mono=True)
        if i <= done:
            cv.text((X + w / 2, top(i) - 4), f'{f[i]}', 26, T['text'], anchor='mb', bold=True)
    if cur is not None and cur >= 2:
        cx = lambda i: x0 + 40 + i * w + w / 2
        cv.arc_arrow((cx(cur - 1), top(cur - 1) - 34), (cx(cur) - 8, top(cur) - 34), 26, T['blue'], 3, 12)
        cv.arc_arrow((cx(cur - 2), top(cur - 2) - 34), (cx(cur) + 8, top(cur) - 34), 60, T['cyan'], 3, 12)


def _formula(S):
    if 'i' not in S:
        if S.get('f', [0, 0])[1] != 1:
            return '`f[i]` 和 `dfs(i)` 定义相同：从 0 爬到 `i` 有多少种方法'
        return '初始值：`f[0] = f[1] = 1`（翻译自递归边界 `dfs(0) = dfs(1) = 1`）'
    i, f = S['i'], S['f']
    return f"`f[{i}] = f[{i - 1}] + f[{i - 2}]` = {f[i - 1]} + {f[i - 2]} = =={f[i - 1] + f[i - 2]}=="


CONFIG = dict(
    num=70, title='爬楼梯', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 → 1:1 翻译成递推',
    code='''
class Solution:
    def climbStairs(self, n: int) -> int:
        f = [0] * (n + 1)
        f[0] = f[1] = 1
        for i in range(2, n + 1):
            f[i] = f[i - 1] + f[i - 2]
        return f[n]
''',
    call='Solution().climbStairs(7)',
    expect=21,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='f', label='f[i] = 爬到第 i 阶的方案数（= dfs(i)）',
             pointers={'i': 'orange'}, color=_f_color,
             dim=lambda S, i, v: i > S.get('i', 1), h=200, cell=96),
        dict(type='custom', draw=lambda cv, S, B, box, T: _legend(cv, box, T, [
            ('green', '当前要算的 f[i]'), ('blue', 'f[i-1]：最后一步爬 1 阶'), ('cyan', 'f[i-2]：最后一步爬 2 阶')]), h=50),
        dict(type='custom', draw=_stairs, h=330),
    ],
    watch=['n', ('i', 'i', 'orange'), ('f[i-1]', 'f[i-1]', 'blue'), ('f[i-2]', 'f[i-2]', 'cyan')],
    captions={
        'f = [0]': '开一个长为 `n+1 = {n+1}` 的数组：`f[i]` 的定义和 `dfs(i)` 完全一样',
        'f[0] = f[1]': '递归边界 `dfs(0)=dfs(1)=1` → 初始值 `f[0]=f[1]=1`：==原地不动也算一种==',
        'for i in': lambda S, B, ret: (f'从小到大枚举 `i = {S.i}`：算它要用的 `f[{S.i - 1}]`、`f[{S.i - 2}]` ==都已经算好了=='
                                       if B.get('i') != S.i else '`i` 已到 `n`，枚举结束'),
        'f[i] = f[i - 1]': '最后一步爬 1 阶有 `f[{i-1}]={f[i-1]}` 种，爬 2 阶有 `f[{i-2}]={f[i-2]}` 种 → 加法原理：`f[{i}]` = =={f[i]}==',
        'return f[n]': '递归入口 `dfs(n)` → 答案 `f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='最后一步爬 1 阶还是 2 阶？分类讨论，再把递归 1:1 翻译成递推',
        complexity='时间 `O(n)`，空间 `O(n)`（可优化到 `O(1)`）',
        problem=['每次可以爬 `1` 或 `2` 个台阶，爬到第 `n` 阶有多少种不同方法？',
                 '示例：`n = 3` → `3`（1+1+1、1+2、2+1）',
                 '演示：`n = 7` → `21`'],
        before=[dict(heading='第一步：寻找子问题，写出记忆化搜索', chapter='② 思路', lines=[
            '最后一步爬 1 阶：先爬到 `i-1`；爬 2 阶：先爬到 `i-2`',
            '定义 `dfs(i)` = 从 0 爬到 `i` 的方案数 → `dfs(i) = dfs(i-1) + dfs(i-2)`',
            '边界 `dfs(0) = dfs(1) = 1`，入口 `dfs(n)`',
            '先 1 后 2、先 2 后 1 都会递归到 `dfs(i-3)`：==重复调用== → `@cache` 记忆化，`O(2^n)` → `O(n)`',
        ])],
        quote='我们可以去掉递归中的「递」，只保留「归」的部分，即自底向上计算。==f[i] 的定义和 dfs(i) 的定义是一样的==。',
        quote_src='—— 灵茶山艾府题解 · 1:1 翻译成递推',
        idea_heading='第二步：1:1 翻译成递推',
        idea=['`dfs(i)` → `f[i]`；递归调用 → ==从小到大的循环==，状态转移方程原样照抄',
              '递归边界 `dfs(0)=dfs(1)=1` → 初始值 `f[0]=f[1]=1`',
              '递归入口 `dfs(n)` → 答案 `f[n]`'],
        after=[dict(heading='第三步：空间优化', lines=[
            '算出 `f[i]` 后，`f[i-2]` 及其左边的状态==再也用不到了==',
            '只记「上上一个」`f0` 和「上一个」`f1`：`new_f = f1 + f0`，然后 `f0 = f1`，`f1 = new_f`',
            '空间 `O(n)` → `O(1)`；进一步还能用矩阵快速幂做到 `O(log n)`',
        ])],
        summary=['时间 `O(n)`；`f` 数组空间 `O(n)`，滚动变量 `O(1)`',
                 '`f[0]` ==是 1 不是 0==：否则 `f[2] = 1`，但爬到 2 阶明明有两种',
                 '循环从 `i = 2` 开始，数组长度是 `n + 1`（答案在 `f[n]`）',
                 '套路：子问题 → 记忆化搜索 → 1:1 翻译成递推 → 空间优化'],
    ),
)
