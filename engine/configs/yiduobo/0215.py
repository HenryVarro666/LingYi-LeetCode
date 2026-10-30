def _wi(S, B, ret):
    i = B.i
    if i <= B.right and B.nums[i] < B.mid:
        return f'`nums[{i}] = {B.nums[i]} < mid = {B.mid}`：留在左边，`i += 1`'
    if i > B.right:
        return '`i` 已经越过 `right`，停下'
    return f'`nums[{i}] = {B.nums[i]} ≥ mid`：`i` 停下'


def _wj(S, B, ret):
    j = B.j
    if j >= B.left and B.nums[j] > B.mid:
        return f'`nums[{j}] = {B.nums[j]} > mid = {B.mid}`：留在右边，`j -= 1`'
    if j < B.left:
        return '`j` 已经越过 `left`，停下'
    return f'`nums[{j}] = {B.nums[j]} ≤ mid`：`j` 停下'


def _part(S):
    if 'j' not in S or 'mid' not in S or S['i'] <= S['j']:
        return ''
    l, i, j, k = S['left'], S['i'], S['j'], S['k']
    mid_part = f"中段 `[{j + 1}, {i - 1}]`（= mid），" if j + 1 <= i - 1 else '中段为空，'
    return (f"划分完：左段 `[{l}, {j}]` 有 =={j - l + 1}== 个（≤ mid），"
            f"{mid_part}右段 `[{i}, {S['right']}]`（≥ mid）；找第 `k = {k}` 小")


