def _txt(S):
    if 'order' not in S:
        return ''
    ln = S['_line']
    rw = S.get('real_word')
    if rw is not None and 'index' in S and ln in (14, 15, 16) and S['index'] + 1 < len(rw):
        a, b = rw[S['index']], rw[S['index'] + 1]
        return f"比较 `{a}` 与 `{b}`：{'==顺序正确==' if a <= b else '==逆序，不合法=='}"
    return '外星字母表 → a-z 的映射：外星第 k 个字母 → 第 k 个英文字母'


def _cmap(S, k, v):
    if 'word' in S and S['_line'] in (10, 11) and k in S['word']:
        return 'blue'
    return None


def _real_color(S, i, v):
    if 'index' not in S or S['_line'] not in (14, 15, 16):
        return None
    if i in (S['index'], S['index'] + 1):
        return 'green' if S['real_word'][S['index']] <= S['real_word'][S['index'] + 1] else 'red'
    return None


CONFIG = dict(
    num=953, title='验证外星语词典', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字母映射成 a-z + 相邻比较',
    code='''
class Solution(object):
    def isAlienSorted(self, words, order):

        char_dict = {}
        for index, char in enumerate(order):
            char_dict[char] = chr(index + 97)

        real_word = []
        for word in words:
            real_word.append(''.join([char_dict[x] for x in word]))
        
        for index in range(len(real_word) - 1):
            if real_word[index] > real_word[index + 1]:
                return False

        return True
''',
    call="Solution().isAlienSorted(['hello', 'leetcode', 'hel'], 'hlecotd')",
    expect=False,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='words', label='words（外星语单词）', cell=150, h=190),
        dict(type='map', var='char_dict', label='char_dict：外星字母 → 英文字母', h=170, font=22),
        dict(type='array', var='real_word', label='real_word（映射后的单词）', cell=150, h=190, color=_real_color),
    ],
    watch=['index', 'char', 'word'],
    captions={
        'char_dict = {}': '建一个字典，把外星字母表一一对应到 `a-z`',
        'for index, char in enumerate(order)': lambda S, B, r: (f'外星字母表第 `{S.index}` 个字母是 `{S.char}`' if B.get('index') != S.index else '字母表扫完，映射建好了'),
        'char_dict[char]': '`{char}` → `{char_dict[char]}`：它在外星语排第 {index}，对应英文第 {index} 个字母',
        'real_word = []': '准备存放“翻译成英文字母”后的单词',
        'for word in words': lambda S, B, r: (f'取出单词 `{S.word}`' if B.get('word') != S.word or not S.real_word else '所有单词都翻译完了'),
        'real_word.append': '逐字母查表翻译：`{word}` → `{real_word[-1]}`，之后就能直接用普通字典序比较',
        'for index in range(len(real_word) - 1)': lambda S, B, r: (f'比较第 `{S.index}` 个和第 `{S.index+1}` 个单词' if B.get('_line') != 15 or B.get('index') != S.index else '相邻单词都比完了，没有逆序'),
        'if real_word[index] >': lambda S, B, r: (f"`{S.real_word[S.index]}` > `{S.real_word[S.index+1]}`：前面的单词更大 → ==顺序不对=="
                                                  if S.real_word[S.index] > S.real_word[S.index+1]
                                                  else f"`{S.real_word[S.index]}` <= `{S.real_word[S.index+1]}`：顺序正确"),
        'return False': '出现逆序，直接返回 `False`',
        'return True': '所有相邻单词都有序 → `True`',
    },
    cards=dict(
        one_liner='先把外星字母映射成 a-z，再按普通字典序比相邻单词',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['外星语字母表顺序由字符串 `order` 给出（26 个小写字母的某个排列）',
                 '判断 `words` 是否按外星语字典序排列',
                 '示例：`words=["hello","leetcode"]`，`order="hlabcdefgijkmnopqrstuvwxyz"` → `true`',
                 '本视频为了演示，字母表缩短成只含出现过的 7 个字母 `hlecotd`',
                 '再加一个 `"hel"`，它排在 `"leetcode"` 后面，应得 `false`'],
        quote='将外星语词典与a到z建立一对一的映射，然后将words中的单词根据这个映射转化为最终的单词，然后一趟遍历比较相邻两个单词的大小关系是否符合要求即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`char_dict`：外星第 `k` 个字母 → 第 `k` 个英文字母，字典序大小关系保持不变',
              '把每个单词逐字母翻译，之后可以直接用 Python 的字符串比较',
              '只需比较相邻单词：相邻都不降，整体就有序'],
        summary=['时间 `O(L)`，`L` 为所有单词字符总数；空间 `O(L)`',
                 '前缀规则：`"hel"` 应排在 `"hello"` 之前，映射后用 `>` 比较自然成立',
                 '只比较相邻两个单词即可，不必两两比较',
                 '原文在 Python 3 下无需修改，逐字照搬'],
    ),
)
