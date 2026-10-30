CODE = '''
class Solution(object):
    def kthSmallestProduct(self, nums1, nums2, k):

        if len(nums1) > len(nums2):
            ma = nums1
            mi = nums2
        else:
            ma = nums2
            mi = nums1

        def cnt(x, multi, nums):
            if multi < 0:
                if x >= multi * nums[0]:
                    return len(nums)
                else:
                    l = 0
                    r = len(nums) - 1
                    while l < r:
                        mid = (l + r + 1) >> 1
                        if x < multi * nums[mid]:
                            l = mid
                        else:
                            r = mid - 1
                    return len(nums) - (l + 1)
            
            elif multi > 0:
                if x >= multi * nums[-1]:
                    return len(nums)
                else:
                    l = 0
                    r = len(nums) - 1
                    while l < r:
                        mid = (l + r) >> 1
                        if x >= multi * nums[mid]:
                            l = mid + 1
                        else:
                            r = mid
                    return l

            else:
                if x >= 0:
                    return len(nums)
                else:
                    return 0

        l = -(10**10)
        r = 10**10

        while l < r:
            mid = (l + r) >> 1
            now = 0
            for num in mi:
                now += cnt(mid, num, ma)

            if now < k:
                l = mid + 1
            else:
                r = mid
        
        return l
'''


def _mat(S):
    ma, mi = S.get('ma'), S.get('mi')
    if not ma or not mi:
        return [[]]
    return [[x * y for y in ma] for x in mi]


def _info(S):
    L = S.get('_line', 0)
    if 'now' not in S:
        return '矩阵每行（固定一个 nums1 值）是单调的：对每一行二分，数出 ≤ mid 的个数'
    t = f"外层二分 `l = {S['l']}`..`r = {S['r']}`；这一轮猜 `mid = {S['mid']}`"
    if L >= 11 and L <= 44 and 'x' in S:
        t = f"当前行：`multi = {S['multi']}`，数 `multi × nums[j] ≤ x = {S['x']}` 的个数"
    return t + f"，累计 `now = {S['now']}`，`k = {S['k']}`"


def _row_mark(S, i, j, v):
    x = S.get('x')
    if x is None or S['mi'][i] != S.get('multi'):
        return None
    return 'green' if v <= x else None


