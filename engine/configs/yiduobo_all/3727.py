CONFIG = dict(
    num=3727, title='最大交替平方和', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按绝对值排序 + 首尾双指针',
    tags=['灵神题单', '贪心与思维', '难度分 1455'],
    code='''
class Solution(object):
    def maxAlternatingSum(self, nums):

        nums.sort(key=lambda d:abs(d))
        left, right = 0, len(nums) - 1
        res = 0
        while left <= right:
            res += nums[right] ** 2
            right -= 1
            if left <= right:
                res -= nums[left] ** 2
                left += 1

        return res
''',
    call='Solution().maxAlternatingSum([1,-1,2,-2,3,-3,4])',
    expect=32,
    views=[
        dict(type='text', fn=lambda S: f"`res = {S['res']}`：右边取绝对值最大的加上，左边取最小的减去" if 'res' in S else '先按绝对值从小到大排序'),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, h=300, label='nums（按绝对值升序）',
             window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '按==绝对值==从小到大排序：绝对值越大平方越大。`{nums}`',
        'left, right': '`left = 0` 指最小，`right = {right}` 指最大',
        'res = 0': '`res` 累计交替得分',
        'while left <= right': lambda S, B, r: (f'`left = {S.left} <= right = {S.right}`，还有数没用' if S.left <= S.right else f'`left = {S.left} > right = {S.right}`，数全用完 → 结束'),
        'res += ': '取剩余里绝对值最大的 `{nums[right]}`，平方 ==加上==：`res` → {res}',
        'right -= 1': '`right` 左移到 {right}',
        'if left <= right': lambda S, B, r: (f'`left <= right` 成立：还剩数可以放到奇数下标' if S.left <= S.right else '`left > right`：没有剩余的数了，不用减'),
        'res -= ': '取剩余里绝对值最小的 `{nums[left]}`，平方 ==减去==：`res` → {res}',
        'left += 1': '`left` 右移到 {left}',
        'return res': '最大交替得分 `{res}`',
    },
    cards=dict(
        one_liner='大的平方放加号位，小的平方放减号位',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`nums` 可任意重排，`score = arr[0]^2 - arr[1]^2 + arr[2]^2 - ...`',
                 '求最大可能得分',
                 '本视频：`[1,-1,2,-2,3,-3,4]` → `32`'],
        quote='为了使得最终答案最大，就应该让偶数下标项的平方尽量大，奇数下标项的平方尽量小。',
        quote_src='—— yiduobo 题解原文',
        idea=['一个数的平方只看绝对值，所以按绝对值排序',
              '双指针从两端向中间：先取最大的加上，再取最小的减去',
              '重复到所有数用完（奇数个时最后一个落在加号位）'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（原地排序）',
                 '易错：减号那步要再判断一次 `left <= right`，奇数个时最后一个数只加不减',
                 '原文为 Python 2 风格，本题无需改动（原文公式里的 `arr[3]^3` 是笔误）',
                 '对比灵神：灵神平方后直接切片求和，这里用双指针模拟取数顺序'],
    ),
)
