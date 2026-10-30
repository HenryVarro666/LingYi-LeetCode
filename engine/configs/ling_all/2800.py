def _line1(S):
    I = S['_inner']
    if 't' in I and 's' in I and I is not S and 'a' not in I:
        i = I.get('i')
        s, t = I['s'], I['t']
        if i is not None:
            return f"s 的后 {i} 个 `{s[-i:]}` vs t 的前 {i} 个 `{t[:i]}`"
        return f"合并 `s = {s}`、`t = {t}`"
    return f"排列 `({S.get('a','')}, {S.get('b','')}, {S.get('c','')})`　`ans = {S.get('ans','')!r}`"


CONFIG = dict(
    num=2800, title='包含三个字符串的最短字符串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='枚举排列 · 两两合并（最大重叠）',
    tags=['灵神题单·字符串', 'KMP'],
    code='''
class Solution:
    def minimumString(self, a: str, b: str, c: str) -> str:
        def merge(s: str, t: str) -> str:
            # 先特判完全包含的情况
            if t in s: return s
            if s in t: return t
            for i in range(min(len(s), len(t)), 0, -1):
                # 枚举：s 的后 i 个字母和 t 的前 i 个字母是一样的
                if s[-i:] == t[:i]:
                    return s + t[i:]
            return s + t

        ans = ""
        for a, b, c in permutations((a, b, c)):
            s = merge(merge(a, b), c)
            if ans == "" or len(s) < len(ans) or len(s) == len(ans) and s < ans:
                ans = s
        return ans
''',
    call='Solution().minimumString("ab", "ba", "aba")',
    expect='aba',
    views=[
        dict(type='text', fn=_line1, size=28, h=70),
        dict(type='string', var=lambda S: S['_inner'].get('s', S.get('s', '')), label='合并中的 s（左）', cell=60, h=150),
        dict(type='string', var=lambda S: S['_inner'].get('t', ''), label='t（右）', cell=60, h=150),
        dict(type='string', var=lambda S: S.get('ans', ''), label='ans（目前最优）', cell=60, h=150,
             color=lambda S, i, v: 'green'),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c', 'cyan'), ('s', 's'), ('ans', 'ans', 'green')],
    captions={
        'if t in s': lambda S, B, r: (f"`t = {S.t!r}` 在 `s = {S.s!r}` 里 → ==完全包含==，直接用 s" if S.t in S.s
                                      else f"`{S.t}` 不在 `{S.s}` 里，没有被 s 包含"),
        'if s in t': lambda S, B, r: (f"`s = {S.s!r}` 在 `t = {S.t!r}` 里 → ==完全包含==，直接用 t" if S.s in S.t
                                      else f"`{S.s}` 不在 `{S.t}` 里，没有被 t 包含"),
        'for i in range(min': '从最长的重叠开始枚举：`i = {i}`',
        'if s[-i:] == t[:i]': lambda S, B, r: (
            f"s 的后 {S.i} 个 `{S.s[-S.i:]}` == t 的前 {S.i} 个 `{S.t[:S.i]}` → ==最大重叠 {S.i}=="
            if S.s[-S.i:] == S.t[:S.i] else f"s 的后 {S.i} 个 `{S.s[-S.i:]}` ≠ t 的前 {S.i} 个 `{S.t[:S.i]}`，缩短重叠"),
        'return s + t[i:]': '重叠 `{i}` 个字母，只需拼上 t 去掉前缀的部分 → `{ret}`',
        'return s + t\n': '没有任何重叠，直接拼接 → `{ret}`',
        'return s\n': '合并结果就是 `{ret}`',
        'return t\n': '合并结果就是 `{ret}`',
        'ans = ""': '`ans` 保存目前最短且字典序最小的答案',
        'for a, b, c in permutations': '枚举排列：`({a}, {b}, {c})`',
        's = merge(merge(a, b), c)': '先合并前两个，再把结果与第三个合并，得到这个排列的最短串 `s`',
        'if ans == ""': lambda S, B, r: (
            f"`ans` 为空 → 直接采用 `{S.s}`" if S.ans == '' else
            f"`len(s) = {len(S.s)}` vs `len(ans) = {len(S.ans)}`" + (
                "：更短 → ==更新==" if len(S.s) < len(S.ans) else
                (f"：一样长，比字典序 `{S.s}` vs `{S.ans}` → " + ('==更新==' if S.s < S.ans else '没有更小，不更新') if len(S.s) == len(S.ans)
                 else "：更长，不要"))),
        'ans = s': '`ans` 更新为 `{ans}`',
        'return ans': '六种排列都试过 → 答案 `{ans}`',
    },
    skip=[],
    max_steps=110,
    cards=dict(
        one_liner='枚举三个串的顺序，两两合并时取最大重叠',
        complexity='时间 `O(n^2)`，空间 `O(n)`，`n` 为串长最大值',
        problem=['找一个最短的字符串，使 `a`、`b`、`c` 都是它的子串；有多个就取字典序最小',
                 '示例：`a="abc"`，`b="bca"`，`c="aaa"` → `"aaabca"`',
                 '本视频：`a="ab"`，`b="ba"`，`c="aba"` → `"aba"`'],
        quote='暴力枚举 a,b,c 的全排列 a′,b′,c′，然后合并 a′,b′ 得到最短字符串 x，再合并 x,c′ 得到最短字符串 s。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`merge(s, t)`：先判断完全包含；否则枚举 s 的后缀等于 t 的前缀的最大长度 `i`',
              '没有完全包含时，合并得越短越好，所以重叠取最大',
              '6 种排列各合并一次，取最短且字典序最小的 `s`'],
        summary=['时间 `O(n^2)`（切片比较 `O(n)`，重叠枚举 `O(n)`），空间 `O(n)`',
                 '易错：必须先特判完全包含，否则会多拼多余的字母',
                 '只枚举顺序、每次取最大重叠，字典序最小靠最后逐个比较',
                 '合并重叠用 KMP 可降到线性，本题数据小，暴力足够'],
    ),
)
