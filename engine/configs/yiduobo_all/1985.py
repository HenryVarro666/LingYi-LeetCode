def _lt(a, b):
    return len(a) < len(b) or (len(a) == len(b) and a < b)


def _gt(a, b):
    return len(a) > len(b) or (len(a) == len(b) and a > b)


CONFIG = dict(
    num=1985, title='找出数组中的第 K 大整数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='快速选择 · 字符串大小比较',
    code='''
class Solution(object):
    def kthLargestNumber(self, nums, k):

        return self.search(nums, 0, len(nums) - 1, len(nums) - k + 1)

    def search(self, nums, left, right, k):
        if left == right:
            return nums[left]

        mid = nums[(left + right) // 2][:]
        i = left
        j = right
        while i <= j:
            while i <= right and len(nums[i]) < len(mid) or (len(nums[i]) == len(mid) and (nums[i] < mid)):
                i += 1
            while j >= left and len(nums[j]) > len(mid) or (len(nums[j]) == len(mid) and (nums[j] > mid)):
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j][:], nums[i][:]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
''',
    call="Solution().kthLargestNumber(['2','21','12','1','10'], 3)",
    expect='10',
    max_steps=90,
    views=[
        dict(type='text', size=26, h=90, fn=lambda S: (f"基准 `mid = {S['mid']}`，当前区间要找第 `{S['k']}` 小" if 'mid' in S else '第 `K` 大 = 第 `n-K+1` 小，用快速选择找')),
        dict(type='array', var='nums', h=240, cell=100, label='nums（小 → 大，先比长度再比字典序）',
             pointers={'i': 'blue', 'j': 'pink'}, window=('left', 'right'),
             dim=lambda S, idx, v: 'left' in S and 'right' in S and not (S['left'] <= idx <= S['right'])),
        dict(type='calls', h=210),
    ],
    watch=[('left', 'left', 'cyan'), ('right', 'right', 'orange'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), 'mid', ('k', 'k', 'green')],
    captions={
        'return self.search(nums, 0': '第 `K` 大 = 第 `n - K + 1` 小：`k = {len(nums) - k + 1}`，在 `[0, {len(nums) - 1}]` 里快速选择',
        'if left == right': lambda S, B, r: (f'区间只剩一个数 `{S.nums[S.left]}`，就是答案' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 还有多个数，继续划分'),
        'return nums[left]': '只剩一个数，返回 `{nums[left]}`',
        'mid = ': '取中间的数作基准 `mid = nums[{(left + right) // 2}]` = =={mid}==',
        'while i <= j': lambda S, B, r: (f'`i = {S.i} <= j = {S.j}`，继续交换' if S.i <= S.j else f'`i = {S.i} > j = {S.j}`：划分完成，`j` 左边都不大于 mid，`i` 右边都不小于 mid'),
        'while i <= right': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]}` 比 `mid = {S.mid}` 小（长度或字典序更小）→ `i` 可以右移' if _lt(S.nums[S.i], S.mid) else f'`nums[{S.i}] = {S.nums[S.i]}` 不比 `mid = {S.mid}` 小 → `i` 停在这里'),
        'while j >= left': lambda S, B, r: (f'`nums[{S.j}] = {S.nums[S.j]}` 比 `mid = {S.mid}` 大 → `j` 可以左移' if _gt(S.nums[S.j], S.mid) else f'`nums[{S.j}] = {S.nums[S.j]}` 不比 `mid = {S.mid}` 大 → `j` 停在这里'),
        'if i <= j': lambda S, B, r: (f'`i = {S.i} <= j = {S.j}`：这一对错位，==交换==' if S.i <= S.j else f'`i = {S.i} > j = {S.j}`：已错开，不用交换'),
        'nums[i], nums[j] =': '交换 `nums[{B.i}]` 与 `nums[{B.j}]` → `{nums}`',
        'i += 1': '`i` → {i}',
        'j -= 1': '`j` → {j}',
        'if j - left + 1 >= k': lambda S, B, r: (f'左半 `[{S.left}, {S.j}]` 有 `{S.j - S.left + 1}` 个 ≥ k={S.k} → 答案在左半，递归左半' if S.j - S.left + 1 >= S.k else f'左半只有 `{S.j - S.left + 1}` 个 < k={S.k}，答案不在左半'),
        'elif i - left >= k': lambda S, B, r: (f'`i - left = {S.i - S.left}` >= k={S.k}：第 k 小夹在 j 和 i 之间，等于 mid，直接取 `nums[{S.left + S.k - 1}]`' if S.i - S.left >= S.k else f'`i - left = {S.i - S.left}` < k={S.k}：答案在右半'),
        'return nums[left + k - 1]': '直接返回 `{nums[left + k - 1]}`',
        'return self.search(nums, left, j, k)': '递归左半 `[{B.left}, {B.j}]`，`k` 不变',
        'return self.search(nums, i, right': '递归右半 `[{B.i}, {B.right}]`：左边 `{B.i - B.left}` 个都比目标小，`k` 减去它们 → {B.k - (B.i - B.left)}',
    },
    cards=dict(
        one_liner='第 K 大 = 第 n-K+1 小，快速选择只递归含答案的一半',
        complexity='时间平均 `O(n)`（比较串另乘 m），空间 `O(log n)`',
        problem=['`nums` 是不含前导零的整数字符串，返回第 `k` 大的那个字符串',
                 '重复的数字算不同元素',
                 '本视频：`["2","21","12","1","10"], k=3` → `"10"`'],
        quote='找第K大数的字符串大整数版本，同样适用快速选择算法，只需要在判断大小时改为字符串数字的判断方式就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['把「第 K 大」换成从小到大的第 `n-K+1` 小',
              '以 `mid` 为基准双指针划分：`i` 跳过小的，`j` 跳过大的，错位就交换',
              '字符串比大小：==先比长度，再比字典序=='],
        summary=['时间平均 `O(n)`，最坏 `O(n^2)`；空间 `O(log n)`',
                 '原文为 Python 2 写法，`(left + right) / 2` 已改为 `//`',
                 '易错点：比较规则不能直接用字符串字典序；划分后三种情况要分清（左半 / 等于 mid / 右半）',
                 '对比灵神：灵神直接按规则整体排序，yiduobo 用快速选择省掉完整排序'],
    ),
)
