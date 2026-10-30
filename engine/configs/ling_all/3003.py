def _L(m):
    return ''.join(chr(97 + b) for b in range(26) if m >> b & 1) or '∅'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    n = len(s)
    suf = S.get('suf')
    cell = min(110, (x1 - x0 - 150) / n)
    sx = x0 + 120
    cv.text((x0 + 10, y0 + 6), '字符串 s 与每个后缀（从右往左分割）的结果', 24, T['muted'], bold=True)
    rows = [('s', y0 + 60), ('suf 段数', y0 + 150), ('末段集合', y0 + 220)]
    for name, y in rows:
        cv.text((x0 + 10, y + 24), name, 22, T['muted'], anchor='lm', bold=True)
    cur = S.get('i')
    in_second = 'ans' in S
    for c in range(n + 1):
        X = sx + c * cell
        if c < n:
            hl = (cur == c)
            cv.rect((X + 2, rows[0][1], X + cell - 2, rows[0][1] + 56), fill=T['blue'] if hl else (60, 66, 76), r=8)
            cv.text((X + cell / 2, rows[0][1] + 28), s[c], 32, T['bg'] if hl else T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, rows[0][1] + 62), c, 18, T['dim'], anchor='mt', mono=True)
        e = suf[c] if suf is not None and c <= n and suf[c] is not None else None
        label = f'suf[{c}]' if c == n else None
        if e is not None:
            use = in_second and cur is not None and c == cur + 1
            fill = T['yellow'] if use else (50, 56, 66)
            fg = T['bg'] if use else T['text']
            cv.rect((X + 2, rows[1][1], X + cell - 2, rows[1][1] + 56), fill=fill, r=8)
            cv.text((X + cell / 2, rows[1][1] + 28), e[0], 30, fg, anchor='mm', bold=True)
            cv.rect((X + 2, rows[2][1], X + cell - 2, rows[2][1] + 56), fill=fill, r=8)
            cv.text((X + cell / 2, rows[2][1] + 28), _L(e[1]), 24, fg, anchor='mm', bold=True, mono=True)
    # 当前扫描方向
    if cur is not None and 0 <= cur < n:
        X = sx + cur * cell + cell / 2
        cv.tri_up(X, rows[2][1] + 90, 10, T['blue'])
        cv.text((X, rows[2][1] + 104), 'i', 22, T['blue'], anchor='mt', bold=True)
    cv.text((x0 + 10, rows[2][1] + 150),
            ('第二遍：从左往右，左边 = 前缀状态 (seg, mask)，右边 = 黄色 suf[i+1]' if in_second
             else '第一遍：从右往左，把每个后缀的 (段数, 末段字母集合) 记进 suf'), 22, T['cyan'], bold=True)


def _info(S):
    if 'ans' not in S or S.get('i') is None:
        return f"当前段：段数 ==seg={S.get('seg')}==，字母集合 `{_L(S.get('mask', 0))}`，种类 `size={S.get('size')}`"
    return (f"修改 `s[{S['i']}]`：左 `preSeg={S['seg']}`，集合 `{_L(S['mask'])}`；"
            f"右 `sufSeg={S['suf'][S['i'] + 1][0]}`，集合 `{_L(S['suf'][S['i'] + 1][1])}`")


