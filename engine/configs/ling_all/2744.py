WORDS = ["cd", "ac", "dc", "ca", "zz"]

CONFIG = dict(
    num=2744, title='最大字符串配对数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合 · 边遍历边配对',
    code='''
class Solution:
    def maximumNumberOfStringPairs(self, words: List[str]) -> int:
        ans = 0
        seen = set()
        for s in words:
            if s[::-1] in seen:
                ans += 1  # s 和 seen 中的 s[::-1] 匹配
            else:
                seen.add(s)
        return ans
''',
    call=f'Solution().maximumNumberOfStringPairs({WORDS})',
    expect=2,
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前 s，绿 = 已配对）', cell=110, h=220,
             pointers={'words.index(s)': 'blue'},
             color=lambda S, i, v: 'green' if 's' in S and i < S['words'].index(S['s']) and v not in S['seen'] else None),
        dict(type='set', var='seen', label='seen（已遇到、还没配对的字符串）', fmt=lambda x: repr(x), h=170, font=34),
        dict(type='text', h=90, size=30, fn=lambda S: f"`s = {S['s']!r}`，反转 `{S['s'][::-1]!r}`" if 's' in S else ''),
    ],
    watch=[('s', 's', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录配对数',
        'seen = set()': '`seen` 存已遍历过的字符串，用来 `O(1)` 查反转串',
        'for s in words': lambda S, B, r: ('遍历结束' if 's' in B and B.s == S.s and S.ans + len(S.seen) == len(S.words) else f'取出 `s = {S.s!r}`，它反转后是 `{S.s[::-1]!r}`'),
        'if s[::-1] in seen': lambda S, B, r: (f'`{S.s[::-1]!r}` 在 seen 里 → 前面有字符串和 `{S.s!r}` 互为反转，==配对成功==' if S.s[::-1] in S.seen
                                               else f'`{S.s[::-1]!r}` 不在 seen 里 → 前面没有能配的，先存起来等后面'),
        'ans += 1': '配对 +1：`ans = {ans}`（字符串互不相同，所以这个配对唯一）',
        'seen.add(s)': '把 `{s!r}` 放进 seen，留给后面的反转串来匹配 → `{sorted(seen)}`',
        'return ans': '最多配对 `{ans}` 对',
    },
    cards=dict(
        one_liner='边遍历边查：反转串之前出现过就配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`words` 里每个字符串长为 2、互不相同',
                 '`words[i]` 等于 `words[j]` 的反转（`i < j`）就能配对，每个串最多配一次',
                 '示例：`["cd","ac","dc","ca","zz"]` → `2`'],
        quote='如果在 s 之前，已经遇到 s 反转后的字符串，那么就找到了一个匹配。由于题目保证 words 中的字符串互不相同，这个匹配是唯一的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历到 `s`，只需看==前面==有没有它的反转串',
              '有 → 答案 +1，而且不必入集合（已经用掉了）',
              '没有 → 把 `s` 加入 `seen`，等后面的串来配'],
        summary=['时间 `O(n)`，字符串长度视作常数；空间 `O(n)`',
                 '配对成功时 `s` 不入 `seen`，保证每个串只用一次',
                 '前提是字符串互不相同；思考题：有重复串时可改用计数哈希表',
                 '`s[::-1]` 是 Python 反转字符串的写法'],
    ),
)
