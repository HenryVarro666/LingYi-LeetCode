CONFIG = dict(
    num=1846, title='减小和重新排列数组后的最大元素', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 逐个压到前一个+1',
    tags=['灵神题单', '难度分 1454'],
    code='''
class Solution:
    def maximumElementAfterDecrementingAndRearranging(self, arr: List[int]) -> int:
        arr.sort()
        arr[0] = 1
        for i in range(1, len(arr)):
            arr[i] = min(arr[i], arr[i - 1] + 1)
        return arr[-1]
''',
    call='Solution().maximumElementAfterDecrementingAndRearranging([100,1,1000,2,2,7])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"`arr[{S['i']}] = min(原值, arr[{S['i']-1}] + 1)`，相邻差不超过 1" if 'i' in S and S['i'] >= 1 else '先排序，再让每个数最多比前一个大 1'),
        dict(type='array', var='arr', pointers={'i': 'blue'}, h=300,
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('arr', 'arr', 'green')],
    captions={
        'arr.sort()': '==从小到大排序==：要减小就先减小的数，保住大的数。排序后 `arr = {arr}`',
        'arr[0] = 1': '第一个元素必须是 1：最小的数一定能减到 1 → `arr[0] = 1`',
        'arr[i] = min': '`min({B.arr[i]}, {arr[i-1]} + 1)`：超过前一个 +1 就压下来，否则保持 → `arr[{i}] = {arr[i]}`',
        'return arr[-1]': '序列非降且每步最多 +1，最大值就是最后一个：返回 `{arr[-1]}`',
    },
    cards=dict(
        one_liner='排序后，每个数最多比前一个大 1',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给正整数数组 `arr`，可以任意减小元素、任意重排',
                 '要求 `arr[0] = 1`，且相邻元素差的绝对值 `<= 1`，求最大可能的元素',
                 '示例：`[100,1,1000]` → `3`；本视频：`[100,1,1000,2,2,7]` → `5`'],
        quote='本题的贪心策略是简单的，难点在证明。把 arr 从小到大排序。把 arr[0] 变成 1。如果 arr[i] > arr[i-1]+1，则把 arr[i] 减小为 arr[i-1]+1，否则不变。答案为 arr[n-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法序列升序排序后仍合法（介值定理反证），所以只看升序的最终序列',
              '交换论证：最优解里 `b[i] <= a[i]` 总成立，不用再重排',
              '于是递推 `arr[i] = min(arr[i], arr[i-1] + 1)`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '易错：第一个数要先置 1；排序必不可少',
                 '写法二：答案至多为 n，大于 n 的数当作 n 做计数排序，`ans = min(ans + cnt[x], x)`，`O(n)`',
                 '同类：贪心 §1.1 从最小/最大开始、§1.7 交换论证法'],
    ),
)
