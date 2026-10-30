NUMS, N, LEFT, RIGHT = [1, 2, 3], 3, 1, 4


def _mat(S):
    s = S.get('one_prefix_s')
    if not s or len(s) < N + 1:
        return [['' for _ in range(N)] for _ in range(N)]
    return [[(s[j] - s[i]) if j > i else '' for j in range(1, N + 1)] for i in range(N)]


def _mcol(S, i, j, v):
    if v == '':
        return None
    lm = S['_inner']
    if 'mid' in lm and 'res' not in lm:
        x = lm['mid']
        return 'green' if v <= x else None
    if 'res' in lm and 'l' in lm:
        return 'cyan' if v < lm['l'] else ('yellow' if v == lm['l'] else None)
    return None


def _cursor_i(S):
    lm = S['_inner']
    return lm.get('i') if 'i' in lm and 'target' in lm else None


def _cursor_j(S):
    lm = S['_inner']
    if 'j' in lm and 'target' in lm:
        return lm['j'] - 1  # 矩阵第 0 列对应 j = 1
    return None


def _top(S):
    lm = S['_inner']
    if 'target' not in lm:
        return f'前 `r` 小之和 − 前 `l−1` 小之和：`get({RIGHT}) − get({LEFT - 1})`'
    t = lm['target']
    if 'res' in lm:
        return f"`get({t})`：`x = {lm['l']}`：累加 `< x`（青），再补若干个 x（黄）"
    if 'mid' in lm:
        return f"`get({t})`：二分第 {t} 小，`mid = {lm['mid']}`，数 `≤ mid` 的个数（绿）"
    return f'`get({t})`：二分第 {t} 小的数'


def _row(S, B, ret):
    s, i, j, mid = S.one_prefix_s, S.i, S.j, S.mid
    return f'第 {i} 行：`s[{j}] − s[{i}] = {s[j] - s[i]} ≤ {mid}`，`j` 右移'


