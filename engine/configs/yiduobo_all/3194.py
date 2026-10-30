CONFIG = dict(
    num=3194, title='最小元素和最大元素的最小平均值', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 双指针',
    tags=[],
    code='''
class Solution(object):
    def minimumAverage(self, nums):

        nums.sort()
        left, right = 0, len(nums) - 1
        res = None

        while left < right:
            v = (nums[left] + nums[right]) * 0.5
            if res is None or res > v:
                res = v
            left += 1
            right -= 1
        
        return res
''',
    call='Solution().minimumAverage([7,8,3,4,15,13,4,1])',
    expect=5.5,
    views=[
        dict(type='array', var='nums', h=280, label='nums', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', h=120, size=28,
             fn=lambda S: (f"当前一对 `{S['nums'][S['left']]}` 和 `{S['nums'][S['right']]}`，平均 =={(S['nums'][S['left']] + S['nums'][S['right']]) * 0.5}==" if 'right' in S and S['left'] < S['right'] else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'v', ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先从小到大排序：最小值在最左，最大值在最右 → `{nums}`',
        'left, right = 0': '两个指针从两侧向中间走：`left = 0`，`right = {right}`',
        'res = None': '`res` 保存最小平均值，先置为 `None`',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}`，还有一对没处理' if S.left < S.right
                                                else f'`left = {S.left} >= right = {S.right}`：n 个数两两配完 → 结束'),
        'v = (': '这一轮的最小是 `{nums[left]}`、最大是 `{nums[right]}`，平均值 `v` = =={v}==',
        'if res is None': lambda S, B, r: ('`res` 还是 `None`，直接记下这个平均值' if B.res is None
                                           else (f'`res = {S.res}` > `v = {S.v}`：更小，更新答案' if S.res > S.v
                                                 else f'`res = {S.res}` <= `v = {S.v}`：不更小，保持')),
        'res = v': '`res` 更新为 =={res}==',
        'left += 1': '最小值已用掉，`left` → {left}',
        'right -= 1': '最大值已用掉，`right` → {right}',
        'return res': '`n // 2` 个平均值里最小的是 =={res}==',
    },
    cards=dict(
        one_liner='排好序，两个指针从两头往中间走，边走边取最小平均',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`n` 为偶数，每轮移除当前最小和最大的元素，计算二者平均值',
                 '返回这 `n // 2` 个平均值中的最小值',
                 '示例：`[7,8,3,4,15,13,4,1]` → `5.5`'],
        quote='将nums从小到大进行排序，接下来只需两个指针从两侧向中间遍历，指向的元素就是当前这一轮需要的最小值和最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮都要取最值，排序后最值就在两端',
              '`left`、`right` 就是这一轮的最小值和最大值',
              '算出平均值 `v`，更新答案，两指针各向里走一步'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`res` 初值设为 `None`，第一次直接赋值，免去选无穷大',
                 '平均值用 `* 0.5` 得到浮点数',
                 '对比灵神：灵神比较两数之和、最后再除 2；yiduobo 每轮直接算平均值'],
    ),
)
