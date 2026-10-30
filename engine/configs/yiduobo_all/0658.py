ARR = [1, 3, 4, 6, 8, 9]
K, X = 3, 5


def _color(S, i, v):
    if 'k' not in S or S['_line'] < 21:
        return None
    return 'green' if S['l'] < i < S['r'] else None


def _dim(S, i, v):
    if 'mid' in S and S['_line'] in range(11, 18):
        return i < S['l'] or i > S['r']
    return False


def _top(S):
    ln = S.get('_line', 0)
    if 'l' not in S:
        return f'`x = {X}`：arr 有序 → 答案必然是==连续的一段=='
    if ln in range(11, 19):
        return f"二分找==第一个 ≥ {X}== 的位置：候选区间 `[{S['l']}, {S['r']}]`"
    l, r = S['l'], S['r']
    picked = ARR[l + 1:r]
    if S.get('k', 0) <= 0:
        return f'已选 `{picked}`，k 用完'
    parts = []
    if l >= 0:
        parts.append(f'左 `{ARR[l]}` 距 {abs(ARR[l] - X)}')
    if r < len(ARR):
        parts.append(f'右 `{ARR[r]}` 距 {abs(ARR[r] - X)}')
    return f"已选 `{picked}`，还差 `{S['k']}` 个；" + '，'.join(parts)


def _cmp(S, B, ret):
    l, r = S.l, S.r
    if r == len(S.arr):
        return '右边已经到头 → 只能往左扩展'
    dl, dr = abs(S.arr[l] - S.x), abs(S.arr[r] - S.x)
    if dl < dr:
        return f'`|{S.arr[l]} − {S.x}| = {dl} < |{S.arr[r]} − {S.x}| = {dr}`：左边更近 → 选左边'
    if dl == dr:
        return f'`|{S.arr[l]} − {S.x}| = {dl} ≤ |{S.arr[r]} − {S.x}| = {dr}`：距离相等，==取较小的左边=='
    return f'`|{S.arr[l]} − {S.x}| = {dl} > |{S.arr[r]} − {S.x}| = {dr}`：右边更近 → 选右边'


def _bin(S, B, ret):
    m = S.mid
    if S.arr[m] >= S.x:
        return f'`arr[{m}] = {S.arr[m]} ≥ {S.x}`：位置可能在 mid 或左边 → `r = mid`'
    return f'`arr[{m}] = {S.arr[m]} < {S.x}`：位置在 mid 右边 → `l = mid + 1`'


CONFIG = dict(
    num=658, title='找到 K 个最接近的元素', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分定位 + 双指针向两侧扩展',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def findClosestElements(self, arr, k, x):

        if x <= arr[0]:
            return arr[:k]
        
        if x >= arr[-1]:
            return arr[len(arr) - k:]

        l = 0
        r = len(arr) - 1
        while l < r:
            mid = (l + r) >> 1
            if arr[mid] >= x:
                r = mid
            else:
                l = mid + 1
        
        r = l
        l -= 1
        while k > 0:
            if l < 0:
                r += 1
            elif r == len(arr) or abs(arr[l] - x) <= abs(arr[r] - x):
                l -= 1
            else:
                r += 1
            k -= 1

        return arr[l + 1 : r]
''',
    call=f'Solution().findClosestElements({ARR}, {K}, {X})',
    expect=[3, 4, 6],
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='arr', label='arr（绿 = 已选中的 (l, r) 开区间）',
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, color=_color, dim=_dim, cell=110, h=280),
        dict(type='array', var=lambda S: [abs(v - X) for v in ARR], label=f'|arr[i] − x|（x = {X}）',
             color=_color, cell=110, index=False, h=180),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('k', 'k', 'orange'), 'x'],
    captions={
        'if x <= arr[0]': '`x = {x}` 不在最左边之外',
        'return arr[:k]': '`x ≤ arr[0]`：直接取前 k 个',
        'if x >= arr[-1]': '`x = {x}` 也不在最右边之外 → 要二分',
        'return arr[len(arr) - k:]': '`x ≥ arr[-1]`：直接取后 k 个',
        'l = 0': '二分区间 `[0, n − 1]`',
        'r = len(arr) - 1': '`r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，继续二分' if S.l < S.r
                                        else f'`l == r = {S.l}`：`arr[{S.l}] = {S.arr[S.l]}` 是==最小的 ≥ x 的数=='),
        'mid = (l + r)': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if arr[mid] >= x': _bin,
        'r = mid': '`r` → {r}',
        'l = mid + 1': '`l` → {l}',
        'r = l': '`p = r = {r}`：最小的 ≥ x 的数的位置',
        'l -= 1': lambda S, B, r: (f'`q = l = {S.l}`：最大的 < x 的数，`(l, r)` 开区间目前为空' if S._line == 20
                                   else f'选中 `arr[{B.l}] = {S.arr[B.l]}`，`l` → {S.l}'),
        'while k > 0': lambda S, B, r: (f'还要选 `k = {S.k}` 个' if S.k > 0 else '选够了'),
        'if l < 0': lambda S, B, r: ('左边已经到头' if S.l < 0 else f'`l = {S.l} ≥ 0`，左边还有候选'),
        'elif r == len': _cmp,
        'r += 1': '选中 `arr[{B.r}] = {arr[B.r]}`，`r` → {r}',
        'k -= 1': '`k` → {k}',
        'return arr[l + 1': '返回开区间 `(l, r)` = `arr[{l + 1}:{r}]` = =={ret}==',
    },
    cards=dict(
        one_liner='arr 有序，答案是连续一段：二分定位 x，再从中间向两边扩展 k 次',
        complexity='时间 `O(log n + k)`，空间 `O(1)`',
        problem=['有序数组 `arr`，返回离 `x` ==最近的 k 个数==，结果按升序',
                 '距离相等时==取较小的数==（`|a − x| == |b − x|` 且 `a < b` 时 a 更近）',
                 '示例：`[1,2,3,4,5], k = 4, x = 3` → `[1,2,3,4]`',
                 '本视频：`[1,3,4,6,8,9], k = 3, x = 5` → `[3,4,6]`'],
        quote='由于arr有序，因此最终的答案必然是arr中连续的一段……从p和q开始往两侧扩展。若arr[q] - x的绝对值==小于等于==arr[p] - x的绝对值，那么我们就将q往下扩展，否则将p往上扩展。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序取前 k（`O(n log n)`）或堆（`O(n log k)`）都没利用 arr 有序',
              '特判 `x ≤ arr[0]`、`x ≥ arr[-1]`；否则二分找 p = 第一个 ≥ x，q = p − 1',
              '比较两侧距离，近的先选，==相等选左边==；选 k 次'],
        summary=['时间 `O(log n + k)`，空间 `O(1)`（不计答案）',
                 '用 `<=` 比较：距离相同时优先较小的左侧元素',
                 '`l < 0` 或 `r == len(arr)` 时只能往另一边扩',
                 '结果是开区间 `(l, r)`，即 `arr[l + 1 : r]`',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
