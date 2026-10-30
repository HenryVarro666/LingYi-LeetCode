ARR = [0, 2, 4, 6, 8, 10, 12, 9, 5, 1]


def _color(S, i, v):
    if 'l' not in S:
        return None
    if i == S.get('mid') and S.get('_line') in (6, 7):
        return 'yellow'
    if S.get('_line') == 12 and i == S['l']:
        return 'green'
    return None


def _dim(S, i, v):
    return 'r' in S and not (S['l'] <= i <= S['r'])


def _formula(S):
    if 'l' not in S or 'r' not in S:
        return ''
    a = S['arr']
    if S.get('_line') in (7, 8, 10) and 'mid' in S:
        m = S['mid']
        if a[m] < a[m + 1]:
            return f"`arr[{m}] < arr[{m + 1}]`（{a[m]} < {a[m + 1]}）：上升段 → ==排除 mid 及之前=="
        return f"`arr[{m}] > arr[{m + 1}]`（{a[m]} > {a[m + 1]}）：mid+1 在下降段 → ==排除 mid+1 及之后=="
    if S['l'] == S['r']:
        return f"`l == r == {S['l']}`：只剩一个候选，它就是峰顶"
    return f"答案一定在 `[{S['l']}, {S['r']}]` 之中（灰色的已排除）"


def _if(S, B, ret):
    a, m = S.arr, S.mid
    if a[m] < a[m + 1]:
        return f'`arr[{m}] = {a[m]} < arr[{m + 1}] = {a[m + 1]}`：`{m}` 处于==上升部分== → 它和左边都不可能是答案'
    return f'`arr[{m}] = {a[m]} > arr[{m + 1}] = {a[m + 1]}`：`{m + 1}` 处于==下降部分== → 它和右边都不可能是答案'


CONFIG = dict(
    num=852, title='山脉数组的峰顶索引', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='二分 · 每次排除一边',
    tags=['List.md'],
    code='''
class Solution(object):
    def peakIndexInMountainArray(self, arr):
        l = 0
        r = len(arr) - 1
        while l < r:
            mid = (l + r) // 2
            if arr[mid] < arr[mid + 1]:
                l = mid + 1
            else:
                r = mid

        return l
''',
    call=f'Solution().peakIndexInMountainArray({ARR})',
    expect=6,
    views=[
        dict(type='bars', var='arr', label='arr（框 = 候选区间 [l, r]，灰 = 已排除，黄 = mid）', h=470,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, window=('l', 'r'), color=_color, dim=_dim, cell=90),
        dict(type='text', fn=_formula, h=60, size=26),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        'l = 0': '`l = 0`：候选区间的左端',
        'r = len(arr) - 1': '`r = {r}`：一开始所有下标 `[0, {r}]` 都可能是峰顶',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：候选不止一个，继续二分' if B.l < B.r
                                        else f'`l == r == {B.l}`：只剩一个候选 → 结束'),
        'mid = (l + r) // 2': '`mid = ({l} + {r}) // 2 = {mid}`',
        'if arr[mid] < arr[mid + 1]': _if,
        'l = mid + 1': '`l = mid + 1 = {l}`：排除 `mid` 以及之前的部分',
        'r = mid': '`r = mid = {r}`：排除 `mid + 1` 以及之后的部分（`mid` 自己可能就是峰顶，要留着）',
        'return l': '返回峰顶下标 `{ret}`（`arr[{ret}] = {arr[ret]}`）',
    },
    cards=dict(
        one_liner='比一次 arr[mid] 和 arr[mid+1]，就能排除掉一边',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['山脉数组 `arr`：先==严格递增==到峰值，再==严格递减==，返回峰值的下标',
                 '要求 `O(log n)`；示例：`[0,10,5,2]` → `1`',
                 '本视频：`[0,2,4,6,8,10,12,9,5,1]` → `6`'],
        quote='每次对于二分的mid，若a[mid] < a[mid + 1]，那么==排除mid以及之前的部分==，于是有l = mid + 1，否则==排除掉mid + 1以及之后的部分==。',
        quote_src='—— yiduobo 题解',
        idea=['`O(n)` 做法：从左往右找第一个 `a[i] > a[i+1]`；但可以更快',
              '`a[i] < a[i+1]`：i 在==上升部分==，i 及之前都不是答案；反之 i+1 及之后都不是',
              '一次比较就能排除一边 → 二分；`l == r` 时剩下的就是峰顶'],
        result='峰顶下标 `6`（`arr[6] = 12`）✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`mid = (l + r) // 2` 偏左，且 `l < r` 时 `mid + 1 ≤ r`，不会越界',
                 '易错：`r = mid` 不能写成 `mid - 1`，mid 自己可能就是峰顶',
                 '原文为 Python 2 写法：`mid = (l + r) / 2` 已改为 `//` 整除，并删去 docstring'],
    ),
)
