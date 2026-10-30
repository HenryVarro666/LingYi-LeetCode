NUMS, K = [2, 2, 1, 2, 1, 2, 2, 1, 2], 2


def _brute(a, k):
    return sum(1 for i in range(len(a)) for j in range(i, len(a)) if sum(x % 2 for x in a[i:j + 1]) == k)


def _ptr(name):
    def f(S):
        v = S.get(name)
        return v if isinstance(v, int) and 0 <= v < len(S['nums']) else None
    return f


_MI, _MA = _ptr('mi_r'), _ptr('ma_r')


def _color(S, i, v):
    if S.get('_line') == 23 and S['mi_r'] <= i <= S['ma_r']:
        return 'green'
    if v % 2 == 1:
        return 'orange'
    return None


def _top(S):
    if 'now' not in S:
        return '奇数（橙色）才计数，偶数可以随便延伸'
    if S.get('_line') == 23:
        return f"左边界 {S['l']}：右边界取 `{S['mi_r']}..{S['ma_r']}` 都恰好有 {S['k']} 个奇数 → =={S['ma_r'] - S['mi_r'] + 1}== 个"
    if 'l' in S and S.get('_line', 0) >= 18:
        return f"左边界 `l = {S['l']}`，最短优美子数组的右边界 `mi_r = {S['mi_r']}`"
    return f"从 0 开始数奇数：已数到 `now = {S['now']}` 个"


CONFIG = dict(
    num=1248, title='统计「优美子数组」', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左边界 · 最短/最长右边界',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def numberOfSubarrays(self, nums, k):

        n = len(nums)
        res = 0
        l = 0
        mi_r = -1
        ma_r = -1
        now = 0
        while now < k and mi_r + 1 < n:
            mi_r += 1
            if nums[mi_r] % 2 == 1:
                now += 1

        if now < k:
            return 0

        while l < n and mi_r < n:
            ma_r = mi_r
            while ma_r + 1 < n and nums[ma_r + 1] % 2 == 0:
                ma_r += 1
            
            res += ma_r - mi_r + 1

            if nums[l] % 2 == 1:
                mi_r = ma_r + 1
            l += 1
        
        return res
''',
    call=f'Solution().numberOfSubarrays({NUMS}, {K})',
    expect=_brute(NUMS, K),
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（橙 = 奇数，框 = [l, mi_r]，绿 = 合法右边界 mi_r..ma_r）',
             pointers={'l': 'blue', _MI: 'pink', _MA: 'purple'}, pointer_labels={_MI: 'mi_r', _MA: 'ma_r'},
             window=('l', _MI), color=_color, cell=96, h=320),
    ],
    watch=[('k', 'k', 'orange'), ('now', 'now'), ('l', 'l', 'blue'), ('mi_r', 'mi_r', 'pink'), ('ma_r', 'ma_r', 'purple'), ('res', 'res', 'green')],
    skip=['res = 0', 'l = 0', 'ma_r = -1'],
    captions={
        'n = len(nums)': '`n = {n}`，要找恰好含 `k = {k}` 个奇数的子数组',
        'mi_r = -1': '`mi_r`：以 l 为左边界的==最短==优美子数组的右边界；`ma_r`：==最长==的',
        'now = 0': '`now`：已经数到的奇数个数',
        'while now < k and': lambda S, B, r: (f'`now = {S.now} < {S.k}`：继续往右找奇数' if S.now < S.k and S.mi_r + 1 < S.n
                                              else (f'凑够 {S.k} 个奇数：`mi_r = {S.mi_r}`' if S.now >= S.k else '到末尾了')),
        'mi_r += 1': '`mi_r` → {mi_r}',
        'if nums[mi_r] % 2 == 1': lambda S, B, r: (f'`nums[{S.mi_r}] = {S.nums[S.mi_r]}` 是奇数' if S.nums[S.mi_r] % 2 else f'`nums[{S.mi_r}] = {S.nums[S.mi_r]}` 是偶数，不计数'),
        'now += 1': '`now` → {now}',
        'if now < k': '奇数够 {k} 个，否则直接返回 0',
        'while l < n and mi_r < n': lambda S, B, r: (f'左边界 `l = {S.l}`，`mi_r = {S.mi_r}` 有效' if S.l < S.n and S.mi_r < S.n
                                                     else '`mi_r` 越界：再也凑不出 k 个奇数，结束'),
        'ma_r = mi_r': '`ma_r` 从 `mi_r = {mi_r}` 出发',
        'while ma_r + 1 < n': lambda S, B, r: (f'`nums[{S.ma_r + 1}] = {S.nums[S.ma_r + 1]}` 是偶数 → 加进来奇数个数不变，延伸' if S.ma_r + 1 < S.n and S.nums[S.ma_r + 1] % 2 == 0
                                               else ('到末尾了' if S.ma_r + 1 >= S.n else f'`nums[{S.ma_r + 1}]` 是奇数，再延伸就多了 → `ma_r = {S.ma_r}`')),
        'ma_r += 1': '`ma_r` → {ma_r}',
        'res += ma_r - mi_r + 1': '右边界取 `{mi_r}..{ma_r}`：`{ma_r} − {mi_r} + 1` 个 → `res` = =={res}==',
        'if nums[l] % 2 == 1': lambda S, B, r: (f'`nums[{S.l}] = {S.nums[S.l]}` 是奇数：移出后少一个奇数，mi_r 要跳到下一个奇数' if S.nums[S.l] % 2
                                                else f'`nums[{S.l}] = {S.nums[S.l]}` 是偶数：移出后奇数个数不变，==mi_r、ma_r 不用动=='),
        'mi_r = ma_r + 1': '`ma_r` 的下一个就是奇数 → `mi_r = {mi_r}`',
        'l += 1': '左边界右移 → `l = {l}`',
        'return res': '一共 =={ret}== 个优美子数组',
    },
    max_steps=80,
    cards=dict(
        one_liner='枚举左边界 l：合法右边界是 [mi_r, ma_r] 一整段',
        complexity='时间最坏 `O(n²)`（ma_r 每轮从 mi_r 重扫），空间 `O(1)`',
        problem=['给整数数组 `nums` 和整数 `k`',
                 '==优美子数组==：恰好有 k 个奇数的连续子数组，求个数',
                 '示例：`[1,1,2,1,1], k = 3` → `2`',
                 '示例：`[2,2,2,1,2,2,1,2,2,2], k = 2` → `16`',
                 f'本视频：`{NUMS}, k = {K}` → `{_brute(NUMS, K)}`'],
        quote='mi_r和ma_r……分别表示以l为左边界的最短优美子数组的右边界以及最长优美子数组的右边界，那么以l为左边界的优美子数组就一共有ma_r - mi_r + 1个。',
        quote_src='—— yiduobo 题解原文',
        idea=['偶数对计数没影响：最短右边界 mi_r 是第 k 个奇数，之后的偶数都能接上',
              'l 右移：移出偶数 → 不变；移出奇数 → `mi_r = ma_r + 1`（下一个奇数）',
              '也可以把奇偶变成 01 数组，用==前缀和 + 哈希表==做'],
        summary=['l、mi_r 只右移；但 ma_r 每轮从 mi_r 重扫，偶数很多时最坏 `O(n²)`',
                 '改进：ma_r 也沿用上一轮（mi_r 不动时 ma_r 也不变），即可 `O(n)`',
                 '`mi_r` 越界说明奇数不够 k 个，可以结束',
                 '题面库里缺失，本视频按 LeetCode 1248 原题描述',
                 '代码本身可在 Python 3 运行，未做改动'],
    ),
)
