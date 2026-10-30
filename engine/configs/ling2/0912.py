NUMS = [2, 5, 1, 4, 3]


def _while_i(S, B, ret):
    i, j = B.i, B.j
    if i <= j and B.nums[i] < B.pivot:
        return f'`nums[{i}] = {B.nums[i]} < pivot = {B.pivot}`：属于左边，`i` 右移'
    if i > j:
        return '`i > j`：左右指针已经交错，`i` 停下'
    return f'`nums[{i}] = {B.nums[i]} ≥ pivot`：`i` 停下（它该去右边）'


def _while_j(S, B, ret):
    i, j = B.i, B.j
    if i <= j and B.nums[j] > B.pivot:
        return f'`nums[{j}] = {B.nums[j]} > pivot = {B.pivot}`：属于右边，`j` 左移'
    if i > j:
        return '`i > j`：左右指针已经交错，`j` 停下'
    return f'`nums[{j}] = {B.nums[j]} ≤ pivot`：`j` 停下（它该去左边）'


def _in_part(S):
    return S.get('_line', 0) < 61 and 'pivot' in S


def _color(S, k, v):
    if 'left' not in S:
        return None
    if _in_part(S) and S['left'] <= k <= S['right']:
        if k == S['left'] and S.get('_line', 0) < 51:
            return 'purple'
        if S.get('_line') in (51, 59) and k == S['j']:
            return 'purple'
    ln = S.get('_line', 0)
    if ln in (67, 68, 69, 70) and 'i' in S and k in (S['i'], S['i'] + 1):
        return 'orange'
    return None


def _dim(S, k, v):
    return 'left' in S and not (S['left'] <= k <= S['right'])


def _formula(S):
    ln = S.get('_line', 0)
    if _in_part(S):
        return f"划分 `[{S['left']}, {S['right']}]`，pivot = =={S['pivot']}==（紫）"
    if ln in (66, 67, 68, 69, 70, 71, 72) and 'left' in S:
        return f"`quick_sort({S['left']}, {S['right']})`：先检查是否==已升序=="
    return ''


def _cap_for(S, B, ret):
    if S.get('i') is None or S.get('i') == B.get('i') and B.get('_line') == 67:
        return '没有逆序对'
    return f'比较相邻的 `nums[{S.i}]` 和 `nums[{S.i + 1}]`'


