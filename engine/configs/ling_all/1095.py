def _ph(S):
    """0 = 在 findInMountainArray 里；1/2/3 = 第几次 search"""
    if 'left' not in (S.get('_inner') or {}):
        return 0
    if 'peak' not in S:
        return 1
    return 3 if 'i' in S else 2


def _off(S):
    return S['peak'] if _ph(S) == 3 else 0


def _in_search(S):
    return _ph(S) != 0


def _lo(S):
    return S['left'] + _off(S) if 'left' in S and _in_search(S) else None


def _hi(S):
    return S['right'] + _off(S) if 'right' in S and _in_search(S) else None


def _mid(S):
    return S['mid'] + _off(S) if 'mid' in S and _in_search(S) else None


def _peak(S):
    return S.get('peak')


def _color(S, i, v):
    arr = S.get('arr')
    if arr is None:
        return None
    if i in arr.last:
        return 'yellow'
    if S.get('_line') == 14 and S.get('i') == i:
        return 'green'
    return None


def _top(S):
    ph = _ph(S)
    arr = S.get('arr')
    cnt = f"，已调用 `get` ==`{arr.cnt}`== 次" if arr else ''
    if ph == 1:
        return '第 1 次二分：找山峰（第一个比右邻居不小的位置）' + cnt
    if ph == 2:
        return f'第 2 次二分：在 `[0, {S["peak"]})` 上升段找第一个 `>= {S["target"]}`' + cnt
    if ph == 3:
        return f'第 3 次二分：在下降段 `[{S["peak"]}, n)` 找第一个 `<= {S["target"]}`' + cnt
    if 'peak' in S:
        return f'峰顶 `peak = {S["peak"]}`' + cnt
    return '山脉数组只能通过 `get` 访问，次数有限' + cnt


def _ret(S, B, ret):
    ph = _ph(B)
    if ph == 1:
        return f'二分结束，山峰下标 `peak = {ret}`'
    if ph == 2:
        return f'上升段里第一个 `>= target` 的位置 = =={ret}=='
    return f'下降段里第一个 `<= target` 的位置，相对 `peak` 偏移 `{ret}` → 数组下标 ==`{B.peak + ret}`=='


def _mid_cap(S, B, ret):
    ph = _ph(S)
    off = _off(S)
    return f'`mid = ({S.left} + {S.right}) // 2 = {S.mid}`，对应数组下标 ==`{S.mid + off}`=='


def _test(S, B, ret):
    ph = _ph(S)
    arr = S.arr
    m = S.mid + _off(S)
    a = arr.a
    if ph == 1:
        ok = a[m] >= a[m + 1]
        return f'`arr[{m}] = {a[m]}` {">=" if ok else "<"} `arr[{m+1}] = {a[m+1]}` → ' + ('已经在下坡，峰顶在 mid 或左边，==right = mid==' if ok else '还在上坡，峰顶在右边，==left = mid + 1==')
    if ph == 2:
        ok = a[m] >= S.target
        return f'`arr[{m}] = {a[m]}` {">=" if ok else "<"} `target = {S.target}` → ' + ('够大了，答案在 mid 或左边，==right = mid==' if ok else '太小，==left = mid + 1==')
    ok = a[m] <= S.target
    return f'`arr[{m}] = {a[m]}` {"<=" if ok else ">"} `target = {S.target}` → ' + ('下降段已经 <= target，答案在 mid 或左边，==right = mid==' if ok else '还比 target 大，==left = mid + 1==')


