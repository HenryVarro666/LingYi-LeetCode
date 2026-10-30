class_setup = '''
class MountainArray:
    def __init__(self, a):
        self.a = a
        self.calls = 0

    def get(self, index):
        self.calls += 1
        return self.a[index]

    def length(self):
        return len(self.a)
'''


def _data(S):
    return S['mountain_arr'].a


def _info(S):
    m = S['mountain_arr']
    pk = S.get('peak')
    if pk is not None:
        return f'山峰 `peak = {pk}`（粉）；已调用 `get` {m.calls} 次（上限 100）'
    return f'三分找山峰：每轮比较 `get(mid-1)` 和 `get(mid)`；已调用 `get` {m.calls} 次'


def _color(S, i, v):
    pk = S.get('peak')
    if pk is not None and i == pk:
        return 'pink'
    if S.get('mid') is not None and i == S['mid'] and 'l' in S:
        return 'yellow'
    return None


def _dim(S, i, v):
    if S.get('peak') is not None or 'l' not in S or 'r' not in S:
        return False
    return i < S['l'] or i > S['r']


CONFIG = dict(
    num=1095, title='山脉数组中查找目标值', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='三分找山峰 + 两次二分',
    tags=['灵神题单', '难度分 1827'],
    setup=class_setup,
    skip=['l = 0', 'r = n - 1', 'mid_tmp = '],
    code='''
class Solution(object):
    def findInMountainArray(self, target, mountain_arr):

        n = mountain_arr.length()

        l = 0
        r = n - 1
        peak = None
        while l < r - 1:
            mid = (l + r) // 2
            mid_tmp = (mid + r) // 2
            mid_v = mountain_arr.get(mid - 1)
            mid_tmp_v = mountain_arr.get(mid)
            if mid_v > mid_tmp_v:
                r = mid_tmp
            else:
                l = mid
        
        l_v = mountain_arr.get(l)
        r_v = mountain_arr.get(r)
        if l_v > r_v:
            if l_v == target:
                return l
            elif l_v < target:
                return -1
            peak = l
        else:
            if r_v == target:
                return r
            elif l_v < target:
                return -1
            peak = r

        l = 0
        r = peak - 1
        while l <= r:
            mid = (l + r) // 2
            v = mountain_arr.get(mid)
            if v == target:
                return mid
            elif v < target:
                l = mid + 1
            else:
                r = mid - 1

        l = peak + 1
        r = n - 1
        while l <= r:
            mid = (l + r) // 2
            v = mountain_arr.get(mid)
            if v == target:
                return mid
            elif v < target:
                r = mid - 1
            else:
                l = mid + 1
        
        return -1
''',
    call='Solution().findInMountainArray(3, MountainArray([1, 2, 3, 4, 5, 3, 1]))',
    expect=2,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var=_data, label='mountain_arr（只能通过 get 访问）', pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'},
             cell=96, h=330, color=_color, dim=_dim),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('peak', 'peak', 'green'), ('target', 'target', 'cyan')],
    captions={
        'n = mountain_arr.length()': '数组长度 `n = {n}`；`get` 最多只能调 100 次',
        'peak = None': '`peak` 先留空，等找到山峰再填',
        'while l < r - 1': lambda S, B, r: (f'`l = {S.l}`、`r = {S.r}`，中间还有数 → 继续找山峰' if S.l < S.r - 1
                                            else f'`l = {S.l}`、`r = {S.r}` 相邻了 → 山峰就在这两个里'),
        'mid = (l + r)': '`mid = {mid}`',
        'mid_v = ': '读 `get({mid - 1})` = `{mid_v}`',
        'mid_tmp_v = ': '读 `get({mid})` = `{mid_tmp_v}`',
        'if mid_v > mid_tmp_v': lambda S, B, r: (
            f'`{S.mid_v}` > `{S.mid_tmp_v}`：已经在下坡 → ==山峰在左侧==，右端点收到 `mid_tmp`'
            if S.mid_v > S.mid_tmp_v else
            f'`{S.mid_v}` <= `{S.mid_tmp_v}`：还在上坡 → ==山峰在 mid 及右侧==，左端点移到 `mid`'),
        'r = mid_tmp': '`r = {r}`',
        'l = mid': '`l = {l}`',
        'l_v = ': '`l_v = get({l}) = {l_v}`',
        'r_v = ': '`r_v = get({r}) = {r_v}`',
        'if l_v > r_v': lambda S, B, r: (f'`{S.l_v}` > `{S.r_v}`：峰顶是 `l = {S.l}`' if S.l_v > S.r_v
                                         else f'`{S.l_v}` <= `{S.r_v}`：峰顶是 `r = {S.r}`'),
        'peak = l': '山峰 `peak = {peak}`，值 `{l_v}`；峰值比 target 大，target 一定在两侧',
        'peak = r': '山峰 `peak = {peak}`，值 `{r_v}`',
        'l_v == target': '山峰值 `{l_v}` 就是 target 吗？`{l_v} == {target}` → {"是，直接返回" if l_v == target else "不是"}',
        'r_v == target': '山峰值 `{r_v}` 就是 target 吗？`{r_v} == {target}` → {"是，直接返回" if r_v == target else "不是"}',
        'elif l_v < target': '`{l_v} < {target}`？山峰是最大值，比它还大 → {"不存在，返回 -1" if l_v < target else "继续找"}',
        'r = peak - 1': '先在上坡段 `[0, {peak}-1]` 二分（升序），因为要最小下标',
        'l = peak + 1': '上坡没找到，再在下坡段 `[{peak}+1, {n}-1]` 二分（降序）',
        'while l <= r': lambda S, B, r: (f'`l = {S.l} <= r = {S.r}`，区间非空' if S.l <= S.r else f'`l = {S.l} > r = {S.r}`，这一段找完了'),
        'v = mountain_arr.get(mid)': '读 `get({mid}) = {v}`，对比 target `{target}`',
        'if v == target': lambda S, B, r: (f'`{S.v} == {S.target}` → ==找到了，返回下标 {S.mid}==' if S.v == S.target
                                           else f'`{S.v} != {S.target}`'),
        'elif v < target': lambda S, B, r: (f'`{S.v} < {S.target}` → ' + ('偏小' if S.v < S.target else '不小，走 else')),
        'return mid': '找到 `target = {target}`，下标 ==`{mid}`==；上坡段先查，所以是最小下标',
        'return -1': '两段都没有 → `-1`',
    },
    cards=dict(
        one_liner='先三分找山峰，再在上坡和下坡各二分一次',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['山脉数组：先严格升后严格降，只能用 `get(k)` / `length()` 访问，`get` 最多 100 次',
                 '返回最小的下标使得值等于 `target`，没有则 `-1`',
                 '本视频：`[1,2,3,4,5,3,1]`，`target = 3` → `2`'],
        quote='我们可以将山脉数组视为一个凸的函数，有一种经典做法用来寻找这个最值点，称为三分查找。',
        quote_src='—— yiduobo 题解原文',
        idea=['比较 `f[mid-1]` 和 `f[mid]`：下降说明山峰在左侧，否则在右侧',
              '找到山峰 `peak` 后，先在 `[0, peak-1]` 升序段二分，找到就返回',
              '再在 `[peak+1, n-1]` 降序段二分（比较方向相反），最后返回 `-1`'],
        summary=['时间 `O(log n)`，`get` 次数远小于 100',
                 '先查上坡段才能保证返回最小下标',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`；`MountainArray` 在 `setup` 里按题意补了最小实现',
                 '易错：降序段里 `v < target` 要移动的是 `r`，方向和升序段相反'],
    ),
)
