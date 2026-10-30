def _clr(S, i, v):
    return {1: 'blue', 2: 'orange', 3: 'purple'}.get(v)


CONFIG = dict(
    num=3840, title='打家劫舍 V', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='打家劫舍 + 颜色分类（滚动变量）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1619'],
    code='''
class Solution:
    def rob(self, nums: List[int], colors: List[int]) -> int:
        f0, f1 = 0, nums[0]
        for i in range(1, len(nums)):
            if colors[i] != colors[i - 1]:
                f0 = f1
                f1 += nums[i]
            else:
                f0, f1 = f1, max(f0 + nums[i], f1)
        return f1
''',
    call='Solution().rob([4,1,5,2,6,3], [1,1,2,2,2,3])',
    expect=18,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=200, label='nums（金额）',
             color=lambda S, k, v: 'green' if 'i' in S and k == S['i'] else None,
             dim=lambda S, k, v: 'i' in S and k > S['i']),
        dict(type='array', var='colors', pointers={}, h=170, label='colors（颜色码：相同颜色才互相冲突）',
             color=lambda S, k, v: _clr(S, k, v)),
        dict(type='text', size=30, fn=lambda S: (f"`f1` = 偷到当前房屋为止的最大金额 = =={S['f1']}==；`f0` = 少一间时的最大金额 = {S['f0']}" if 'f0' in S else '')),
    ],
    watch=['i', ('f0', 'f0', 'cyan'), ('f1', 'f1', 'green')],
    captions={
        'f0, f1 = 0, nums[0]': '`f1 = nums[0] = {f1}`：只有一间房，必偷；`f0 = 0`：没有房子可偷',
        'for i in range': lambda S, B, r: (f'看第 `{S.i}` 间房：金额 `{S.nums[S.i]}`，颜色 `{S.colors[S.i]}`' if B.get('i') != S.i else '所有房屋处理完'),
        'if colors[i] != colors[i - 1]': lambda S, B, r: (f"`colors[{S.i}] = {S.colors[S.i]}` ≠ `colors[{S.i - 1}] = {S.colors[S.i - 1]}`：颜色不同 → 可以同时偷两间" if S.colors[S.i] != S.colors[S.i - 1] else f"`colors[{S.i}] = {S.colors[S.i]}` == `colors[{S.i - 1}]`：颜色相同 → 不能同时偷，要「选或不选」"),
        'f0 = f1': '颜色不同：前一间照偷，`f0` 记下旧的 `f1 = {f0}`',
        'f1 += nums[i]': '`nums[i] > 0`，偷了不亏 → `f1 += {nums[i]}` = =={f1}==',
        'f0, f1 = f1, max': lambda S, B, r: f'选或不选：偷 `nums[{S.i}]` 则前一间不能偷 → `{B.f0} + {S.nums[S.i]} = {B.f0 + S.nums[S.i]}`；不偷 → `{B.f1}`；取大 `f1 = {S.f1}`',
        'return f1': '`f1` 就是 `f[n]`，答案 `{f1}`',
    },
    cards=dict(
        one_liner='颜色不同就全偷，颜色相同才是打家劫舍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每间房有金额 `nums[i]` 和颜色码 `colors[i]`',
                 '相邻且颜色相同的两间房，不能同时偷；颜色不同则不受限',
                 '示例：`nums=[1,4,3,5], colors=[1,1,2,2]` → `9`；本视频：`[4,1,5,2,6,3]` → `18`'],
        quote='如果 $colors[i-1] \\ne colors[i]$，那么 $nums[i]$ 偷或不偷，都可以偷 $nums[i-1]$。由于 $nums[i] > 0$，所以偷更好，得 $f[i+1] = f[i] + nums[i]$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i+1]` 表示在 `[0, i]` 中能偷的最大总和，`f[0] = 0`',
              '颜色不同：`nums[i]` 和 `nums[i-1]` 互不影响，金额为正 → 直接 `f[i] + nums[i]`',
              '颜色相同：和 198 题一样「选或不选」，`max(f[i-1] + nums[i], f[i])`'],
        summary=['时间 `O(n)`，空间 `O(1)`（写法一用数组 `f`，空间 `O(n)`）',
                 '易错点：==颜色不同时不是取 max，而是必偷==（金额均为正）',
                 '滚动变量时赋值顺序：颜色不同先 `f0 = f1` 再 `f1 += nums[i]`',
                 '灵神给了数组写法和空间优化写法，这里选后者',
                 '前置题：198. 打家劫舍'],
    ),
)
