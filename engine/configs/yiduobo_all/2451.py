def _eq(S, p, q):
    return S['diff_list'][p] == S['diff_list'][q]


CONFIG = dict(
    num=2451, title='差值数组不同的字符串', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='比较前三个字符串的差值数组',
    tags=[],
    code='''
class Solution(object):
    def oddString(self, words):

        diff_list = []
        for word in words:
            diff_list.append([])
            for index in range(1, len(word)):
                diff_list[-1].append(ord(word[index]) - ord(word[index - 1]))
        
        def same(p, q):
            for index in range(len(diff_list[p])):
                if diff_list[p][index] != diff_list[q][index]:
                    return False
            return True

        if same(0, 1):
            for index in range(2, len(words)):
                if not same(0, index):
                    return words[index]
        elif same(0, 2):
            return words[1]
        else:
            return words[0]
''',
    call='''r1 = Solution().oddString(["aaa","bob","ccc","ddd"])
r2 = Solution().oddString(["adc","wzy","abc"])
[r1, r2]''',
    expect=['bob', 'abc'],
    views=[
        dict(type='array', var='words', label='words', cell=110,
             color=lambda S, i, v: 'blue' if 'p' in S and 'q' in S and i == S['q'] and S['_line'] in (12, 13, 14, 15, 16) else None),
        dict(type='grid', var='diff_list', label='diff_list（每行是一个字符串的差值数组）', cell=80,
             cursors=[('len(diff_list) - 1', 'index - 1', 'yellow', '')] if False else []),
    ],
    watch=['p', 'q', 'index'],
    captions={
        'diff_list = []': '`diff_list[i]` 存第 `i` 个字符串的差值数组',
        'for word in words': '处理 `word = "{word}"`',
        'diff_list.append([])': '先给它开一行空数组',
        'for index in range(1, len(word))': lambda S, B, r: (f'从第 `{S.index}` 个字母开始，和前一个字母作差' if 'index' in S and S.index < len(S.word) else '这个字符串的差值算完了'),
        'diff_list[-1].append': '`ord("{word[index]}") − ord("{word[index - 1]}")` = ==`{diff_list[-1][-1]}`==，追加进当前行',
        'def same': '定义 `same(p, q)`：比较第 `p`、`q` 个字符串的差值数组是否完全相同',
        'for index in range(len(diff_list[p]))': '逐位比较差值',
        'if diff_list[p][index] != ': lambda S, B, r: f'`diff_list[{S.p}][{S.index}] = {S.diff_list[S.p][S.index]}` 和 `diff_list[{S.q}][{S.index}] = {S.diff_list[S.q][S.index]}` ' + ('==不同=='  if S.diff_list[S.p][S.index] != S.diff_list[S.q][S.index] else '相同，继续'),
        'return False': '有一位不同 → 这两个字符串的差值数组不同',
        'return True': '每一位都相同 → 差值数组相同',
        'if same(0, 1)': lambda S, B, r: ('`words[0]` 和 `words[1]` 的差值数组' + ('==相同==：答案在后面，去找和 `words[0]` 不同的' if _eq(S, 0, 1) else '==不同==：答案是它俩之一，拿 `words[2]` 来裁决')),
        'for index in range(2, len(words))': '从下标 2 往后，逐个和 `words[0]` 比',
        'if not same(0, index)': lambda S, B, r: f'`words[{S.index}] = "{S.words[S.index]}"` 和 `words[0]` 的差值数组' + ('相同，继续' if _eq(S, 0, S.index) else '不同 → 就是它'),
        'return words[index]': '找到了不同的那个：`"{ret}"`',
        'elif same(0, 2)': lambda S, B, r: ('`words[0]` 和 `words[2]` ' + ('相同 → `words[1]` 才是异类' if _eq(S, 0, 2) else '也不同 → `words[0]` 才是异类')),
        'return words[1]': '`words[0]`、`words[2]` 相同，所以 `words[1]` 是答案：`"{ret}"`',
        'return words[0]': '`words[1]`、`words[2]` 相同，`words[0]` 是答案：`"{ret}"`',
    },
    cards=dict(
        one_liner='只比前三个：先看 0 和 1，再用 2 裁决',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['字符串的差值数组：相邻字母位置之差，如 `"acb"` → `[2, -1]`',
                 '除一个字符串外，其余差值数组都相同，找出不同的那个',
                 '本视频两次：`["aaa","bob","ccc","ddd"]` → `"bob"`；`["adc","wzy","abc"]` → `"abc"`'],
        quote='对比words[0]、words[1]这两个字符串的差值数组，若相同，说明答案出现在后面；若不同，则说明答案就是words[0]或者words[1]，此时只需要检测words[0]和words[2]对应的差值数组是否相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把所有字符串的差值数组算好，放进 `diff_list`',
              '`same(0, 1)` 为真：异类在后面，逐个跟 `words[0]` 比',
              '为假：异类是 0 或 1，再比 0 和 2：相同则 1 是异类，否则 0 是异类'],
        result='两次依次得到 `"bob"`、`"abc"` ✓',
        summary=['时间 `O(mn)`，空间 `O(mn)`（存了所有差值数组）',
                 '易错：`same(0, 1)` 为假时，不能直接断定答案，要靠 `words[2]` 裁决',
                 '`index` 从 1 开始，是字母下标；两个 `index` 循环用途不同（外层 `range(2, len(words))` 是单词下标）',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：他用哈希表按差值分组，yiduobo 只比较前三个'],
    ),
)
