CONFIG = dict(
    num=2562, title='找出数组的串联值', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='两侧向中间 · 字符串拼接',
    tags=[],
    code='''
class Solution(object):
    def findTheArrayConcVal(self, nums):

        res = 0
        left = 0
        right = len(nums) - 1
        while left < right:
            res += int(str(nums[left]) + str(nums[right]))
            left += 1
            right -= 1
        
        if left == right:
            res += nums[left]
        
        return res
''',
    call='Solution().findTheArrayConcVal([5, 14, 13, 8, 12])',
    expect=673,
    views=[
        dict(type='text', fn=lambda S: (f"拼接：`'{S['nums'][S['left']]}' + '{S['nums'][S['right']]}'` = `{S['nums'][S['left']]}{S['nums'][S['right']]}`" if 'right' in S and S['left'] < S['right'] and S['_line'] == 8 else ''), size=28, h=70),
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=300,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计串联值',
        'left = 0': '`left = 0`，从左边开始',
        'right = len': '`right = {right}`，从右边开始',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：两端各有一个数，拼接' if S.left < S.right else f'`left = {S.left} ≥ right = {S.right}`：两两配对结束'),
        'res += int': '`int(str({nums[left]}) + str({nums[right]}))` = `{int(str(nums[left]) + str(nums[right]))}`，累加 → `res = {res}`',
        'left += 1': '`left` 右移 → {left}',
        'right -= 1': '`right` 左移 → {right}',
        'if left == right': lambda S, B, r: (f'`left == right == {S.left}`：长度为奇数，中间还剩一个数' if S.left == S.right else '`left != right`：长度为偶数，没有剩余'),
        'res += nums[left]': '中间的数没人配对，直接加 `{nums[left]}` → `res = {res}`',
        'return res': '串联值 `{res}`',
    },
    cards=dict(
        one_liner='两端向中间走，转字符串拼接后累加',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['每次取首尾两个数拼成一个新数，加到串联值上',
                 '只剩一个数时，直接加上这个数',
                 '示例：`[7,52,2,4]` → `74 + 522 = 596`'],
        quote='从两侧向中间遍历数组，每一轮都将遍历到的两个数拼接起来累加到最终答案中。需要注意数组长度为奇数的情况，此时需要额外将数组正中间的数也累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left`、`right` 从两端向中间靠拢',
              '拼接直接用字符串：`str(a) + str(b)` 再转回 `int`',
              '循环结束后若 `left == right`，补加中间那个数'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`（临时字符串）',
                 '易错：奇数长度别漏掉正中间的数',
                 '原文本身是 Python 3 可运行的写法，无需修改',
                 '对比灵神：灵神不转字符串，用 `x *= 10` 数位左移'],
    ),
)
