ARR = [0, 2, 4, 6, 8, 10, 12, 9, 5, 1]


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i == S.get('mid') and S.get('_line') in (5, 6):
        return 'yellow'
    if i <= S['left']:
        return 'blue'
    if S['right'] <= i <= len(S['arr']) - 2:
        return 'red'
    return None


def _dim(S, i, v):
    return i == len(S['arr']) - 1


def _formula(S):
    if 'left' not in S:
        return ''
    a = S['arr']
    if S.get('_line') in (6, 7, 9) and 'mid' in S:
        m = S['mid']
        ok = a[m] > a[m + 1]
        return (f"`arr[{m}] > arr[{m + 1}]`？`{a[m]} > {a[m + 1]}` → " +
                ('==成立：下坡==，峰顶 ≤ mid' if ok else '==不成立：上坡==，峰顶 > mid'))
    return f"开区间 `({S['left']}, {S['right']})` 里的下标还没确定"


def _if(S, B, ret):
    a, m = S.arr, S.mid
    if a[m] > a[m + 1]:
        return f'`arr[{m}] = {a[m]} > arr[{m + 1}] = {a[m + 1]}`：==下坡==，峰顶下标 `≤ {m}`'
    return f'`arr[{m}] = {a[m]} < arr[{m + 1}] = {a[m + 1]}`：==上坡==，峰顶下标 `> {m}`'


CONFIG = dict(
    num=852, title='山脉数组的峰顶索引', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='开区间二分 · 上坡还是下坡',
    tags=['List.md'],
    code='''
class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        left, right = 0, len(arr) - 2
        while left + 1 < right:
            mid = (left + right) // 2
            if arr[mid] > arr[mid + 1]:
                right = mid
            else:
                left = mid
        return right
''',
    call=f'Solution().peakIndexInMountainArray({ARR})',
    expect=6,
    views=[
        dict(type='bars', var='arr', label='arr（蓝 = 确定是上坡，红 = 确定 arr[i] > arr[i+1]，黄 = mid）', h=470,
             pointers={'left': 'blue', 'right': 'red', 'mid': 'yellow'}, color=_color, dim=_dim, cell=90),
        dict(type='text', fn=_formula, h=60, size=26),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'red'), ('mid', 'mid', 'yellow')],
    captions={
        'left, right = 0': '开区间二分：`left = 0`（`arr[0] > arr[1]` 一定==不成立==），`right = n-2 = {right}`（一定==成立==）',
        'while left + 1 < right': lambda S, B, r: (
            f'`{B.left} + 1 < {B.right}`：开区间 `({B.left}, {B.right})` 还有没确定的下标' if B.left + 1 < B.right
            else f'`left + 1 == right = {B.right}`：开区间为空，==全部染好色了=='),
        'mid = (left + right) // 2': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if arr[mid] > arr[mid + 1]': _if,
        'right = mid': '`right = {right}`：`{right}` 及右边都满足 `arr[i] > arr[i+1]`（染红）',
        'left = mid': '`left = {left}`：`{left}` 及左边都是上坡（染蓝）',
        'return right': '`right` 是==第一个==满足 `arr[i] > arr[i+1]` 的下标，也就是峰顶：返回 `{ret}`',
    },
    cards=dict(
        one_liner='arr[i] > arr[i+1] 从不成立变成成立，二分找分界点',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['山脉数组 `arr`：先==严格递增==到峰值，再==严格递减==，返回峰值的下标',
                 '要求 `O(log n)`；示例：`[0,10,5,2]` → `1`',
                 '本视频：`[0,2,4,6,8,10,12,9,5,1]` → `6`'],
        quote='上坡：如果 ==arr[i]<arr[i+1]，那么峰顶下标 >i==。下坡：如果 ==arr[i]>arr[i+1]，那么峰顶下标 ≤i==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['随着 `i` 变大，`arr[i] > arr[i+1]` 从「不成立」变成「成立」→ ==有单调性，就能二分==',
              '开区间二分：`i = 0` 一定不成立，`i = n-2` 一定成立，作为初始的 `left`、`right`',
              '循环结束时 `left + 1 == right`，`right` 就是峰顶'],
        result='峰顶下标 `6`（`arr[6] = 12`）✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '为什么 `n-2` 不用放进二分范围？排除法：峰顶不在 `[1, n-3]` 中就只能是 `n-2`',
                 '开区间写法：条件 `left + 1 < right`，更新 `left = mid` / `right = mid`，不用 ±1',
                 '库函数写法：`bisect_left(range(n - 2), True, 1, key=check)`'],
    ),
)
