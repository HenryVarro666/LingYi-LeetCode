CONFIG = dict(
    num=3627, title='中位数之和的最大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='降序排序隔一个取一个',
    tags=['贪心', '排序', '难度分 1561'],
    code='''
class Solution(object):
    def maximumMedianSum(self, nums):
        
        res = 0
        nums.sort(reverse=True)
        index = 1
        for _ in range(len(nums) // 3):
            res += nums[index]
            index += 2
        
        return res
''',
    call='Solution().maximumMedianSum([4,1,9,2,7,3,8,5,6])',
    expect=18,
    views=[
        dict(type='text', fn=lambda S: ('降序后每两个一组：大的陪跑，==次大的==当中位数' if 'index' in S else '先从大到小排序'), size=30),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=260,
             color=lambda S, i, v: ('green' if 'index' in S and i < S['index'] and i % 2 == 1 else None)),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '从大到小排序：`nums` = {nums}。最小的三分之一留给每组当「最小值」，其余两两配对',
        'for _ in': '还要选 `len(nums) // 3` = {len(nums)//3} 组，每组一个中位数',
        'index = 1': '最大值 `nums[0]` 注定当不了中位数（它得陪着次大值一组），所以从下标 `1` 开始取',
        'res += nums[index]': '第 `{index}` 个数 `{nums[index]}` 当这一组的中位数：`res = {B.res} + {nums[index]} = {res}`',
        'index += 2': '下标跳 `2`：每组用掉「一个大的 + 一个中位数」，下一组的中位数在 `{index}`',
        'return res': '一共取了 `n // 3` 次，中位数之和为 =={res}==',
    },
    cards=dict(
        one_liner='降序排序，取下标 1、3、5…，共取 n/3 个',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地排序）',
        problem=['每次从数组取 3 个数，移除，得分是它们的中位数',
                 '数组长度是 3 的倍数，清空数组，求中位数之和最大值',
                 '示例：`[2,1,3,2,1,3]` → `5`'],
        quote='最小的那三分之一的元素应该逐个分配到每次操作中，理由是每一组中必须有一个最小值，这三分之一的元素来填每一组的最小值是最合适的。',
        quote_src='—— yiduobo 题解',
        idea=['若某组的最小值不在最小的 1/3 里，必有另一组含两个小元素；交换后中位数只增不减',
              '剩下的数从大到小两两一组：最大的被浪费，次大的当中位数',
              '所以降序后取下标 `1, 3, 5, ...`'],
        summary=['时间 `O(n log n)`，主要是排序',
                 '易错点：不要从下标 0 开始取，最大值当不了中位数',
                 '取的次数是 `len(nums) // 3`，步长为 2',
                 '和 1561「你可以获得的最大硬币数目」完全一样'],
    ),
)
