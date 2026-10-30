def _seg(S, i, v):
    if 'i' not in S:
        return None
    mid = S.get('mid')
    if mid is not None:
        return 'blue' if i < mid else 'pink'
    return 'blue' if i < S['i'] else None


def _txt(S):
    if 'n' not in S:
        return ''
    i, n, mid = S['i'], S['n'], S.get('mid')
    if mid is None:
        return f'第一段递增：`nums[0..{i - 1}]`，长度 {i}'
    return f'第二段从 `mid = {mid}` 开始，长度 `n − mid = {n - mid}` = 右移次数'


CONFIG = dict(
    num=2855, title='使数组成为递增数组的最少右移次数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='至多两段递增子数组',
    code='''
class Solution:
    def minimumRightShifts(self, nums: List[int]) -> int:
        i, n = 1, len(nums)
        while i < n and nums[i - 1] < nums[i]:
            i += 1
        if i == n:
            return 0
        if nums[0] < nums[-1]:
            return -1
        mid = i
        i += 1
        while i < n and nums[i - 1] < nums[i]:
            i += 1
        if i < n:
            return -1
        return n - mid
''',
    call='Solution().minimumRightShifts([3,4,5,1,2])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, color=_seg, h=300),
        dict(type='text', fn=_txt, h=70),
    ],
    watch=['i', 'n', ('mid', "S.get('mid', '-')", 'pink')],
    captions={
        'i, n = 1': '`i = 1`，`n = {n}`：从下标 1 开始找第一段递增子数组的末尾',
        'while i < n and nums[i - 1] < nums[i]': lambda S, B, r: (
            f'`nums[{S.i - 1}] = {S.nums[S.i - 1]}` < `nums[{S.i}] = {S.nums[S.i]}`：仍然递增 → 继续'
            if S.i < S.n and S.nums[S.i - 1] < S.nums[S.i]
            else (f'`i = {S.i} = n`：已走到数组末尾，这一段到头了' if S.i >= S.n
                  else f'`nums[{S.i - 1}] = {S.nums[S.i - 1]}` > `nums[{S.i}] = {S.nums[S.i]}`：递增中断，这一段结束')),
        '            i += 1': '`i` → {i}，把递增段往后延伸',
        'if i == n': '`i == n`？{i} vs {n} → {"整个数组本来就递增，右移 0 次" if i == n else "不是，至少有两段"}',
        'if nums[0] < nums[-1]': '有两段时，第二段要拼到第一段前面，需要 `nums[0] > nums[-1]`：`{nums[0]}` vs `{nums[-1]}` → {"首 < 尾，拼起来不递增 → -1" if nums[0] < nums[-1] else "首 > 尾，可以拼"}',
        11: '`i += 1`：`nums[mid]` 已经属于第二段，从下一个元素继续往后看',
        'mid = i': '第二段的起点 `mid = {mid}`，它之后的元素要整体移到最前面',
        'if i < n': '`i < n`？{i} vs {n} → {"还有第三段 → 无法构成，返回 -1" if i < n else "第二段走到末尾，恰好两段"}',
        'return n - mid': '第二段长度 `n - mid` = `{n} - {mid}` = =={ret}==，就是需要右移的次数',
    },
    cards=dict(
        one_liner='最多两段递增，且第二段整体搬到最前面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 元素互不相同，一次右移把下标 `i` 的元素移到 `(i+1) % n`',
                 '求让数组变成递增的最少右移次数，不可能则返回 `-1`',
                 '示例：`[3,4,5,1,2]` → `2`'],
        quote='问题等价于：nums 有至多两段递增子数组；如果有两段，我们需要把第二段拼在第一段前面，所以还需要满足 nums[0] > nums[n-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['循环右移相当于把数组末尾一段整体搬到最前面',
              '所以原数组只能是两段递增，且第二段的末尾 < 第一段的开头',
              '先扫第一段，再记 `mid`、扫第二段；第二段长度就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：本来就递增要返回 0；有两段时还要检查 `nums[0] > nums[-1]`',
                 '第二段扫完若 `i < n`，说明有第三段，返回 `-1`',
                 '方法一是暴力：每次右移后用 pairwise 判断有序，`O(n^2)`'],
    ),
)
