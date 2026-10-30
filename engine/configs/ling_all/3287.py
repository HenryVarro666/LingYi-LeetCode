

def _chips_row(cv, T, x, y, vals, cell=44, color=None, maxn=14, size=24):
    vals = sorted(vals)
    shown = vals[:maxn]
    for k, v in enumerate(shown):
        X = x + k * (cell + 6)
        cv.rect((X, y, X + cell, y + cell - 6), fill=(color or T['panel2']), r=8, outline=T['border'])
        cv.text((X + cell / 2, y + (cell - 6) / 2), str(v), size, T['bg'] if color else T['text'], anchor='mm', bold=True, mono=True)
    if len(vals) > maxn:
        cv.text((x + maxn * (cell + 6) + 4, y + (cell - 6) / 2), f'…共{len(vals)}个', 20, T['muted'], anchor='lm')
    if not vals:
        cv.text((x + 4, y + (cell - 6) / 2), '（空）', 22, T['dim'], anchor='lm')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    k = S['k']
    line = S.get('_line', 0)
    in_pre = 'ans' in S
    cell = min(70, (x1 - x0 - 40) / n)
    sx = x0 + 20
    cv.text((x0 + 18, y0 + 2), 'nums：蓝 = 前缀（左半 OR），粉 = 后缀（右半 OR）', 22, T['muted'], bold=True)
    cut = S.get('i')
    for t, v in enumerate(nums):
        X = sx + t * cell
        col = T['panel2']
        tc = T['text']
        if cut is not None:
            if in_pre:
                if t <= cut:
                    col, tc = T['blue'], T['bg']
                elif t >= cut + 1:
                    col, tc = T['pink'], T['bg']
            else:
                if t >= cut:
                    col, tc = T['pink'], T['bg']
        cv.rect((X + 2, y0 + 36, X + cell - 2, y0 + 36 + cell - 8), fill=col, r=8, outline=T['border'])
        cv.text((X + cell / 2, y0 + 36 + (cell - 8) / 2), str(v), 28, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, y0 + 36 + cell - 4), str(t), 16, T['dim'], anchor='mt', mono=True)
    y = y0 + 36 + cell + 36
    f = S.get('f')
    title = 'f[j]（前缀）：恰选 j 个数能 OR 出的值' if in_pre else 'f[j]（后缀）：恰选 j 个数能 OR 出的值'
    if isinstance(f, list):
        cv.text((x0 + 18, y), title, 22, T['blue'] if in_pre else T['pink'], bold=True)
        y += 34
        for j, st in enumerate(f):
            cv.text((x0 + 24, y + 18), f'j={j}', 22, T['muted'], anchor='lm', mono=True)
            _chips_row(cv, T, x0 + 90, y, st, color=(T['blue'] if in_pre else T['pink']) if j == len(f) - 1 else None)
            y += 46
    suf = S.get('suf')
    if isinstance(suf, list):
        y += 6
        cv.text((x0 + 18, y), 'suf[i]：后缀 i.. 里恰选 k 个的 OR 值集合', 22, T['pink'], bold=True)
        y += 34
        for t, st in enumerate(suf):
            if st is None:
                continue
            cv.text((x0 + 24, y + 18), f'suf[{t}]', 22, T['muted'], anchor='lm', mono=True)
            _chips_row(cv, T, x0 + 130, y, st, color=T['pink'] if (in_pre and cut is not None and t == cut + 1) else None)
            y += 46
    if in_pre and cut is not None and isinstance(f, list) and line >= LINE_B and isinstance(S.get('suf'), list) and cut + 1 < len(S['suf']) and S['suf'][cut + 1] is not None:
        y += 6
        cv.text((x0 + 18, y + 14), f"左 {sorted(f[-1])} 与右 {sorted(S['suf'][cut + 1])} 各取一个异或，最大 = {S['ans']}", 24, T['text'], anchor='lm', bold=True)


def _txt(S):
    if 'ans' not in S:
        return '左半 OR 与右半 OR 异或最大：枚举分割线，左右各算「恰选 k 个」的 OR 值集合'
    return f'分割线把 `nums` 分成前缀和后缀，全局答案 `ans = {S["ans"]}`'


CODE = '''
class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        suf = [None] * (n - k + 1)
        f = [set() for _ in range(k + 1)]
        f[0].add(0)
        for i in range(n - 1, k - 1, -1):
            v = nums[i]
            for j in range(min(k - 1, n - 1 - i), -1, -1):
                f[j + 1].update(x | v for x in f[j])
            if i <= n - k:
                suf[i] = f[k].copy()

        mx = reduce(or_, nums)
        ans = 0
        f = [set() for _ in range(k + 1)]
        f[0].add(0)
        for i, v in enumerate(nums[:-k]):
            for j in range(min(k - 1, i), -1, -1):
                f[j + 1].update(x | v for x in f[j])
            if i < k - 1:
                continue
            # 这里 f[k] 就是 pre[i]
            ans = max(ans, max(x ^ y for x in f[k] for y in suf[i + 1]))
            if ans == mx:
                return ans
        return ans
'''
LINE_B = CODE.strip('\n').split('\n').index('            ans = max(ans, max(x ^ y for x in f[k] for y in suf[i + 1]))') + 1


