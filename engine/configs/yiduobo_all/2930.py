_RH = [f"l{l}e{e}" for l in (0, 1) for e in (0, 1, 2)]


def _tab(name):
    def g(S):
        v = S.get(name)
        if not v or len(v) != 12:
            return [[0, 0]] * 6
        return [[v[l * 6 + e * 2], v[l * 6 + e * 2 + 1]] for l in (0, 1) for e in (0, 1, 2)]
    return g


def _which(S, B):
    if 'f' not in S or 'g' not in S:
        return None
    return [k for k in range(12) if S['f'][k] != B.get('f', S['f'])[k]] if isinstance(B.get('f'), list) and len(B['f']) == 12 else []


def _col(S, i, j, v):
    f = S.get('f')
    if f is None or len(f) != 12:
        return None
    return 'green' if (i, j) == (5, 1) else None


CONFIG = dict(
    num=2930, title='重新排列后包含指定子字符串的字符串数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='计数 DP · 12 种状态 + 滚动数组',
    tags=['灵神题单', '动态规划', '难度分 2227'],
    code='''
class Solution(object):
    def stringCount(self, n):

        mod = 10 ** 9 + 7
        f = [0] * 12
        f[0] = 1
        for i in range(n):
            g = f[:]
            f = [0] * 12

            f[0] = g[0] * 23 % mod
            f[1] = (g[0] + g[1] * 24) % mod
            f[2] = (g[0] + g[2] * 23) % mod
            f[3] = (g[1] + g[2] + g[3] * 24) % mod
            f[4] = (g[2] + g[4] * 24) % mod
            f[5] = (g[3] + g[4] + g[5] * 25) % mod

            f[6] = (g[0] + g[6] * 24) % mod
            f[7] = (g[1] + g[6] + g[7] * 25) % mod
            f[8] = (g[2] + g[6] + g[8] * 24) % mod
            f[9] = (g[3] + g[7] + g[8] + g[9] * 25) % mod
            f[10] = (g[4] + g[8] + g[10] * 25) % mod
            f[11] = (g[5] + g[9] + g[10] + g[11] * 26) % mod
        
        return f[-1]
''',
    call='Solution().stringCount(4)',
    expect=12,
    views=[
        dict(type='table', var=_tab('g'), label='g：上一轮（行 = l、e 的个数档位，列 = t）', rows=_RH, cols=['t0', 't1'], h=330, cell=96),
        dict(type='table', var=_tab('f'), label='f：这一轮（f[11] = 至少 1 个 l、2 个 e、1 个 t）', rows=_RH, cols=['t0', 't1'], h=330, cell=96,
             color=_col),
    ],
    watch=[('i', 'i', 'blue'), ('f[11]', "f[11] if len(f) == 12 else 0", 'green')],
    captions={
        'f = [0] * 12': lambda S, B, r: ('12 种状态：l 取 0/1 个（1 = 至少 1 个）× e 取 0/1/2 个（2 = 至少 2 个）× t 取 0/1 个。下标 = l×6 + e×2 + t' if 'i' not in S
                                         else '清空，准备算新一轮（长度 `i+1`）的 12 个状态'),
        'f[0] = 1': '长度 0 的空串：l、e、t 都是 0 个，1 种',
        'g = f[:]': '拷贝上一轮 `g`，每一轮只依赖上一轮（滚动数组，省掉 i 这一维）',
        'f[0] = g': '`l0 e0 t0`：只能再添 23 个其它字母，`g[0] × 23` = {f[0]}',
        'f[1] = ': '`t1`：上一轮没有 t 时添 t，或已有 t 时添 24 个字母（除 l、e 外加 t 本身）= {f[1]}',
        'f[2] = ': '`e1`：上一轮没有 e 时添 e，或已有 1 个 e 时添 23 个字母 = {f[2]}',
        'f[3] = ': '`e1 t1`：来自 g[1]（加 e）、g[2]（加 t），或原状态再添 24 个字母 = {f[3]}',
        'f[4] = ': '`e2`：e 档位「至少 2 个」：从 1 个再加 e，或本身再添 24 个（含 e）= {f[4]}',
        'f[5] = ': '`e2 t1` = {f[5]}',
        'f[6] = ': '`l1`：l 档位「至少 1 个」：从 0 个加 l，或本身再添 24 个（含 l）= {f[6]}',
        'f[7] = ': '`l1 t1` = {f[7]}',
        'f[8] = ': '`l1 e1` = {f[8]}',
        'f[9] = ': '`l1 e1 t1` = {f[9]}',
        'f[10] = ': '`l1 e2` = {f[10]}',
        'f[11] = ': lambda S, B, r: f'`l1 e2 t1`：目标状态，来自 g[5]、g[9]、g[10]，或 g[11] 再添任意 26 个字母 → ==f[11] = {S.f[11]}==',
        'return f[-1]': '`f[11]` 就是长度为 n 的好字符串个数 =={ret}==',
    },
    cards=dict(
        one_liner='把 l、e、t 的个数压成 2×3×2 = 12 种状态',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['重新排列后能包含 `"leet"` 的字符串是好字符串，只含小写字母',
                 '求长度为 `n` 的好字符串个数（对 `10^9+7` 取模）',
                 '本视频：`n = 4` → `12`'],
        quote='题目实际上就是要求找出长度为n的字符串中，l和t都至少出现一次，e至少出现两次的字符串数量……每个长度为i的字符串只会对应到2*3*2 = 12种状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['l、t 只关心「0 个 / 至少 1 个」，e 只关心「0 / 1 / 至少 2 个」',
              '每种状态：从上一轮「少一个特定字符」的状态加字符，或同状态加一个不改变档位的字符',
              '「至少」档位自己再加字符仍留在原档，所以系数比 23 大：24、25、26'],
        summary=['时间 `O(n)`，空间 `O(1)`（滚动数组）',
                 '12 条转移方程要对准：系数 = 本状态下不改变档位的字母数',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '另可写成矩阵乘法加速，但常数很大；灵神用容斥可做到 `O(log n)`'],
    ),
)
