CONFIG = dict(
    num=1684, title='统计一致字符串的数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希集合 · 逐字符检查',
    code='''
class Solution(object):
    def countConsistentStrings(self, allowed, words):

        allowed_set = set()
        for char in allowed:
            allowed_set.add(char)
        
        res = len(words)
        for word in words:
            for char in word:
                if char not in allowed_set:
                    res -= 1
                    break
        
        return res
''',
    call="Solution().countConsistentStrings('ab', ['ad', 'bd', 'aaab', 'baa', 'badab'])",
    expect=2,
    views=[
        dict(type='set', var='allowed_set', h=130, label='allowed_set（允许的字符）', fmt=lambda x: str(x)),
        dict(type='array', var='words', h=170, label='words', pointers={}, color=lambda S, i, v: ('blue' if 'word' in S and S['word'] == v and S.get('_line') else None)),
        dict(type='string', var=lambda S: S.get('word', ''), h=170, label='当前单词 word', pointers={}, color=lambda S, i, v: ('red' if S.get('char') == v and S['_line'] in (11, 12) and v not in S['allowed_set'] and i == S['word'].index(v) else ('blue' if S.get('char') == v and i == S['word'].index(v) else None))),
    ],
    watch=['char', ('res', 'res', 'green')],
    captions={
        'allowed_set = set()': '先建一个空集合，装 `allowed` 里的字符',
        'allowed_set.add': '把 `{char}` 放进集合：`{allowed_set}`',
        'res = len(words)': '先假设==每个单词都一致==：`res = {res}`，遇到不一致的再减掉',
        'for char in word': '取出字符 `{char}`',
        'if char not in allowed_set': lambda S, B, r: (f"`{S.char}` 不在集合里 → 这个单词不一致" if S.char not in S.allowed_set else f"`{S.char}` 在集合里 → 合法，继续看下一个字符"),
        'res -= 1': '`{word}` 含有不允许的字符，==少一个==：`res` = {res}',
        'break': '已经不一致了，不用再看这个单词剩下的字符',
        'return res': '一致字符串一共 `{res}` 个',
    },
    cards=dict(
        one_liner='用集合 O(1) 判断字符是否允许，逐个单词检查',
        complexity='时间 `O(n+m)`（m 为所有单词总长），空间 `O(1)`',
        problem=['给你字符串 `allowed`（字符互不相同）和字符串数组 `words`',
                 '一个字符串的每个字符都在 `allowed` 里，就叫==一致字符串==',
                 '示例：`allowed="ab"`，`words=["ad","bd","aaab","baa","badab"]` → `2`'],
        quote='使用allowed构造哈希表，然后检测word中的每个字符是否出现在哈希表中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `allowed` 的字符放进集合，查询只要 `O(1)`',
              '答案先设为单词总数，发现某个字符不在集合里就减 1',
              '该单词一旦不一致就 `break`，不重复扣减'],
        summary=['时间 `O(n+m)`，空间 `O(1)`（集合最多 26 个字符）',
                 '易错点：不一致后必须 `break`，否则同一个单词会被扣多次',
                 '也可以反过来：一致才 `res += 1`'],
    ),
)
