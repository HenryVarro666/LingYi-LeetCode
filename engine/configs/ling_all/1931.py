M = 2
NCOL = {0: 'red', 1: 'green', 2: 'blue'}


def _digits(c, m=M):
    return [c // 3 ** k % 3 for k in range(m)]


def _col(cv, T, x, y, c, w=44, h=44, outline=None, m=M):
    for k, d in enumerate(_digits(c, m)):
        cv.rect((x, y + k * (h + 3), x + w, y + k * (h + 3) + h), fill=T[NCOL[d]], r=6, outline=outline, width=4 if outline else 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    valid = S.get('valid') or []
    nxt = S.get('nxt')
    line = S.get('_line', 0)
    cv.text((x0 + 18, y0 + 4), 'valid：合法的一列（红绿蓝 = 0/1/2 三进制数），下方数字是它在 valid 中的下标', 22, T['muted'], bold=True)
    n = max(len(valid), 1)
    cw = min(110, (x1 - x0 - 40) / max(n, 6))
    sx = x0 + 30
    top = y0 + 50
    cur_j = S.get('j') if 'f' in S or (nxt is not None and 'i' in S and line >= 16) else None
    cur_i = S.get('i') if nxt is not None and 'i' in S and line >= 16 else None
    hi = set()
    if nxt is not None and cur_j is not None and cur_j < len(nxt):
        hi = set(nxt[cur_j]) if 'f' in S else set()
    for idx, c in enumerate(valid):
        X = sx + idx * cw
        ol = None
        if 'f' in S and cur_j == idx:
            ol = T['pink']
        elif 'f' in S and idx in hi:
            ol = T['yellow']
        elif 'f' not in S and nxt is not None and cur_i == idx:
            ol = T['pink']
        elif 'f' not in S and nxt is not None and 'j' in S and S.get('j') == idx and line >= 16:
            ol = T['yellow']
        _col(cv, T, X, top, c, outline=ol)
        cv.text((X + 22, top + 2 * 47 + 12), idx, 24, T['pink'] if ol == T['pink'] else T['yellow'] if ol else T['dim'], anchor='mt', mono=True, bold=bool(ol))
    if 'f' in S and cur_j is not None:
        cv.text((x0 + 20, y1 - 28), '粉 = 第 i 列的状态 j；黄 = 它左/右相邻一列可以选的状态 nxt[j]', 22, T['muted'])


CONFIG = dict(
    num=1931, title='用三种不同颜色为网格涂色', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='轮廓线 DP · 三进制状压（递推）',
    tags=['灵神题单', '难度分 2170'],
    code='''
class Solution:
    def colorTheGrid(self, m: int, n: int) -> int:
        pow3 = [3 ** i for i in range(m)]
        valid = []
        for color in range(3 ** m):
            for i in range(1, m):
                if color // pow3[i] % 3 == color // pow3[i - 1] % 3:  # 相邻颜色相同
                    break
            else:  # 没有中途 break，合法
                valid.append(color)

        nv = len(valid)
        nxt = [[] for _ in range(nv)]
        for i, color1 in enumerate(valid):
            for j, color2 in enumerate(valid):
                for p3 in pow3:
                    if color1 // p3 % 3 == color2 // p3 % 3:  # 相邻颜色相同
                        break
                else:  # 没有中途 break，合法
                    nxt[i].append(j)

        MOD = 1_000_000_007
        f = [[0] * nv for _ in range(n)]
        f[0] = [1] * nv  # dfs 的递归边界就是 DP 数组的初始值
        for i in range(1, n):
            for j in range(nv):
                f[i][j] = sum(f[i - 1][k] for k in nxt[j]) % MOD
        return sum(f[-1]) % MOD  # 递归入口就是答案
''',
    call=f'Solution().colorTheGrid({M}, 2)',
    expect=18,
    skip=['for color in range', 'for i in range(1, m)', 'if color //', 'break', 'else:', 'for i, color1', 'for j, color2', 'for p3 in pow3',
          'if color1 //', 'for i in range(1, n)', 'for j in range(nv)', 'nv = len', 'MOD = '],
    max_steps=48,
    views=[
        dict(type='custom', draw=_draw, h=260),
        dict(type='table', var='f', label='f[i][j]：前 i+1 列、第 i 列状态为 valid[j] 的方案数', h=250, cell=100),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('nv', lambda S: len(S['valid']) if 'valid' in S else '', 'green')],
    captions={
        'pow3 = [': '`pow3[k] = 3^k`：用来取三进制数的第 `k` 位，共 `m = {m}` 位',
        'valid.append': lambda S, B, r: f'三进制数 `{S.color}` = 各位 `{" ".join(map(str, _digits(S.color)))}`：相邻两位都不同 → ==合法==，记入 `valid`（共 {len(S.valid)} 个）',
        'nxt = [[]': '`nxt[i]`：和 `valid[i]` 相邻的下一列，可以选哪些 `valid[j]`',
        'nxt[i].append(j)': lambda S, B, r: f'`valid[{S.i}]` 和 `valid[{S.j}]` ==每一行颜色都不同== → `{S.j}` 可以放在它旁边：`nxt[{S.i}] = {S.nxt[S.i]}`',
        'f = [[0]': '`f[i][j]` 对应记忆化的 `dfs(i, j)`，行数 `n = {n}`',
        'f[0] = [1]': '边界：只剩 0 列时只有 1 种方案（每个合法状态各 1 种）',
        'f[i][j] = sum': '`f[{i}][{j}] = Σ f[{i-1}][k]`，`k ∈ nxt[{j}] = {nxt[j]}` → =={f[i][j]}==',
        'return sum': '最后一列选哪个合法状态都行 → 把 `f[n-1]` 求和：=={ret}=='
    },
    cards=dict(
        one_liner='一列看成三进制数：先预处理合法列，再逐列转移',
        complexity='时间 `O(n·4^m)`，空间 `O(4^m + n·2^m)`',
        problem=['`m × n` 的网格，用红、绿、蓝给每个格子涂色，相邻格子颜色不同',
                 '返回涂色方案数（对 `10^9+7` 取模），`1 ≤ m ≤ 5`，`1 ≤ n ≤ 1000`',
                 '示例：`m = 5, n = 5` → `580986`；本视频：`m = 2, n = 2` → `18`'],
        quote='本题有红绿蓝三种颜色，可以分别用 0,1,2 表示，用一个长为 m 的三进制数表示一列的颜色。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一列颜色 = 长为 `m` 的三进制数；列内相邻颜色不同才合法，一共 `3·2^(m-1)` 个',
              '预处理 `nxt[i]`：`valid[i]` 右边那一列有哪些选择（逐位比较都不同）',
              '`f[i][j] = Σ f[i-1][k]`（`k` 取遍 `nxt[j]`），把记忆化搜索 1:1 翻译成递推'],
        summary=['时间 `O(n·4^m)`，空间 `O(4^m + n·2^m)`（滚动数组可降到 `O(4^m)`）',
                 '合法列数 `|valid| = 3·2^(m-1)`；`m = 5` 时才 48 个，状态很少',
                 '`for ... else`：中途没 `break` 才合法；`break` 说明有相邻相同颜色',
                 '`f[0]` 全 1：它就是记忆化搜索的递归边界',
                 '其他写法：记忆化搜索（本写法 1:1 翻译）、`0/1` 转移矩阵快速幂、BM + Kitamasa；双倍经验 1411'],
    ),
)
