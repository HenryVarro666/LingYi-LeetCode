def _col(S, i, v):
    if 'k' not in S or 'n' not in S or S['_line'] < 15:
        return None
    k, n = S['k'], S['n']
    if 1 < k < n:
        if i < k - 1:
            return 'green'
        if i == k:
            return 'yellow'
    return None


def _dim(S, i, v):
    if 'k' not in S or 'n' not in S or S['_line'] < 15:
        return False
    k, n = S['k'], S['n']
    return 1 < k < n and not (i < k - 1 or i == k)


def _text(S):
    if 'n' not in S:
        return '先按 `n` 和 `k` 分情况：`n = 1` → `k` 奇偶；`n > 1` → 看 `k` 与 `n` 的大小'
    n, k = S['n'], S['k']
    if S['_line'] < 15 and n > 1:
        return f'`n = {n}`，`k = {k}`：从特殊情况 `k = 0`、`k = 1` 开始逐个排除'
    if n == 1:
        return '`n = 1`：只能「删、放、删、放…」，看 `k` 的奇偶'
    if k == 0:
        return '`k = 0`：一次操作都不能做 → `nums[0]`'
    if k == 1:
        return '`k = 1`：只能删掉栈顶 → `nums[1]`'
    if k < n:
        return f'`1 < k < n`：前 `k-1` 个（绿）弹出后挑最大放回，或直接弹 `k` 个露出 `nums[{k}]`（黄）'
    if k == n:
        return '`k = n`：不能把栈弹空，只看前 `n-1` 个的最大值'
    return '`k > n`：全部弹出还有富余 → 整个数组的最大值'


CONFIG = dict(
    num=2202, title='K 次操作后最大化顶端元素', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按 n 与 k 分情况讨论',
    tags=['灵神题单', '难度分 1717'],
    code='''
class Solution(object):
    def maximumTop(self, nums, k):

        n = len(nums)
        if n == 1:
            if k % 2 == 0:
                return nums[0]
            else:
                return -1

        if k == 0:
            return nums[0]
        elif k == 1:
            return nums[1]
        elif k < n:
            return max(nums[k], max(nums[:k - 1]))
        elif k == n:
            return max(nums[:n - 1])
        else:
            return max(nums)
''',
    call='Solution().maximumTop([5,2,2,4,0,6], 4)',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='array', var='nums', pointers={'k': 'pink'}, h=260, color=_col, dim=_dim),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink')],
    captions={
        'n = len(nums)': '`n = len(nums) = {n}`，`k = {k}`：先看数组长度',
        'if n == 1': lambda S, B, r: ('`n = 1`：栈只有一个元素，要单独讨论' if S.n == 1 else '`n = {}`，不是单元素，往下看 `k`'.format(S.n)),
        'if k == 0': '`k = {k}`：不等于 0，有操作空间' ,
        'elif k == 1': '`k = {k}`：不等于 1，继续',
        'elif k < n': '`k = {k} < n = {n}`：成立 → 属于 `1 < k < n`',
        'return max(nums[k], max(nums[:k - 1]))': '两种策略取大：前 `k-1` 个弹出再放回最大的 `max(nums[:{k-1}]) = {max(nums[:k-1])}`；或弹 `k` 个露出 `nums[{k}] = {nums[k]}` → 返回 `{ret}`',
        'return nums[0]': '`k` 为偶数或 `k = 0`：回到 `nums[0]`',
        'return -1': '`k` 为奇数，最后栈空 → `-1`',
        'return nums[1]': '只能弹出栈顶 → `nums[1]`',
        'return max(nums[:n - 1])': '`k = n`：前 `n-1` 个里的最大值',
        'return max(nums)': '`k > n`：全弹出再放回最大的，多余操作靠其他元素进出消耗 → 最大值',
    },
    cards=dict(
        one_liner='先看 n=1 的特例，再按 k 与 n 的大小分五种情况',
        complexity='时间 `O(n)`，空间 `O(n)`（切片会复制）',
        problem=['`nums[0]` 是栈顶；每次操作==弹出栈顶==或==放回一个弹出过的数==',
                 '恰好 `k` 次操作后求栈顶最大值，栈空则 `-1`',
                 '示例：`nums=[5,2,2,4,0,6], k=4` → `5`'],
        quote='注意到样例2，那么应该先考虑数组长度n = 1的情况。此时若k为奇数，那么答案就是-1，否则就是nums中的唯一元素nums[0]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k > n`：先全部弹出，留一次放回最大值，其余操作让别的数进出',
              '`1 < k <= n`：弹 `k-1` 个，再放回其中最大的 → `max(nums[:k-1])`',
              '`k < n` 时还可以直接弹 `k` 个，露出 `nums[k]`；`k = n` 不行，会弹空'],
        after=[dict(heading='五种情况汇总', lines=[
            '`n = 1`：`k` 奇数 `-1`，偶数 `nums[0]`',
            '`k = 0` → `nums[0]`；`k = 1` → `nums[1]`',
            '`1 < k < n` → `max(nums[:k-1], nums[k])`',
            '`k = n` → `max(nums[:k-1])`；`k > n` → `max(nums)`'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`k = n` 时不能取 `nums[k]`（越界，也会弹空）',
                 '`k = 1` 要单独写，因为 `nums[:0]` 为空，`max` 会报错',
                 '原文无 Python 2 专有写法，未做修改'],
    ),
)
