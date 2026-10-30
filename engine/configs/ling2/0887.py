K, N = 3, 14


def _hist(i):
    rows = [[0] * (K + 1)]
    for _ in range(i):
        p = rows[-1]
        rows.append([0] + [p[j] + p[j - 1] + 1 for j in range(1, K + 1)])
    return rows


def _table(S):
    """二维表 f[i][j]：前 i-1 行已完成；第 i 行只显示已经更新过的格子（倒序更新，j 从大到小）"""
    i, f = S.get('i'), S.get('f')
    if f is None:
        return None
    if i is None:
        return [list(f)]
    h = _hist(i)
    cur = [h[i][j] if j >= 1 and f[j] == h[i][j] else None for j in range(K + 1)]
    cur[0] = 0
    return h[:i] + [cur]


def _tcolor(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return None
    if S.get('_line') == 6:
        if (r, c) == (i, j):
            return 'yellow'
        if (r, c) == (i - 1, j):
            return 'blue'
        if (r, c) == (i - 1, j - 1):
            return 'pink'
    if S.get('_line') == 7 and (r, c) == (i, K):
        return 'green' if v is not None and v >= N else 'red'
    return None


def _fcolor(S, idx, v):
    i, f = S.get('i'), S.get('f')
    if i is None or idx == 0:
        return None
    h = _hist(i)
    if f[idx] == h[i][idx]:
        return 'green'
    return None


def _cap_f(S, B, ret):
    j = S.j
    a, b = B.f[j], B.f[j - 1]
    return (f'`f[{j}] = {a} + {b} + 1 = {S.f[j]}`：在第 `{b} + 1` 层扔，碎了管下面 `{b}` 层（少一枚蛋），'
            f'没碎管上面 `{a}` 层')


CONFIG = dict(
    num=887, title='鸡蛋掉落', difficulty='Hard', category='多维动态规划',
    author='灵茶山艾府', technique='反向思考 · 次数 i 和蛋数 j 能确定多少层',
    tags=['字节30天'],
    code='''
class Solution:
    def superEggDrop(self, k: int, n: int) -> int:
        f = [0] * (k + 1)
        for i in count(1):  # 从 1 开始枚举 i
            for j in range(k, 0, -1):
                f[j] += f[j - 1] + 1
            if f[k] >= n:
                return i
''',
    setup='from itertools import count',
    call=f'Solution().superEggDrop({K}, {N})',
    expect=4,
    skip=['for j in range'],
    views=[
        dict(type='text', h=60, size=25, fn=lambda S: '`f[i][j]`：==i 次操作、j 枚鸡蛋==，最多能确定 f 值的楼层数（表格 = 一维 f 的历史）'),
        dict(type='grid', var=_table, label='f[i][j]（行 = 操作次数 i，列 = 鸡蛋数 j；黄 = 正在算，蓝 = 没碎，粉 = 碎了）',
             rows=lambda S: list(range(len(_table(S) or []))), cols=list(range(K + 1)), cell=88, h=400, color=_tcolor),
        dict(type='array', var='f', label='一维数组 f（绿 = 已更新为第 i 行，其余仍是第 i−1 行）', cell=88, h=172,
             pointers={'j': 'yellow'}, color=_fcolor),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'yellow'), ('f[k]', 'f[k]', 'green'), ('n', 'n')],
    captions={
        'f = [0] * (k + 1)': '`f[j]`：用 j 枚蛋能确定的最大楼层数；0 次操作什么都确定不了 → 全 0',
        'for i in count(1)': lambda S, B, ret: f'操作次数 `i = {S.i}`：==倒序==枚举 j，就地把第 i−1 行更新成第 i 行',
        'f[j] += f[j - 1] + 1': _cap_f,
        'if f[k] >= n': lambda S, B, ret: (f'`f[{S.k}] = {S.f[S.k]} ≥ n = {S.n}`：`{S.i}` 次操作已经够用' if S.f[S.k] >= S.n
                                           else f'`f[{S.k}] = {S.f[S.k]} < n = {S.n}`：`{S.i}` 次还不够，再多给一次'),
        'return i': '首个满足 `f[k] ≥ n` 的 `i` 就是答案：返回 `{ret}`',
    },
    cards=dict(
        one_liner='反过来想：给定操作次数和鸡蛋数，最多能确定多少层？',
        complexity='时间 `O(k*ans)`（`ans` 为答案，即操作次数），空间 `O(k)`',
        problem=['`k` 枚相同的鸡蛋、`n` 层楼，存在 `f`：高于 `f` 层扔下会碎，否则不碎',
                 '碎了的蛋不能再用；求确定 `f` 的==最坏情况下的最小操作次数==',
                 '示例：`k = 1, n = 2` → `2`；`k = 2, n = 6` → `3`；`k = 3, n = 14` → `4`（本视频）'],
        quote='在 dfs(i−1,j−1)+1 楼扔第一枚鸡蛋：如果鸡蛋碎了，接下来只需要在 [1,dfs(i−1,j−1)] 中扔鸡蛋……如果鸡蛋没碎，问题变成在有 i−1 次操作机会和 j 枚鸡蛋的情况下……',
        quote_src='—— 灵茶山艾府题解「状态定义与状态转移方程」',
        idea=['`dfs(i, j)` = i 次操作、j 枚蛋最多能确定的层数：`dfs(i−1, j) + dfs(i−1, j−1) + 1`',
              '边界 `dfs(0, j) = dfs(i, 0) = 0`；枚举 `i = 1, 2, …`，首个 `dfs(i, k) ≥ n` 即答案',
              '空间优化：`f[j] += f[j−1] + 1`，==j 倒序==，保证 `f[j−1]` 还是上一轮的值'],
        result='`f[3] = 14 ≥ 14` → 返回 `4`：4 次操作、3 枚蛋恰好能确定 14 层',
        summary=['时间 `O(k*ans)`：每个操作次数 i 更新一遍 f；空间 `O(k)`',
                 '关键：把“求最少次数”反过来变成“给定次数能管多少层”，转移变成简单加法',
                 '易错：一维写法 `j` 必须==倒序==（同 0-1 背包），正序会用到本轮已更新的 `f[j−1]`',
                 '题解还给了记忆化搜索和二维递推，三者状态与转移完全相同'],
    ),
)
