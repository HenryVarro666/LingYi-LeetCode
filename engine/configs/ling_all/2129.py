def _rule(w):
    return w.title() if len(w) > 2 else w.lower()


def _words(S):
    t = S.get('title')
    if not t:
        return ''
    return '  '.join(f"`{w}`({len(w)})→=={_rule(w)}==" for w in t.split())


CONFIG = dict(
    num=2129, title='将标题首字母大写', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='split + title/lower + join',
    tags=[],
    code='''
class Solution:
    def capitalizeTitle(self, title: str) -> str:
        f = lambda s: s.title() if len(s) > 2 else s.lower()
        return ' '.join(map(f, title.split()))
''',
    call='Solution().capitalizeTitle("i lOve leetcode")',
    expect='i Love Leetcode',
    views=[
        dict(type='string', var='title', label='title（原始输入）', cell=40, h=190),
        dict(type='text', fn=lambda S: '按空格分词，逐词套规则：', size=26),
        dict(type='text', fn=_words, size=26, h=150),
        dict(type='text', fn=lambda S: '规则：长度 `> 2` → `s.title()`（首字母大写、其余小写）；否则 `s.lower()`', size=24),
    ],
    watch=[('title', 'title', 'blue')],
    captions={
        'f = lambda': '定义 `f`：词长 `> 2` 用 `title()`（首字母大写，其余小写），否则全部 `lower()`',
        "return ' '.join": lambda S, B, ret: f'`title.split()` 按空格分出 `{len(S.title.split())}` 个词，`map(f, …)` 逐个处理，再用单个空格拼回：=={ret}==',
    },
    cards=dict(
        one_liner='分词、按长度套规则、再拼回去，一行搞定',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`title` 由单个空格隔开的若干单词组成',
                 '单词长度为 1 或 2：全部小写；否则==首字母大写、其余小写==',
                 '示例：`"First leTTeR of EACH Word"` → `"First Letter of Each Word"`',
                 '本视频：`"i lOve leetcode"` → `"i Love Leetcode"`'],
        quote='用空格分割 title，得到所有单词。对于每个单词，如果长度大于 2，将其首字母转成大写，其余字母转成小写；如果长度小于等于 2，将所有字母转成小写。把所有单词用单个空格拼接。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`split()` 得到单词，`map(f, …)` 对每个单词应用规则',
              '`str.title()` 恰好是“首字母大写、其余小写”，单词只含字母，直接可用',
              '`" ".join(…)` 用单个空格拼回去'],
        after=[dict(heading='逐词套规则', lines=[
            '`i`(1) → 长度 ≤ 2 → `lower()` → `i`（单个字母也要小写）',
            '`lOve`(4) → 长度 > 2 → `title()` → `Love`',
            '`leetcode`(8) → `title()` → `Leetcode`',
            '3 个结果用 `" ".join` 拼回：`i Love Leetcode`；另：长度恰为 2 也全小写'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：长度 ==等于 2== 也要全小写，判断是 `len(s) > 2`',
                 '`title()` 只适合纯字母单词；有撇号等字符时会出错',
                 '引擎里 `map` 是惰性的，`join` 时才真正调用 `f`'],
    ),
)