CONFIG = dict(
    num=215, title='数组中的第K个最大元素', difficulty='Medium', category='堆',
    author='yiduobo', technique='快速选择（取中 pivot，递归一侧）',
    code='''
class Solution(object):
    def findKthLargest(self, nums, k):
        return self.search(nums, 0, len(nums) - 1, len(nums) - k + 1)

    def search(self, nums, left, right, k):
        #print left, right, k
        if left == right:
            return nums[left]

        mid = nums[(left + right) // 2]
        i = left
        j = right
        while i <= j:
            while i <= right and nums[i] < mid:
                i += 1
            while j >= left and nums[j] > mid:
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
''',
    call='Solution().findKthLargest([3, 2, 3, 1, 2, 4], 5)',
    expect=2,
    skip=['j = right', 'i += 1', 'j -= 1'],
    views=[
        dict(type='text', fn=lambda S: (f"在 `[{S['left']}, {S['right']}]` 里找==第 {S['k']} 小==" +
                                        (f"　　mid = =={S['mid']}==（紫色）" if 'mid' in S else '')) if 'left' in S else
             '第 k 大 = 第 `n − k + 1` 小', size=28),
        dict(type='array', var='nums', cell=96, h=250,
             pointers={'i': 'blue', 'j': 'pink'}, window=('left', 'right'),
             color=lambda S, i, v: 'purple' if 'mid' in S and S['left'] <= i <= S['right'] and v == S['mid'] else None,
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=_part, size=24, lines=2, h=80),
        dict(type='calls', h=170),
    ],
    watch=[('left', 'left', 'cyan'), ('right', 'right', 'cyan'), ('k', 'k', 'orange'), ('i', 'i', 'blue'),
           ('j', 'j', 'pink'), ('mid', 'mid', 'purple')],
    captions={
        'return self.search(nums, 0': '第 `k` 大 = 第 `n − k + 1` 小：调用 `search(nums, 0, {B.nums.__len__() - 1}, {k})`',
        'if left == right': lambda S, B, ret: (f'`left == right == {S.left}`：只剩一个数，它就是答案' if S.left == S.right
                                               else f'区间 `[{S.left}, {S.right}]` 不止一个数，继续划分'),
        'mid = nums[(left + right) // 2]': '“取中快排”：分割点取中间位置的数 `mid = nums[{(left + right) // 2}] = {mid}`',
        'i = left': '`i = left` 从左往右，`j = right` 从右往左',
        'while i <= j': lambda S, B, ret: (f'`i = {B.i} ≤ j = {B.j}`：继续划分' if B.i <= B.j
                                           else f'`i = {B.i} > j = {B.j}`：划分结束'),
        'while i <= right and nums[i] < mid': _wi,
        'while j >= left and nums[j] > mid': _wj,
        'if i <= j': lambda S, B, ret: (f'`i = {S.i} ≤ j = {S.j}`：交换 `nums[{S.i}]` 和 `nums[{S.j}]`' if S.i < S.j
                                        else f'`i == j == {S.i}`：`nums[{S.i}]` 就等于 mid，自己和自己交换，然后 `i`、`j` 交错'
                                        if S.i == S.j else '`i > j`：不交换'),
        'nums[i], nums[j] = nums[j], nums[i]': lambda S, B, ret: ('自己和自己交换，数组不变；接着 `i += 1`、`j -= 1`，两指针交错' if S.i == S.j else f'交换后 `nums[{S.i}] = {S.nums[S.i]}`、`nums[{S.j}] = {S.nums[S.j]}`；然后 `i += 1`、`j -= 1` 各向内走一格'),
        'if j - left + 1 >= k': lambda S, B, ret: (f'左段有 `{S.j - S.left + 1}` 个 ≥ `k = {S.k}`：答案在左段 → 递归左段'
                                                   if S.j - S.left + 1 >= S.k
                                                   else f'左段只有 `{S.j - S.left + 1}` 个 < `k = {S.k}`：答案不在左段'),
        'elif i - left >= k': lambda S, B, ret: (f'左段 + 中段共 `{S.i - S.left}` 个 ≥ `k`：==第 k 小就等于 mid==（等于分割点的特判）'
                                                 if S.i - S.left >= S.k
                                                 else f'左段 + 中段共 `{S.i - S.left}` 个 < `k = {S.k}`：答案在右段'),
        'return nums[left + k - 1]': '返回 `nums[{left} + {k} - 1] = {ret}`',
        'return self.search(nums, left, j, k)': '递归左段 `[{B.left}, {B.j}]`，仍找第 `{B.k}` 小',
        'return self.search(nums, i, right': '递归右段 `[{B.i}, {B.right}]`，减去左边 `{B.i - B.left}` 个 → 找第 `{B.k - (B.i - B.left)}` 小',
    },
    max_steps=70,
    cards=dict(
        one_liner='快排分成两部分后，第 k 大只会在其中一部分，只递归那一边',
        complexity='平均时间 `O(n)`，最坏 `O(n²)`；递归栈平均 `O(log n)`',
        problem=['给定整数数组 `nums` 和整数 `k`，返回数组排序后第 `k` 个最大的元素',
                 '要求时间复杂度 `O(n)`',
                 '本视频示例：`[3,2,3,1,2,4], k = 5` → ==2==（有重复元素）'],
        quote='考虑最常见的快速排序，选择分割点后，将数组分成两个部分然后递归继续排序。很明显，我们要找的第k大的数只会属于其中某一个部分，那么每次只需要递归计算其中一个部分就行了。',
        quote_src='—— yiduobo 题解',
        idea=['先把“第 k 大”转成“第 `n − k + 1` 小”，`search(nums, left, right, k)` 找区间里第 k 小',
              '分割点 `x` 取中间位置的数，划分后看==左段长度 `j − left + 1`== 和 `k` 的关系决定去哪边',
              '等于 `x` 的数可能落在 `j` 和 `i` 之间，所以要==特判第 k 小就是 x== 的情况'],
        summary=['平均 `O(n)`；作者自己也说取中快排“并不是最稳妥的做法”，特殊数据会退化',
                 '划分结束时 `j < i`：`[left, j]` ≤ x，`(j, i)` = x，`[i, right]` ≥ x',
                 '去右段时 `k` 要减去左边的 `i − left` 个数',
                 '原文为 Python 2 写法：`(left + right) / 2` 已改为 `//`，并删去了 `"""type"""` 文档字符串'],
    ),
)
