def _while_i(S, B, ret):
    i, j = B.i, B.j
    if i <= j and B.nums[i] < B.pivot:
        return f'`nums[{i}] = {B.nums[i]} < pivot = {B.pivot}`：属于左边，`i` 继续右移'
    if i > j:
        return f'`i > j`：左右指针已经交错，`i` 停下'
    return f'`nums[{i}] = {B.nums[i]} ≥ pivot`：`i` 停下（它该去右边）'


def _while_j(S, B, ret):
    i, j = B.i, B.j
    if i <= j and B.nums[j] > B.pivot:
        return f'`nums[{j}] = {B.nums[j]} > pivot = {B.pivot}`：属于右边，`j` 继续左移'
    if i > j:
        return f'`i > j`：左右指针已经交错，`j` 停下'
    return f'`nums[{j}] = {B.nums[j]} ≤ pivot`：`j` 停下（它该去左边）'


CONFIG = dict(
    num=215, title='数组中的第K个最大元素', difficulty='Medium', category='堆',
    author='灵茶山艾府', technique='快速选择（随机 pivot + 相向双指针划分）',
    code='''
class Solution:
    def partition(self, nums: List[int], left: int, right: int) -> int:
        """
        在子数组 [left, right] 中随机选择一个基准元素 pivot
        根据 pivot 重新排列子数组 [left, right]
        重新排列后，<= pivot 的元素都在 pivot 的左侧，>= pivot 的元素都在 pivot 的右侧
        返回 pivot 在重新排列后的 nums 中的下标
        特别地，如果子数组的所有元素都等于 pivot，我们会返回子数组的中心下标，避免退化
        """

        # 1. 在子数组 [left, right] 中随机选择一个基准元素 pivot
        i = randint(left, right)
        pivot = nums[i]
        # 把 pivot 与子数组第一个元素交换，避免 pivot 干扰后续划分，从而简化实现逻辑
        nums[i], nums[left] = nums[left], nums[i]

        # 2. 相向双指针遍历子数组 [left + 1, right]
        # 循环不变量：在循环过程中，子数组的数据分布始终如下图
        # [ pivot | <=pivot | 尚未遍历 | >=pivot ]
        #   ^                 ^     ^         ^
        #   left              i     j         right

        i, j = left + 1, right
        while True:
            while i <= j and nums[i] < pivot:
                i += 1
            # 此时 nums[i] >= pivot

            while i <= j and nums[j] > pivot:
                j -= 1
            # 此时 nums[j] <= pivot

            if i >= j:
                break

            # 维持循环不变量
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1

        # 循环结束后
        # [ pivot | <=pivot | >=pivot ]
        #   ^             ^   ^     ^
        #   left          j   i     right

        # 3. 把 pivot 与 nums[j] 交换，完成划分（partition）
        # 为什么与 j 交换？
        # 如果与 i 交换，可能会出现 i = right + 1 的情况，已经下标越界了，无法交换
        # 另一个原因是如果 nums[i] > pivot，交换会导致一个大于 pivot 的数出现在子数组最左边，不是有效划分
        # 与 j 交换，即使 j = left，交换也不会出错
        nums[left], nums[j] = nums[j], nums[left]

        # 交换后
        # [ <=pivot | pivot | >=pivot ]
        #               ^
        #               j

        # 返回 pivot 的下标
        return j

    def findKthLargest(self, nums: list[int], k: int) -> int:
        n = len(nums)
        target_index = n - k  # 第 k 大元素在升序数组中的下标是 n - k
        left, right = 0, n - 1  # 闭区间
        while True:
            i = self.partition(nums, left, right)
            if i == target_index:
                # 找到第 k 大元素
                return nums[i]
            if i > target_index:
                # 第 k 大元素在 [left, i - 1] 中
                right = i - 1
            else:
                # 第 k 大元素在 [i + 1, right] 中
                left = i + 1
''',
    setup='import random\nrandom.seed(6)\nfrom random import randint',
    call='Solution().findKthLargest([3, 2, 1, 5, 6, 4], 2)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"pivot = =={S['pivot']}==（紫色）　　目标下标 `n − k = {S['target_index']}`"
                                        if 'pivot' in S and 'target_index' in S else
                                        f"目标下标 `n − k = {S['target_index']}`" if 'target_index' in S else ''), size=28),
        dict(type='array', var='nums', cell=96, h=260,
             pointers={'i': 'blue', 'j': 'pink', 'target_index': 'orange'},
             pointer_labels={'target_index': 'n-k'},
             window=('left', 'right'),
             color=lambda S, i, v: ('purple' if 'pivot' in S and S['left'] <= i <= S['right'] and v == S['pivot']
                                    else None),
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='calls', h=150),
    ],
    watch=[('left', 'left', 'cyan'), ('right', 'right', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'pink'),
           ('pivot', 'pivot', 'purple')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'target_index = n - k': '第 k 大元素在升序数组中的下标是 `n - k = {target_index}`：==找第 k 大 = 找升序下标 n−k==',
        'left, right = 0, n - 1': '在闭区间 `[{left}, {right}]` 里找',
        'i = self.partition': '划分子数组 `[{B.left}, {B.right}]`，看 pivot 最终落在哪个下标',
        'i = randint(left, right)': '随机选下标 `i = {i}` 作为基准（视频里固定了随机种子，可复现）',
        'pivot = nums[i]': '`pivot = nums[{i}] = {pivot}`',
        'nums[i], nums[left] = nums[left], nums[i]': '把 pivot 换到子数组最左边 `nums[{left}]`，==不干扰后面的划分==',
        'i, j = left + 1, right': '相向双指针：`i = {i}` 从左往右，`j = {j}` 从右往左',
        'while i <= j and nums[i] < pivot': _while_i,
        38: '交换后 `nums[{B.i}]` 已经 `≤ pivot`，`i` → {i}',
        39: '交换后 `nums[{B.j}]` 已经 `≥ pivot`，`j` → {j}',
        'break': '跳出循环，此时 `j` 指向最后一个 `≤ pivot` 的位置',
        'while i <= j and nums[j] > pivot': _while_j,
        'if i >= j': lambda S, B, ret: (f'`i = {S.i} ≥ j = {S.j}`：所有元素都看过了，退出' if S.i >= S.j
                                        else f'`i = {S.i} < j = {S.j}`：`nums[i] ≥ pivot` 且 `nums[j] ≤ pivot`，交换它们'),
        'nums[i], nums[j] = nums[j], nums[i]': '交换 `nums[{i}]` 和 `nums[{j}]`：==维持循环不变量==',
        'nums[left], nums[j] = nums[j], nums[left]': 'pivot 与 `nums[{j}]` 交换：`j` 左边都 `≤ {pivot}`，右边都 `≥ {pivot}`',
        'return j': 'pivot 的最终下标就是 `{j}`，等于它在升序数组中的位置',
        'if i == target_index': lambda S, B, ret: (f'`i == n - k == {S.i}`：==找到了==！' if S.i == S.target_index
                                                   else f'`i = {S.i}` ≠ `n - k = {S.target_index}`，还没找到'),
        'return nums[i]': '第 k 大元素就是 `nums[{i}] = {ret}`',
        'if i > target_index': lambda S, B, ret: (f'`{S.i} > {S.target_index}`：答案在 pivot ==左侧==' if S.i > S.target_index
                                                  else f'`{S.i} < {S.target_index}`：答案在 pivot ==右侧=='),
        'right = i - 1': '只在 `[{left}, {right}]` 里继续找，==另一半直接扔掉==',
        'left = i + 1': '只在 `[{left}, {right}]` 里继续找，==另一半直接扔掉==',
    },
    skip=['while True', '                i += 1', '                j -= 1'],
    max_steps=70,
    cards=dict(
        one_liner='第 k 大就是升序下标 n−k：每次划分只留答案所在的那一半',
        complexity='期望时间 `O(n)`，空间 `O(1)`',
        problem=['给定整数数组 `nums` 和整数 `k`，返回数组排序后第 `k` 个最大的元素',
                 '要求时间复杂度 `O(n)`',
                 '示例：`[3,2,1,5,6,4], k = 2` → ==5=='],
        quote='第 k 大元素在升序数组中的下标是 n−k……这类似二分查找，只要我们每次能把问题的规模缩小一半，就可以用 O(n) 时间解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['随机选 pivot，划分成 ==`≤ pivot` | pivot | `≥ pivot`==，pivot 落在它升序后的位置 `i`',
              '`i == n−k` 就是答案；`i > n−k` 去左边找，否则去右边找',
              '把 `<` 改成 `≤`（两边都可以放等于 pivot 的数），==大量重复元素时也不会退化=='],
        summary=['期望时间 `O(n + n/2 + n/4 + …) = O(n)`，最坏 `O(n²)`；随机 pivot 让最坏情况几乎不出现',
                 '`nums[i] < pivot` 不能改成 `<=`：全相同时会划分到最边上，退化成 `O(n²)`',
                 '`i <= j` 不能改成 `i < j`：例如 `[2,1,3]` 会划分失败',
                 '最后 pivot 要与 `nums[j]` 交换：与 `i` 交换可能越界',
                 '题解还给了库函数写法；视频固定了随机种子以便复现'],
    ),
)
