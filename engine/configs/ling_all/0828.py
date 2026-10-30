S0 = 'BCADEAFGA'


def _delta(S):
    if 'last0' not in S or 'c' not in S or 'total' not in S or S.get('_line', 0) not in (6, 7):
        return '`total` = 以 `s[i]` 结尾的所有子串的唯一字符数之和；`ans` 累加每个 `total`'
    i, c = S['i'], S['c']
    a, b = S['last0'].get(c, -1), S['last1'].get(c, -1)
    return f'变化量 = `i − 2×last0 + last1` = `{i} − 2×({a}) + ({b})` = =={i - 2 * a + b}=='


def _col(S, k, v):
    c = S.get('c')
    if 'last0' not in S or c is None or S.get('_line', 0) not in (6, 7):
        return None
    if k == S['i']:
        return 'blue'
    if S['last0'].get(c, -1) == k and S['s'][k] == c:
        return 'cyan'
    if S['last1'].get(c, -1) == k and S['s'][k] == c:
        return 'orange'
    return None


CONFIG = dict(
    num=828, title='统计子串中的唯一字符', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子数组 DP · 按右端点分组 + 上一次/上上一次位置',
    tags=['灵神题单', '动态规划', '难度分 2034'],
    code='''
class Solution:
    def uniqueLetterString(self, s: str) -> int:
        ans = total = 0
        last0, last1 = {}, {}
        for i, c in enumerate(s):
            total += i - 2 * last0.get(c, -1) + last1.get(c, -1)
            ans += total
            last1[c] = last0.get(c, -1)
            last0[c] = i
        return ans
''',
    call=f'Solution().uniqueLetterString({S0!r})',
    expect=132,
    skip=['for i, c in enumerate'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前 i，青 = 上一次出现，橙 = 上上一次出现）', h=230, cell=90,
             pointers={'i': 'blue'}, color=_col),
        dict(type='map', var='last0', label='last0（上一次出现的下标）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=26),
        dict(type='map', var='last1', label='last1（上上一次出现的下标）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=26),
        dict(type='text', fn=_delta, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c'), ('total', 'total', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = total = 0': '`total`：以 `s[i]` 结尾的子串的 countUniqueChars 之和；`ans`：所有 `total` 之和',
        'last0, last1': '`last0[c]`、`last1[c]`：字母 `c` 上一次、上上一次出现的下标，没有就当 -1',
        'total +=': lambda S, B, r: (f'`s[{S.i}] = {S.c}` 接到以 `s[{S.i - 1}]` 结尾的子串后面，自己也单独成一个子串：'
                                     f'上一次在 {S.last0.get(S.c, -1)}、上上一次在 {S.last1.get(S.c, -1)}\n'
                                     f'增加 `{S.i} − ({S.last0.get(S.c, -1)})`，减少 `({S.last0.get(S.c, -1)}) − ({S.last1.get(S.c, -1)})`'
                                     f' → `total` = =={S.total}=='),
        'ans += total': '以 `s[{i}]` 结尾的子串都统计完了：`ans` += `{total}` → =={ans}==',
        'last1[c] =': '`c` 的上一次变成上上一次：`last1[{c!r}] = {last1[c]}`',
        'last0[c] = i': '记下这一次出现：`last0[{c!r}] = {i}`',
        'return ans': '所有子串的唯一字符数之和 = =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='按右端点分组：新字母只改变中间那一段子串的贡献',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['`countUniqueChars(t)` 统计 `t` 中只出现一次的字母个数',
                 '求 `s` 所有子串的该值之和（重复子串也要算）',
                 '示例：`"ABA"` → `8`；本视频：`"BCADEAFGA"` → `132`'],
        quote='以 s[i] 结尾的子串，可以看成是以 s[i-1] 结尾的子串，在末尾添加上 s[i] 组成。……上面这一串提示是思考子串统计类问题的通用技巧之一。',
        quote_src='—— 灵茶山艾府题解（提示 1-3）',
        idea=['新字母 `c` 接到旧子串后：没出现过的 ==+1==，恰好出现一次的 ==−1==，已重复的不变',
              '三段的分界就是 `last0[c]` 和 `last1[c]`，所以变化量 = `i − 2·last0 + last1`',
              '`total` 维护当前右端点的总和，每轮累加进 `ans`'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '易错：`s[i]` 自己单独成子串贡献 1，已包含在 `i − last0` 里',
                 '不存在的位置当 `-1`，公式不用特判',
                 '同类题：2262 字符串的总引力（只算出现过的种类）'],
    ),
)
