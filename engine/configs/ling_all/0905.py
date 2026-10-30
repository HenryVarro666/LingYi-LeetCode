CONFIG = dict(
    num=905, title='按奇偶排序数组', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 交换',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        i, j = 0, len(nums) - 1
        while i < j:  # 循环直到不足两个数
            if nums[i] % 2 == 0:  # 寻找最左边的奇数
                i += 1
            elif nums[j] % 2 == 1:  # 寻找最右边的偶数
                j -= 1
            else:
                nums[i], nums[j] = nums[j], nums[i]
                # 交换后，问题变成 [i+1,j-1] 的子问题
                i += 1
                j -= 1
        return nums
''',
    call='Solution().sortArrayByParity([3,1,2,4,5,6,7])',
    expect=[6, 4, 2, 1, 5, 3, 7],
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), h=300,
             color=lambda S, idx, v: ('green' if v % 2 == 0 else 'orange') if ('i' in S and (idx < S['i'] or idx > S['j'])) else None,),
        dict(type='text', fn=lambda S: '绿 = 已就位的偶数，橙 = 已就位的奇数，框内是待处理的子问题'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'i, j = 0': '`i` 从左、`j` 从右往中间走：`i = {i}`，`j = {j}`',
        'while i < j': '`i = {i}`，`j = {j}`：{"还有至少两个数 → 继续" if i < j else "不足两个数 → 结束"}',
        'if nums[i] % 2 == 0': '`nums[{i}] = {nums[i]}` 是{"偶数 → 已经在前面的正确一侧，`i` 要右移" if nums[i] % 2 == 0 else "奇数 → 这就是最左边的奇数，找到了"}',
        'elif nums[j] % 2 == 1': '`nums[{j}] = {nums[j]}` 是{"奇数 → 已经在后面的正确一侧，`j` 要左移" if nums[j] % 2 == 1 else "偶数 → 这就是最右边的偶数，找到了"}',
        'i += 1': '`i` → {i}',
        'j -= 1': '`j` → {j}',
        'nums[i], nums[j] =': '左边是奇数、右边是偶数 → 交换，`nums = {nums}`',
        'return nums': '返回 `{nums}`',
    },
    cards=dict(
        one_liner='左边找奇数、右边找偶数，找到就交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把所有偶数移到数组前面，奇数放后面',
                 '返回任一满足条件的数组即可',
                 '示例：`[3,1,2,4]` → `[2,4,3,1]`，本视频用 `[3,1,2,4,5,6,7]`'],
        quote='找到最左边的奇数 nums[i] 和最右边的偶数 nums[j]，交换这两个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['交换后，`[0,i]` 全是偶数，`[j,n-1]` 全是奇数',
              '剩下 `[i+1,j-1]` 是规模更小的同样子问题',
              '`i` 跳过偶数，`j` 跳过奇数，都卡住了才交换'],
        summary=['时间 `O(n)`，空间 `O(1)`，每步至少缩小一格',
                 '用 `if / elif / else` 三选一，每轮只动一个指针或交换',
                 '循环条件 `i < j`：不足两个数时没有需要交换的对',
                 '同类：第 75 题荷兰国旗、第 922 题'],
    ),
)
