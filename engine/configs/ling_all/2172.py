NUMS = [2, 3]
SLOTS = 2


_SP = lambda S: S.get('s') if S.get('_line') == 10 else None


def _baskets(S):
    i = S.get('i')
    if i is None:
        return '用二进制 `i` 表示 2×numSlots 个「半篮」里哪些已放了数；第 j 位对应编号 `j//2+1` 的篮子'
    line = S.get('_line')
    def fmt(m):
        out = []
        for b in range(SLOTS):
            cells = ''.join('■' if m >> (2 * b + k) & 1 else '□' for k in range(2))
            out.append(f'篮{b + 1} {cells}')
        return '　'.join(out)
    s = f"状态 `i = {i:0{SLOTS * 2}b}`：{fmt(i)}"
    if 'c' in S and 'j' in S and line in (8, 9, 10):
        s += f"　→　放 `nums[{S['c']}] = {NUMS[S['c']]}` 到空位 `j = {S['j']}`（篮 {S['j'] // 2 + 1}）"
    return s


def _cap_f(S, B, ret):
    c, j = S.c, S.j
    gain = (j // 2 + 1) & NUMS[c]
    old = B.f[S.s]
    return (f'`nums[{c}] = {NUMS[c]}` 放进篮 `{j // 2 + 1}`：得分 `{j // 2 + 1} & {NUMS[c]} = {gain}`，'
            f'`f[{S.i}] + {gain} = {S.fi + gain}`，和旧 `f[{S.s}] = {old}` 取最大 → =={S.f[S.s]}==')


CONFIG = dict(
    num=2172, title='数组的最大与和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状压 DP · 篮子集合 + 前 c 个数',
    tags=['图论算法', '难度分 2392'],
    code='''
class Solution:
    def maximumANDSum(self, nums: List[int], numSlots: int) -> int:
        f = [0] * (1 << (numSlots * 2))
        for i, fi in enumerate(f):
            c = i.bit_count()
            if c >= len(nums): continue
            for j in range(numSlots * 2):
                if (i & (1 << j)) == 0:  # 枚举空篮子 j
                    s = i | (1 << j)
                    f[s] = max(f[s], fi + ((j // 2 + 1) & nums[c]))
        return max(f)
''',
    call=f'Solution().maximumANDSum({NUMS!r}, {SLOTS})',
    expect=4,
    max_steps=42,
    skip=['for j in range', 's = i |', 'c = i.bit_count()'],
    views=[
        dict(type='array', var='f', label='f[i]：篮子集合为 i 时（已放前 popcount(i) 个数）的最大与和', cell=64, h=190,
             pointers={'i': 'blue', _SP: 'pink'}, pointer_labels={_SP: 's'},
             color=lambda S, k, v: 'blue' if k == S.get('i') and S.get('_line', 0) >= 4 else ('pink' if k == S.get('s') and S.get('_line') == 10 else None)),
        dict(type='text', fn=_baskets, size=24, h=100),
        dict(type='text', fn=lambda S: (f"`nums` = {NUMS}，下一个要放的是第 `c = {S['c']}` 个数 `{NUMS[S['c']]}`" if 'c' in S and S['c'] < len(NUMS) else f"`nums` = {NUMS}"), size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'yellow'), ('j', 'j', 'pink'), ('max f', 'max(f)', 'green')],
    captions={
        'f = [0]': '`f` 有 `2^(2·numSlots) = {len(f)}` 项；`f[0] = 0`：一个数都没放',
        'for i, fi in enumerate(f)': '枚举篮子集合 `i = {i:04b}`，`fi = f[i] = {fi}`',
        'if c >= len(nums)': lambda S, B, r: (f'`i` 有 `{S.c}` 个 1 → 已放 {S.c} 个数，≥ `len(nums) = {len(NUMS)}`：==无法再转移== → continue' if S.c >= len(NUMS) else f'`i` 有 `{S.c}` 个 1 → 前 {S.c} 个数已放，下一个放 `nums[{S.c}]`，继续'),
        'if (i & (1 << j)) == 0': lambda S, B, r: (f'枚举 `j = {S.j}`：这一位是 0，篮 `{S.j // 2 + 1}` 的这个位置空着 → 可以放' if (S.i >> S.j) & 1 == 0 else f'枚举 `j = {S.j}`：这一位是 1，已被占用 → 跳过'),
        'f[s] = max': _cap_f,
        'return max(f)': '篮子装满肯定不比有空篮更差，所以直接取 `max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='篮子编号不能变，数的位置无所谓：用篮子集合当状态',
        complexity='时间 `O(n · 4^numSlots)`，空间 `O(4^numSlots)`',
        problem=['`nums` 有 `n` 个数，`numSlots` 个篮子（编号 1 到 numSlots），每个篮子最多放 2 个数',
                 '与和 = 每个数与它所在篮子编号的按位与之和，求最大与和',
                 '示例：`nums = [2,3]`，`numSlots = 2` → `4`（2、3 都放篮2）'],
        quote='由于每个篮子至多可以放 2 个整数，我们可以视作有 2·numSlots 个篮子，每个篮子至多可以放 1 个整数。……用二进制数 x 表示这 2·numSlots 个篮子中放了数字的篮子集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一个篮子拆成两个「半篮」，每个半篮至多放 1 个数，编号 `j//2+1`',
              '`f[i]`：半篮集合为 `i`，放了 `nums` 的前 `popcount(i)` 个数时的最大与和',
              '转移：枚举空半篮 `j`，把 `nums[c]` 放进去，加上 `(j//2+1) & nums[c]`'],
        summary=['状态 `4^numSlots`，每个状态枚举 `2·numSlots` 个位置，时间 `O(n·4^numSlots)`',
                 '易错：`c ≥ len(nums)` 时要跳过，否则 `nums[c]` 越界',
                 '装满一定最优，所以答案是 `max(f)`，不必只看 `c = n` 的状态',
                 '同类题：1879 两个数组最小的异或值之和；还可以用最小费用最大流（题解后半）'],
    ),
)
