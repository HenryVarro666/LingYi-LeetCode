from itertools import product as _prod

def _nums(S):
    return [int(''.join(map(str, t))) for t in _prod(range(S['l'], S['r'] + 1), repeat=S['k'])]


def _tab(S):
    l, r, k = S['l'], S['r'], S['k']
    m = r - l + 1
    return [[x * 10 ** i * m ** (k - 1) for i in range(k)] for x in range(l, r + 1)]


CONFIG = dict(
    num=3855, title='给定范围内 K 位数字之和', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贡献法 + 等差/等比求和 + 快速幂',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution:
    def sumOfNumbers(self, l: int, r: int, k: int) -> int:
        MOD = 1_000_000_007
        m = r - l + 1
        return (l + r) * m * (pow(10, k, MOD) - 1) * pow(18, -1, MOD) * pow(m, k - 1, MOD) % MOD
''',
    call='Solution().sumOfNumbers(1, 2, 3)',
    expect=1332,
    views=[
        dict(type='text', size=26, fn=lambda S: '所有 3 位数：' + ' '.join(map(str, _nums(S))) + f'，和 = =={sum(_nums(S))}=='),
        dict(type='table', var=_tab, rows=lambda S: [f'x={x}' for x in range(S['l'], S['r'] + 1)],
             cols=lambda S: [f'10^{i}' for i in range(S['k'])], h=260, cell=120, label='每格 = 第 i 位填 x 的贡献'),
        dict(type='text', size=26, fn=lambda S: ('表格每格 = `x·10^i·m^(k-1)`：第 i 位填 x 时，其余 k-1 位各有 m 种填法' + (f'；`m` 的值是 =={S["m"]}==' if 'm' in S else ''))),
    ],
    watch=['l', 'r', 'k', ('m', 'm', 'blue')],
    captions={
        'MOD = ': '答案对 `10^9+7` 取模',
        'm = r - l': '`m = r - l + 1 = {m}`：每一位有 `m` 种数字可选',
        'return (l': lambda S, B, ret: (f'每个数字 x 在第 i 位上贡献 `x·10^i·m^(k-1)`。对 x 求和（等差）`(l+r)·m/2`，对 i 求和（等比）`(10^k−1)/9`，再乘 `m^(k-1)`；两个除法合并成 `/18`，用逆元 `pow(18, -1, MOD)` 代替 → 返回 =={ret}=='),
    },
    cards=dict(
        one_liner='每一位填 x，贡献就是 x·10^i 乘上其余位的填法数',
        complexity='时间 `O(log k)`（快速幂），空间 `O(1)`',
        problem=['从 `[l, r]` 里为 `k` 位数字的每一位独立选一个数，含 0 则允许前导 0',
                 '求所有这样的数之和，对 `10^9+7` 取模；`k` 最大 `10^9`',
                 '示例：`l=1, r=2, k=2` → `66`；本视频演示 `l=1, r=2, k=3` → `1332`'],
        quote='在从低到高第 i 位上填 x，相当于填了一个 x·10^i。其余 k-1 位，每一位都有 r-l+1 种填法，所以 x 对答案的贡献为 x·10^i·(r-l+1)^(k-1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贡献法：不枚举 `m^k` 个数，而是看「某一位填某个 x」被数了多少次',
              '`x·10^i` 出现 `m^(k-1)` 次；对 `x` 等差求和、对 `i` 等比求和',
              '公式：`(l+r)m/2 · (10^k−1)/9 · m^(k-1)`，除法用逆元，幂用快速幂'],
        after=[dict(heading='公式拆解', lines=[
            '`Σx` = `(l+r)·m / 2`（等差数列）',
            '`Σ10^i` = `(10^k − 1) / 9`（等比数列，即 111…1）',
            '`2 × 9 = 18` → 一次 `pow(18, -1, MOD)` 就是两个除法的逆元',
            '`pow(a, b, MOD)` 是内置快速幂，`b` 为 `10^9` 也只要 30 来步'])],
        summary=['时间 `O(log k)`，空间 `O(1)`',
                 '易错点：`10^k` 和 `m^(k-1)` 要用快速幂，不能直接算',
                 '除以 2 和 9 要用模逆元，`pow(18, -1, MOD)` 需要 Python 3.8+',
                 '答疑：贡献法 = 统计「某个数字」在总和这个式子里出现了多少次'],
    ),
)
