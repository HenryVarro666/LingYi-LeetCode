def _cur(S):
    if 'abbr' not in S['_inner']:
        return '把单词的每一位要么==保留字母==，要么==并入数字==，枚举出全部缩写'
    now = ''.join(S['_inner']['now'])
    ab = S['_inner']['abbr']
    return f'已确定前缀 `{now or "（空）"}`，待并入的连续省略数 `abbr = {ab}`'


CONFIG = dict(
    num=411, title='最短独占单词缩写', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='dfs 枚举全部缩写 + 哈希集合',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def minAbbreviation(self, target, dictionary):

        def dfs(level, now, abbr, word_set):
            if level == n:
                if abbr > 0:
                    tmp = str(abbr)
                else:
                    tmp = ''
                word_set.add(''.join(now) + tmp)
                return

            dfs(level + 1, now, abbr + 1, word_set)
            
            if abbr > 0:
                now.append(str(abbr))
                now.append(word[level])
                dfs(level + 1, now, 0, word_set)
                now.pop()
                now.pop()
            else:
                now.append(word[level])
                dfs(level + 1, now, 0, word_set)
                now.pop()
        
        dict_set = set()
        for word in dictionary:
            if len(word) != len(target):
                continue
            n = len(word)
            dfs(0, [], 0, dict_set)
        
        target_set = set()
        word = target
        n = len(word)
        dfs(0, [], 0, target_set)
        for res in sorted(list(target_set), key=lambda d:len(d)):
            if res not in dict_set:
                return res
''',
    call='Solution().minAbbreviation("ab", ["ac", "bb"])',
    expect="ab",
    views=[
        dict(type='string', var='word', label='word（当前在枚举缩写的单词）', cell=90, h=190, pointers={'level': 'blue'}),
        dict(type='text', h=80, size=26, fn=_cur),
        dict(type='set', var='dict_set', label='dict_set（字典单词的全部缩写）', h=120, font=26),
        dict(type='set', var='target_set', label='target_set（target 的全部缩写）', h=120, font=26),
        dict(type='calls', h=150),
    ],
    watch=[('level', 'level', 'blue'), ('abbr', 'abbr', 'orange'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'dfs(level + 1, now, abbr + 1, word_set)': '第 `{B.level + 1}` 位选择==省略==：连续省略数 `abbr` 从 `{B.abbr}` 变成 `{B.abbr + 1}`，进入下一层',
        'if level == n': lambda S, B, r: ('`level == n`：每一位都决定完了，得到一个完整缩写' if S.level == S.n
                                          else f'`level = {S.level} < {S.n}`：还有字母没决定，继续往下'),
        'word_set.add': '缩写 `{"".join(now) + tmp}` 记入集合（末尾的省略数要补上）',
        'if abbr > 0': lambda S, B, r: (f'`abbr = {S.abbr} > 0`：保留字母前，要先把省略数 `{S.abbr}` 写出来' if S.abbr > 0
                                        else '`abbr = 0`：前面没有省略，直接保留字母'),
        'now.append(word[level])': '第 `{level + 1}` 位选择==保留==字母 `{word[level]}`',
        'if len(word) != len(target)': '缩写相同则长度必相同，长度不同的字典单词直接跳过',
        'dict_set = set()': '`dict_set` 存字典中所有单词的全部缩写',
        'target_set = set()': '`target_set` 存 target 的全部缩写',
        'for res in sorted': '按缩写长度从短到长，逐个检查 `{res}`',
        'if res not in dict_set': lambda S, B, r: (f'`{S.res}` 不在 dict_set 中 → 它不是任何字典单词的缩写，是==独占==的' if S.res not in S.dict_set
                                                   else f'`{S.res}` 已在 dict_set 中 → 和字典单词冲突，试下一个更长的'),
        'return res': '最短的独占缩写：`{res}`',
    },
    skip=['now.pop()', 'tmp = str(abbr)', "tmp = ''", 'now.append(str(abbr))', 'n = len(word)'],
    max_steps=68,
    cards=dict(
        one_liner='数据范围保证暴力可行：枚举全部缩写，挑最短的独占者',
        complexity='时间 `O(n·2^m)`，空间 `O(n·2^m)`',
        problem=['把单词的若干连续字母换成其长度即为缩写，如 `apple` → `a3e`',
                 '求 `target` 最短的缩写，且不是字典中任何单词的缩写',
                 '本视频：`target = ab`，`dictionary = [ac, bb]` → `ab`'],
        quote='注意到题目中有一个条件 log2(n) + m <= 21 ……换言之，在这里使用暴力算法是完全可行的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 dfs 枚举字典里每个单词的全部缩写，放进哈希集合',
              '再 dfs 枚举 `target` 的全部缩写，按长度排序',
              '第一个不在集合里的就是答案；长度不同的字典单词可直接跳过'],
        summary=['时间空间都约 `O(n·2^m)`，m 为单词长度，靠数据范围保证可行',
                 '`abbr` 记录连续省略的字母数，保留字母前要先写出它',
                 '遍历结束时末尾的 `abbr` 也要补写',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
