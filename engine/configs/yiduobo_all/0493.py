def _info(S):
    if 'mid' not in S['_inner']:
        return '把 `nums` 一分为二，先递归、再合并；==合并前先数翻转对=='
    I = S['_inner']
    return f"区间 `[{I['l']}, {I['r']}]`，`mid = {I['mid']}`：左半 `[{I['l']}, {I['mid']}]`、右半 `[{I['mid'] + 1}, {I['r']}]` 都已排好序，当前 `res = {I.get('res')}`"


CONFIG = dict(
    num=493, title='翻转对', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='归并排序 · 双指针数翻转对',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def reversePairs(self, nums):

        if not nums:
            return 0

        return self.mergeSort(nums, 0, len(nums) - 1)

    def mergeSort(self, nums, l, r):
        if l == r:
            return 0

        mid = (l + r) // 2
        res = self.mergeSort(nums, l, mid) + self.mergeSort(nums, mid + 1, r)

        i = l
        j = mid + 1
        while i <= mid or j <= r:
            if i <= mid:
                if j <= r and nums[i] > nums[j] * 2:
                    j += 1
                else:
                    i += 1
                    res += j - mid - 1
            else:
                j += 1
        
        i = l
        j = mid + 1
        tmp = []
        while i <= mid or j <= r:
            if i <= mid:
                if j > r or nums[i] <= nums[j]:
                    tmp.append(nums[i])
                    i += 1
                else:
                    tmp.append(nums[j])
                    j += 1
            else:
                tmp.append(nums[j])
                j += 1
                
        for index, num in enumerate(tmp):
            nums[index + l] = num

        return res
''',
    call='Solution().reversePairs([5, 2, 1])',
    expect=2,
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var=lambda S: S['_inner'].get('nums', S.get('nums')), label='nums（框 = 当前归并的区间；归并后区间内变为有序）', h=200,
             pointers={'i': 'blue', 'j': 'pink'}, window=('l', 'r')),
        dict(type='array', var='tmp', label='tmp（归并结果）', h=130),
        dict(type='calls', h=200, hide=('nums',)),
    ],
    watch=['l', 'r', 'mid', 'i', 'j', ('res', 'res', 'green')],
    skip=['if l == r', 'while i <= mid or j <= r', 'if i <= mid', 'for index, num', 'if not nums', 11, 5, 17, 28, 29, 44],
    max_steps=90,
    captions={
        'return self.mergeSort(nums, 0': '从整个数组 `[0, {len(nums) - 1}]` 开始分治',
        'mid = (l + r)': '`mid = ({l} + {r}) // 2 = {mid}`：左半 `[{l}, {mid}]`，右半 `[{mid + 1}, {r}]`（单个元素的区间翻转对为 0，直接返回）',
        'res = self.mergeSort': '左右两半递归完毕：各自的翻转对已算好，且都已排好序；`res` = =={res}==',
        16: '开始数跨越左右两半的翻转对：`i` 指左半，`j` 指右半',
        20: lambda S, B, r: (f'`nums[i] = {S.nums[S.i]}`、`nums[j] * 2 = {S.nums[S.j] * 2}`：' + ('==大于== → 构成翻转对' if S.nums[S.i] > S.nums[S.j] * 2 else '不大于 → `nums[i]` 在右半里找完了')) if S.j <= S.r else f'`j` 已越过右半末尾：`nums[i]` 的数完了',
        21: '`{B.nums[B.i]} > {B.nums[B.j]} * 2`：右半有序，更靠前的数更小，也都满足 → `j` 右移到 {j}，看还能多吃几个',
        23: '`nums[i]` 在右半里数完了 → `i` → {i}；下一个 `nums[i]` 更大，所以 `j` 不用回退',
        24: '`nums[i]` 和右半 `mid+1..j-1` 的 `{j - mid - 1}` 个数都构成翻转对 → `res` = =={res}==',
        26: '左半已经用完，`j` 继续右移到末尾（不再有新的翻转对）',
        30: '翻转对数完了，接着做普通二路归并：`tmp` 存归并结果，保持区间有序',
        33: lambda S, B, r: ('`j` 已越界或 `nums[i] <= nums[j]`：先放左边的 `nums[i]`' if (S.j > S.r or S.nums[S.i] <= S.nums[S.j]) else f'`nums[i] = {S.nums[S.i]} > nums[j] = {S.nums[S.j]}`：右边更小，先放右边的'),
        34: '把 `nums[{i}] = {nums[i]}` 放进 `tmp`',
        35: '`i` → {i}',
        37: '把 `nums[{j}] = {nums[j]}` 放进 `tmp`',
        38: '`j` → {j}',
        40: '左半用完，右半剩下的依次放进 `tmp`：`nums[{j}] = {nums[j]}`',
        41: '`j` → {j}',
        46: '`tmp` 写回 `nums[{l}..{r}]`，区间有序；其内共 `{res}` 个翻转对（含左右两半各自的）',
        7: '整个数组一共 `{ret}` 个翻转对',
    },
    cards=dict(
        one_liner='和逆序对一样用归并排序，合并前先双指针数翻转对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数对 `(i, j)` 满足 `i < j` 且 `nums[i] > 2 * nums[j]`，求个数',
                 '示例：`[1,3,2,3,1]` → `2`',
                 '本视频：`[5, 2, 1]` → `2`'],
        quote='题目描述与逆序对十分类似，差别之处在于……这里求的是 i < j 时，nums[i] > nums[j] * 2 的数量，因此具体的做法也可以照搬求逆序对的做法，使用归并排序来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['`[l, mid]` 和 `[mid+1, r]` 递归后各自有序',
              '`nums[i]` 大于 `nums[j]*2`，则它也大于更小的 `nums[mid+1..j]` 的两倍：一次性加上 `j - mid - 1`',
              '`i` 变大时满足条件的 `j` 只会更靠右，所以 `j` 不回退，一趟扫描搞定',
              '数完之后再做普通归并，把区间排好序'],
        summary=['时间 `O(n log n)`：每层两次线性扫描',
                 '翻转对条件是 `nums[i] > 2 * nums[j]`，数翻转对和归并是两个独立的 while，不能合并',
                 '数的时候两半都必须已经有序，所以先递归再数',
                 '原文为 Python 2 写法，`mid = (l + r) / 2` 已改为 `//`',
                 '`nums[j] * 2` 在 Python 中不会溢出，其他语言要用 long'],
    ),
)
