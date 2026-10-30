
CONFIG = dict(
    num=360, title='有序转化数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='抛物线两端取最远 + 相向双指针',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def sortTransformedArray(self, nums, a, b, c):

        n = len(nums)

        def f(x):
            return a * x * x + b * x + c

        if a == 0:
            if b == 0:
                return [c] * n
            else:
                res = [f(x) for x in nums]
                if b < 0:
                    res.reverse()
                return res
        
        else:
            if a > 0:
                delta = 1
            else:
                delta = -1

            left = 0
            right = n - 1
            res = []
            while left <= right:
                left_v = f(nums[left])
                right_v = f(nums[right])
                if left_v * delta > right_v * delta:
                    res.append(left_v)
                    left += 1
                else:
                    res.append(right_v)
                    right -= 1
            
            if a > 0:
                res.reverse()
            
            return res
''',
    call='Solution().sortTransformedArray([-4, -2, 2, 4], 1, 3, 5)',
    expect=[3, 9, 15, 33],
    skip=['return a * x * x'],
    views=[
        dict(type='array', var='nums', h=190, label='nums（蓝 = left，粉 = right）',
             pointers={'left': 'blue', 'right': 'pink'},
             dim=lambda S, i, v: 'right' in S and 'res' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: ('blue' if i == S['left'] else 'pink' if i == S['right'] else None) if 'right' in S else None),
        dict(type='array', var='res', h=190, label='res：按「离顶点从远到近」依次加入'),
        dict(type='text', fn=lambda S: (f"`f(nums[left]) = {S['left_v']}`，`f(nums[right]) = {S['right_v']}`；a {'> 0 开口向上：越远越大' if S['a'] > 0 else '< 0 开口向下：越远越小'}"
                                 if 'left_v' in S and 'right_v' in S and 30 <= S['_line'] <= 35 else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('left_v', 'left_v', 'blue'), ('right_v', 'right_v', 'pink'), ('delta', 'delta', 'yellow')],
    captions={
        'n = len': '`n` 是数组长度',
        'def f': '`f(x) = a x^2 + b x + c`：这题要对每个数算 f 再排序',
        'if a == 0': lambda S, B, ret: ('`a == 0`：f 是直线或常数，单独处理' if S.a == 0 else '`a != 0`：f 是抛物线，往下走第三种情况'),
        'if a > 0': lambda S, B, ret: ('`a > 0`：开口向上，`delta = 1`；`a < 0` 开口向下，`delta = -1`，统一用 `delta` 比较' if S['_line'] < 30
                                       else '`a > 0`：加入的顺序是「大 → 小」，要反转成升序'),
        'delta = 1': '开口向上：离顶点越远，f 越大，`delta = 1`',
        'left = 0': '`left` 指向最小的数，离顶点可能最远',
        'right = n - 1': '`right` 指向最大的数：`right = {right}`',
        'res = []': '`res` 先放离顶点最远的值，所以最终要反转',
        'while left <= right': lambda S, B, ret: (f'`left = {S.left} <= right = {S.right}`，还有数没处理' if S.left <= S.right
                                                  else f'`left = {S.left} > right = {S.right}`：都处理完了'),
        'left_v = f': '`f({nums[left]}) = {a * nums[left] ** 2 + b * nums[left] + c}`：代入左端的数',
        'right_v = f': '`f({nums[right]}) = {a * nums[right] ** 2 + b * nums[right] + c}`：代入右端的数',
        'if left_v * delta': lambda S, B, ret: (
            f'`{S.left_v} * {S.delta} > {S.right_v} * {S.delta}`：左端离顶点更远 → 取左端' if S.left_v * S.delta > S.right_v * S.delta
            else f'`{S.left_v} * {S.delta} <= {S.right_v} * {S.delta}`：右端更远（或相等）→ 取右端'),
        'res.append(left_v)': '把 `{left_v}` 加入 `res`，`left` 将右移到 {left + 1}，剩下的数离顶点更近',
        'res.append(right_v)': '把 `{right_v}` 加入 `res`，`right` 将左移到 {right - 1}，剩下的数离顶点更近',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'res.reverse': '开口向上时 `res` 是从大到小加入的 → ==反转==成升序：`{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='抛物线两端离顶点最远：每次取两端中更极端的那个',
        complexity='时间 `O(n)`，空间 `O(n)`（输出）',
        problem=['给定升序数组 `nums` 和 `a, b, c`，对每个 `x` 算 `f(x) = ax² + bx + c`，返回升序结果',
                 '示例：`nums = [-4,-2,2,4], a = 1, b = 3, c = 5` → `[3,9,15,33]`'],
        quote='每次将nums剩余数中的最大值nums[right]和最小值nums[left]带入到f(x)，然后根据a与0的大小关系就可以判断f(nums[left])和f(nums[right])哪个离极值点更远。将更远的这个值加入到答案数组中，然后将对应的指针向中间移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a = 0`：`f` 是直线（或常数），逐个代入，`b < 0` 时反转',
              '`a != 0`：`f` 是抛物线，剩余数的最值一定在两端，更远的离极值点更远',
              '用 `delta` 统一两种开口方向：`left_v * delta > right_v * delta`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`a > 0` 时按远到近加入是降序，需要 `res.reverse()`；`a < 0` 则天然升序',
                 '`a == 0` 要先拆开：`b == 0` 返回 `n` 个 `c`',
                 '本视频示例只走 `a > 0` 的分支'],
    ),
)