CONFIG = dict(
    num=3287, title='求出数组中最大序列值', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 + 0-1 背包（OR 集合）+ 试填法',
    tags=['灵神题单·位运算', '灵神题单·动态规划', '难度分 2545'],
    setup='from operator import or_',
    code=CODE,
    call='Solution().maxValue([4, 2, 5, 6, 7], 2)',
    expect=2,
    views=[
        dict(type='text', h=50, size=26, fn=_txt),
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('i', 'i', 'yellow'), ('v', 'v', 'cyan'), ('j', 'j if "j" in S else None', 'pink'), ('ans', 'ans', 'green')],
    skip=['for j in range(min(k - 1', 'n = len(nums)', 'suf = [None]', 'f[0].add(0)', 'v = nums[i]', 'ans = 0', 'f = [set()', 'if i < k - 1', 'return ans'],
    captions={
        'for i in range(n - 1, k - 1, -1)': lambda S, B, r: ('后缀处理完了，`suf[i]` 记下了每条分割线右边的 OR 集合' if B.get('i') == S.get('i') and 'v' in B else '后缀从右往左：做「选 j 个数，OR 能得到哪些值」的 0-1 背包'),
        'f[j + 1].update': '`j = {j}`（倒序）：选 `v = {v}`，`f[{j}]` 里每个 x → `f[{j + 1}]` 加入 `x | v` = =={sorted(f[j + 1])}==',
        'if i <= n - k': lambda S, B, r: (f'`i = {S.i} ≤ n − k = {S.n - S.k}`：后缀有 ≥ k 个数，可以记录' if S.i <= S.n - S.k else f'`i = {S.i} > n − k = {S.n - S.k}`：后缀不足 k 个数，不记录'),
        'suf[i] = f[k].copy()': '`suf[{i}]` = 后缀 `nums[{i}:]` 里选 k 个数的 OR 值集合 = =={sorted(suf[i])}==（复制一份存起来）',
        'continue': '前缀 `nums[:i+1]` 还不足 k 个数，凑不出 → 跳过',
        'mx = reduce': '`mx` = 所有数的 OR，答案不可能超过它',
        'for i, v in enumerate(nums[:-k])': lambda S, B, r: (f'分割线放在 `{S.i}` 之后：前缀 `nums[:{S.i + 1}]`，后缀 `nums[{S.i + 1}:]`' if S.i != B.get('i') or 'ans' not in B else '分割线都枚举完了'),
        'ans = max(ans, max(x ^ y': lambda S, B, r: f'`f[k]` 是前缀的 OR 集合 {sorted(S.f[S.k])}，`suf[{S.i + 1}]` 是后缀的 {sorted(S.suf[S.i + 1])}：两两异或取最大 → `ans = {S.ans}`',
        'if ans == mx': '`ans = {ans}`，到了理论最大值 `mx = {mx}` 就能提前返回；还没到，继续',
    },
    max_steps=130,
    cards=dict(
        one_liner='分割线两边各求「选 k 个」能 OR 出的值，再两两取最大异或',
        complexity='时间 `O(nkU + nU^2)`，空间 `O(nU)`',
        problem=['从 `nums` 里选长为 `2k` 的子序列，前 k 个的 OR 与后 k 个的 OR 做 XOR',
                 '求 XOR 的最大值，`nums[i] < 128`',
                 '演示：`nums = [4,2,5,6,7], k = 2` → `2`（`(4 OR 5) XOR (6 OR 7)`）'],
        quote='想象有一根分割线，把 nums 分成左右两部分，左和右分别计算所有长为 k 的子序列的 OR 都有哪些值。……把 OR 理解成一个类似加法的东西，转换成二维 0-1 背包。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分割线左边算「选 k 个数」的 OR 集合，右边同理，两两异或取最大',
              '二维 0-1 背包：个数 `j` + OR 值 `x`；`suf[i]` 记后缀、`pre` 记前缀',
              '优化：至多选 `popcount(mx)` 个数就够 OR 出任何值；用「超集计数」判断恰好 k 个能否凑出；最大异或用试填法'],
        summary=['时间 `O(nkU + nU^2)`，空间 `O(nU)`（`U` = 所有数的 OR，本题 < 128）',
                 '灵神给了三种写法：布尔数组 DP、集合 DP（本视频，Python 优化代码）、再用超集计数 + 试填法降到 `O(nU log U)`；这里演示集合写法，另两种一句话带过',
                 '`j` 要倒序枚举，否则同一个数会被选两次',
                 '`or_` 来自 `operator`（演示在 `setup` 里导入）；`ans` 达到 `mx` 时可提前返回'],
    ),
)