CONFIG = dict(
    num=1508, title='子数组和排序后的区间和', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分第 k 小 · 双前缀和',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def rangeSum(self, nums, n, left, right):

        one_prefix_s = [0]
        for num in nums:
            one_prefix_s.append(one_prefix_s[-1] + num)
        
        two_prefix_s = [0]
        for s in one_prefix_s[1:]:
            two_prefix_s.append(two_prefix_s[-1] + s)
        
        mod = 10 ** 9 + 7
        res = self.get(n, one_prefix_s, two_prefix_s, right, mod)
        if left > 1:
            res -= self.get(n, one_prefix_s, two_prefix_s, left - 1, mod)
        
        return res
    
    def get(self, n, one_prefix_s, two_prefix_s, target, mod):
        l = 1
        r = one_prefix_s[-1]

        while l < r:
            mid = (l + r) >> 1
            i = 0
            j = 1
            cnt = 0
            while i < n:
                while j <= n and one_prefix_s[j] - one_prefix_s[i] <= mid:
                    j += 1

                j -= 1

                cnt += j - i
                i += 1

            if cnt < target:
                l = mid + 1
            else:
                r = mid

        res = 0
        i = 0
        j = 1
        cnt = 0
        while i < n:
            while j <= n and one_prefix_s[j] - one_prefix_s[i] < l:
                j += 1
            
            j -= 1

            res = (res + two_prefix_s[j] - two_prefix_s[i] - one_prefix_s[i] * (j - i) + mod) % mod
            cnt += j - i
            i += 1

        res = (res + (target - cnt) * l) % mod

        return res
''',
    call=f'Solution().rangeSum({NUMS}, {N}, {LEFT}, {RIGHT})',
    expect=9,
    views=[
        dict(type='text', fn=_top, size=25, h=90),
        dict(type='table', var=_mat, label='子数组和矩阵 m[i][j] = s[j] − s[i]（行 = 起点 i，列 = 终点 j）', h=300,
             rows=[f'i={i}' for i in range(N)], cols=[f'j={j}' for j in range(1, N + 1)], color=_mcol,
             cursors=[(_cursor_i, _cursor_j, 'yellow', '')], cell=110),
        dict(type='array', var='one_prefix_s', label='one_prefix_s（前缀和 s）', cell=90, h=150),
        dict(type='array', var='two_prefix_s', label='two_prefix_s（前缀和的前缀和）', cell=90, h=150),
    ],
    watch=['target', 'l', 'r', 'mid', 'cnt', ('res', 'res', 'green')],
    captions={
        'one_prefix_s.append': '前缀和 `s`：`one_prefix_s = {one_prefix_s}`',
        'two_prefix_s.append': '二级前缀和：`two_prefix_s = {two_prefix_s}`，用来快速求 `s[a] + … + s[b]`',
        'mod = 10': '答案对 `10^9 + 7` 取模',
        'res = self.get(': '前 `right = {right}` 小的数之和：调用 `get(target = {right})`',
        'if left > 1': lambda S, B, r: (f'`left = {S.left} > 1`：再减去前 `left − 1` 小之和' if S.left > 1
                                        else f'`left = 1`：前 0 小之和为 0，==不用再减==；`res = {S.res}`'),
        'res -= self.get': '`res = {res}`',
        20: '二分第 `target = {target}` 小的数 `x`：下界 `l = 1`',
        'r = one_prefix_s[-1]': '上界 `r = s[n] = {r}`：整个数组的和最大',
        'while l < r': lambda S, B, r: (f'区间 `[{S.l}, {S.r}]` 还有多个候选，继续二分' if S.l < S.r else f'`l = r = {S.l}`：第 `{S.target}` 小的数就是 =={S.l}=='),
        'mid = (l + r) >> 1': '猜 `mid = ({l} + {r}) >> 1 = {mid}`：数一数矩阵中 `≤ {mid}` 的有几个',
        'while j <= n and one_prefix_s[j] - one_prefix_s[i] <= mid':
            lambda S, B, r: (f'第 {S.i} 行：`j = {S.j}` 还在对角线左侧（空位），右移' if S.j <= S.i else
                             f'第 {S.i} 行：`m[{S.i}][{S.j}] = {S.one_prefix_s[S.j] - S.one_prefix_s[S.i]} ≤ {S.mid}`，`j` 继续右移'
                             if S.j <= S.n and S.one_prefix_s[S.j] - S.one_prefix_s[S.i] <= S.mid
                             else (f'第 {S.i} 行：`j = {S.j}` 出界，停下' if S.j > S.n else
                                   f'第 {S.i} 行：`m[{S.i}][{S.j}] = {S.one_prefix_s[S.j] - S.one_prefix_s[S.i]} > {S.mid}`，停下')),
        34: '这一行 `≤ {mid}` 的有 `j − i` 个：累计 `cnt = {cnt}`；下一行 ==j 不用回头==',
        'if cnt < target': lambda S, B, r: (f'`cnt = {S.cnt} < target = {S.target}`：`mid` 太小' if S.cnt < S.target else f'`cnt = {S.cnt} ≥ target = {S.target}`：第 {S.target} 小的数 `≤ {S.mid}`'),
        'l = mid + 1': '`l = {l}`',
        40: '`r = {r}`',
        'res = 0': '求所有 ==严格小于 x = {l}== 的数之和，再补 `target − cnt` 个 x',
        'while j <= n and one_prefix_s[j] - one_prefix_s[i] < l':
            lambda S, B, r: (f'第 {S.i} 行：`j = {S.j}` 还在对角线左侧（空位），右移' if S.j <= S.i else
                             f'第 {S.i} 行：`m[{S.i}][{S.j}] = {S.one_prefix_s[S.j] - S.one_prefix_s[S.i]} < {S.l}`，`j` 右移'
                             if S.j <= S.n and S.one_prefix_s[S.j] - S.one_prefix_s[S.i] < S.l
                             else (f'第 {S.i} 行：`j = {S.j}` 出界，停下' if S.j > S.n else
                                   f'第 {S.i} 行：`m[{S.i}][{S.j}] = {S.one_prefix_s[S.j] - S.one_prefix_s[S.i]} ≥ {S.l}`，停下')),
        'res = (res + two_prefix_s[j]': lambda S, B, r: (f'第 {S.i} 行 `< x` 的和 = `two_s[{S.j}] − two_s[{S.i}] − s[{S.i}]×({S.j}−{S.i})` = '
                                                         f'`{S.two_prefix_s[S.j] - S.two_prefix_s[S.i] - S.one_prefix_s[S.i] * (S.j - S.i)}` → `res = {S.res}`'),
        'res = (res + (target - cnt) * l)': '`< x` 的有 `cnt = {cnt}` 个，补 `{target} − {cnt}` 个 `x = {l}`：==重复值也算对==，`res = {res}`',
    },
    skip=[4, 5, 8, 9, 12, 25, 26, 27, 28, 30, 32, 35, 43, 44, 45, 46, 48, 50, 53, 54],
    max_steps=75,
    cards=dict(
        one_liner='子数组和排成行列单调的矩阵，二分第 k 小，再用二级前缀和求和',
        complexity='时间 `O(n log S)`，空间 `O(n)`，`S = sum(nums)`',
        problem=['正整数数组 `nums`（长 `n`）的 `n(n+1)/2` 个子数组和==从小到大排序==',
                 '返回排序后第 `left` 到第 `right` 个数（从 1 开始）之和，对 `10^9+7` 取模',
                 '示例：`[1,2,3,4], n = 4, left = 1, right = 5` → `13`；本视频 `[1,2,3], 1, 4` → `9`'],
        quote='对于起点相同的子数组而言，终点越靠后的子数组和就越大。而对于终点相同的子数组而言，则是起点越靠前的子数组和就越大……第i行第j列的值就是==s[j] - s[i]==。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案 = 前 `right` 小之和 − 前 `left−1` 小之和，都交给 `get(target)`',
              '矩阵行递增、列递减：数 `≤ x` 的个数时 `j` 只右移不回头，`O(n)`',
              '第 `target` 小为 `x`：先加所有 `< x` 的数，再补 `target − cnt` 个 `x`'],
        summary=['时间 `O(n log S)`，空间 `O(n)`；暴力排序是 `O(n² log n)`',
                 '一行 `< x` 的和 = `two_s[p] − two_s[i] − s[i]·(p − i)`',
                 '直接求「`≤ x` 之和」会被重复值坑，所以用「`< x` 之和 + 补 x」',
                 '原文为 Python 2 风格（已用 `>>`），代码无需改动即可在 Python 3 运行'],
    ),
)
