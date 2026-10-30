def _bin(S):
    n = S.get('n')
    return n


def _top(S):
    if 'n' not in S or 'queries' not in S:
        return ''
    inner = S.get('_inner', {})
    line = S.get('_line', 0)
    if 'l' in inner and 'r' in inner and 's' in S and len(S['s']) > 1 and 'pow2' in S:
        l, r = inner['l'], inner['r']
        return f"查询 `[{l}, {r}]`：幂次和 = `s[{r + 1}] − s[{l}]` = {S['s'][r + 1]} − {S['s'][l]} = =={S['s'][r + 1] - S['s'][l]}==，答案 = `2^{S['s'][r + 1] - S['s'][l]}`"
    n = S['n']
    return f"剩下的 n = `{bin(n)[2:] if n else '0'}`（二进制），已拆出 {len(S['s']) - 1 if 's' in S else 0} 个 2 的幂"


def _wl(S):
    inner = S.get('_inner', {})
    return inner['l'] if 'l' in inner and 'r' in inner and len(S['s']) > 1 else None


def _wr(S):
    inner = S.get('_inner', {})
    return inner['r'] + 1 if 'l' in inner and 'r' in inner and len(S['s']) > 1 else None


CONFIG = dict(
    num=2438, title='二的幂数组中查询范围内的乘积', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='lowbit 拆分 + 幂次前缀和',
    tags=['灵神题单·位运算', '难度分 1610'],
    code='''
MOD = 1_000_000_007
MX = 436
pow2 = [0] * MX
pow2[0] = 1
for i in range(1, MX):
    pow2[i] = pow2[i - 1] * 2 % 1_000_000_007

class Solution:
    def productQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        s = [0]
        while n:
            lowbit = n & -n
            e = lowbit.bit_length() - 1
            # 直接计算 e 的前缀和
            s.append(s[-1] + e)
            n ^= lowbit
        return [pow2[s[r + 1] - s[l]] for l, r in queries]
''',
    call='Solution().productQueries(45, [[0,1],[2,3],[0,3]])',
    expect=[4, 256, 1024],
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='string', var=lambda S: bin(S['n'])[2:] if S.get('n') else '0', label='n 的二进制（拆掉最低位的 1）', cell=70, h=150),
        dict(type='array', var='s', label='s：幂次 e 的前缀和（s[k] = 前 k 个 e 之和）', cell=90, h=200,
             window=(_wl, _wr)),
        dict(type='array', var=lambda S: S.get('queries'), label='queries', cell=110, h=130),
    ],
    watch=[('n', 'n'), ('lowbit', 'lowbit', 'blue'), ('e', 'e', 'pink'), ('s', 's', 'green')],
    captions={
        'lowbit = n & -n': '`n & -n` 取出最低位的 1：`lowbit = {lowbit}`，它就是 powers 里的下一个数',
        'e = lowbit': '`{lowbit}` = 2^`{e}`，只记幂次 `e = {e}`：乘积变成幂次相加',
        's.append': '前缀和 `s` 追加 `{B.s[-1]} + {e}` = =={s[-1]}==，现在 `s = {s}`',
        'n ^= lowbit': '异或抹掉这一位：`n` 剩 `{n}`' ,
        'while n': lambda S, B, ret: (f'`n = {S.n}` 还有 1 → 继续拆' if S.n else '`n = 0`，拆完了'),
        'return': lambda S, B, ret: f'每个查询 O(1)：`2^(s[r+1] − s[l])` 查表 → =={ret}==',
        's = [0]': '`s` 是幂次前缀和，`s[0] = 0`（空前缀）',
        'pow2[0] = 1': '`pow2[i] = 2^i % MOD`，预处理，幂次和不超过 435',
    },
    skip=['pow2[i] = pow2', 'for i in range(1, MX)', 'MX = 436', 'pow2 = [0]'],
    cards=dict(
        one_liner='2 的幂相乘 = 幂次相加：乘积查询变成前缀和',
        complexity='时间 `O(m + log n)`，空间 `O(log n)`',
        problem=['把 `n` 拆成最少个 2 的幂（即二进制每个 1 一项），升序排成 `powers`',
                 '每个查询 `[l, r]`：求 `powers[l..r]` 的乘积，对 `10^9+7` 取模',
                 '示例：`n=15` → `powers=[1,2,4,8]`，`[0,3]` → `64`；本视频用 `n=45`'],
        quote='计算 powers 子数组的元素积，等价于先计算 e 中对应的子数组和，然后再计算 2 的幂。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`lowbit = n & -n` 依次取出每个 2 的幂，`n ^= lowbit` 去掉它',
              '只记幂次 `e`，子数组乘积 = `2^(e 之和)`，e 的区间和用前缀和',
              '取模后不能直接做前缀积相除；预处理 `pow2` 表就免去逆元'],
        summary=['时间 `O(m + log n)`，预处理 `pow2` 不计入',
                 '`n < 2^30`，幂次和最多 `1+2+…+29 = 435`，所以 `MX = 436`',
                 '前缀和下标：区间 `[l, r]` 的和是 `s[r+1] − s[l]`',
                 '另两种写法：暴力 `reduce(mul)`，或预处理所有子数组积表（`O(log² n)`）'],
    ),
)
