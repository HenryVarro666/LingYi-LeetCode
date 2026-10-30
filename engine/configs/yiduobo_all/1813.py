def _suf(S):
    return S['_line'] >= 22


def _o_ptr(S):
    if 'index' not in S or 'm' not in S or 'left' not in S:
        return None
    if _suf(S):
        return S['n'] - S['m'] + S['index']
    return S['index']


def _col_t(S, i, v):
    if 'left' not in S or 'index' not in S:
        return None
    if _suf(S):
        return 'green' if (i > S['index'] or i < S['left']) else None
    k = S['left'] if S['left'] < S['m'] else S['index']
    return 'green' if i < k else None


def _col_o(S, i, v):
    if 'left' not in S or 'index' not in S:
        return None
    if _suf(S):
        return 'green' if (i > S['n'] - S['m'] + S['index'] or i < S['left']) else None
    k = S['left'] if S['left'] < S['m'] else S['index']
    return 'green' if i < k else None


def _info(S):
    if 'target' not in S:
        return ''
    if _suf(S) and 'n' in S:
        return f"后缀：从 target 末尾向前比，已匹配到 `index = {S.get('index')}`；前缀只匹配了 `left = {S['left']}` 个词"
    if 'left' in S and S['left'] < S['m']:
        return f"前缀匹配了 `{S['left']}` 个词，`origin[{S['left']}]` 与 `target[{S['left']}]` 不同"
    return '先从前往后比前缀：相同就继续，遇到不同就记下 left'


CONFIG = dict(
    num=1813, title='句子相似性 III', difficulty='Medium', category='字符串',
    author='yiduobo', technique='最长公共前缀 + 后缀',
    tags=[],
    code='''
class Solution(object):
    def areSentencesSimilar(self, sentence1, sentence2):

        word_list1 = sentence1.split(' ')
        word_list2 = sentence2.split(' ')
        if len(word_list1) < len(word_list2):
            origin, target = word_list2, word_list1
        else:
            origin, target = word_list1, word_list2
        
        m = len(target)
        left = m
        for index in range(m):
            if origin[index] != target[index]:
                left = index
                break
        
        if left == m:
            return True

        n = len(origin)
        for index in range(m - 1, left - 1, -1):
            if origin[n - m + index] != target[index]:
                return False

        return True
''',
    call='Solution().areSentencesSimilar("My name is Haley", "My Haley")',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='origin', label='origin（较长的句子）', pointers={_o_ptr: 'pink'}, pointer_labels={_o_ptr: '对齐'}, h=210, cell=130, color=_col_o),
        dict(type='array', var='target', label='target（较短的句子）', pointers={'index': 'blue'}, h=210, cell=130, color=_col_t),
    ],
    watch=['m', 'left', 'index', 'n'],
    captions={
        'split(\' \')': '按空格切成单词列表',
        'if len(word_list1)': '`{len(word_list1)}` 个词 vs `{len(word_list2)}` 个词：比较长度，找出长句和短句',
        'origin, target = word_list2': '句 2 更长：`origin` 是长句，`target` 是短句',
        'origin, target = word_list1': '句 1 不比句 2 短：`origin` 是长句，`target` 是短句',
        'm = len(target)': '`m = {m}`：短句词数。相似 ⇔ 短句 = 长句的某个前缀 + 某个后缀',
        'left = m': '`left` 记录前缀匹配了几个词；先假设全部匹配，`left = {left}`',
        'for index in range(m)': '从前往后逐词比较前缀，`index = {index}`',
        'if origin[index] != target[index]': lambda S, B, r: (f"`origin[{S.index}] = '{S.origin[S.index]}'` 与 `target[{S.index}] = '{S.target[S.index]}'`：相同 → 前缀继续延伸"
                                                              if S.origin[S.index] == S.target[S.index]
                                                              else f"`'{S.origin[S.index]}' != '{S.target[S.index]}'`：前缀在这里断开"),
        'left = index': '前缀只匹配了 `{left}` 个词，记下 `left = {left}` 然后跳出',
        'break': '不用再往后比前缀了',
        'if left == m': lambda S, B, r: ('`left == m`：短句整个是长句的前缀 → 相似，直接返回 True' if S.left == S.m
                                          else f'`left = {S.left} < m = {S.m}`：前缀没匹配完，剩下的 {S.m - S.left} 个词要靠后缀来匹配'),
        'n = len(origin)': '`n = {n}`：长句词数。短句第 `index` 个词应对齐长句 `n - m + index`（后缀对齐）',
        'for index in range(m - 1': '从后往前比后缀：`index` 从 `m-1` 倒数到 `left`，`index = {index}`',
        'if origin[n - m + index]': lambda S, B, r: (f"`origin[{S.n - S.m + S.index}] = '{S.origin[S.n - S.m + S.index]}'` 与 `target[{S.index}] = '{S.target[S.index]}'`："
                                                     + ('相同 → 后缀继续匹配' if S.origin[S.n - S.m + S.index] == S.target[S.index] else '不同 → 这个词既不在前缀也不在后缀 → 不相似')),
        'return False': '有一个词前后缀都对不上 → 返回 False',
        'return True': '前缀 `{left}` 个词 + 后缀 `{m - left}` 个词 正好覆盖整个短句 → 相似，返回 True',
    },
    cards=dict(
        one_liner='短句 = 长句的一段前缀 + 一段后缀',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['句子是由单个空格分隔的单词；可以在一个句子里插入一个（可为空的）句子，使其与另一个句子相同，则两句相似',
                 '示例：`"My name is Haley"` 与 `"My Haley"` → `true`',
                 '（插入 `"name is"` 即可）'],
        quote='就是问能否用长句的某个前缀拼上某个后缀得到短句。于是可以先从前向后一趟扫描，记录前缀匹配的长度，然后再从后向前一趟扫描，记录后缀匹配的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['在短句中插一段话就变成长句 ⇔ 短句被「切开」成前缀和后缀，中间缺的就是插入的内容',
              '先从前往后数前缀相同的词数 `left`；整个短句都是前缀就直接成立',
              '否则剩下的词 `left..m-1` 必须在长句末尾对得上，从后往前逐个比'],
        summary=['时间 `O(n)`，空间 `O(n)`（`split` 产生单词列表）',
                 '后缀对齐的下标是 `n - m + index`，不是 `index`',
                 '要先把句子按空格切成单词再比，不能按字符比',
                 '原文为 Python 2 风格，本题无需改动，代码照搬原文'],
    ),
)
