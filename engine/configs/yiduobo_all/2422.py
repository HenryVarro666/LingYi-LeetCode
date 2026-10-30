def _txt(S):
    if 'right' not in S or 'left' not in S:
        return ''
    l, r, a = S['left'], S['right'], S['nums']
    if l >= r:
        return '两指针相遇，不需要再合并'
    if a[l] == a[r]:
        return f'`nums[{l}] = nums[{r}] = {a[l]}`：两端配对成功'
    if a[l] < a[r]:
        return f'`{a[l]} < {a[r]}`：较小的左端必须并入右邻居'
    return f'`{a[l]} > {a[r]}`：较小的右端必须并入左邻居'


CONFIG = dict(
    num=2422, title='使用合并操作将数组转换为回文序列', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针 · 小的一端合并',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minimumOperations(self, nums):

        res = 0
        left = 0
        right = len(nums) - 1
        while left < right:
            while nums[left] != nums[right]:
                res += 1
                if nums[left] < nums[right]:
                    left += 1
                    nums[left] += nums[left - 1]
                else:
                    right -= 1
                    nums[right] += nums[right + 1]

            left += 1
            right -= 1

        return res
''',
    call='Solution().minimumOperations([4,3,2,1,2,3,1])',
    expect=2,
    views=[
        dict(type='text', h=70, size=32, fn=_txt),
        dict(type='array', var='nums', label='nums（合并后的值写在右/左邻居上）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), h=330, cell=100,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right'])),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录合并操作的次数',
        'left = 0': '从两侧向中间考虑：`left = 0`',
        'right = len': '`right = len(nums) - 1 = {right}`',
        'while left < right': lambda S, B, r: ('`left < right`：中间还有没配对的数' if S.left < S.right
                                               else f'`left = {S.left} ≥ right = {S.right}`：指针相遇，回文已成'),
        'while nums[left] != nums[right]': lambda S, B, r: (
            f'`nums[{S.left}] = {S.nums[S.left]}`，`nums[{S.right}] = {S.nums[S.right]}`：==不相等==，必须合并'
            if S.nums[S.left] != S.nums[S.right] else
            f'`nums[{S.left}] = nums[{S.right}] = {S.nums[S.left]}`：相等，这一对已配好'),
        'res += 1': '又要合并一次：`res` → {res}',
        'if nums[left] < nums[right]': '`{nums[left]}` 对 `{nums[right]}`：数都是正数，合并只会变大，==较小的一侧==必须合并',
        11: '左端更小：`left` 右移到 {left}，准备把它并进来',
        'nums[left] += nums[left - 1]': '合并：`nums[{left}]` = `{B.nums[left]} + {B.nums[left-1]}` = =={nums[left]}==',
        14: '右端更小：`right` 左移到 {right}，准备把它并进来',
        'nums[right] += nums[right + 1]': '合并：`nums[{right}]` = `{B.nums[right]} + {B.nums[right+1]}` = =={nums[right]}==',
        17: '这一对配好了：`left` → {left}',
        18: '`right` → {right}，两端一起向中间',
        'return res': '一共合并 `{res}` 次',
    },
    cards=dict(
        one_liner='数都是正数，合并只会变大：哪端小就并哪端',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个正整数数组，一次操作可以把==相邻两个数==替换成它们的和',
                 '求把数组变成回文的最少操作次数',
                 '示例：`[4,3,2,1,2,3,1]` → `2`'],
        quote='由于数组中的数都为正数，那么合并操作只能让数组中的数变得更大。基于这一点，不妨从两侧开始向中间考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['两端相等：这一对已配好，`left`、`right` 一起向中间',
              '两端不等：==较小的一侧必须合并==（大的一侧再合并只会更大）',
              '小的并入邻居后，新值写在邻居上，继续比较'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '合并后的值直接写回 `nums`，所以会修改输入',
                 '相遇（`left == right`）时中间只剩一个数，天然回文',
                 '原文已是 Python 3 可运行的写法，只删去了空行里的多余空格',
                 '同类：双指针 + 贪心，哪边小就动哪边'],
    ),
)
