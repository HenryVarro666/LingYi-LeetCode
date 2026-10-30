A0 = [0, 3, 2, 1]
N = len(A0)


def _K(S):
    return S.get('k')


def _J(S):
    return S.get('j') if 'ans' not in S else None


def _ft(S):
    f = S.get('f')
    if f is None:
        return [['∞'] * N for _ in range(1 << N)]
    return [['∞' if v == inf else v for v in row] for row in f]


def _col(S, r, c, v):
    s, j, k = S.get('s'), S.get('j'), S.get('k')
    if 'ans' in S or s is None:
        if 'ans' in S and S.get('s') is not None and r == S['s'] and c == S.get('j'):
            return 'green'
        return None
    if j is not None and r == s and c == j:
        return 'yellow'
    if j is not None and k is not None and r == (s | 1 << k) and c == k:
        return 'blue'
    return None


def _txt(S):
    s, j = S.get('s'), S.get('j')
    if 'ans' in S and s is not None:
        return f'还原方案：从 `s={s:0{N}b}, j={j}` 沿 `g` 走，已得到 `ans = {S["ans"]}`'
    if s is None or j is None:
        return '`f[s][j]`：已填集合为 s、上一个填的是 j 时，剩余数字的最低分数'
    k = S.get('k')
    t = f'`s = {s:0{N}b}`，`j = {j}`'
    if k is not None:
        t += f'，试填 `k = {k}`'
    return t


