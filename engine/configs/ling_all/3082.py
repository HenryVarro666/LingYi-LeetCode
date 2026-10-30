def _txt(S):
    if 'x' not in S or 'j' not in S['_inner'] or S.get('_line') != 6:
        return '`f[j]` = 在已看过的数里，「和恰好为 j 的子序列 S」的 ==T 的个数=='
    j, x, f = S['j'], S['x'], S['f']
    return f'`f[{j}]` = 2×(旧 f[{j}]) + ' + (f'旧 `f[{j - x}]`' if j >= x else '0（`j < x`，放不下）')


def _fcol(S, t, v):
    if 'x' in S and 'j' in S['_inner'] and S.get('_line') == 6:
        if t == S['j']:
            return 'yellow'
        if S['j'] >= S['x'] and t == S['j'] - S['x']:
            return 'pink'
    return None


CONFIG = dict(
    num=3082, title='求出所有子序列的能量和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='一维 0-1 背包 · 每个数三种归属',
    tags=['灵神题单', '动态规划', '难度分 2242'],
    code='''
class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        f = [1] + [0] * k
        for x in nums:
            for j in range(k, -1, -1):
                f[j] = (f[j] * 2 + (f[j - x] if j >= x else 0)) % 1_000_000_007
        return f[k]
''',
    call='Solution().sumOfPower([3, 1, 3, 2], 6)',
    expect=8,
    skip=['f = [1]', 'for j in range'],
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前处理的数 x）', cell=84, h=170,
             color=lambda S, t, v: 'blue' if 'x' in S and 'nums' in S and v == S['x'] else None),
        dict(type='array', var='f', label='f[j]：和为 j 的 S 的贡献总数（黄 = 正在更新，粉 = 来源 f[j-x]）', cell=84, h=210, color=_fcol),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=['x', 'j', ('f[k]', 'f[k]', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：空的 S（和为 0）算一种，其他和先记 0',
        'for x in nums': lambda S, B, r: ('所有数都处理完了' if B.get('x') == S.x and S.nums.count(S.x) == 1 else f'处理 `x = {S.x}`：不在 S 里（在或不在 T，×2），或在 S 里（接在和为 j-x 的后面）'),
        'f[j] = (f[j] * 2': lambda S, B, r: (f'`f[{S.j}] = {B.f[S.j]}×2 + ' + (f'f[{S.j - S.x}]({B.f[S.j - S.x]})' if S.j >= S.x else '0（j < x）') + f'` = =={S.f[S.j]}=='),
        'return f[k]': '和为 `k = {k}` 的 S 的贡献总数，即所有子序列能量和 = =={f[k]}=='
    },
    cards=dict(
        one_liner='每个数有三种归属：都不在、只在大子序列 T、在和为 k 的 S 里',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['子序列的「能量」= 它的子序列里和等于 k 的个数',
                 '求 ==所有子序列的能量之和==，对 `10^9+7` 取余',
                 '本视频：`[3,1,3,2], k=6` → `8`；原题示例 `[1,2,3], k=3` → `6`'],
        quote='对于 nums[i]，它只有三种可能：不在子序列 S，也不在子序列 T 中；不在子序列 S，在子序列 T 中；在子序列 S 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换个角度数：枚举和为 k 的子序列 S，数有多少个 T 包含它（T 是 S 的超序列）',
              '`nums[i]` 不在 S：在不在 T 都行 → `f[j]` 乘 2；在 S：从 `f[j-x]` 转移',
              '所以 `f[j] = f[j]*2 + f[j-x]`，倒序遍历 j 压缩成一维，答案 `f[k]`'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '`j` 要从 `k` ==倒序==到 0（含 0）：`f[j]` 要乘 2，哪怕 `j < x` 放不下',
                 '`j < x` 时只能乘 2，不能访问 `f[j-x]`（负下标）',
                 '另一种写法：先枚举 S 的长度 c，二维背包 `f[j][c]`，答案 `sum f[k][c] * 2^(n-c)`，`O(n²k)`'],
    ),
)
