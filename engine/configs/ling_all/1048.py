def _top(S):
    if 's' not in S or 'i' not in S or S['_line'] not in (7, 8):
        return '先按长度排序，再从短到长递推：`f[s]` = 以 s 结尾的最长词链' if 's' not in S else (f"当前处理 `{S['s']}`" if S['_line'] != 10 else '答案 = `max(f.values())`')
    s, i = S['s'], S['i']
    if i >= len(s):
        return f"`{s}` 的每个删法都试过了"
    t = s[:i] + s[i + 1:]
    ok = t in S['f']
    return f"`{s}` 去掉 `s[{i}]='{s[i]}'` → `{t or '空串'}`，" + (f"在 f 中，链长 =={S['f'][t]}==" if ok else '不在 f 中，记 0')


def _col(S, k, v):
    if 's' in S and 'words' in S and v == S['s']:
        return 'blue'
    return None


CONFIG = dict(
    num=1048, title='最长字符串链', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='按长度排序 · 哈希表递推',
    tags=['灵神题单', '难度分 1599'],
    code='''
class Solution:
    def longestStrChain(self, words: List[str]) -> int:
        words.sort(key=len)
        f = {}  # 不要用 defaultdict，这会在字符串不存在的时候插入字符串
        for s in words:
            res = 0
            for i in range(len(s)):  # 枚举去掉 s[i]
                res = max(res, f.get(s[:i] + s[i + 1:], 0))
            f[s] = res + 1
        return max(f.values())
''',
    call='Solution().longestStrChain(["bdca","a","bca","b","ba","bda"])',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=28, h=90),
        dict(type='array', var='words', label='words（已按长度排序，蓝 = 当前 s）', cell=120, h=170, color=_col),
        dict(type='map', var='f', label='f[s]：以 s 结尾的最长词链长度', fmt=lambda k, v: f"'{k}': {v}", h=260, font=34),
    ],
    watch=[('s', 's', 'blue'), ('i', 'i', 'pink'), ('res', 'res', 'yellow')],
    captions={
        'words.sort': '短的只能接在长的前面：先按长度排序，保证算 `s` 时，它的所有「前身」都已算好',
        'f = {}': '`f[s]` 表示以 `s` 结尾的词链最长长度',
        'for s in words': lambda S, B, r: ('words 都处理完了，循环结束' if S.s in S.f else f'处理 `s = "{S.s}"`，从最短的往长的算'),
        'res = 0': '`res` 记录「前身」里最长的链，初始为 0',
        'for i in range': lambda S, B, r: ('每个位置都试过了，进入 `f[s] = res + 1`' if 'i' in B and B.get('s') == S.s and B['i'] == S.i and 'res' in B and B['_line'] != 6 else '枚举去掉 `s[%d]`' % S.i),
        'res = max': '前身 `{s[:i] + s[i + 1:] or "空串"}` 的链长是 `{f.get(s[:i] + s[i + 1:], 0)}`（不在 words 里就是 0）→ `res = {res}`',
        'f[s] = res': '`f["{s}"] = res + 1 = {f[s]}`：最长前身再接上自己',
        'return max': '答案是所有 `f[s]` 的最大值 `{ret}`',
    },
    cards=dict(
        one_liner='删掉一个字母找前身，按长度从短到长递推',
        complexity='时间 `O(nlogn + nL²)`，空间 `O(nL)`',
        problem=['在 `word_A` 任意位置插入一个字母得到 `word_B`，则 A 是 B 的==前身==',
                 '从 `words` 中选单词组成词链，每个都是下一个的前身，求最长长度',
                 '示例：`["a","b","ba","bca","bda","bdca"]` → `4`'],
        quote='对于字符串 s 来说，假设它是词链的最后一个单词，那么去掉 s 中的一个字母，设新字符串为 t，问题就变成计算以 t 结尾的词链的最长长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(s)` 是「以 s 结尾的最长词链」，去掉一个字母得到 `t`，`t` 在 words 中就转移',
              '记忆化搜索 1:1 翻译成递推：先按长度排序，从短到长算',
              '本视频演示递推写法，`f` 用普通 dict 存'],
        summary=['时间 `O(nlogn + nL²)`：状态 `n` 个，每个枚举删字母并拼接 `O(L²)`',
                 '`f` 不要用 `defaultdict`：`f.get(t, 0)` 不会把不存在的串插进去',
                 '排序只需按 `len` 排；同长度之间不能互相转移',
                 '另一种写法：`@cache` 记忆化搜索 `dfs(s)`，和递推一一对应'],
    ),
)
