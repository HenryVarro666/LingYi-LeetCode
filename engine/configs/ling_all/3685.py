def _fv(S):
    return [int(b) for b in S['f']] if 'f' in S else None


def _av(S):
    return ['T' if b else 'F' for b in S['ans']] if 'ans' in S else None


def _fcol(S, t, v):
    if S.get('_line') in (21, 22) and 'j' in S['_inner'] and 'x' in S and t == S['k'] - S['j'] * S['x']:
        return 'pink'
    if S.get('_line') in (15, 16) and 'j' in S['_inner'] and t == S['j']:
        return 'yellow'
    return 'green' if v else None


def _txt(S):
    if 'x' not in S or 'f' not in S:
        return '`f[s]` = 从「已加入的 ≤ x 的数」里能否凑出和 `s`'
    k, x, i, n = S['k'], S['x'], S['i'], S['n']
    line = S.get('_line', 0)
    if 'j' in S['_inner'] and line in (21, 22):
        j = S['j']
        return f'`x = {x}`：大于 x 的还有 `{n - i}` 个，当成 {x} 选 `{j}` 个 → 还要凑 `{k - j * x}`，`f[{k - j * x}]` = =={S["f"][k - j * x]}=='
    return f'`x = {x}`：已加入所有 ≤ {x} 的数（共 `{i}` 个），其余 `{n - i}` 个都被截成 {x}'


CONFIG = dict(
    num=3685, title='含上限元素的子序列和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='排序 + 增量 0-1 背包 + 枚举选几个 x',
    tags=['灵神题单', '动态规划', '难度分 2073'],
    code='''
class Solution:
    def subsequenceSumAfterCapping(self, nums: List[int], k: int) -> List[bool]:
        nums.sort()

        n = len(nums)
        ans = [False] * n
        f = [False] * (k + 1)
        f[0] = True  # 不选元素，和为 0

        i = 0
        for x in range(1, n + 1):
            # 增量地考虑所有恰好等于 x 的数
            # 小于 x 的数在之前的循环中已计算完毕，无需重复计算
            while i < n and nums[i] == x:
                for j in range(k, nums[i] - 1, -1):
                    f[j] = f[j] or f[j - nums[i]]  # 0-1 背包：不选 or 选
                i += 1

            # 枚举（从大于 x 的数中）选了 j 个 x
            for j in range(min(n - i, k // x) + 1):
                if f[k - j * x]:
                    ans[x - 1] = True
                    break
        return ans
''',
    call='Solution().subsequenceSumAfterCapping([4,3,2,4], 5)',
    expect=[False, False, True, True],
    skip=['n = len(nums)', 'ans = [False]', 'f = [False]', 'for j in range(k, nums[i]', 'for j in range(min'],
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums（排序后；i 左边 = 已加入背包的数，≤ x）', cell=90, h=170,
             pointers={'i': 'blue'}, color=lambda S, t, v: 'green' if 'i' in S and t < S['i'] else None,
             dim=lambda S, t, v: 'i' in S and t >= S['i']),
        dict(type='array', var=_fv, label='f[s]：能否凑出和 s（1 = 能；粉 = 正在查的目标，黄 = 正在更新）', cell=80, h=190,
             color=_fcol),
        dict(type='array', var=_av, label='ans[x-1]（x = 1..n）', cell=80, h=170,
             color=lambda S, t, v: 'green' if v == 'T' else ('blue' if 'x' in S and t == S['x'] - 1 else None)),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=['x', 'i', 'j', ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '==先排序==：x 从小到大时，≤ x 的数是一个不断变长的前缀 → `{nums}`',
        'f[0] = True': '`f[0] = True`：一个数都不选，和为 0',
        'i = 0': '`i = 0`：指针 `i` 指向下一个要加入背包的数',
        'for x in range': lambda S, B, r: ('`x` 枚举完了，结束循环' if B.get('x') == S.x else f'枚举上限 `x = {S.x}`：大于 {S.x} 的数都被截成 {S.x}'),
        'while i < n and nums[i] == x': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]}` 恰好等于 x → 增量加入背包' if S.i < S.n and S.nums[S.i] == S.x
                                                         else f'没有等于 {S.x} 的新数了（`i = {S.i}`）：≤ x 的数都已在背包里'),
        'f[j] = f[j] or': '0-1 背包：和 `{j}` = 不选 `{B.f[j]}` or 选 `f[{j - nums[i]}]` = {B.f[j - nums[i]]}，结果 =={f[j]}==（==倒序==，保证每个数只用一次）',
        'i += 1': '`nums[{B.i}] = {nums[B.i]}` 已加入背包，指针 `i` 右移 → {i}',
        'if f[k - j * x]': lambda S, B, r: (f'选 `{S.j}` 个 {S.x}（共 {S.j * S.x}），还需凑 `k - {S.j * S.x} = {S.k - S.j * S.x}`：`f[{S.k - S.j * S.x}]` = '
                                           f'{"==True，找到了==" if S.f[S.k - S.j * S.x] else "False，换个 j"}'),
        'ans[x - 1] = True': '`x = {x}` 时能凑出 `k = {k}` → `ans[{x - 1}] = True`，==不用再枚举 j== → break',
        'return ans': '每个 x 的结果：`{ans}`',
    },
    cards=dict(
        one_liner='排序后 x 递增，增量做 0-1 背包；大于 x 的数当 x 枚举选几个',
        complexity='时间 `O(nk + n log n + min(n², k log n))`，空间 `O(k)`',
        problem=['数组 `nums`，每个元素替换成 `min(nums[i], x)`，要对 `x = 1..n` 都回答',
                 '能否选一个子序列，使和 ==恰好等于 k==',
                 '示例：`[4,3,2,4], k=5` → `[F,F,T,T]`'],
        quote='对于 ≤ 3 的数，考虑选或不选。对于 > 3 的数，考虑枚举选多少个。这些数都替换成了 3，相当于枚举选多少个 3。',
        quote_src='—— 灵茶山艾府题解',
        idea=['对每个 x：≤ x 的数做 ==0-1 背包==（选或不选），> x 的数全是 x，只需枚举选 `j` 个',
              '每个 x 都重算背包是 `O(n²k)`，太慢 → 排序 + 双指针，==在 x-1 的基础上增量加入== 等于 x 的数',
              '`j` 最多枚举到 `min(n-i, k//x)`，调和级数使总次数很小'],
        summary=['时间 `O(nk + n log n + min(n², k log n))`，空间 `O(k)`',
                 '背包要==倒序==遍历 j，否则一个数会被选多次',
                 '`nums.sort()` 会原地修改输入',
                 '题解还给了 bitset 优化：`f |= (f << nums[i]) & u`，把背包压成一个大整数'],
    ),
)
