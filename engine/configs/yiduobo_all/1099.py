CONFIG = dict(
    num=1099, title='小于 K 的两数之和', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 相向双指针',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def twoSumLessThanK(self, nums, k):

        nums.sort()

        left = 0
        right = len(nums) - 1
        res = -1
        while left < right:
            if nums[left] + nums[right] < k:
                res = max(res, nums[left] + nums[right])
                left += 1
            else:
                right -= 1
        
        return res
''',
    call='Solution().twoSumLessThanK([34, 23, 1, 24, 75, 33, 54, 8], 60)',
    expect=58,
    views=[
        dict(type='array', var='nums', h=260, label='nums（排序后；蓝 = left，粉 = right）',
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None),
        dict(type='text', fn=lambda S: (f"`{S['nums'][S['left']]} + {S['nums'][S['right']]}` = =={S['nums'][S['left']] + S['nums'][S['right']]}==，k = {S['k']}；目前最大的合法和 `res = {S['res']}`"
                                 if 'res' in S and 'right' in S and S['left'] < S['right'] else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '又是两数之和：==先排序==，再让双指针从两侧往中间扫',
        'left = 0': '`left` 指向最小的数',
        'right = len': '`right` 指向最大的数：`right = {right}`',
        'res = -1': '`res = -1`：找不到小于 k 的和时就返回 -1',
        'while left < right': lambda S, B, ret: (f'`left = {S.left} < right = {S.right}`，还有两个不同的数可选' if S.left < S.right
                                                 else f'`left = {S.left} >= right = {S.right}`：扫完了'),
        'if nums[left] + nums[right] < k': lambda S, B, ret: (
            f'`{S.nums[S.left]} + {S.nums[S.right]} = {S.nums[S.left] + S.nums[S.right]} < {S.k}`：合法；`nums[left]` 还可以配更小的 right 找更大的和'
            if S.nums[S.left] + S.nums[S.right] < S.k else
            f'`{S.nums[S.left]} + {S.nums[S.right]} = {S.nums[S.left] + S.nums[S.right]} >= {S.k}`：和太大，`nums[right]` 配任何更大的 left 也不行'),
        'res = max': '更新最大合法和：`max({B.res}, {nums[left] + nums[right]}) = {res}`',
        'left += 1': '和还小于 k，`left` 右移让和变大，看能不能更接近 k：`left` → {left}',
        'right -= 1': '和 `>= k`，`right` 左移让和变小：`right` → {right}',
        'return res': '返回最大的合法和 `{res}`',
    },
    cards=dict(
        one_liner='排序后双指针：和太大缩右端，和合法就记录并增大左端',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['在 `nums` 中选两个下标不同的数，使和 ==小于 k== 且最大，没有就返回 `-1`',
                 '示例：`nums = [34,23,1,24,75,33,54,8], k = 60` → `58`（`34 + 24`）'],
        quote='又回到了两数之和问题。直接使用第一题中的处理方法，排序后双指针从两侧往中间扫进行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，左右指针各指最小和最大',
              '和 `< k`：合法，更新答案，`left` 右移想让和更大',
              '和 `>= k`：太大，`right` 左移让和变小'],
        summary=['时间 `O(n log n)`（排序），空间 `O(1)`',
                 '`res` 初值 `-1` 对应「不存在」',
                 '`while left < right`：不能选同一个下标',
                 '同类题：167 两数之和 II、15 三数之和'],
    ),
)
