WORDS = ["a", "b", "c", "ab", "bc", "abc"]


CONFIG = dict(
    num=2255, title='统计是给定字符串前缀的字符串数目', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='库函数 startswith',
    tags=[],
    code='''
class Solution:
    def countPrefixes(self, words: List[str], s: str) -> int:
        return sum(s.startswith(word) for word in words)
''',
    call='''Solution().countPrefixes(["a", "a"], "aa")
Solution().countPrefixes(%r, "abc")''' % (WORDS,),
    expect=3,
    views=[
        dict(type='string', var='s', label='s（被匹配的字符串）', cell=84, h=130),
        dict(type='array', var='words', label='words（绿 = 是 s 的前缀，灰 = 不是）', cell=96,
             color=lambda S, i, v: 'green' if S['s'].startswith(v) else None,
             dim=lambda S, i, v: not S['s'].startswith(v), h=170),
        dict(type='text', fn=lambda S: '`startswith` 逐个判断：' + '、'.join(
            f"`{w}`{'✓' if S['s'].startswith(w) else '✗'}" for w in S['words']) if 'words' in S else '', size=26, h=70),
        dict(type='text', fn=lambda S: f"是前缀的有 =={sum(S['s'].startswith(w) for w in S['words'])}== 个" if 'words' in S else '', size=34, h=70),
    ],
    watch=[('s', 's', 'blue'), ('n = len(words)', 'len(words)')],
    captions={
        'sum(s.startswith': lambda S, B, ret: (
            '`sum` 对每个 `word` 求 `s.startswith(word)`，`True` 当 1 加：是前缀的有 {} 个 → ==返回 {}==，重复的单词也各算一次'.format(ret, ret)
            if len(S.words) > 2 else
            '先看示例 2：`["a","a"]`，两个 `a` 都是 `"aa"` 的前缀，重复出现要计==多次== → 返回 `{}`'.format(ret)),
    },
    cards=dict(
        one_liner='库函数 startswith 判断前缀，是就计一个，求和',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['给字符串数组 `words` 和字符串 `s`，数出 `words` 里有多少个是 `s` 的==前缀==',
                 '相同的单词出现多次，要计多次',
                 '示例：`words = [a,b,c,ab,bc,abc]`，`s = "abc"` → `3`（a、ab、abc）'],
        quote='用库函数判断 words[i] 是否为 s 的前缀，是就把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['逐个枚举 `word`，`s.startswith(word)` 返回 `True` / `False`',
              '`True` 在 Python 里就是 `1`，所以直接 `sum(...)` 就是个数',
              '长度、字母的比较都由库函数完成，一行搞定'],
        after=[dict(heading='一行里发生了什么', lines=[
            '生成器表达式对每个 `word` 求一次 `s.startswith(word)`',
            '`startswith` 只比较 `s` 开头的 `len(word)` 个字符',
            '结果是 `True` / `False`，`sum` 把它们当 `1` / `0` 加起来'])],
        summary=['时间 `O(nm)`：`n = len(words)`，`m = len(s)`；空间 `O(1)`',
                 '`sum(布尔表达式 for ...)` 是 Python 计数的常用写法',
                 '注意是 `s.startswith(word)`，不是 `word.startswith(s)`，方向别写反',
                 '比 word 更长的串自然不是前缀，`startswith` 会自己返回 False'],
    ),
)
