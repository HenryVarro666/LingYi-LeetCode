CONFIG = dict(
    num=3865, title='反转K个子数组', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='分段 · 相向双指针交换',
    code='''
class Solution(object):
    def reverseSubarrays(self, nums, k):
        
        n = len(nums)
        length = n // k
        for index in range(0, n, length):
            left, right = index, index + length - 1
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1
        
        return nums
''',
    call='Solution().reverseSubarrays([1,2,3,4,5,6,7,8], 2)',
    expect=[4, 3, 2, 1, 8, 7, 6, 5],
    views=[
        dict(type='text', fn=lambda S: (f"当前这一段：下标 `{S['index']}` ~ `{S['index'] + S['length'] - 1}`，每段长 `{S['length']}`" if 'index' in S else (f"每段长 `n // k` = `{S['length']}`" if 'length' in S else '')), size=30),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, h=300,
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else 'cyan' if S['index'] <= i < S['index'] + S['length'] else None) if 'right' in S else None,
             dim=lambda S, i, v: 'index' in S and not (S['index'] <= i < S['index'] + S['length'])),
    ],
    watch=['n', 'length', 'index', ('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'length = n // k': '分成 `k` 段，每段长 `n // k` = =={length}==（整除，所以每段一样长）',
        'for index in range': lambda S, B, r: (f'这一段的起点 `index` = =={S.index}==（起点依次是 0、length、2·length…）' if B.get('index') != S.index else '所有起点都处理完，循环结束'),
        'left, right = index': '段首 `left` = {left}，段尾 `right` = `index + length - 1` = =={right}==',
        'while left < right': lambda S, B, r: (f"`left = {S.left} < right = {S.right}`：中间还有没换的对 → 继续" if S.left < S.right else f"`left = {S.left} >= right = {S.right}`：两指针相遇或交错，这一段反转完了"),
        'nums[left], nums[right] =': '交换 `nums[{left}]` 与 `nums[{right}]`，两端各归位一个',
        'left += 1': '`left` 右移到 {left}',
        'right -= 1': '`right` 左移到 {right}',
        'return nums': '每段都反转过了，返回 `{nums}`',
    },
    skip=['n = len(nums)'],
    cards=dict(
        one_liner='按步长 length 切段，每段内相向双指针交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 长度 `n` 能被 `k` 整除，把它从左到右划分成 `k` 个等长连续子数组，并反转每个子数组',
                 '示例：`[1,2,3,4,5,6,7,8]`，`k = 2` → `[4,3,2,1,8,7,6,5]`'],
        quote='这些子数组的起点分别为0、k、2k、...，由于长度为k，那么对应的终点就是k - 1、2k - 1、3k - 1、...。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目要求连续划分，所以只能从左到右按固定长度切',
              '遍历每段的起点 `index`，终点 = `index + length - 1`',
              '`left`、`right` 相向移动并交换，直到相遇'],
        summary=['时间 `O(n)`，空间 `O(1)`，原地反转',
                 '每段长度是 `n // k`，不是 `k`；本例 `n = 8, k = 2`，每段长 4',
                 '原文变量名 `k` 在题里是段数，原文代码里的段长 `length` 才是步长',
                 '原文已是 Python 3 写法，无需修改'],
    ),
)
