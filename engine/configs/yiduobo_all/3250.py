CONFIG = dict(
    num=3250, title='单调数组对的数目 I', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='DP + 前缀和优化',
    tags=['灵神题单', '其他线性 DP', '难度分 1898'],
    code='''
class Solution(object):
    def countOfPairs(self, nums):

        ma = max(nums)

        f = [0] * (ma + 1)
        s = [0] * (ma + 1)

        mod = 10 ** 9 + 7
        for v in range(nums[0] + 1):
            f[v] = 1
            if v == 0:
                s[v] = f[v]
            else:
                s[v] = s[v - 1] + f[v]

        pre = nums[0]
        for x in nums[1:]:
            f = [0] * (ma + 1)
            for v in range(0, x + 1):
                threshold = min(v, pre + v - x)
                if threshold >= 0:
                    f[v] = s[threshold]

            s = [0] * (ma + 1)
            for v in range(0, x + 1):
                if v == 0:
                    s[v] = f[v]
                else:
                    s[v] = s[v - 1] + f[v]
                    if s[v] >= mod:
                        s[v] -= mod
        
            pre = x
        return s[nums[-1]]
''',
    call='Solution().countOfPairs([2, 3, 2])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（arr1[i] + arr2[i] = nums[i]）', h=130, cell=90,
             color=lambda S, k, v: 'yellow' if S.get('x') is not None and k == S['nums'].index(S['x'], 1 if k > 0 else 0) and False else None),
        dict(type='array', var='f', label='f[v]：当前位置 arr1 取 v 的方案数', h=190, cell=100,
             pointers={'v': 'blue'}, color=lambda S, k, v: 'yellow' if k == S.get('v') and S.get('_line', 0) > 0 and v else None),
        dict(type='array', var='s', label='s[v] = f[0] + … + f[v]（前缀和）', h=190, cell=100,
             pointers={'threshold': 'pink'}),
        dict(type='text', size=24, h=70,
             fn=lambda S: (f'`f[v] = s[min(v, pre+v-x)]` = `s[min({S["v"]}, {S["pre"]}+{S["v"]}-{S["x"]})]`'
                           if S.get('x') is not None and S.get('v') is not None and S.get('pre') is not None
                           else '`f[v]` 是前缀和 `s` 上的一个值，O(1) 转移')),
    ],
    watch=[('x', 'x', 'blue'), ('pre', 'pre', 'cyan'), ('v', 'v', 'blue'), ('threshold', 'threshold', 'pink')],
    captions={
        'ma = max(nums)': '`ma = {ma}`：arr1 的取值最多到这么大，数组开 `ma + 1` 格',
        'f = [0] * (ma + 1)\n': '`f[v]`：arr1 当前位取 v 时的方案数',
        'mod = ': '答案取模 `10^9 + 7`',
        'for v in range(nums[0] + 1)': '第 0 位：arr1[0] 可以取 `0..{nums[0]}`，arr2 自动是 `nums[0] - v`',
        'f[v] = 1': '`f[{v}] = 1`：第 0 位取 {v} 只有一种方案',
        'if v == 0': lambda S, B, r: '`v == 0`：前缀和从 `f[0]` 开始' if S.v == 0 else '`v > 0`：前缀和累加',
        's[v] = f[v]': '`s[0] = f[0]` = {s[0]}',
        's[v] = s[v - 1] + f[v]': '`s[{v}] = s[{v-1}] + f[{v}]` = =={s[v]}==',
        'pre = nums[0]': '`pre` = 上一位的 nums 值 = {pre}',
        'for x in nums[1:]': '处理下一位：`x = {x}`，上一位 `pre = {pre}`',
        'f = [0] * (ma + 1)': '清空 `f`，准备算这一位',
        'for v in range(0, x + 1)': lambda S, B, r: f'枚举 arr1 这一位取 `v`（`0..{S.x}`）',
        'threshold = min': ('上一位 `pre_v` 须满足：`pre_v <= v` 且 `pre - pre_v >= x - v`；'
                            '上界 `min({v}, {pre}+{v}-{x})` = =={threshold}=='),
        'if threshold >= 0': lambda S, B, r: ('上界合法，可以转移' if S.threshold >= 0 else f'`threshold = {S.threshold} < 0`：没有合法的上一位，`f[{S.v}]` 保持 0'),
        'f[v] = s[threshold]': '`f[{v}] = s[{threshold}]` = =={f[v]}==（上一位 `0..{threshold}` 的方案数之和）',
        's = [0] * (ma + 1)': '用新的 `f` 重建前缀和 `s`',
        'if s[v] >= mod': lambda S, B, r: '超过 mod，减掉 mod' if S.s[S.v] >= 10**9 + 7 else '没超过 mod',
        's[v] -= mod': '减 mod',
        'pre = x': '这一位处理完，`pre` 更新为 {x}',
        'return s[nums[-1]]': '最后一位 arr1 取 `0..{nums[-1]}` 的方案数之和 = `s[{nums[-1]}]` = =={ret}==',
    },
    skip=['if v == 0', 'mod ='],
    max_steps=110,
    cards=dict(
        one_liner='f[index][v] 是上一行的前缀和：O(nm^2) 变 O(nm)',
        complexity='时间 `O(n * m)`，空间 `O(m)`',
        problem=['给正整数数组 `nums`，构造非负数组 `arr1`（不减）和 `arr2`（不增）',
                 '要求每个位置 `arr1[i] + arr2[i] = nums[i]`，求方案数，对 `10^9+7` 取模',
                 '本视频：`nums = [2, 3, 2]` → `4`'],
        quote='f[index][v] = s[index - 1][min(v, nums[index - 1] + v - nums[index])]',
        quote_src='—— yiduobo 题解原文',
        idea=['`arr1[index] = v` 就决定了 `arr2[index] = nums[index] - v`，只需记 v',
              '上一位 `pre_v` 要满足 `pre_v <= v`，且 `nums[index-1] - pre_v >= nums[index] - v`',
              '合法的 `pre_v` 是 `0..上界` 一段前缀，用前缀和 `s` 一步取到'],
        summary=['时间 `O(n * m)`，m 为 nums 最大值；空间 `O(m)`（f、s 滚动）',
                 '易错：上界 `threshold` 可能为负，此时 `f[v] = 0`',
                 '易错：前缀和也要取模；最后答案是最后一位所有 v 的和',
                 '不加前缀和是 `O(n * m^2)`，yiduobo 用 `s` 把求和省掉',
                 '原文为 Python 2 风格，除删去类型说明外无改动'],
    ),
)
