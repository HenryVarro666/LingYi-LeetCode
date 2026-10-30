CONFIG = dict(
    num=3774, title='最大和最小 K 个元素的绝对差', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='排序后前后各取 k 个',
    code='''
class Solution(object):
    def absDifference(self, nums, k):
        
        nums.sort()
        return sum(nums[-k:]) - sum(nums[:k])
''',
    call='Solution().absDifference([5,2,7,2,4,1,6,3], 3)',
    expect=13,
    views=[
        dict(type='text', size=34, fn=lambda S: ('后 k 个之和 ==' + str(sum(S['nums'][-S['k']:])) + '==  −  前 k 个之和 ==' + str(sum(S['nums'][:S['k']])) + '==') if S['nums'] == sorted(S['nums']) else '还没排序：最大、最小的元素散落在各处'),
        dict(type='array', var='nums', h=300, label='nums（绿 = 前 k 个，粉 = 后 k 个）',
             color=lambda S, i, v: ('green' if i < S['k'] else 'pink' if i >= len(S['nums']) - S['k'] else None) if S['nums'] == sorted(S['nums']) else None),
    ],
    watch=['k'],
    captions={
        'nums.sort()': '按从小到大排序 → `{nums}`，此后前 {k} 个就是最小的，后 {k} 个就是最大的',
        'return sum': '后 {k} 个之和 =={sum(nums[-k:])}== 减去前 {k} 个之和 =={sum(nums[:k])}== = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='为什么排序就够了', lines=['题目只关心最大的 k 个和最小的 k 个，不关心它们原来的位置', '排序后它们分别就是末尾 k 个和开头 k 个', '`k = n` 时两段相同，差为 0，例如 `[100], k=1`'])],
        before=[dict(heading='示例拆解', lines=['`[5,2,2,4], k=2`：最大两个 `4,5`，和 9', '最小两个 `2,2`，和 4', '差 `9 - 4 = 5`'])],
        one_liner='排序，后 k 个之和减去前 k 个之和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给数组 `nums` 和整数 `k`，求 k 个最大元素之和与 k 个最小元素之和的差',
                 '示例：`[5,2,2,4], k=2` → `(4+5) - (2+2) = 5`',
                 '演示用：`[5,2,7,2,4,1,6,3], k=3` → `13`'],
        quote='将nums按从小到大的顺序排序，然后使用后k个元素之和减去前k个元素之和即可。',
        quote_src='—— yiduobo 题解',
        idea=['题目要的是两端元素的和，先排序就能让它们各自聚在一起',
              '排好序后，直接用切片求和即可'],
        summary=['时间 `O(n log n)`，主要是排序',
                 '后 k 个之和不会小于前 k 个之和，所以不用取绝对值',
                 '易错点：`nums[-k:]` 是末尾 k 个'],
    ),
)
