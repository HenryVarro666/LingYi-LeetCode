def _col(S, i, v):
    return 'green' if S.get('x') is not None and 'i' in S and i in S.get('_hit', ()) else None


CONFIG = dict(
    num=2942, title='查找包含给定字符的单词', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='列表推导式 · x in s',
    code='''
class Solution:
    def findWordsContaining(self, words: List[str], x: str) -> List[int]:
        return [i for i, s in enumerate(words) if x in s]
''',
    call='Solution().findWordsContaining(["abc","bcd","aaaa","cbc"], "a")',
    expect=[0, 2],
    views=[
        dict(type='array', var='words', label='words', pointers={'i': 'blue'}, cell=170,
             color=lambda S, i, v: 'green' if S['x'] in v else None, h=260),
        dict(type='text', fn=lambda S: f"要找的字符 `x` = =='{S['x']}'==；包含它的单词标成绿色", h=80),
    ],
    watch=['x', 'i', 's'],
    captions={
        'return [i for': lambda S, B, r: f"枚举每个 `(i, s)`，`x in s` 成立就把 `i` 收进答案，最终得到 ==`{r}`==",
    },
    cards=dict(
        before=[dict(heading='先手算一遍', lines=['`words = ["abc","bcd","aaaa","cbc"]`，`x = "a"`',
                     '`"abc"` 含 `a` → 收下标 `0`；`"bcd"` 没有 → 跳过', '`"aaaa"` 含 `a` → 收下标 `2`；`"cbc"` 没有 → 跳过',
                     '答案 `[0, 2]`']),],
        after=[dict(heading='为什么不用写 if', lines=['列表推导式的末尾 `if x in s` 就是过滤条件', '等价于 `for` + `if` + `append` 三行',
                    '`x in s` 对字符串是子串判断，`x` 只有一个字母时就是「是否出现」']),],
        one_liner='逐个单词看 x 在不在里面',
        complexity='时间 `O(L)`，空间 `O(1)`（返回值不计）',
        problem=['给字符串数组 `words` 和字符 `x`，返回包含 `x` 的单词的下标，顺序任意',
                 '示例：`["abc","bcd","aaaa","cbc"]`，`x = "a"` → `[0,2]`'],
        quote='遍历 words，判断 x 是否在 words[i] 中，如果是则把 i 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`enumerate` 同时拿到下标 `i` 和单词 `s`', '`x in s` 判断子串，成立就保留 `i`',
              '一行列表推导式写完'],
        summary=['时间 `O(L)`，L 为所有单词长度之和；空间 `O(1)`',
                 '答案按下标升序，满足「任意顺序」要求',
                 '一个字符也能用 `in` 判断，不用手写循环'],
    ),
)
