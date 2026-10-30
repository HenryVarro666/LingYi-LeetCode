CONFIG = dict(
    num=2862, title='完全子集的最大元素和', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='贪心 · 基础集合 × mul',
    tags=['灵神题单', '数学算法', '难度分 2292'],
    code='''
class Solution(object):
    def maximumSum(self, nums):

        index_list = []
        x = 1
        n = len(nums)
        while x * x <= n:
            index_list.append(x * x)
            x += 1
        
        res = 0
        mul = 1
        while index_list:
            res = max(res, sum([nums[p * mul - 1] for p in index_list]))
            mul += 1
            while index_list and index_list[-1] * mul > n:
                index_list.pop()
        
        return res
''',
    call='Solution().maximumSum([8,10,3,8,1,13,7,9,4])',
    expect=20,
    views=[
        dict(type='array', var='nums', h=230, label='nums（下标从 0 数；选中的是 p×mul 对应的下标 p×mul−1）',
             color=lambda S, i, v: 'green' if 'index_list' in S and 'mul' in S and (i + 1) in [p * S['mul'] for p in S['index_list']] else None,
             dim=lambda S, i, v: 'index_list' in S and 'mul' in S and (i + 1) not in [p * S['mul'] for p in S['index_list']]),
        dict(type='array', var='index_list', h=190, label='index_list（基础集合，都是完全平方数；乘以 mul 后得到当前备选集合）', index=False, cell=70),
        dict(type='text', h=70, fn=lambda S: (f"当前备选下标（从 1 数）= `{[p * S['mul'] for p in S['index_list']]}`，答案 `res = {S['res']}`" if 'mul' in S and 'res' in S else '先造基础集合：n 以内的所有完全平方数')),
    ],
    watch=[('mul', 'mul', 'blue'), ('res', 'res', 'green'), ('n', 'n', 'cyan')],
    captions={
        'index_list.append': '`{x*x}` 是不超过 n={n} 的完全平方数，放进基础集合',
        'while x * x <= n': lambda S, B, r: (f'`{S.x}² = {S.x*S.x} ≤ {S.n}`，还能放' if S.x * S.x <= S.n else f'`{S.x}² = {S.x*S.x} > {S.n}`：基础集合造好了 → `{S.index_list}`'),
        'while index_list:': lambda S, B, r: (f'基础集合还有 `{len(S.index_list)}` 个元素，继续试 `mul = {S.mul}`' if S.index_list else '基础集合空了，所有 mul 都试完 → 结束'),
        'res = max': '`mul = {mul}`：集合 `{[p * mul for p in index_list]}`，元素和 `{sum([nums[p * mul - 1] for p in index_list])}`，`res = max({B.res}, …)` = =={res}==',
        'mul += 1': '换下一个倍数：`mul = {mul}`',
        'index_list[-1] * mul > n': lambda S, B, r: (f'最大元素 `{S.index_list[-1]} × {S.mul} = {S.index_list[-1] * S.mul} > {S.n}`，超出数组 → ==弹掉它==' if S.index_list and S.index_list[-1] * S.mul > S.n else ('集合已经弹空，不会再有更大的 mul 能用' if not S.index_list else '剩下的最大元素乘 mul 没超过 n，停止弹出')),
        'index_list.pop()': '弹出后 `index_list = {index_list}`',
        'return res': '最大元素和 `{res}`',
    },
    skip=['x += 1', 'x = 1', 'index_list = []', 'n = len', 'res = 0', 'mul = 1'],
    max_steps=70,
    cards=dict(
        one_liner='元素都是正数，所以要选就选满：基础集合 × mul',
        complexity='时间 `O(n√n)`，空间 `O(√n)`',
        problem=['下标从 1 开始，选一组下标，要求任意两个下标的乘积都是 ==完全平方数==',
                 '求被选中元素的最大和',
                 '示例：`[8,10,3,8,1,13,7,9,4]` → `20`（选下标 1、4、9）'],
        quote='对于样例2中的集合而言，在可以选择{1, 4, 9}的前提下就没有理由选择{1, 4}、{1, 9}、{4, 9}。',
        quote_src='—— yiduobo 题解',
        idea=['元素全为正，集合越满越好：先取基础集合 `{1, 4, 9, …}`（≤ n 的完全平方数）',
              '其他候选都是基础集合每个元素乘同一个 `mul`，超出 n 的元素直接去掉',
              '`mul` 越大越多元素越界，所以只需从尾部不断 `pop` 最大元素'],
        summary=['每个 `mul` 的集合大小不超过 `√n`，共 `n` 轮，`O(n√n)`',
                 '易错点：下标从 1 数，取元素时 `nums[p * mul - 1]`',
                 '`index_list` 弹空时就没有更多候选，循环结束'],
    ),
)