CONFIG = dict(
    num=1095, title='山脉数组中查找目标值', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='三次二分：找山峰、上升段、下降段（Go 原文转写）',
    tags=['灵神题单', '二分算法', '难度分 1827'],
    setup='''
class MountainArray:
    def __init__(self, a):
        self.a = a
        self.cnt = 0
        self.last = []

    def get(self, k):
        self.cnt += 1
        self.last = (self.last + [k])[-2:]
        return self.a[k]

    def length(self):
        return len(self.a)
''',
    code='''
def search(n, f):  # Go 的 sort.Search：[0, n) 中第一个 f(i) 为真的 i，没有则返回 n
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if not f(mid):
            left = mid + 1
        else:
            right = mid
    return left

class Solution:
    def findInMountainArray(self, target: int, arr: 'MountainArray') -> int:
        n = arr.length()
        peak = search(n - 1, lambda i: arr.get(i) >= arr.get(i + 1))
        i = search(peak, lambda i: arr.get(i) >= target)
        if arr.get(i) != target:
            i = peak + search(n - 1 - peak, lambda i: arr.get(peak + i) <= target)
            if arr.get(i) != target:
                return -1
        return i
''',
    call='Solution().findInMountainArray(4, MountainArray([1,3,5,7,6,4,2]))',
    expect=5, max_steps=110,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var=[1, 3, 5, 7, 6, 4, 2], label='山脉数组（黄 = 刚用 get 读过的位置）', h=330, cell=90,
             pointers={_lo: 'blue', _hi: 'pink', _mid: 'yellow', _peak: 'orange'},
             pointer_labels={_lo: 'left', _hi: 'right', _mid: 'mid', _peak: 'peak'},
             color=_color),
    ],
    watch=[('target', 'target', 'yellow'), ('peak', 'peak', 'orange'), ('left', 'left', 'blue'), ('right', 'right', 'pink'),
           ('mid', 'mid', 'yellow'), ('get 次数', 'arr.cnt', 'cyan'), ('i', 'i', 'green')],
    captions={
        'n = arr.length()': '`n = {n}`：数组长度',
        'left, right = 0, n': lambda S, B, r: (f'在 `{S.n}` 个位置里二分（下标从 `peak = {S.peak}` 往后数）：`left = 0`，`right = {S.right}`（开区间）' if _ph(S) == 3 else f'在 `[0, {S.n})` 里二分：`left = 0`，`right = {S.right}`（开区间）'),
        'while left < right': '`left < right` → {"区间还没空，继续" if left < right else "区间空了，left 就是答案"}',
        'mid = (': _mid_cap,
        'if not f(mid)': _test,
        'left = mid + 1': '`left` → {left}',
        'right = mid': '`right` → {right}',
        'return left': _ret,
        'peak = search': '第 1 次二分：找山峰 `peak`，==第一个 arr[i] >= arr[i+1] 的位置==',
        'i = search(peak': '第 2 次二分：只看上升段 `[0, peak)`，找第一个 `>= target`',
        'i = peak + search': '上升段没找到 → 第 3 次二分：在下降段里找第一个 `<= target`',
        'return -1': '两段都没有 target，返回 -1',
        'return i': '找到了，最小下标 `i = {i}`（`get` 共 {arr.cnt} 次）',
    },
    cards=dict(
        one_liner='先二分找山峰，再在上升段、下降段各二分一次',
        complexity='时间 `O(log n)`，`get` 约 `3 log n` 次',
        problem=['交互题：只能用 `get(k)` 读山脉数组（先升后降），`get` 不能超过 100 次',
                 '返回 ==最小== 的下标使 `get(index) == target`，没有则 `-1`',
                 '本视频：`[1,3,5,7,6,4,2]`，`target = 4` → `5`'],
        quote='peak := sort.Search(n-1, func(i int) bool { return arr.get(i) >= arr.get(i+1) })',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['`sort.Search` 就是二分：找第一个让条件为真的下标',
              '山峰：第一个 `arr[i] >= arr[i+1]` 的位置；上升段找第一个 `>= target`',
              '上升段没找到，再去下降段找第一个 `<= target`；先查上升段保证下标最小'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；Go 标准库的 `sort.Search` 展开成等价的 `search` 函数放在代码开头',
                 '三次二分，每次 `O(log n)`，`get` 次数远小于 100',
                 '易错：第二次判断要先用 `arr.get(i) != target`，找不到才进下降段',
                 '下降段的条件反过来：`arr.get(peak+i) <= target`',
                 '同类题：二分的「第一个满足条件」模板（题单「二分算法」）'],
    ),
)
