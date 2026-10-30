def _phase(S):
    return 'res' in S


def _formula(S):
    i = S.get('index')
    if i is None or 'v' not in S:
        return '`diff[i] = nums[i] − i`：条件变成 ==diff 不降==；只有正数才可能进最优解'
    if not _phase(S):
        return '先把所有正数的 `v − index` 收集起来，排序后映射成排名 `1..m`'
    v = S['nums'][i]
    if v <= 0:
        return f'`nums[{i}] = {v} ≤ 0`：最优解里不会有它，跳过'
    return f'`diff = {v} − {i} = {v - i}` → 排名 `{S["mapping"][v - i]}`'


CONFIG = dict(
    num=2926, title='平衡子序列的最大和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='差值数组 + 树状数组求前缀最大',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2448'],
    code='''
class Solution(object):
    def maxBalancedSubsequenceSum(self, nums):

        num_set = set()
        flag = False
        for index, v in enumerate(nums):
            if v > 0:
                flag = True
                num_set.add(v - index)
        
        mapping = {}
        num_list = sorted(list(num_set))
        for index, v in enumerate(num_list):
            mapping[v] = index + 1
        
        if not flag:
            return max(nums)

        f = [0] * (len(num_list) + 1)

        def add(x, v):
            while x <= len(num_list):
                f[x] = max(f[x], v)
                x += x & -x
        
        def get(x):
            ma = 0
            while x:
                ma = max(ma, f[x])
                x -= x & -x
            return ma

        res = 0
        for index, v in enumerate(nums):
            if v > 0:
                left_max = get(mapping[v - index])
                res = max(res, left_max + v)
                add(mapping[v - index], left_max + v)
        
        return res
''',
    call='Solution().maxBalancedSubsequenceSum([3,-2,3,5,6])',
    expect=14,
    skip=['flag = False', 'mapping = {}', 'num_list = sorted'],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='nums', label='nums（负数直接忽略）', h=190, cell=90,
             pointers={'index if "res" in locals() else None': 'blue'}, pointer_labels={'index if "res" in locals() else None': 'index'},
             color=lambda S, k, v: 'blue' if _phase(S) and k == S.get('index') else None),
        dict(type='array', var='num_list', label='num_list：正数的 v−index 排序去重（第 k 个 ↔ 排名 k+1）', h=200, cell=90,
             pointers={'mapping[nums[index] - index] - 1 if "res" in locals() and nums[index] > 0 else None': 'pink'},
             pointer_labels={'mapping[nums[index] - index] - 1 if "res" in locals() and nums[index] > 0 else None': '排名'}),
        dict(type='array', var='f', label='树状数组 f：每格 = 一段排名上的最大和（0 不用）', h=210,
             pointers={"_inner.get('x') if 'ma' in _inner or 'x' in _inner else None": 'yellow'},
             pointer_labels={"_inner.get('x') if 'ma' in _inner or 'x' in _inner else None": 'x'}),
    ],
    max_steps=70,
    watch=[('index', 'index', 'blue'), ('v', 'v', 'blue'), ('left_max', 'left_max', 'cyan'), ('res', 'res', 'green')],
    captions={
        'if v > 0:': lambda S, B, r: (f'`{S.v} > 0`：有可能进最优解，处理' if S.v > 0 else f'`{S.v} <= 0`：最优解里不会有负数（全负另算），跳过'),
        'flag = True': '有正数，记下 `flag`',
        'num_set.add': '收集 `v - index = {v - index}`：把数值和下标合并成一个差值',
        'mapping[v] = index + 1': '差值 `{v}` 的排名是 `{index + 1}`：把大范围压到 `1..n`',
        'if not flag': '`flag = {flag}`：有正数，继续；全是负数则答案就是最大的那个',
        'f = [0]': '树状数组 `f` 全 0，长度 `{len(num_list) + 1}`：维护排名前缀上的最大和',
        'left_max = get': '`diff = {v - index}` 排名 `{mapping[v - index]}`：问树状数组，排名不超过它的子序列最大和是多少',
        'res = max': '接在最优前缀后面：`left_max + {v} = {left_max + v}`，`res` → =={res}==',
        'add(mapping': '把 `{left_max + v}` 写进排名 `{mapping[v - index]}`，后面差值不小于它的都能接',
        'while x <= len': lambda S, B, r: (f'`x = {S.x}`：没出界，更新这一段' if S.x <= len(S.num_list) else f'`x = {S.x}` 出界，更新结束'),
        'f[x] = max': '`f[{x}] = max(旧值, {v}) = {f[x]}`',
        'x += x & -x': '`x` 加最低位 1 → 上一层管着我的位置：`x = {x}`',
        'while x:': lambda S, B, r: (f'`x = {S.x}`：还有一段没看' if S.x else '`x = 0`：前缀看完了'),
        'ma = max': '`ma = max({B.ma}, f[{x}]) = {ma}`',
        'x -= x & -x': '`x` 去掉最低位 1 → 前一段：`x = {x}`',
        'return ma': '排名前缀的最大和 = =={ma}==',
        'return res': '最大平衡子序列和 = =={res}==',
    },
    cards=dict(
        one_liner='把 nums[i] − nums[j] >= i − j 移项：数值和下标分到两边',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选一条下标递增的子序列，相邻两项满足 `nums[i] − nums[j] >= i − j`',
                 '求这样的"平衡子序列"的最大元素和',
                 '本视频：`[3,-2,3,5,6]` → `14`（选 3、5、6）'],
        quote='对于这类数值和下标同时相减的式子，一个经典的处理方法就是将数值和下标归类到一起，也就是将式子变形成nums[i] - i >= nums[j] - j。',
        quote_src='—— yiduobo 题解原文',
        idea=['得到差值数组 `diff`，题目变成：选 `diff` 不降的子序列，==对应 nums 之和最大==',
              '朴素 DP 是 `O(n^2)`：把状态改成 "以差值 j 结尾的最大和" 再离散化到排名',
              '"排名不超过 r 的最大值" 是动态前缀最大，树状数组 `O(log n)`',
              '负数不可能出现在最优解里（全负时取最大值），所以直接忽略'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '全是负数时直接返回 `max(nums)`，其余情况负数一律跳过',
                 '树状数组初值为 0，所以 `left_max` 为 0 就等于 "从自己重新开始"',
                 '原文本身是 Python 3 可运行的写法，代码未做修改',
                 '对比灵神：灵神保留负数，用 `max(pre_max, 0)` 处理；yiduobo 先把负数剔除'],
    ),
)
