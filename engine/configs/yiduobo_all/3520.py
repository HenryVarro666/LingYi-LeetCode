def _in(S):
    I = S.get('_inner') or {}
    return I if 'threshold' in I else None


def _top(S):
    I = _in(S)
    if I is None:
        if 'right' in S and 'left' in S and 'ma' in S:
            return f"二分阈值：区间 [`{S['left']}`, `{S['right']}`]（`{S['ma'] + 1}` 表示无解），要至少 `{'k'}` 对".replace("`k`", "k") if False else f"二分阈值区间 [`{S['left']}`, `{S['right']}`]，`{S['ma'] + 1}` = 无解标记"
        return ''
    return f"检测阈值 `threshold = {I['threshold']}`：逆序对要求 `0 < nums[i] - nums[j] <= {I['threshold']}`，目标 `k = {S['k']}`"


def _win(name):
    return f"{name} if 'threshold' in _inner else None"


def _cap_mid(S, B, ret):
    return f'`mid = ({S.left} + {S.right}) // 2 = =={S.mid}==`：试一试阈值 `{S.mid}` 够不够 k 对'


CONFIG = dict(
    num=3520, title='逆序对计数的最小阈值', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 归并排序数逆序对',
    tags=[],
    code='''
class Solution(object):
    def minThreshold(self, nums, k):
        
        ma = max(nums) - min(nums)
        left = 1
        right = ma + 1

        def calc(arr, left, right, threshold):
            if left == right:
                return 0

            tot = 0
            mid = (left + right) // 2
            tot += calc(arr, left, mid, threshold)
            if tot >= k:
                return tot
            tot += calc(arr, mid + 1, right, threshold)
            if tot >= k:
                return tot

            i = left
            j = mid + 1
            p = 0
            tmp = []
            while i <= mid or j <= right:
                if i == mid + 1 or (j <= right and arr[i] > arr[j]):
                    if p < i:
                        p = i
                    while p <= mid and arr[p] - arr[j] <= threshold:
                        p += 1

                    tot += p - i
                    if tot >= k:
                        return tot
                    tmp.append(arr[j])
                    j += 1
                else:
                    tmp.append(arr[i])
                    i += 1

            for index, v in enumerate(tmp):
                arr[index + left] = v

            return tot

        while left < right:
            mid = (left + right) // 2
            arr = nums[:]
            if calc(arr, 0, len(nums) - 1, mid) >= k:
                right = mid
            else:
                left = mid + 1
        
        if left == ma + 1:
            return -1
        return left
''',
    call='Solution().minThreshold([4, 2, 5, 1], 3)',
    expect=3,
    max_steps=66,
    skip=['arr[index + left] = v', 'tot = 0', 'j = mid + 1'],
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var=lambda S: (S['_inner'].get('arr') if 'arr' in S['_inner'] else S.get('nums')),
             label='arr（归并中，蓝框 = 当前处理的 left..right）', cell=96, h=260,
             pointers={'i': 'blue', 'j': 'pink', 'p': 'yellow'},
             window=(_win('left'), _win('right'))),
        dict(type='array', var='tmp', label='tmp（合并结果，左到右依次放入）', cell=96, h=130),
        dict(type='calls', h=190, hide=('arr', 'nums')),
    ],
    watch=[('threshold', lambda S: S['_inner'].get('threshold'), 'orange'),
           ('tot', lambda S: S['_inner'].get('tot'), 'green'), ('k', 'k', 'pink')],
    captions={
        'ma = max': '阈值最大不超过 `max - min = {ma}`',
        'left = 1': '阈值至少为 `1`（要求 `nums[i] - nums[j] > 0`）',
        'right = ma + 1': '`right = ma + 1 = {right}`：多留一格表示==无解==，二分结束停在它就返回 -1',
        'while left < right': lambda S, B, r: (f'二分区间 [`{S.left}`, `{S.right}`] 还没收缩到一个数 → 继续试' if S.left < S.right else f'`left = right = {S.left}`：二分结束'),
        47: _cap_mid,
        13: '从中间切开：左半 [{left}, {mid}]，右半 [{mid + 1}, {right}]',
        'arr = nums[:]': '阈值越大，满足条件的逆序对越多（==单调==）→ 可二分；每轮复制一份 nums 来排序',
        'if calc(arr, 0': lambda S, B, r: (f'`calc` 返回 `{r}`' if r is not None else '数一数阈值 `mid` 下的逆序对是否 `>= k`'),
        'right = mid': '对数 ≥ k：阈值 `mid` 够用，答案 ≤ mid → `right = {right}`',
        'left = mid + 1': '对数 < k：阈值 `mid` 不够，答案 > mid → `left = {left}`',
        'if left == ma + 1': lambda S, B, r: (f'`left = {S.left} == ma + 1`：连最大阈值都凑不够 k 对 → 无解' if S.left == S.ma + 1 else f'`left = {S.left} != ma + 1 = {S.ma + 1}`：有解，答案就是 left'),
        'return left': '最小阈值 `{left}`',
        'return -1': '无解返回 `-1`',
        'if left == right': lambda S, B, r: (f'`left = right = {S.left}`：只有一个元素，没有逆序对，返回 0' if S.left == S.right else f'区间 [`{S.left}`, `{S.right}`] 有多个元素 → 继续拆分'),
        'return 0': '单个元素：逆序对 `0`，也不需要排序',
        'tot += calc(arr, left, mid': '先递归左半 [{left}, {mid}]：排好序并数出左半内部的逆序对 → `tot = {tot}`',
        'tot += calc(arr, mid + 1': '再递归右半 [{mid + 1}, {right}] → `tot = {tot}`',
        'if tot >= k': lambda S, B, r: (f'`tot = {S.tot} >= k = {S.k}`：已经够 k 对，==剪枝提前返回==' if S.tot >= S.k else f'`tot = {S.tot} < k = {S.k}`：还不够，继续'),
        'return tot': '返回 `tot = {tot}`',
        'i = left': '`i` 扫左半、`j = mid + 1` 扫右半（两半都已排序）',
        'tmp = []': '`tmp` 存合并后的有序结果',
        'p = 0': '`p`：左半里第一个 `arr[p] - arr[j] > threshold` 的位置（只会往右走）',
        'while i <= mid or j <= right': '两半还没合并完 → 继续二路归并',
        'if i == mid + 1 or (j <= right and arr[i] > arr[j])': lambda S, B, r: (
            '左半用完了 → 取右半 `arr[j]`' if S.i == S.mid + 1 else
            (f'`arr[i] = {S.arr[S.i]} > arr[j] = {S.arr[S.j]}` → ==构成逆序对==，右边 `arr[j]` 先放入 tmp' if S.j <= S.right and S.arr[S.i] > S.arr[S.j]
             else f'`arr[i] = {S.arr[S.i]}` 不大于 `arr[j]` → 左边更小，先放左边')),
        'if p < i': '`p` 不能落在 `i` 左边：`i` 之前的已经放进 tmp 了，`p` 至少是 `i`',
        'p = i': '`p = i = {p}`',
        'while p <= mid and arr[p] - arr[j]': lambda S, B, r: (
            f'`p = {S.p}`：`arr[p] - arr[j] = {S.arr[S.p] - S.arr[S.j]} <= {S.threshold}` → 差值在阈值内，`p` 右移'
            if S.p <= S.mid and S.arr[S.p] - S.arr[S.j] <= S.threshold
            else (f'`p = {S.p}`：`arr[p] - arr[j] = {S.arr[S.p] - S.arr[S.j]} > {S.threshold}` → 差太大了，停' if S.p <= S.mid else '`p` 越过左半末尾，停')),
        'p += 1': '`p` → {p}',
        'tot += p - i': '`i..p-1` 这 `{p - i}` 个数与 `arr[{j}]` 的差都在 `(0, threshold]` → `tot = {B.tot} + {p - i} = =={tot}==`',
        'tmp.append(arr[j])': '`arr[j] = {arr[j]}` 放入 tmp',
        'j += 1': '`j` → {j}',
        'tmp.append(arr[i])': '`arr[i] = {arr[i]}` 放入 tmp',
        'i += 1': '`i` → {i}',
        'for index, v in enumerate(tmp)': lambda S, B, r: f'把 tmp 写回 `arr[left..right]`：这一段现在已排好序',
        'arr[index + left] = v': '`arr[{index + left}] = {v}`',
    },
    cards=dict(
        one_liner='阈值越大逆序对越多：二分阈值，归并排序里数逆序对',
        complexity='时间 `O(n log n log M)`，空间 `O(n)`（M = max − min）',
        problem=['逆序对 `(i, j)`：`i < j` 且 `0 < nums[i] - nums[j] <= x`，`x` 叫阈值',
                 '求最小的阈值，使得逆序对至少有 `k` 对；不存在返回 `-1`',
                 '本视频：`nums = [4,2,5,1]`，`k = 3` → `3`'],
        quote='若min_threshold越小，那么阈值为min_threshold的逆序对就越少，因此在这里可以二分答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['阈值 `x` 变大，满足条件的对只增不减 → ==二分答案==，上界多留一格 `ma + 1` 表示无解',
              '对给定阈值，用归并排序数对：右边 `arr[j]` 先出时，左边剩余的比它大的数都能配对',
              '但还要差值 `<= threshold`：左半有序，用单调右移的 `p` 找到分界，对数 = `p - i`'],
        summary=['时间 `O(n log n · log M)`：外层二分 × 归并计数',
                 '左半有序，所以满足差值限制的是一段前缀 `[i, p)`，`p` 只右移',
                 '`tot >= k` 时提前返回，省时间；此时 arr 没有排完，所以每轮都复制 `nums`',
                 '二分上界 `ma + 1` 表示无解，最后判断 `left == ma + 1` 返回 `-1`',
                 '原文已是 Python 3 兼容写法，代码未作修改'],
    ),
)
