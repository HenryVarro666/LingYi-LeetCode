CONFIG = dict(
    num=2740, title='找出分区值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 遍历相邻差', tags=['难度分 1302'],
    code='''
class Solution(object):
    def findValueOfPartition(self, nums):

        nums.sort()
        res = None
        for index in range(1, len(nums)):
            if res is None or res > nums[index] - nums[index - 1]:
                res = nums[index] - nums[index - 1]
        
        return res
''',
    call='Solution().findValueOfPartition([100,1,10,13,4])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=280, label='nums',
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and 'res' in S and S['res'] is not None and S['res'] == S['nums'][S['index']] - S['nums'][S['index']-1] and i in (S['index']-1, S['index']) else None),
        dict(type='text', h=130, size=34, fn=lambda S: (
            f"划分点在 `nums[{S['index']-1}]` 和 `nums[{S['index']}]` 之间：差 `{S['nums'][S['index']]}−{S['nums'][S['index']-1]}={S['nums'][S['index']]-S['nums'][S['index']-1]}`，当前最小 =={S['res']}==" if 'index' in S and S.get('res') is not None else '')),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '先排序：`{nums}`。左边是 nums1、右边是 nums2，分界处必须是相邻两数',
        'res = None': '`res` 记录最小分区值，还没有候选',
        'if res is None': '`res` 为空或比 `{nums[index]} - {nums[index-1]}` = {nums[index]-nums[index-1]} 更大吗？ → {res is None or res > nums[index]-nums[index-1]}',
        'res = nums': '更新最小值：`res = {res}`',
        'return': '遍历完所有相邻差，最小的就是答案 =={ret}==',
    },
    cards=dict(
        one_liner='最优划分点两侧的数，在排序后一定相邻',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把数组分成两个非空部分 `nums1`、`nums2`',
                 '分区值 = `|max(nums1) - min(nums2)|`，求最小',
                 '示例：`[1,3,2,4]` → `1`'],
        quote='若原数组中存在某个整数v满足max(nums1) < v < min(nums2)，那么v如果属于nums1，此时的max(nums1)就应该是v而不是小于v，同样的v也不能属于nums2。',
        quote_src='—— yiduobo 题解',
        idea=['两种情况分开讨论：`max(nums1) < min(nums2)` 时，中间夹着别的数会矛盾',
              '`max(nums1) > min(nums2)` 时，夹着数 v 可以搬动元素让答案更小',
              '所以用来计算的两个数必然相邻：排序后遍历一遍相邻差'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：`res` 初值用 `None`，别用 0；下标从 1 开始',
                 '原文已是 Python 3 可运行写法，未改动'],
        before=[dict(heading='举例：[100,1,10]', lines=['排序得 `[1,10,100]`，相邻差 `9`、`90`', '取最小 `9`，即 `nums1=[1]`、`nums2=[10,100]`'])],
    ),
)
