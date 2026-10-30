def _color(S, i, v):
    arr = S.get('arr') or S.get('mountain_arr')
    if arr is None:
        return None
    if i in arr.last:
        return 'yellow'
    return None


def _phase(S):
    if 'peak' in S and S['peak'] is not None:
        return 2 if S['_line'] < 51 else 3
    return 1


def _top(S):
    m = S.get('mountain_arr')
    cnt = f"，已调用 `get` ==`{m.cnt}`== 次" if m else ''
    ln = S.get('_line', 0)
    if 'l' not in S:
        return '山脉数组只能用 `get` 访问' + cnt
    if S.get('peak') is None and ln <= 17:
        return '先找山顶：用相邻两个位置比大小「三分」收缩' + cnt
    if S.get('peak') is None:
        return '收缩完毕，山顶就在 `l` / `r` 其中一个' + cnt
    if ln <= 45:
        return f'山顶 `peak = {S["peak"]}`，先在左边上升段二分' + cnt
    return f'左边没有，再在右边下降段二分（`peak = {S["peak"]}`）' + cnt


def _l(S):
    return S.get('l')


def _r(S):
    return S.get('r')


def _mid(S):
    return S.get('mid')


def _peak(S):
    return S.get('peak')


CONFIG = dict(
    num=1095, title='山脉数组中查找目标值', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='三分找山顶 + 两次二分',
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
    call='Solution().findInMountainArray(4, MountainArray([1,3,5,7,6,4,2]))',
    expect=5, max_steps=100,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var=[1, 3, 5, 7, 6, 4, 2], label='山脉数组（黄 = 刚用 get 读过的位置）', h=330, cell=90,
             pointers={_l: 'blue', _r: 'pink', _mid: 'yellow', _peak: 'orange'},
             pointer_labels={_l: 'l', _r: 'r', _mid: 'mid', _peak: 'peak'},
             color=_color),
    ],
    watch=[('target', 'target', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'),
           ('peak', 'peak', 'orange'), ('get 次数', 'mountain_arr.cnt', 'cyan')],
    captions={
        'n = mountain_arr.length()': '`n = {n}`',
        'l = 0': '`l = 0`：搜索区间左端',
        'r = n - 1': '`r = n - 1 = {r}`：搜索区间右端',
        'peak = None': '`peak` 先留空，等找到山顶再填',
        'while l < r - 1': '`l < r - 1`？`{l} < {r - 1}` → {"区间里还不止两个位置，继续收缩" if l < r - 1 else "只剩两个位置，山顶就在 l、r 里"}',
        'mid = (l + r)': '`mid = ({l} + {r}) // 2 = {mid}`',
        'mid_tmp = ': '`mid_tmp = ({mid} + {r}) // 2 = {mid_tmp}`：mid 和 r 之间的点',
        'mid_v = ': '读 `arr[{mid - 1}] = {mid_v}`（get 第 {mountain_arr.cnt} 次）',
        'mid_tmp_v = ': '读 `arr[{mid}] = {mid_tmp_v}`（get 第 {mountain_arr.cnt} 次）',
        'if mid_v > mid_tmp_v': '`{mid_v} > {mid_tmp_v}`？{"是：已经在下坡，山顶在左边，==r = mid_tmp=="  if mid_v > mid_tmp_v else "否：还在上坡，山顶在右边，==l = mid=="}',
        'r = mid_tmp': '`r` → {r}',
        'l = mid\n': '`l` → {l}',
        'l_v = ': '`l_v = arr[{l}] = {l_v}`',
        'r_v = ': '`r_v = arr[{r}] = {r_v}`',
        'if l_v > r_v': '`l_v = {l_v}` 和 `r_v = {r_v}` 比较 → {"l 更高，山顶是 l" if l_v > r_v else "r 更高，山顶是 r"}',
        'if l_v == target': '山顶 `{l_v}` 是 target 吗？{"是，直接返回" if l_v == target else "不是"}',
        'elif l_v < target': '山顶是最大值：`{l_v} < {target}` → {"连山顶都比 target 小，不可能有，返回 -1" if l_v < target else "target 在山顶下面，两侧可能有"}',
        'peak = l': '`peak = {peak}`',
        'peak = r': '`peak = {peak}`',
        'l = 0\n': '左边上升段：`l = 0`',
        'r = peak - 1': '`r = peak - 1 = {r}`，在 `[0, {r}]` 上二分',
        'l = peak + 1': '右边下降段：`l = peak + 1 = {l}`',
        'r = n - 1\n': '`r = n - 1 = {r}`',
        'while l <= r': '`l <= r`？`{l} <= {r}` → {"继续二分" if l <= r else "区间空了，这一段没有 target"}',
        'v = mountain_arr.get(mid)': '读 `arr[{mid}] = {v}`（get 第 {mountain_arr.cnt} 次）',
        'if v == target': '`v = {v}` 和 `target = {target}` → {"相等，找到了" if v == target else "不相等"}',
        'elif v < target': lambda S, B, r: (f'`{S.v} < {S.target}`：' + ('==上升段== 太小，往右：`l = mid + 1`' if S.mid < S.peak else '==下降段== 太小，往左：`r = mid - 1`')) if S.v < S.target else (f'`{S.v} > {S.target}`：' + ('==上升段== 太大，往左：`r = mid - 1`' if S.mid < S.peak else '==下降段== 太大，往右：`l = mid + 1`')),
        'l = mid + 1': '`l` → {l}',
        'r = mid - 1': '`r` → {r}',
        'return mid': '找到了！下标 `{mid}`（`get` 共 {mountain_arr.cnt} 次）',
        'return -1': '返回 -1',
        'return l': '返回 `{l}`',
        'return r': '返回 `{r}`',
    },
    cards=dict(
        one_liner='把山脉看成凸函数：三分找最高点，再两边各二分',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['交互题：只能用 `get(k)` 读山脉数组（先升后降），`get` 不能超过 100 次',
                 '返回 ==最小== 的下标使 `get(index) == target`，没有则 `-1`',
                 '本视频：`[1,3,5,7,6,4,2]`，`target = 4` → `5`'],
        quote='我们可以将山脉数组视为一个凸的函数，有一种经典做法用来寻找这个最值点，称为三分查找。',
        quote_src='—— yiduobo 题解原文',
        idea=['三分：比较 `mid-1` 和 `mid` 两个点的函数值，判断山顶在哪一侧并收缩 `l`/`r`',
              '确定山顶 `peak` 后，先在 `[0, peak-1]` 上升段二分，找到就直接返回（保证下标最小）',
              '没找到再去 `[peak+1, n-1]` 下降段二分，两边的大小关系相反'],
        summary=['原文为 Python 2 写法，`/` 取整已改为 `//`，并删去了注释里的 MountainArray 接口说明',
                 '`get` 次数：三分约 `2 log n`，两次二分各 `log n`，远小于 100',
                 '易错：下降段二分里 `v < target` 要移动 `r`（方向与上升段相反）',
                 '对比灵神：灵神用三次 `sort.Search`，每次只读 `arr` 的一个条件；yiduobo 把山顶、两段二分分开写'],
    ),
)