CONFIG = dict(
    num=2040, title='两个有序数组的第 K 小乘积', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 + 逐行二分计数',
    tags=['难度分 2518'],
    code=CODE,
    call='Solution().kthSmallestProduct([0, 4], [-2, -1, 3], 3)',
    expect=0,
    views=[
        dict(type='grid', var=_mat, rows='mi', cols='ma', h=300, cell=120, label='乘积矩阵：行 = mi 的每个值，列 = ma（绿 = 当前行里 ≤ x 的数）',
             color=_row_mark),
        dict(type='text', fn=_info, size=26, h=100),
    ],
    watch=['l', 'r', 'mid', 'now', 'k', 'x', 'multi'],
    skip=['if multi < 0', 'elif multi > 0', 'while l < r:', 'for num in mi', 'l = 0', 'r = len(nums) - 1', 'now = 0', 'ma = nums', 'mi = nums', 'l = -(10**10)'],
    captions={
        'if len(nums1) > len(nums2)': lambda S, B, r: ('`nums1` 更长 → 把长的当 `ma`，短的当 `mi`' if len(S.nums1) > len(S.nums2)
                                                       else '`nums2` 不比 `nums1` 短 → 长的 `nums2` 当 `ma`，短的 `nums1` 当 `mi`'),
        'r = 10**10': '答案一定在 `[-10^10, 10^10]` 里（乘积最大 10^5 × 10^5）',
        50: '外层二分：猜第 k 小乘积 `mid = {mid}`',
        'now += cnt(mid, num, ma)': '`mi` 里取 `{num}`，让 `cnt` 数这一行 ≤ {mid} 的个数；累计 `now` = =={now}==',
        'if now < k': lambda S, B, r: (f'`now = {S.now} < k = {S.k}`：≤ {S.mid} 的不够 k 个 → 答案更大 → ==`l = mid + 1`==' if S.now < S.k
                                       else f'`now = {S.now} ≥ k = {S.k}`：够了 → 答案 ≤ {S.mid} → ==`r = mid`=='),
        56: '`l` → {l}',
        60: '`l = r` 时二分结束，第 {k} 小的乘积就是 `{ret}`',
        13: '`multi < 0`（负数）：乘积随 j 增大而变小；若 `x ≥ multi × nums[0]`（最大的那个）→ 整行都 ≤ x',
        27: '`multi > 0`：乘积随 j 增大而变大；若 `x ≥ multi × nums[-1]`（最大的那个）→ 整行都 ≤ x',
        41: '`multi = 0`：整行全是 0，`x ≥ 0` 就整行都算，否则一个都没有',
        14: '整行 `{len(nums)}` 个都 ≤ x，返回 {len(nums)}',
        28: '整行 `{len(nums)}` 个都 ≤ x，返回 {len(nums)}',
        42: '整行 {len(nums)} 个全是 0 ≤ x，返回 {len(nums)}',
        44: 'x < 0：一个都不算，返回 0',
        19: '负数行，找最后一个 `multi × nums[mid] > x` 的位置：`mid = (l+r+1) >> 1`（向上取整防死循环）= {mid}',
        20: lambda S, B, r: (f'`{S.x} < {S.multi} × {S.nums[S.mid]} = {S.multi * S.nums[S.mid]}`：乘积 > x → ==`l = mid`==（这个也太大了）' if S.x < S.multi * S.nums[S.mid]
                             else f'`{S.x} ≥ {S.multi} × {S.nums[S.mid]} = {S.multi * S.nums[S.mid]}`：乘积 ≤ x → ==`r = mid - 1`=='),
        24: '`len(nums) - (l + 1)`：下标 > l 的都 ≤ x → 共 =={ret}== 个',
        33: '正数行，找第一个乘积 > x 的位置：`mid = (l+r) >> 1` = {mid}',
        34: lambda S, B, r: (f'`{S.x} ≥ {S.multi} × {S.nums[S.mid]} = {S.multi * S.nums[S.mid]}`：这个 ≤ x → ==`l = mid + 1`==' if S.x >= S.multi * S.nums[S.mid]
                             else f'`{S.x} < {S.multi} × {S.nums[S.mid]} = {S.multi * S.nums[S.mid]}`：乘积 > x → ==`r = mid`=='),
        38: '`l` 就是第一个乘积 > x 的下标 → 前面 =={ret}== 个都 ≤ x',
    },
    max_steps=52,
    cards=dict(
        one_liner='二分猜乘积 mid，每一行再二分数出有几个 ≤ mid',
        complexity='时间 `O(min(n,m)·log max(n,m)·log C)`，空间 `O(1)`',
        problem=['两个升序数组，所有 `nums1[i] × nums2[j]` 里求第 `k` 小',
                 '示例：`[2,5],[3,4],k=2` → `8`',
                 '本视频：`nums1=[0,4], nums2=[-2,-1,3], k=3` → `0`'],
        quote='虽然题目给出的矩阵只是局部单调的，但是对于矩阵中的每一行或者每一列，都是由单调性质的。',
        quote_src='—— yiduobo 题解原文',
        idea=['整体不单调，但==每一行==单调：负数递减、0 全为 0、正数递增',
              '外层二分答案 `mid`，枚举短数组的每个值，在长数组里二分数出 ≤ mid 的个数',
              '负数行和正数行二分的写法不同：取中点、收边界要小心死循环'],
        summary=['枚举较短的数组，在较长的里二分，省时间',
                 '负数行用 `(l + r + 1) >> 1`，正数行用 `(l + r) >> 1`，避免死循环',
                 '乘积范围固定 `[-10^10, 10^10]`，外层约二分 35 次（视频中间部分快进）',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神按正负分四块用双指针计数；yiduobo 逐行二分，更直观'],
    ),
)
