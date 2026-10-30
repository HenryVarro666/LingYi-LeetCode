CONFIG = dict(
    num=2426, title='满足不等式的数对数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='变形成 nums[i] <= nums[j] + diff + 归并排序计数',
    tags=['树状数组', '难度分 2030'],
    code='''
class Solution(object):
    def numberOfPairs(self, nums1, nums2, diff):

        n = len(nums1)
        nums = [nums1[index] - nums2[index] for index in range(n)]
        
        def merge(left, right):
            if left == right:
                return 0
            
            mid = (left + right) >> 1
            cnt = merge(left, mid) + merge(mid + 1, right)

            p1 = left
            p2 = p = mid + 1
            tmp = []
            while p1 <= mid or p2 <= right:
                if p2 == right + 1 or (p1 != mid + 1 and nums[p1] < nums[p2]):
                    while p <= right and nums[p] + diff < nums[p1]:
                        p += 1
                    cnt += right - p + 1
                    tmp.append(nums[p1])
                    p1 += 1
                else:
                    tmp.append(nums[p2])
                    p2 += 1
            
            for index in range(left, right + 1):
                nums[index] = tmp[index - left]

            return cnt

        return merge(0, n - 1)
''',
    call='Solution().numberOfPairs([3,2,5], [2,2,1], 1)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"本层区间 `[{S['left']}, {S['right']}]`，mid = {S['mid']}：左半 `[{S['left']}, {S['mid']}]` 与右半 `[{S['mid']+1}, {S['right']}]` 各自已有序" if 'mid' in S and 'left' in S else '【nums[i] = nums1[i] - nums2[i]，数 i<j 且 nums[i] <= nums[j] + diff】'), h=60),
        dict(type='array', var='nums', label='nums（框 = 归并区间；p = 右半第一个满足 nums[p]+diff >= nums[p1] 的位置）',
             pointers={'p1': 'blue', 'p2': 'pink', 'p': 'orange'}, window=('left', 'right'), h=190),
        dict(type='array', var='tmp', label='tmp：归并后的有序结果', h=130),
        dict(type='calls', h=180),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'cnt', 'p'],
    captions={
        'nums = [nums1': '`nums[i] = nums1[i] - nums2[i]` → {nums}，问题变成数 `i < j` 且 `nums[i] <= nums[j] + diff`',
        'if left == right': lambda S, B, r: (f'区间只剩一个数，没有数对 → 返回 0' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 还有多个数，继续二分'),
        'mid = (left': '`mid = {mid}`：数对只可能是 `i<j<=mid`、`mid<i<j`、跨 mid 三种',
        'cnt = merge': '先递归左右两半：各自数好、各自排好序，`cnt` 是两半内部的数对和',
        'p2 = p = mid + 1': '`p1` 从左半头开始，`p2`、`p` 从右半头开始',
        'while p1 <= mid or': '两半还没取完，继续归并',
        'if p2 == right + 1': lambda S, B, r: (f'右半取完或 `nums[{S.p1}]={S.nums[S.p1]}` 较小 → 取左边的 p1' if (S.p2 == S.right + 1 or (S.p1 != S.mid + 1 and S.nums[S.p1] < S.nums[S.p2])) else f'`nums[{S.p2}]` 不大于左边当前数 → 取右边的 p2'),
        'while p <= right and': '`p` 右移：跳过右半中 `nums[p] + diff < nums[p1]` 的数；左边变大，p 只会往右',
        'cnt += right - p + 1': '`p = {p}`：右半从 p 起共 `right-p+1 = {right - p + 1}` 个 j 满足 `nums[p1] <= nums[j]+diff` → `cnt` = =={cnt}==',
        'tmp.append(nums[p1])': '`nums[p1]` 进 tmp，`p1` 后移',
        'p1 += 1': '`p1` → {p1}',
        'tmp.append(nums[p2])': '`nums[p2]` 进 tmp，保持有序',
        'p2 += 1': '`p2` → {p2}',
        'return cnt': 'tmp 已写回 nums（两半合并成有序），本层数对共 `{cnt}` 个，返回上一层',
        'return merge(0': '从整个数组 `[0, {n - 1}]` 开始：先递归，再数跨 mid 的数对，再合并',
    },
    skip=['tmp = []', 'p1 = left', 'for index in range', 'nums[index] = tmp', 'return 0'],
    max_steps=130,
    cards=dict(
        one_liner='把式子并拢成 nums[i] <= nums[j]+diff，用归并排序顺手数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个数组 `nums1`、`nums2` 和整数 `diff`',
                 '数 `i < j` 且 `nums1[i]-nums1[j] <= nums2[i]-nums2[j]+diff` 的数对',
                 '示例：`[3,2,5]`、`[2,2,1]`、`diff=1` → `3`；本视频直接用示例 1'],
        quote='可以离散化后使用树状数组计数，也可以使用类似求逆序对的方法，在归并排序的过程中顺便求解。我在这里采用的是后面这种方法。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 i 和 j 并拢：`nums[i] = nums1[i] - nums2[i]`，条件变成 `nums[i] <= nums[j] + diff`',
              '区间 `[left, right]` 的数对分三类：全在左半、全在右半、跨 mid；前两类递归',
              '两半都有序后，左边 i 增大时右边合法的起点 `p` 只会右移，一趟双指针数完跨 mid 的数对'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '计数必须在两半各自排好序之后做，所以是「先递归，再数，再合并」',
                 '`p` 只增不减，跨 mid 部分是 `O(n)`；合法数对数 = `right - p + 1`',
                 '原文已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神用离散化树状数组，yiduobo 用归并排序'],
    ),
)
