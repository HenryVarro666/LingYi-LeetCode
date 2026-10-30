def _txt(S):
    if 'x' not in S or 'pre' not in S:
        return '`f[v]` = 当前位 `arr1 = v` 的方案数；`s` 是 `f` 的前缀和'
    v = S.get('v')
    if v is None or 'threshold' not in S:
        return f'上一项 `pre = {S["pre"]}`，当前项 `x = {S["x"]}`'
    t = S['threshold']
    return f'`min(v, pre + v − x)` = `min({v}, {S["pre"]} + {v} − {S["x"]})` = =={t}==' + ('：<0，不可能' if t < 0 else f'，`f[{v}] = s[{t}]`')


CONFIG = dict(
    num=3251, title='单调数组对的数目 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和优化 DP · f/s 互相更新',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2323'],
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
    call='Solution().countOfPairs([1,2,2])',
    expect=4,
    skip=['ma = max', 'mod = 10', 'if v == 0', 'else:', 's[v] >= mod', 's[v] -= mod'],
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=70),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='f', label='f[v]：arr1 = v 的方案数', h=210, cell=70, pointers={'v': 'yellow'}),
        dict(type='array', var='s', label='s[v] = f[0] + … + f[v]', h=210, cell=70, pointers={'v': 'yellow'}),
    ],
    watch=[('pre', 'pre', 'blue'), ('x', 'x', 'pink'), ('v', 'v', 'yellow'), ('threshold', 'threshold', 'orange')],
    captions={
        'f = [0] * (ma + 1)': lambda S, B, r: ('`f[v]`：arr1[index] = v 时的方案数，先全 0；`arr2 = nums − arr1` 自动确定' if 'x' not in S
                                               else '新开一行 `f`，==只依赖上一轮的 s=='),
        's = [0] * (ma + 1)': lambda S, B, r: ('`s`：`f` 的前缀和' if 'x' not in S else '新开 `s`，等会儿用新 `f` 重算前缀和'),
        'f[v] = 1': '第 0 项：`arr1[0]` 取 `0..nums[0]` 都合法，各 1 种 → `f[{v}] = 1`',
        's[v] = f[v]': '`s[0] = f[0] = {s[0]}`',
        's[v] = s[v - 1] + f[v]': lambda S, B, r: (f'`s[{S.v}] = s[{S.v - 1}] + f[{S.v}]` = =={S.s[S.v]}==：前缀和'),
        'pre = nums[0]': '`pre` 记住上一项的 `nums` 值 = {pre}',
        'for x in nums[1:]': lambda S, B, r: ('所有项都处理完了' if B.get('x') == S.x and B.get('pre') == S.pre
                                              else f'处理下一项 `x = {S.x}`，上一项 `pre = {S.pre}`'),
        'threshold = min': '上一位 `arr1` 的上限：`min(v, pre + v − x) = min({v}, {pre} + {v} − {x})` = =={threshold}==。==既不能超过 v（arr1 不降），也要让 arr2 不升==',
        'if threshold >= 0': '`threshold = {threshold}` {"≥ 0，有合法的上一位" if threshold >= 0 else "< 0，没有合法的上一位，f[v] 保持 0"}',
        'f[v] = s[threshold]': '`f[{v}] = s[{threshold}]` = =={f[v]}==：上一位取 `0..{threshold}` 的方案数之和',
        'pre = x': '`pre` 更新为 {x}，进入下一项',
        'return s[nums[-1]]': '最后一位 `arr1 = 0..nums[-1]` 的方案数 = `s[nums[-1]]` = =={ret}==',
    },
    cards=dict(
        one_liner='f 记当前位 arr1 取 v 的方案数，上一位的取值是一段前缀',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['`arr1` 不减、`arr2` 不增，且 `arr1[i] + arr2[i] = nums[i]`，求构造方案数（模 `10^9+7`）',
                 '示例：`nums = [2,3,2]` → `4`；`[5,5,5,5]` → `126`',
                 '本视频：`nums = [1,2,2]` → `4`'],
        quote='arr1[index - 1] 必须小于等于 arr1[index]，因此必须满足 pre_v <= v；arr2[index - 1] 必须大于等于 arr2[index]，因此必须满足 nums[index - 1] - pre_v >= nums[index] - v。',
        quote_src='—— yiduobo 题解原文',
        idea=['`arr1[index] = v` 就同时定下了 `arr2[index] = nums[index] − v`',
              '两个不等式合起来：`0 ≤ pre_v ≤ min(v, nums[index−1] + v − nums[index])`',
              '`f[index][v]` 就是 `f[index-1]` 前缀的和 → 用 `s` 存前缀和，`O(1)` 取',
              '`f`、`s` 只和上一轮有关，直接重新开数组省掉 index 一维'],
        summary=['时间 `O(nm)`，`m = max(nums)`；空间 `O(m)`',
                 '易错：`threshold < 0` 时 `f[v]` 必须保持 0；`s` 要在新 `f` 算完后整行重算',
                 '最后答案是 `s[nums[-1]]`：只统计 `arr1[n-1] ≤ nums[n-1]` 的状态',
                 '原文为 Python 2 风格，但语法在 Python 3 下可直接运行，代码未改动',
                 '对比灵神：灵神把前缀和和右移合并在一维数组里原地做；yiduobo 用 f、s 两个数组轮流重算'],
    ),
)
