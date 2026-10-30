CONFIG = dict(
    num=154, title='寻找旋转排序数组中的最小值 II', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='有重复 → 退化为线性扫描 min',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findMin(self, nums):

        return min(nums)
''',
    call='Solution().findMin([2, 2, 2, 0, 1, 2, 2])',
    expect=0,
    views=[
        dict(type='text', fn=lambda S: '`nums[mid] == nums[right]` 时无法判断旋转点在哪一半 → 二分失效', size=26, h=60),
        dict(type='array', var='nums', cell=96, h=330,
             color=lambda S, i, v: 'green' if v == min(S['nums']) else None),
    ],
    watch=[('min(nums)', 'min(nums)', 'green')],
    captions={
        'return min': '放弃二分，==扫一遍整个数组取最小值==：`min(nums) = {ret}`（绿格）',
    },
    cards=dict(
        before=[dict(heading='为什么二分不灵了', lines=['无重复：`nums[mid]` 和 `nums[right]` 比大小就能判断旋转点在哪半边',
                                                  '有重复：相等时两种情况都可能——`1 2 2 2 2 2 2` 和 `2 2 2 2 2 1 2`',
                                                  '想继续二分，只能 `right -= 1` 缩小一格，最坏全相同就是 `O(n)`']),
                dict(heading='所以直接取 min', lines=['最坏复杂度反正都是 `O(n)`', '干脆不二分：一行 `min(nums)`', '代码最短，也不会写错边界'])],
        one_liner='有重复元素，最坏就是 O(n)，不如直接 min',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['升序数组旋转若干次，元素可能重复，找最小值',
                 '上一题（153）没有重复，可以 `O(log n)` 二分',
                 '本视频：`[2,2,2,0,1,2,2]` → `0`'],
        quote='这样做的话最坏情况下二分就退化到了O(n)，于是干脆就选择O(n)的做法即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['例如 `1 2 2 2 2 2 2` 和 `2 2 2 2 2 1 2` 都是合法旋转',
              '第一次二分 `nums[mid] == nums[right]`，==看不出旋转点在哪半边==',
              '可以每次 `right -= 1`，但最坏全相同时本来就是 `O(n)`',
              '那就直接用 `min(nums)`，代码最短'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`min` 内部是一次线性扫描，视频里只表现为一步',
                 '对比灵神：灵神保留二分，相等时 `right -= 1`，通常更快，最坏同为 `O(n)`',
                 '无重复时（153 题）才值得二分，复杂度 `O(log n)`'],
    ),
)
