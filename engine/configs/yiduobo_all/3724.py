CONFIG = dict(
    num=3724, title='转换数组的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='逐位累加 + 最小额外调整',
    tags=['灵神题单', '难度分 1790'],
    code='''
class Solution(object):
    def minOperations(self, nums1, nums2):
        
        res = 0
        n = len(nums1)
        mi = None
        for index in range(n):
            res += abs(nums1[index] - nums2[index])
            if nums1[index] <= nums2[-1] <= nums2[index] or nums1[index] >= nums2[-1] >= nums2[index]:
                cost = 0
            elif nums2[-1] >= max(nums1[index], nums2[index]):
                cost = nums2[-1] - max(nums1[index], nums2[index])
            else:
                cost = min(nums1[index], nums2[index]) - nums2[-1]
            
            if mi is None or mi > cost:
                mi = cost
        
        return res + mi + 1
''',
    call='Solution().minOperations([1,3,6], [2,4,5,3])',
    expect=4,
    views=[
        dict(type='array', var='nums1', label='nums1', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='array', var='nums2', label='nums2（黄色 = nums2[-1]）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'yellow' if i == len(S['nums2']) - 1 else ('blue' if S.get('index') == i else None)),
        dict(type='text', fn=lambda S: (f"累计变换 `res = {S['res']}`；最小额外调整 `mi = {S.get('mi')}`" if 'res' in S else ''), h=60),
    ],
    watch=['index', 'cost', ('res', 'res', 'blue'), ('mi', 'mi', 'orange')],
    captions={
        'res = 0': '`res` 累计每个位置的变换次数',
        'mi = None': '`mi`：让 `nums2[-1]` 出现所需的最小额外调整，先空着',
        'res += abs': '位置 `{index}`：必须从 `{nums1[index]}` 挪到 `{nums2[index]}`，`res += {abs(nums1[index] - nums2[index])}` → =={res}==',
        'if nums1[index] <= nums2[-1]': lambda S, B, r: (f'`nums2[-1] = {S.nums2[-1]}` 落在 `{S.nums1[index]}` 和 `{S.nums2[index]}` 之间 → 途中经过，顺手复制'
                                                       if (S.nums1[S.index] <= S.nums2[-1] <= S.nums2[S.index] or S.nums1[S.index] >= S.nums2[-1] >= S.nums2[S.index])
                                                       else f'`nums2[-1] = {S.nums2[-1]}` 不在 `{S.nums1[index]}`、`{S.nums2[index]}` 之间'),
        'cost = 0': '无需额外调整：`cost = 0`',
        'elif nums2[-1] >= max': lambda S, B, r: (f'两端点都 ≤ `{S.nums2[-1]}`：在较大的那个端点复制' if S.nums2[-1] >= max(S.nums1[S.index], S.nums2[S.index])
                                                  else '两端点都 > target：在较小的那个端点复制'),
        'cost = nums2[-1] - max': '在最大值处复制，再往上调：`cost = {nums2[-1]} - {max(nums1[index], nums2[index])}` = =={cost}==',
        'cost = min(': '在最小值处复制，再往下调：`cost = {min(nums1[index], nums2[index])} - {nums2[-1]}` = =={cost}==',
        'if mi is None': lambda S, B, r: ('`mi` 还没有值，或这个 `cost` 更小 → 更新' if (B.mi is None or B.mi > S.cost) else f'`mi = {B.mi}` 不比 `cost = {S.cost}` 大，保持'),
        'mi = cost': '`mi` → =={mi}==',
        'return res': '`res + mi + 1` = `{res} + {mi} + 1` = =={ret}==；这个 1 是复制那一次',
    },
    cards=dict(
        one_liner='途中经过 nums2[-1] 就顺手复制，否则选最近的端点复制',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums1` 长 `n`，`nums2` 长 `n+1`；操作：某个数 `+1`、`-1`、或复制到末尾',
                 '求把 `nums1` 变成 `nums2` 的最少操作次数',
                 '示例：`[1,3,6]` → `[2,4,5,3]`，答案 `4`'],
        quote='对于下标为index的元素nums1[index]，如果在将其变换为nums2[index]的过程中恰好经过了nums2[-1]，那么只需在变成nums2[-1]的时刻将其复制到数组末尾就行了，也就是说对于这种情况没有额外的开销。',
        quote_src='—— yiduobo 题解原文',
        idea=['前 `n` 位的次数固定：`|nums1[i] - nums2[i]|`，累加到 `res`',
              '难点是 `nums2[-1]` 从哪来：途中经过它 → 额外开销 0',
              '否则在离它最近的端点复制，再调整：`target - max(..)` 或 `min(..) - target`',
              '`mi` 取所有位置里额外开销的最小值，最后加上复制的 1 次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '别忘了复制本身的 1 次操作：`return res + mi + 1`',
                 '三种情况：经过 target / target 更大 / target 更小',
                 '对比灵神：灵神先交换成 `x <= y`、用一个 `max` 表达式统一；yiduobo 写成三个分支'],
    ),
)
