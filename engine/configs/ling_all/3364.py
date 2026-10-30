NUMS = [-2, -3, -2, 5, 5, 3]
L_, R_ = 2, 3


def _i_star(S):
    """index i whose s[i] is sl[k-1] (the best left end for this j), searched inside the window"""
    if S.get('_line') not in (9, 10) or not S.get('k'):
        return None
    j, s, sl = S['j'], S['s'], S['sl']
    for i in range(max(j - S['r'], 0), j - S['l'] + 1):
        if s[i] == sl[S['k'] - 1]:
            return i
    return None


def _sub_left(S):
    return _i_star(S)


def _scolor(S, i, v):
    if 'j' not in S:
        return None
    if i == S['j']:
        return 'blue'
    if i == _i_star(S):
        return 'green'
    return None


def _slcolor(S, i, v):
    if S.get('_line') in (9, 10) and S.get('k') and i == S['k'] - 1:
        return 'green'
    return None


def _txt(S):
    if 'j' not in S:
        return '子数组 `nums[i..j-1]` 的和 = `s[j] − s[i]`：要正数且尽量小 → 找 ==小于 s[j] 的最大 s[i]=='
    ln, j = S['_line'], S['j']
    lo, hi = max(j - S['r'], 0), j - S['l']
    if ln <= 7:
        return f'`j = {j}`：`i` 的范围 `[{lo}, {hi}]`（`l ≤ j−i ≤ r`），`s[{j}] = {S["s"][j]}`'
    k = S['k']
    sj = S['s'][j]
    if ln == 8 or (ln == 9 and not k) or (ln == 10 and not k):
        return f'`s[{j}] = {sj}`，集合里小于它的有 `{k}` 个' + ('，没有可用的左端点' if k == 0 else '')
    if ln in (9, 10):
        pre = S['sl'][k - 1]
        return f'`s[{j}] − sl[{k - 1}] = {sj} − ({pre}) = ` =={sj - pre}=='
    return f'`s[{j}] = {sj}`，当前 `ans = {S["ans"]}`'


def _k_cap(S, B, ret):
    if S.k == 0:
        return f'`k = 0`：集合里没有比 `s[{S.j}] = {S.s[S.j]}` 小的前缀和 → 这个右端点凑不出正和，不更新'
    return f'`k = {S.k} > 0`：有比 `s[{S.j}]` 小的前缀和，最大的是 `sl[{S.k - 1}] = {S.sl[S.k - 1]}`，差最小且为正'


def _rm_cap(S, B, ret):
    if S.j >= S.r:
        return f'`j = {S.j} ≥ r = {S.r}`：窗口已满，`s[{S.j - S.r}]` 马上离开（下个 j 的 `i` 不能小于 `{S.j - S.r + 1}`）'
    return f'`j = {S.j} < r = {S.r}`：`j − r` 为负，还没有 `i` 需要离开，不用删'