CONFIG = dict(
    num=3003, title='执行操作后的最大分割数量', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 + 分类讨论',
    tags=['其他线性 DP', '多维 DP', '难度分 3039'],
    code='''
class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        if k == 26:
            return 1

        seg, mask, size = 1, 0, 0
        def update(i: int) -> None:
            nonlocal seg, mask, size
            bit = 1 << (ord(s[i]) - ord('a'))
            if mask & bit:  # s[i] 已经在当前这一段中，无影响
                return
            size += 1
            if size > k:
                seg += 1  # s[i] 在新的一段中
                mask = bit
                size = 1
            else:
                mask |= bit

        n = len(s)
        suf = [None] * n + [(0, 0)]
        for i in range(n - 1, -1, -1):
            update(i)
            suf[i] = (seg, mask)

        ans = seg  # 不修改任何字母
        seg, mask, size = 1, 0, 0
        for i in range(n):
            suf_seg, suf_mask = suf[i + 1]
            res = seg + suf_seg  # 情况 3
            union_size = (mask | suf_mask).bit_count()
            if union_size < k:
                res -= 1  # 情况 1
            elif union_size < 26 and size == k and suf_mask.bit_count() == k:
                res += 1  # 情况 2
            ans = max(ans, res)
            update(i)
        return ans
''',
    call='Solution().maxPartitionsAfterOperations("accca", 2)',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('seg', 'seg', 'blue'), ('mask', lambda S: _L(S['mask']) if 'mask' in S else '', 'cyan'), ('size', 'size', 'pink'),
           ('res', lambda S: S.get('res', ''), 'yellow'), ('ans', lambda S: S.get('ans', ''), 'green')],
    captions={
        'if k == 26': '`k = 26`：字母表只有 26 个，怎么改都凑不出第 27 种 → 永远一段',
        'seg, mask, size = 1, 0, 0': '重置：从空段开始，`seg = 1`（当前段算一段），`mask` 空，`size = 0`',
        'bit = 1 <<': '`s[{i}] = {s[i]}` 对应一个二进制位 `bit`，集合用位掩码表示',
        'if mask & bit': lambda S, B, r: (f'`{S.s[S.i]}` 已在当前段里 → 种类数不变，直接返回' if B.get('mask', 0) & S.bit
                                           else f'`{S.s[S.i]}` 不在当前段里 → 要把它加进去'),
        'size += 1': '新字母 → 种类数 `size = {size}`，和 `k = {k}` 比大小',
        'if size > k': lambda S, B, r: (f'`size = {S.size} > k = {S.k}`：超出，必须在这里切一刀' if S.size > S.k
                                         else f'`size = {S.size} ≤ k = {S.k}`：还能装下，并入当前段'),
        'seg += 1': '切出新的一段：`seg = {seg}`，`s[{i}]` 是新段的第一个字母',
        'mask = bit': '新段的集合只含 `s[{i}]`',
        'size = 1': '新段种类数重置为 1',
        'mask |= bit': '并入当前段：集合 = `{_L(mask)}`',
        'suf[i] = (seg, mask)': '记下后缀 `s[{i}:]` 的结果：==段数 {seg}==，末段集合 `{_L(mask)}`',
        'ans = seg': '不修改任何字母时的段数 `{seg}`，作为答案的起点',
        'suf_seg, suf_mask = suf[i + 1]': '假设修改 `s[{i}]`：右边已分好 `suf[{i + 1}]` = ({suf_seg} 段，末段 `{_L(suf_mask)}`)',
        'res = seg + suf_seg': '先按情况 3（总段数不变）：`{seg} + {suf_seg}` = =={res}==',
        'union_size =': '左末段与右首段（按从右往左的末段）的字母并集大小 = ==`{union_size}`==',
        'if union_size < k': lambda S, B, r: (f'`{S.union_size} < {S.k}`：无论改成什么字母，并集都不超过 k → 左右两段被迫合并（情况 1）'
                                              if S.union_size < S.k else f'`{S.union_size} ≥ {S.k}`：不是情况 1'),
        'elif union_size < 26': lambda S, B, r: (f'并集 {S.union_size} < 26，且 `size = k`、右段也满 k 种 → 改成两边都没有的字母，左右各自切满，多出一段（情况 2）'
                                                 if (S.union_size < 26 and S.size == S.k and S.suf_mask.bit_count() == S.k)
                                                 else '条件不满足（需左右两段都恰好有 k 种、且还有空闲字母）→ 总段数不变（情况 3）'),
        'res -= 1': '情况 1：左右合并成一段，`res = {res}`',
        'res += 1': '情况 2：多出一段，`res = {res}`',
        'ans = max(ans, res)': '`ans = max({B.ans}, {res}) = {ans}`',
        'return ans': '修改哪个位置最划算都试过了，答案 `{ans}`',
    },
    skip=[9, 11, 15, 16, 22, 23, 28, 37],
    max_steps=90,
    cards=dict(
        one_liner='枚举修改哪个位置：左边前缀 + 右边后缀，分三种情况',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次取至多含 `k` 种字母的最长前缀删掉，得到的段数就是分割数',
                 '最多可以把一个字母改成别的小写字母，求最大段数',
                 '示例：`s = "accca"`，`k = 2` → `3`（把 `s[2]` 改成 `b`）'],
        quote='对于 s 的任意后缀，从左到右分割出的段数，等于从右到左分割出的段数。',
        quote_src='—— 灵茶山艾府题解（方法二：前后缀分解）',
        idea=['枚举改 `s[i]`：前缀 `[0,i-1]`、后缀 `[i+1,n-1]` 都不能再改，可以独立算段数',
              '后缀从右往左分，段数不变 → 先预处理 `suf[i]`，再从左往右扫前缀',
              '合并左末段与右首段：并集 `< k` 要少一段；两边都满 k 且有空字母可用要多一段；否则不变'],
        summary=['时间 `O(n)`，空间 `O(n)`；方法一是记忆化搜索 `dfs(i, mask, changed)`，状态数 `O(nk|Σ|)`，这里选 `O(n)` 的前后缀分解',
                 '易错点：`k == 26` 要特判返回 1',
                 '「从右往左的段数 = 从左往右的段数」是前后缀分解成立的关键定理',
                 '`bit_count()` 需要 Python 3.10+',
                 '同类：前后缀分解 + 位运算分类讨论'],
    ),
)