CONFIG = dict(
    num=912, title='排序数组', difficulty='Medium', category='普通数组',
    author='灵茶山艾府', technique='快速排序 · 随机 pivot + 相向双指针 + 有序优化',
    tags=['字节30天'],
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

    def sortArray(self, nums: List[int]) -> List[int]:
        # 快速排序子数组 [left, right]
        def quick_sort(left: int, right: int) -> None:
            # 优化：如果子数组已是升序，直接返回
            # 也可以写 if all(nums[i] <= nums[i + 1] for i in range(left, right)): return
            ordered = True
            for i in range(left, right):
                if nums[i] > nums[i + 1]:
                    ordered = False
                    break
            if ordered:
                return

            i = self.partition(nums, left, right)  # 划分子数组
            quick_sort(left, i - 1)   # 排序在 pivot 左侧的元素
            quick_sort(i + 1, right)  # 排序在 pivot 右侧的元素

        quick_sort(0, len(nums) - 1)
        return nums
''',
    setup='import random\nrandom.seed(5)\nfrom random import randint',
    call=f'Solution().sortArray({NUMS})',
    expect=[1, 2, 3, 4, 5],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='nums', cell=110, h=260,
             pointers={'i': 'blue', 'j': 'pink'},
             window=('left', 'right'), color=_color, dim=_dim),
        dict(type='calls', h=170),
    ],
    watch=[('left', 'left', 'cyan'), ('right', 'right', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'pink'),
           ('pivot', 'pivot', 'purple')],
    captions={
        'quick_sort(0, len(nums) - 1)': '递归入口：排序整个数组 `[0, {len(nums) - 1}]`',
        'ordered = True': '先假设 `[{left}, {right}]` 已经升序',
        'for i in range(left, right)': _cap_for,
        'if nums[i] > nums[i + 1]': lambda S, B, ret: (f'`{S.nums[S.i]} > {S.nums[S.i + 1]}`：逆序 → 不是升序' if S.nums[S.i] > S.nums[S.i + 1]
                                                        else f'`{S.nums[S.i]} ≤ {S.nums[S.i + 1]}`，继续检查'),
        'ordered = False': '发现逆序对，需要排序',
        70: '`break`：不用再检查了',
        'if ordered': lambda S, B, ret: (f'`[{S.left}, {S.right}]` ==已经升序==（或只有 ≤ 1 个元素）→ 直接返回' if S.ordered
                                         else '不是升序 → 划分 + 递归'),
        72: '返回上一层',
        'i = self.partition': '调用 `partition` 划分 `[{left}, {right}]`，返回 pivot 的最终下标',
        'quick_sort(left, i - 1)': '递归排序 pivot ==左侧== `[{left}, {i - 1}]`',
        'quick_sort(i + 1, right)': '递归排序 pivot ==右侧== `[{i + 1}, {right}]`',
        'return nums': '排序完成：`{ret}`',
        'i = randint(left, right)': '随机选下标 `i = {i}` 作为基准（视频固定了随机种子，可复现）',
        'pivot = nums[i]': '`pivot = nums[{i}] = {pivot}`',
        'nums[i], nums[left] = nums[left], nums[i]': '把 pivot 换到子数组最左边 `nums[{left}]`，==不干扰后续划分==',
        'i, j = left + 1, right': '相向双指针：`i = {i}` 从左往右，`j = {j}` 从右往左',
        'while i <= j and nums[i] < pivot': _while_i,
        'while i <= j and nums[j] > pivot': _while_j,
        'if i >= j': lambda S, B, ret: (f'`i = {S.i} ≥ j = {S.j}`：所有元素都看过了，退出' if S.i >= S.j
                                        else f'`i = {S.i} < j = {S.j}`：`nums[i] ≥ pivot` 且 `nums[j] ≤ pivot`，交换'),
        'break': '跳出循环：`j` 指向最后一个 `≤ pivot` 的位置',
        'nums[i], nums[j] = nums[j], nums[i]': '交换 `nums[{i}]` 和 `nums[{j}]`：==维持循环不变量==',
        38: '交换后 `nums[{B.i}]` 已经 `≤ pivot`，`i` → {i}',
        39: '交换后 `nums[{B.j}]` 已经 `≥ pivot`，`j` → {j}',
        'nums[left], nums[j] = nums[j], nums[left]': 'pivot 与 `nums[{j}]` 交换：左边都 `≤ {pivot}`，右边都 `≥ {pivot}`',
        'return j': 'pivot 的最终下标 `{j}`，就是它在排序后数组中的位置',
    },
    skip=['while True', '                i += 1', '                j -= 1'],
    max_steps=70,
    cards=dict(
        one_liner='随机选 pivot 划分成「≤ pivot | pivot | ≥ pivot」，左右两边递归；已升序就直接返回',
        complexity='期望时间 `O(n log n)`，期望空间 `O(log n)`',
        problem=['给定整数数组 `nums`，将其==升序==排列',
                 '要求不使用内置排序，时间 `O(n log n)`、空间尽量小',
                 '示例：`[5,2,3,1]` → `[1,2,3,5]`',
                 f'本视频：`{NUMS}` → `[1,2,3,4,5]`'],
        quote='定义一个递归函数 sort(left, right)，表示把子数组 [left, right] 升序排序。划分子数组 [left, right]……在 pivot 左侧的元素，继续递归排序；在 pivot 右侧的元素，继续递归排序。一个简单有效的优化：如果子数组已是升序，直接返回。',
        quote_src='—— 灵茶山艾府题解',
        idea=['划分同 215 题：随机 pivot 换到最左，相向双指针把 `< pivot` 留左、`> pivot` 留右',
              '最后 pivot 与 `nums[j]` 交换，pivot 就落在了它排序后的位置',
              '递归边界：子数组已升序（包括空 / 只剩一个元素）直接返回'],
        summary=['期望 `O(n log n)`：递归深度期望 `O(log n)`，每层 `O(n)`',
                 '不随机选 pivot：遇到降序数组会退化成 `O(n²)`',
                 '`nums[i] < pivot` 不能改成 `<=`：全相同时划分最不均匀，退化成 `O(n²)`',
                 '`i <= j` 不能改成 `i < j`：例如 `[2,1,3]` 会划分失败',
                 '视频固定了随机种子以便复现；题解还提到小数组切插入排序等优化'],
    ),
)
