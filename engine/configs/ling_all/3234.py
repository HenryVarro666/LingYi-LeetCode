def _txt(S):
    if S.get('_line') in (22, 23, 24) and 'p' in S and 'cnt1' in S:
        c0, c1 = S['cnt0'], S['cnt1']
        lo, hi = S['p'] + 1, S['q'] - max(c0 * c0 - c1, 0)
        return (f'恰好 =={c0}== 个 0 的子串：最短 `[{S["q"]},{S["r"]}]` 有 {c1} 个 1，需要至少 `{c0}²={c0*c0}` 个 1；'
                f'合法左端点 `[{lo},{hi}]`' + (f' 共 =={max(hi - lo + 1, 0)}== 个' if True else ''))
    if 'r' in S:
        return f'右端点 `r = {S["r"]}`：`[0,r]` 里有 `{S.get("total1", 0)}` 个 1，`cnt0²` 超过它就停'
    return '右端点 `r` 从左到右；用 `pos0` 记下每个 0 的位置'


CONFIG = dict(
    num=3234, title='统计 1 显著的字符串的数量', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右端点 · 根号分治（0 的个数）',
    tags=['灵神题单·常用数据结构', '难度分 2557'],
    code='''
# 手写 max 更快
max = lambda a, b: b if b > a else a

class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        pos0 = [-1]  # 哨兵，方便处理 cnt0 达到最大时的计数
        total1 = 0  # [0,r] 中的 1 的个数
        ans = 0

        for r, ch in enumerate(s):
            if ch == '0':
                pos0.append(r)  # 记录 0 的下标
            else:
                total1 += 1
                ans += r - pos0[-1]  # 单独计算不含 0 的子串个数

            # 倒着遍历 pos0，就相当于在从小到大枚举 cnt0
            for i in range(len(pos0) - 1, 0, -1):
                cnt0 = len(pos0) - i
                if cnt0 * cnt0 > total1:
                    break
                p, q = pos0[i - 1], pos0[i]
                cnt1 = r - q + 1 - cnt0  # [q,r] 中的 1 的个数 = [q,r] 的长度 - cnt0
                ans += max(q - max(cnt0 * cnt0 - cnt1, 0) - p, 0)

        return ans
''',
    call='Solution().numberOfSubstrings("101101")',
    expect=16,
    views=[
        dict(type='string', var='s', label='s（黄 = 0 的位置，r = 当前右端点）', pointers={'r': 'blue'}, cell=90, h=200,
             color=lambda S, i, v: ('yellow' if 'pos0' in S and i in S['pos0'] and v == '0' else None)),
        dict(type='array', var='pos0', label='pos0（0 的下标，-1 是哨兵）', cell=80, h=170, color=lambda S, i, v: 'yellow'),
        dict(type='text', h=130, size=26, fn=_txt),
    ],
    watch=[('r', 'r', 'blue'), 'total1', 'cnt0', 'cnt1', ('p', 'p', 'pink'), ('q', 'q', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'pos0 = [-1]': '`pos0` 存每个 0 的下标；先放哨兵 `-1`，最左边的 0 之前也能算出左端点个数',
        'total1 = 0': '`total1`：`[0,r]` 里 1 的总数，用来判断 `cnt0²` 还可不可能达到',
        'ans = 0': '`ans` 统计 1 显著子串个数',
        'pos0.append': '遇到 0：记下下标 `{r}` → `pos0 = {pos0}`',
        'total1 += 1': '遇到 1：`total1 = {total1}`',
        'ans += r - pos0[-1]': '右端点 `{r}` 且不含 0 的子串：左端点 `{pos0[-1]+1} … {r}`，共 `{r} - {pos0[-1]}` = =={r - pos0[-1]}== 个；`ans = {ans}`',
        'for i in range': '倒着扫 `pos0`：从最近的 0 开始，相当于 `cnt0 = 1, 2, 3 …`',
        'cnt0 = len': '这次枚举 =={cnt0}== 个 0 的子串',
        'if cnt0 * cnt0': lambda S, B, r: (f'`cnt0² = {S.cnt0**2}` > `total1 = {S.total1}`：1 不够，更多 0 也不可能显著 → ==break==' if S.cnt0 ** 2 > S.total1
                                           else f'`cnt0² = {S.cnt0**2}` ≤ `total1 = {S.total1}`，还有可能，继续算'),
        'p, q = ': '`p = {p}`、`q = {q}`：`(p, q]` 内的左端点都恰好含 {cnt0} 个 0；`[q,r]` 是最短的这种子串',
        'cnt1 = r': '`[q,r]` 长 `{r}-{q}+1`，减去 0 的个数 → `cnt1` = =={cnt1}==',
        'ans += max(q': '还缺 `max({cnt0}² − {cnt1}, 0)` 个 1，左端点最大 `q − 缺口`，最小 `p+1` → 加 `max({q} − {max(cnt0*cnt0-cnt1,0)} − {p}, 0)` = =={ans - B.ans}==；`ans = {ans}`',
        'return ans': '全部右端点处理完，答案 `{ans}`',
    },
    skip=['for i in range'],
    max_steps=110,
    cards=dict(
        one_liner='1 显著子串至多 √n 个 0：枚举右端点，再枚举 0 的个数',
        complexity='时间 `O(n√n)`，空间 `O(n)`',
        problem=['二进制字符串 `s`，子串里 1 的个数 ≥ 0 的个数的平方，就是 1 显著',
                 '求 1 显著子串的数量，`n ≤ 4×10⁴`',
                 '本视频：`s = "101101"` → `16`（共 21 个子串，5 个不显著）'],
        quote='1 显著子串**至多**有 √n 个 0。枚举子串右端点，分别计算恰好有 0 个 0、1 个 0、2 个 0 …… 的子串有多少个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt0² ≤ cnt1 ≤ n`，所以 `cnt0 ≤ √n`，内层最多枚举 √n 次',
              '固定右端点和 0 的个数，左端点落在两个 0 之间的一段区间；越靠左 1 越多',
              '算出“刚好够 1”的最大左端点，区间长度就是个数'],
        summary=['时间 `O(n√n)`，空间 `O(n)`（用队列只留最近 √n 个 0 可降到 `O(√n)`）',
                 '易错：哨兵 `-1` 让最左边的 0 也能算左端点；个数可能为负要与 0 取 max',
                 '不含 0 的子串单独在遇到 1 时统计：`r - pos0[-1]`',
                 '`max` 手写成 lambda 只是为了更快；同类：根号分治 / 枚举右维护左'],
    ),
)
