CONFIG = dict(
    num=2597, title='美丽子集的数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按模 k 分类 + 打家劫舍式 DP',
    tags=['其他线性 DP', '子集型回溯', '难度分 2023'],
    code='''
class Solution(object):
    def beautifulSubsets(self, nums, k):

        r_dict = {}
        for v in nums:
            r = v % k
            v //= k
            if r not in r_dict:
                r_dict[r] = []
            r_dict[r].append(v)
        
        res = 1
        for r in r_dict:
            cnt = [0] * 1001
            for v in r_dict[r]:
                cnt[v] += 1
                
            f = [1, 1 << (cnt[0])]
            for v in range(1, 1001):
                f.append(f[-1] + f[v - 1] * ((1 << cnt[v]) - 1))

            res *= f[-1]
        
        return res - 1
''',
    call='Solution().beautifulSubsets([2,4,6,4], 2)',
    expect=6,
    skip=['if r not in r_dict', 'r_dict[r] = []', 'for v in range(1, 1001)', 'for v in nums', 'for v in r_dict[r]'],
    max_steps=40,
    views=[
        dict(type='text', fn=lambda S: (f"本类 `r = {S['r']}`：数 `÷ k` 后的值 `{S['r_dict'][S['r']]}`" if 'r' in S and S.get('r') in S.get('r_dict', {}) else '先按 `v % k` 分类，同类的数除以 `k`，相邻两数差 1 就不能同选'), size=26, h=70),
        dict(type='array', var=lambda S: S['cnt'][:9], label='cnt[0..8]（值 v 出现的次数，粉 = 当前 v）', cell=84,
             pointers={'v': 'pink'}, h=220,
             color=lambda S, i, x: 'pink' if i == S.get('v') else None),
        dict(type='array', var=lambda S: S['f'][:10], label='f（只画前 10 项；f[i] = 值在 0..i-1 范围内的方案数，含空集）', cell=84, h=220, color=lambda S, i, x: 'green' if i == len(S['f']) - 1 else None, pointers={}),
    ],
    watch=[('r', 'r', 'cyan'), ('v', 'v', 'pink'), ('res', 'res', 'green')],
    captions={
        'r_dict = {}': '`r_dict[r]` 存放“模 k 余 r”的那一类数',
        'r = v % k': '`v = {B.v}`：余数 `r = {r}`，同余的数分在一类（不同类的差一定不是 k）',
        'v //= k': '`v` 除以 `k`：同一类里相差 `k` 的两个数，变成==相差 1== → `v = {v}`',
        'r_dict[r].append(v)': '放进第 `{r}` 类：`{r_dict[r]}`',
        'res = 1': '`res` 是各类方案数的乘积',
        'for r in r_dict': lambda S, B, r: (f'处理第 `r = {S.r}` 类' if S.get('r') != B.get('r') or 'r' not in B else '所有类都处理完了'),
        'cnt = [0] * 1001': '`cnt[v]` 记录值 `v` 出现的次数',
        'cnt[v] += 1': '`cnt[{v}]` → {cnt[v]}',
        'f = [1, 1 <<': '`f[0] = 1`：一个数都不选；`f[1] = 2^cnt[0] = {f[1]}`：值 0 任意选或不选（相同的值可以同时选）',
        'f.append': lambda S, B, r: (f'值 `{S.v}` 出现 {S.cnt[S.v]} 次：不选它沿用旧的 `f[{S.v}]`；选它（`2^{S.cnt[S.v]} − 1` 种非空选法）就不能选 `{S.v - 1}`，加 `f[{S.v - 1}] × {2 ** S.cnt[S.v] - 1}` → `f[{S.v + 1}] = {S.f[-1]}`'
                                     if S.cnt[S.v] else f'`cnt[{S.v}] = 0`：这个值不存在，`f[{S.v + 1}] = {S.f[-1]}` 和上一项相同'),
        'res *= f[-1]': '这一类共 `{f[-1]}` 种（含空）→ 乘到 `res`：`res = {res}`',
        'return res - 1': '空集被每一类都算了一次，最后减 1：`{res} − 1 = {res - 1}`',
    },
    cards=dict(
        one_liner='按模 k 分类后，每类就是打家劫舍：不能选相邻值',
        complexity='时间 `O(n + V)`（V = 1000），空间 `O(V)`',
        problem=['正整数数组 `nums` 和 `k`，子集中任意两数之差不等于 `k` 就是美丽子集',
                 '求非空美丽子集的数目',
                 '本视频：`nums = [2,4,6,4]`，`k = 2` → `6`'],
        quote='不同类直接的数之差必然不是k的倍数，因此也必然不会等于k，因此在这里只需分别讨论每一类可以得到的合法子集数目，然后相乘就得到了最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 `v % k` 分类，类内的数除以 `k`，要求变成“不能选值相邻的数”',
              '`f[i]` = 值在 `0..i-1` 的方案数：`f[i] = f[i-1] + f[i-2] × (2^cnt − 1)`',
              '“不能选相邻值”与打家劫舍相似；相同的值可以随意选，所以是 `2^cnt`'],
        summary=['时间 `O(n + V)`，空间 `O(V)`，`V = 1000` 是值域',
                 '易错：`2^cnt − 1` 减掉的是“一个都不选”，它已含在 `f[i-1]` 里',
                 '最后 `res - 1`，每一类都把空集算了一次',
                 '原文为 Python 2 写法，`v /= k` 已改为 `v //= k`',
                 '演示用 `[2,4,6,4]` 只有一类；多个类时各类的 `f[-1]` 相乘（循环中间的重复步骤已快进）'],
    ),
)
