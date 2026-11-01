def _sa(w):
    # 后缀数组：等价于 Go 的 suffixarray.New(w) 里的 sa
    return sorted(range(len(w)), key=lambda i: w[i:])


def _top(S):
    if 's' not in S or 'rank' not in S or 'i' not in S:
        return ''
    s, t = S['s'], S['t']
    if not s or not t:
        return '有一个字符串空了，另一个直接接上'
    return f"s 剩 `{s}`（rank {S['rank'][S['i']]}）　t 剩 `{t}`（rank {S['rank'][S['j']]}）"


CONFIG = dict(
    num=1754, title='构造字典序最大的合并字符串', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='后缀数组 rank 代替字符串比较（Go 原文转写）',
    tags=['贪心与思维', '字符串', '难度分 1829'],
    setup='''
def suffix_array(w):
    return sorted(range(len(w)), key=lambda i: w[i:])
''',
    code='''
class Solution:
    def largestMerge(self, s: str, t: str) -> str:
        n = len(s)
        sa = suffix_array(s + "#" + t)
        rank = [0] * (n + 1 + len(t))
        for i in range(len(rank)):
            rank[sa[i]] = i
        ans = []
        i, j = 0, n + 1
        while True:
            if s == "":
                ans += t
                break
            if t == "":
                ans += s
                break
            if rank[i] > rank[j]:  # s > t
                ans.append(s[0])
                s = s[1:]
                i += 1
            else:
                ans.append(t[0])
                t = t[1:]
                j += 1
        return "".join(ans)
''',
    call='Solution().largestMerge("caba", "bcaa")',
    expect='cbcabaaa',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s 剩余', cell=70, color=lambda S, k, v: 'blue' if k == 0 else None),
        dict(type='string', var='t', label='t 剩余', cell=70, color=lambda S, k, v: 'pink' if k == 0 else None),
        dict(type='array', var='ans', label='ans（已合并的结果）', cell=70, color=lambda S, k, v: 'green'),
        dict(type='array', var='rank', label='rank[i]：后缀 w[i:] 的字典序名次（w = s + "#" + t）', cell=60,
             pointers={'i': 'blue', 'j': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'blue'), ('t', 't', 'pink')],
    captions={
        'sa = suffix_array': '把 `s + "#" + t` 的所有后缀按字典序排好 → `sa`；`#` 比小写字母小，隔开两串',
        'rank = [0]': '`rank` 用来替代“整段字符串比较”，长度 = `n + 1 + len(t)`',
        'rank[sa[i]] = i': '`rank[{sa[i]}] = {i}`：下标 `sa[i]` 开头的后缀排第 `{i}` 名',
        'i, j = 0, n + 1': '`i` 指向 s 的起点，`j = n + 1` 指向 t 的起点（跳过 `#`）',
        'if s == ""': lambda S, B, r: '`s` 空了 → 只剩 t，整段接上' if S.s == '' else '`s` 还有字符',
        'ans += t': '`s` 已取完，把剩下的 `t = "{t}"` 全接到 `ans`',
        'if t == ""': lambda S, B, r: '`t` 空了 → 只剩 s，整段接上' if S.t == '' else '`t` 还有字符',
        'ans += s': '`t` 已取完，把剩下的 `s = "{s}"` 全接到 `ans`',
        'if rank[i] > rank[j]': lambda S, B, r: (f'`rank[{S.i}] = {S.rank[S.i]}` > `rank[{S.j}] = {S.rank[S.j]}`：'
                                                   '==s 的后缀更大== → 取 s 的首字符' if S.rank[S.i] > S.rank[S.j] else
                                                   f'`rank[{S.i}] = {S.rank[S.i]}` < `rank[{S.j}] = {S.rank[S.j]}`：'
                                                   '==t 的后缀更大== → 取 t 的首字符'),
        'ans.append(s[0])': '取 s 的首字符 `{s[0]}` 放进 `ans` → `{"".join(ans)}`',
        'ans.append(t[0])': '取 t 的首字符 `{t[0]}` 放进 `ans` → `{"".join(ans)}`',
        's = s[1:]': '`s` 去掉首字符，剩 `"{s}"`',
        't = t[1:]': '`t` 去掉首字符，剩 `"{t}"`',
        'i += 1': '`i` 右移到 {i}，rank 不用重算',
        'j += 1': '`j` 右移到 {j}，rank 不用重算',
        'return': '合并完成，返回 `"{ret}"`',
    },
    cards=dict(
        one_liner='每步取“后缀更大”的那个串的首字符，比较用 rank 一步完成',
        complexity='时间 `O(n log n)` 或线性（取决于后缀数组），空间 `O(n)`',
        problem=['把 `word1`、`word2` 每次取一个串的首字符拼成 `merge`，求字典序==最大==的 `merge`',
                 '示例：`"cabaa"`、`"bcaaa"` → `"cbcabaaaaa"`',
                 '本视频：`"caba"`、`"bcaa"` → `"cbcabaaa"`'],
        quote='利用 rank 数组来代替原来的字符串比较逻辑，从而做到线性复杂度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：谁的剩余后缀更大，就先取谁的首字符',
              '朴素做法每次直接比较两个后缀，最坏要 `O(n)`',
              '把 `s + "#" + t` 的后缀数组求出来，`rank` 一查就知道谁大'],
        result='每一步都取后缀更大的串，得到 `"cbcabaaa"` ✓',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Go 里用 unsafe 反射取标准库后缀数组 `sa`，Python 没有，用 `suffix_array` 排序后缀等价代替（视频里不追踪）',
                 '`#` 比小写字母小，用来隔开两个串，避免后缀比较串到另一边',
                 '易错：比较的是==整个剩余后缀==，不是只看首字符；首字符相同时要继续往后比',
                 '时间取决于求后缀数组：`O(n log n)`～`O(n)`，空间 `O(n)`'],
    ),
)
