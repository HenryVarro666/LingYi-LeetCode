def _mat(S):
    return S.get('a') or S.get('m') or [[0] * 26 for _ in range(26)]


def _res(S):
    r = S.get('res') or S.get('f0')
    return [row[0] for row in r] if r else [0] * 26


def _info(S):
    n = S.get('n')
    if 'res' not in S or n is None:
        return '`f[i][j] = Σ f[i-1][(j+1 .. j+nums[j]) mod 26]`：字母 j 替换 i 次后的长度；矩阵 `m[i][j] = 1` 表示 i 变成 j'
    return f'剩余次数 `t = {n}`（二进制 `{bin(n)[2:] if n else "0"}`）；`res` = 各字母已累积的 `M^…` × 全 1 向量'


CONFIG = dict(
    num=3337, title='字符串转换后的长度 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='矩阵快速幂优化 DP',
    tags=['难度分 2412'],
    code='''
MOD = 1_000_000_007

# a @ b，其中 @ 是矩阵乘法
def mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[sum(x * y for x, y in zip(row, col)) % MOD for col in zip(*b)]
            for row in a]

# a^n @ f0
def pow_mul(a: List[List[int]], n: int, f0: List[List[int]]) -> List[List[int]]:
    res = f0
    while n:
        if n & 1:
            res = mul(a, res)
        a = mul(a, a)
        n >>= 1
    return res

class Solution:
    def lengthAfterTransformations(self, s: str, t: int, nums: List[int]) -> int:
        SIZE = 26
        f0 = [[1] for _ in range(SIZE)]
        m = [[0] * SIZE for _ in range(SIZE)]
        for i, c in enumerate(nums):
            for j in range(i + 1, i + c + 1):
                m[i][j % SIZE] = 1
        mt = pow_mul(m, t, f0)

        ans = 0
        for ch, cnt in Counter(s).items():
            ans += mt[ord(ch) - ord('a')][0] * cnt
        return ans % MOD
''',
    call='Solution().lengthAfterTransformations("abcyy", 5, [1]*25 + [2])',
    expect=7,
    skip=['return [[sum', 'for row in a]', 'for i, c in enumerate', 'for j in range(i + 1', 'm[i][j % SIZE]'],
    max_steps=60,
    views=[
        dict(type='text', fn=_info, size=22, h=90),
        dict(type='table', var=_mat, label='a（26×26 系数矩阵：蓝格 = 1，行 i 列 j 表示 i → j）', h=520, cell=19, values=False,
             color=lambda S, i, j, v: 'blue' if v else None),
        dict(type='array', var=_res, label='res（26 个字母的 f 值，a 到 z）', h=130, cell=34),
    ],
    watch=[('t / n', 'n', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'SIZE = 26': '字母表大小 `26`',
        'f0 = ': '`F[0]`：长为 26 的全 1 列向量，对应 `f[0][j] = 1`（不替换时每个字母长度为 1）',
        'm = [[0]': '先造 26×26 的全 0 矩阵 `M`',
        'mt = pow_mul': '把 `m[i][j%26] = 1` 填好后（每个字母 i 变成后面 `nums[i]` 个字母，`z` 之后回绕），求 `M^t @ F[0]`',
        'res = f0': '`res` 先放 `F[0]`，相当于 `M^0 @ F[0]`',
        'while n': lambda S, B, r: (f'`t = {S.n}` 还没用完 → 看最低位' if S.n else '次数用完了，`res = M^t @ F[0]`，`res[j]` 就是字母 j 替换 t 次后的长度'),
        'if n & 1': lambda S, B, r: ('`n & 1 = 1`：最低位是 1 → ==把当前 a（M 的 2^k 次幂）乘进 res==' if S.n & 1
                                     else '`n & 1 = 0`：最低位是 0 → 这一块不用'),
        'res = mul(a, res)': '`res = a @ res`：多走 `2^k` 次替换',
        'a = mul(a, a)': '`a` 自乘：一次走 `2^k` 步变成一次走 `2^(k+1)` 步',
        'n >>= 1': '`n` 右移一位 → {n}',
        'return res': '返回 `M^t @ F[0]`',
        'ans = 0': '`ans` 累加：每个字母的长度 × 它在 `s` 里出现的次数',
        'for ch, cnt': lambda S, B, r: (f'字母 `{S.ch}` 在 `s` 中出现 `{S.cnt}` 次' if S.get('ch') != B.get('ch') else '所有字母都累加完了'),
        'ans += mt': '`ans += mt[{ord(ch) - 97}][0] * {cnt}` = `{mt[ord(ch) - 97][0]} × {cnt}` → =={ans}==',
        'return ans': '最终长度 `{ans}` 对 `10^9+7` 取模 = =={ret}==',
    },
    cards=dict(
        one_liner='先算每个字母替换 t 次的长度，递推写成矩阵再快速幂',
        complexity='时间 `O(n + 26^3 · log t)`，空间 `O(26^2)`',
        problem=['`s` 的每个字符每次被替换为后面 `nums[c]` 个字母（`z` 后回绕），做 `t` 次',
                 '求最终字符串长度，对 `10^9+7` 取模，`t` 最大 `10^9`',
                 '本视频：`s = "abcyy", t = 5`，`nums` 只有 `z` 为 2，其余为 1 → `7`'],
        quote='定义 f[i][j] 表示字母 j 替换 i 次后的长度。……F[t] = M^t × F[0]，其中 F[0] 是一个长为 26 的列向量，值全为 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` = 字母 j 替换 i 次后的长度 = 它变成的各字母再替换 `i-1` 次的长度之和',
              '`m[i][j%26] = 1` 表示 i 会变成 j，于是 `F[t] = M^t × F[0]`',
              '`F[0]` 全 1，所以 `res[j]` 就是 `M^t` 第 j 行之和；答案 = 各字母 `res × 出现次数`'],
        summary=['时间 `O(n + 26^3 log t)`，空间 `O(26^2)`',
                 '易错：下标要 `% 26` 回绕；矩阵相乘每步都要取模，最后 `ans` 再取模',
                 '`F[0]` 全 1，不需要单独乘个数向量，最后用 `Counter(s)` 加权求和',
                 '灵神还给了 Berlekamp-Massey + Kitamasa 写法，把 26^3 降为 26^2']
    ),
)
