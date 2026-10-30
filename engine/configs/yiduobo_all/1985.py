def _cmp_i(S, B, r):
    if S.i > S.right:
        return f'`i = {S.i}` 超出右边界 → 左指针停下'
    a, m = S.nums[S.i], S.mid
    if len(a) < len(m):
        return f'`{a}` 位数 {len(a)} < `{m}` 位数 {len(m)} → 更小，`i` 继续右移'
    if len(a) == len(m) and a < m:
        return f'位数相同，字符串比较 `{a}` < `{m}` → 更小，`i` 继续右移'
    return f'`{a}` 不比基准 `{m}` 小 → `i` 停在 {S.i}'


def _cmp_j(S, B, r):
    if S.j < S.left:
        return f'`j = {S.j}` 超出左边界 → 右指针停下'
    a, m = S.nums[S.j], S.mid
    if len(a) > len(m):
        return f'`{a}` 位数 {len(a)} > `{m}` 位数 {len(m)} → 更大，`j` 继续左移'
    if len(a) == len(m) and a > m:
        return f'位数相同，字符串比较 `{a}` > `{m}` → 更大，`j` 继续左移'
    return f'`{a}` 不比基准 `{m}` 大 → `j` 停在 {S.j}'


def _col(S, i, v):
    return None


CONFIG = dict(
    num=1985, title='找出数组中的第 K 大整数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='快速选择（比较字符串大整数）',
    tags=[],
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
    call="Solution().kthLargestNumber(['3', '10', '7', '2', '6'], 2)",
    expect='7',
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 当前处理的区间 [left, right]）', cell=100, h=300,
             pointers={'i': 'blue', 'j': 'pink'}, window=('left', 'right'),
             color=lambda S, i, v: 'yellow' if 'mid' in S and v == S['mid'] and 'left' in S and S['left'] <= i <= S['right'] and False else None,
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='calls', h=200),
        dict(type='text', fn=lambda S: (f"基准 `mid = {S['mid']}`；目标：区间内从小到大第 `{S['k']}` 个" if 'mid' in S else (f"目标：从小到大第 `{S['k']}` 个" if 'k' in S and 'left' in S else ''))),
    ],
    watch=['left', 'right', 'k', 'mid', ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'return self.search(nums, 0': '第 `k` 大 = 从小到大第 `len(nums) − k + 1` 个：`{len(nums)} − {k} + 1 = {len(nums) - k + 1}`',
        'if left == right': lambda S, B, r: ('区间只剩一个数 → 它就是答案' if S.left == S.right else '区间还有 `%d` 个数，继续划分' % (S.right - S.left + 1)),
        'return nums[left]': '只剩一个数 `{nums[left]}` → 返回',
        'mid = nums': '取中间位置的数当基准：`mid = {mid}`（字符串，复制一份）',
        'i = left': '`i` 从区间最左开始',
        'j = right': '`j` 从区间最右开始',
        'while i <= j': lambda S, B, r: ('`i = %d ≤ j = %d`：两指针还没交错，继续划分' % (S.i, S.j)) if S.i <= S.j else ('`i = %d > j = %d`：交错，划分结束' % (S.i, S.j)),
        14: _cmp_i,
        16: _cmp_j,
        15: '`nums[i]` 比基准小，属于左半部分 → `i` → {i}',
        17: '`nums[j]` 比基准大，属于右半部分 → `j` → {j}',
        18: lambda S, B, r: ('`i = %d ≤ j = %d`：左边停在 ≥ 基准的数、右边停在 ≤ 基准的数 → 交换' % (S.i, S.j)) if S.i <= S.j else '`i > j`：已经交错，不交换',
        20: '交换后两边各收缩一步：`i` → {i}',
        21: '`j` → {j}',
        'nums[i], nums[j] =': '交换 `{nums[j]}` 和 `{nums[i]}`：小的去左边，大的去右边',
        'if j - left + 1 >= k': '左半部分 `[left, j]` 有 `{j - left + 1}` 个数；目标是第 `{k}` 个 → ' + '{"答案在左半部分" if j - left + 1 >= k else "不在左半部分"}',
        'return self.search(nums, left, j, k)': '只在左半部分 `[{left}, {j}]` 里找第 `{k}` 个',
        'elif i - left >= k': lambda S, B, r: ('`i − left = %d ≥ k = %d`：第 `k` 个落在 `j` 和 `i` 之间的已就位区，答案就是它' % (S.i - S.left, S.k)) if S.i - S.left >= S.k else '`i − left = %d < k = %d`：答案在右半部分' % (S.i - S.left, S.k),
        'return nums[left + k - 1]': '位置 `left + k − 1 = {left + k - 1}` 就是答案 `{nums[left + k - 1]}`',
        'return self.search(nums, i, right': '答案在右半部分：去 `[{i}, {right}]` 找第 `{k - (i - left)}` 个（左边 `{i - left}` 个已排除）',
    },
    cards=dict(
        one_liner='快速选择：只在包含目标的那一半里继续划分',
        complexity='平均时间 `O(n)`，空间 `O(log n)`（递归栈）',
        problem=['`nums` 是字符串数组，每个字符串是不含前导零的整数，求第 `k` 大的那个字符串',
                 '重复数字算不同元素；字符串很长，不能直接转成 int 比较',
                 '本视频：`nums = ["3","10","7","2","6"]`，`k = 2` → `"7"`'],
        quote='找第K大数的字符串大整数版本，同样适用快速选择算法，只需要在判断大小时改为字符串数字的判断方式就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `k` 大 = 从小到大第 `n − k + 1` 个，用快速选择划分',
              '大小比较：==位数多的更大，位数相同再按字符串字典序==',
              '划分后只递归含目标的一侧，其余丢掉'],
        summary=['平均时间 `O(n)`，最坏 `O(n²)`；空间 `O(log n)`',
                 '易错点：比较字符串大整数要先比长度，再比字典序（`"10" < "7"` 在字典序上成立，但数值上 10 更大）',
                 '易错点：第 `k` 大要转成第 `n − k + 1` 小',
                 '原文为 Python 2 写法，`(left + right) / 2` 已改为 `//`'],
    ),
)
