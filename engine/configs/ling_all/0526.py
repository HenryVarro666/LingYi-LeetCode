N = 3


def _bits(s, n=N):
    return '{' + ', '.join(str(j + 1) for j in range(n) if s >> j & 1) + '}'


def _txt(S):
    s = S.get('s')
    if s is None:
        return '`f[S]` = 可选数字集合为 `S` 时的优美排列数；`S` 用二进制表示，最低位 = 数字 1'
    i = S['i'] if 'i' in S else s.bit_count()
    base = f'`S = {s:0{N}b}` = =={_bits(s)}==，要填第 `i = {i}` 个位置'
    j = S.get('j')
    if j is not None and S.get('_line') in (8, 9):
        ok = (s >> (j - 1) & 1) and (i % j == 0 or j % i == 0)
        return base + f'；试 `j = {j}`' + ('：可选且整除' if ok else '：不行')
    return base


def _color(S, k, v):
    s = S.get('s')
    if s is None:
        return None
    if k == s:
        return 'yellow'
    j = S.get('j')
    if j is not None and S.get('_line') == 9 and (s >> (j - 1) & 1) and k == s ^ (1 << (j - 1)):
        return 'green'
    return None


def _cap_if(S, B, ret):
    s, i, j = S.s, S.i, S.j
    if not (s >> (j - 1) & 1):
        return f'`j = {j}` 不在集合 {_bits(s)} 里，不能选'
    if i % j == 0 or j % i == 0:
        return f'`{i}` 和 `{j}` 一个整除另一个 → ==可以把 {j} 放到第 {i} 位=='
    return f'`{i}` 与 `{j}` 互不整除 → 不能放第 {i} 位'


CONFIG = dict(
    num=526, title='优美的排列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='排列型状压 DP · 1:1 翻译成递推',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution:
    def countArrangement(self, n: int) -> int:
        f = [0] * (1 << n)
        f[0] = 1
        for s in range(1, 1 << n):
            i = s.bit_count()
            for j in range(1, n + 1):
                if s >> (j - 1) & 1 and (i % j == 0 or j % i == 0):
                    f[s] += f[s ^ (1 << (j - 1))]
        return f[-1]
''',
    call=f'Solution().countArrangement({N})',
    expect=3,
    skip=['for j in range', 'f = [0]'],
    max_steps=130,
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='f', label='f[S]（下标 = 集合 S 的二进制值；黄 = 当前 S，绿 = 被取走 j 之后的子集）',
             cell=64, h=230, color=_color),
    ],
    watch=[('s', 's', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[s]', 'f[s]', 'green')],
    captions={
        'f[0] = 1': '`f[∅] = 1`：没有数字可填，恰好一种排列（递归边界）',
        'for s in range': lambda S, B, r: (f'`s = {S.s}`：集合更小的状态已算完（`s ^ bit` 一定小于 `s`）→ 从小到大枚举'
                                           if S.get('s') != B.get('s') else '所有集合都算完了'),
        'i = s.bit_count()': '`s` 里有 `{i}` 个数 → 现在要填排列的第 `{i}` 位',
        'if s >> (j - 1)': _cap_if,
        'f[s] +=': lambda S, B, r: (f'`f[{S.s}] += f[{S.s ^ (1 << (S.j - 1))}]` → =={S.f[S.s]}=='
                                    f'（第 {S.i} 位放 {S.j}，剩下集合 {_bits(S.s ^ (1 << (S.j - 1)))}）'),
        'return f[-1]': '全集 `U` 的方案数 `f[U]` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举第 i 位放哪个数；集合代替排列，去掉重复子问题',
        complexity='时间 `O(n·2^n)`，空间 `O(2^n)`',
        problem=['`1..n` 的排列，若每个位置 `perm[i]` 与 `i` 一个能整除另一个，就是优美排列',
                 '求优美排列的数量，`n ≤ 15`',
                 '示例：`n = 2` → `2`；本视频：`n = 3` → `3`'],
        quote='前面的排列具体长啥样，我们并不关心，我们记录的是无序的集合，不是有序的列表。',
        quote_src='—— 灵茶山艾府题解（一、寻找子问题）',
        idea=['`dfs(S)`：可选数字集合为 `S` 时的方案数；位置 `i = |S|`，枚举 `j ∈ S` 且 `i`、`j` 整除关系成立',
              '`f[S] = Σ f[S \\ {j}]`，边界 `f[∅] = 1`，答案 `f[U]`',
              '集合用二进制数表示：最低位 = 数字 1，所以 `S` 从小到大枚举即可 1:1 翻译成递推'],
        summary=['时间 `O(n·2^n)` = 状态数 `2^n` × 单状态转移 `O(n)`；空间 `O(2^n)`',
                 '`i = s.bit_count()` 不必作为参数：集合大小就是当前位置',
                 '灵神还给了记忆化写法（`@cache` + 正向集合 `s | bit`，或反向 `s ^ bit`），本视频用递推',
                 '`int.bit_count` 需要 Python 3.10+，渲染环境满足'],
    ),
)