CONFIG = dict(
    num=3364, title='最小正和子数组', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 定长滑窗 + 有序集合',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        ans = inf
        s = list(accumulate(nums, initial=0))
        sl = SortedList()  # sortedcontainers
        for j in range(l, len(nums) + 1):
            sl.add(s[j - l])
            k = sl.bisect_left(s[j])
            if k:
                ans = min(ans, s[j] - sl[k - 1])
            if j >= r:
                sl.remove(s[j - r])
        return -1 if ans == inf else ans
''',
    setup='''
class SortedList(list):  # 演示用的最小实现，行为同 sortedcontainers.SortedList（本题只用到这三个操作）
    def add(self, x):
        bisect.insort(self, x)

    def bisect_left(self, x):
        return bisect.bisect_left(self, x)
''',
    call=f'Solution().minimumSumSubarray({NUMS!r}, {L_}, {R_})',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前找到的子数组 nums[i..j-1]）', cell=72, pointers={'j - 1': 'blue'},
             pointer_labels={'j - 1': 'j-1'}, window=(_sub_left, 'j - 1'), h=185),
        dict(type='array', var='s', label='s 前缀和（青框 = 合法的 i ∈ [j−r, j−l]，绿 = 选中的 s[i]）', cell=72,
             pointers={'j': 'blue'}, window=('max(j - r, 0)', 'j - l'), color=_scolor, h=185),
        dict(type='array', var='sl', label='sl 有序集合（k = s[j] 在其中的插入位置）', cell=72, min_slots=4,
             pointers={'k if _line in (8, 9, 10) else None': 'orange'},
             pointer_labels={'k if _line in (8, 9, 10) else None': 'k'}, color=_slcolor, h=180),
        dict(type='text', h=85, size=28, fn=_txt),
    ],
    watch=[('j', 'j', 'blue'), ('s[j]', 's[j]', 'cyan'), ('k', 'k', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans` 初始无穷大：还没找到正和子数组',
        's = list(accumulate': '前缀和 `s`：`nums[i..j-1]` 的和 = `s[j] − s[i]`',
        'sl = SortedList()': '有序集合 `sl` 里放 ==i ∈ [j−r, j−l]== 的 `s[i]`，能快速找「小于 s[j] 的最大值」',
        'for j in range': lambda S, B, r_: (f'枚举右端点 `j = {S.j}`：左端点 `i` 要在 `[{max(S.j - S.r, 0)}, {S.j - S.l}]` 里'
                                            if 'j' in S and ('j' not in B or S.j != B.j) else '右端点枚举完了'),
        'sl.add': '新进入范围的 `i = {j - l}`：`s[{j - l}] = {s[j - l]}` 加入集合 → `{list(sl)}`',
        'k = sl.bisect_left': '`bisect_left` 返回 `k = {k}`：集合里有 `{k}` 个数小于 `s[{j}] = {s[j]}`',
        'if k:': _k_cap,
        'ans = min': '子数组和 = `s[j] − sl[k-1]` = `{s[j]} − ({sl[k - 1]})` = `{s[j] - sl[k - 1]}`，`ans = min({B.ans}, {s[j] - sl[k - 1]})` → =={ans}==',
        'if j >= r': _rm_cap,
        'sl.remove': '`s[{j - r}]` 离开集合 → `{list(sl)}`',
        'return -1': lambda S, B, r_: (f'`ans = {S.ans}` 就是最小正和，返回 =={S.ans}==' if S.ans != inf else '`ans` 还是 inf：没有正和子数组，返回 `-1`'),
    },
    max_steps=70,
    cards=dict(
        one_liner='把子数组和变成 s[j] − s[i]：找小于 s[j] 的最大前缀和',
        complexity='时间 `O(n + (n−l)log(r−l))`，空间 `O(n)`',
        problem=['在长度为 `l ~ r` 的子数组里，找和 ==大于 0== 的最小和；没有则返回 `-1`',
                 '示例：`[3,-2,1,4], l=2, r=3` → `1`（`[3,-2]`）',
                 '本视频：`[-2,-3,-2,5,5,3], l=2, r=3` → `3`'],
        quote='利用前缀和，问题变成：找到一个小于 s[j] 的最大前缀和 s[i]，满足 l≤j−i≤r。枚举 j，那么 i 需要满足 j−r≤i≤j−l。用有序集合维护这个范围内的 s[i]。',
        quote_src='—— 灵茶山艾府题解（方法二，公式符号为引用时改写）',
        idea=['和 = `s[j] − s[i]` 要为正且最小 → `s[i]` ==小于 s[j] 且尽量大==',
              '`i ∈ [j−r, j−l]` 随 `j` 右移而滑动：右边进一个，左边出一个',
              '窗口里的前缀和放进有序集合，`bisect_left` 一步得到前驱'],
        summary=['时间 `O(n + (n−l)log(r−l))`，空间 `O(n)`',
                 '`k = 0` 表示没有比 `s[j]` 小的数，不能取 `sl[k-1]`，所以要 `if k`',
                 '顺序：先 `add` 新的 `s[j−l]`，再查询，最后删 `s[j−r]`',
                 'Python 没有内置有序集合：原题解用 sortedcontainers，视频里用等价的小 SortedList 代替',
                 '方法一：暴力枚举左右端点边加边判断，`O((n−l)r)`，数据范围小也能过'],
    ),
)