CONFIG = dict(
    num=3149, title='找出分数最低的排列', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排列型状压 DP · 1:1 翻译成递推 + 输出方案',
    tags=['状压 DP', '输出具体方案', '难度分 2642'],
    code='''
class Solution:
    def findPermutation(self, a: List[int]) -> List[int]:
        n = len(a)
        f = [[inf] * n for _ in range(1 << n)]
        g = [[-1] * n for _ in range(1 << n)]
        for j in range(n):
            f[-1][j] = abs(j - a[0])
        for s in range((1 << n) - 3, 0, -2):  # 注意偶数不含 0，是无效状态
            for j in range(n):
                if s >> j & 1 == 0:  # 无效状态，因为 j 一定在 s 中
                    continue
                for k in range(1, n):
                    if s >> k & 1:  # k 之前填过
                        continue
                    v = f[s | 1 << k][k] + abs(j - a[k])
                    if v < f[s][j]:
                        f[s][j] = v
                        g[s][j] = k  # 记录该状态下填了哪个数

        ans = []
        s = j = 0
        while j >= 0:
            ans.append(j)
            s |= 1 << j
            j = g[s][j]
        return ans
''',
    call=f'Solution().findPermutation({A0})',
    expect=[0, 2, 3, 1],
    skip=['if s >> j & 1 == 0', 'for j in range(n)', 'continue', 'for k in range', 'n = len(a)', 'g = [[-1]', 's = j = 0', 'ans = []'],
    views=[
        dict(type='array', var='a', label='a（下标 = 数字，值 = a[下标]）', cell=60, h=130, pointers={_K: 'pink', _J: 'blue'}, pointer_labels={_K: 'k', _J: 'j'}),
        dict(type='text', fn=_txt, size=22, h=64),
        dict(type='table', var=_ft, label='f[s][j]：行 = s（二进制，最低位是数字 0），列 = j；黄 = 正在算，蓝 = 依赖', h=450, cell=60,
             rows=lambda S: [format(x, f'0{N}b') for x in range(1 << N)], cols=lambda S: [str(x) for x in range(N)], color=_col),
        dict(type='array', var='ans', label='ans', cell=56, h=96),
    ],
    watch=[('s', lambda S: format(S['s'], f'0{N}b') if 's' in S else '', 'cyan'), ('j', 'j', 'blue'), ('k', 'k', 'pink'), ('v', 'v', 'green')],
    captions={
        'f = [[inf]': '`f[s][j]`：已填集合是 s、上一个填的是 j，剩余数字能得到的最低分数；先全设 `inf`',
        'f[-1][j] =': '边界：全部填完（`s = U`），最后一个是 j，只差首尾相接 → `f[U][{j}] = |{j} − a[0]| = {f[-1][j]}`',
        'for s in range': lambda S, B, r: (f'`s = {S.s:0{N}b}`：要先有 `s ∪ {{k}}` 的结果，所以 ==s 从大到小==；偶数不含 0，已跳过' if S.get('s') is not None and S.s != B.get('s', None)
                                          else '所有状态算完，下面从 `s = {0}, j = 0` 出发还原方案'),
        'if s >> k & 1': lambda S, B, r: (f'`k = {S.k}` 之前填过 → 不能再填' if S.s >> S.k & 1 else f'`k = {S.k}` 没填过 → 可以填在 j 后面'),
        'v = f[s | 1 << k][k]': lambda S, B, r: f'`v = f[{S.s | 1 << S.k:0{N}b}][{S.k}] + |{S.j} − a[{S.k}]| = {S.f[S.s | 1 << S.k][S.k]} + {abs(S.j - S.a[S.k])}` = =={S.v}==',
        'if v < f[s][j]': lambda S, B, r: (f'`v = {S.v} < f[s][j] = {S.f[S.s][S.j]}`' if S.v < S.f[S.s][S.j] else f'`v = {S.v}` 不比 `f[s][j] = {S.f[S.s][S.j]}` 小 → 不更新')
                                             .replace('inf', '∞'),
        'f[s][j] = v': lambda S, B, r: f'`f[{S.s:0{N}b}][{S.j}]` 更新为 =={S.v}==',
        'g[s][j] = k': '`g[s][j] = {k}`：记下最优选择；==k 从小到大枚举且严格 < 才更新==，所以同分时字典序最小',
        'while j >= 0': lambda S, B, r: ('`j = -1`：没有后续了，方案还原完毕' if S.j < 0 else '`j >= 0`：继续沿 g 走'),
        'ans.append': '把 `{j}` 加入方案 → `ans = {ans}`',
        's |= 1 << j': lambda S, B, r: f'`s` 加入 {S.j}：`s = {S.s:0{N}b}`',
        'j = g[s][j]': '下一个填 `g[s][j]` = =={j}==',
        'return ans': '分数最低且字典序最小的排列：`{ret}`',
    },
    max_steps=64,
    cards=dict(
        one_liner='循环左移分数不变 → p[0] = 0；剩下的用「集合 + 上一个数」状压 DP',
        complexity='时间 `O(n^2 2^n)`，空间 `O(n 2^n)`',
        problem=['`a` 是 `0..n-1` 的排列，排列 `p` 的分数 = `|p[0]-a[p[1]]| + ... + |p[n-1]-a[p[0]]|`',
                 '求分数最低的 `p`，分数相同取字典序最小',
                 '本视频：`a = [0,3,2,1]` → `[0,2,3,1]`（分数 4）'],
        quote='循环左移后，分数是不变的。推论：题目要计算的字典序最小的排列 p，一定满足 p_0 = 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`p` 循环左移分数不变，所以答案以 0 开头；之后一位一位「枚举选哪个」',
              '前面的顺序不重要，只记==已选集合 s==和==上一个数 j== → `f[s][j]`',
              '`f[s][j] = min_k f[s ∪ {k}][k] + |j − a[k]|`；用 `g[s][j]` 记下 k，再顺着还原方案'],
        summary=['时间 `O(n^2 2^n)`，空间 `O(n 2^n)`',
                 '0 一定在 s 里，所以 s 只会是奇数；k 从 1 枚举，因为 0 已经在开头',
                 '要字典序最小：k 从小到大枚举，只在 `v < f[s][j]` 严格更小时才更新 g',
                 '灵神还给了记忆化搜索（`@cache` + `make_ans` 递归还原），本视频演示最后的递推写法'],
    ),
)
