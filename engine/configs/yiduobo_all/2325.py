_N = [0]


def _for(S, B, r):
    _N[0] = _N[0] + 1 if 'char' in B else 1
    if _N[0] > len(S.key):
        return 'key 扫描完了，对照表建好'
    return f'取 key 的下一个字符 `{S.char!r}`'


def _txt(S):
    if 'mapping' not in S:
        return ''
    return f'已知 `{len(S["mapping"])}` 个映射：下一个新字母的密文是 `chr({len(S["mapping"])} + 97)` = =={chr(len(S["mapping"]) + 97)}=='


CONFIG = dict(
    num=2325, title='解密消息', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表：长度即字母顺序',
    code='''
class Solution(object):
    def decodeMessage(self, key, message):

        mapping = {}
        cnt = 0
        for char in key:
            if char != ' ' and char not in mapping:
                mapping[char] = chr(len(mapping) + 97)

        return ''.join([mapping.get(char, ' ') for char in message])
''',
    call="Solution().decodeMessage('happy boy', 'hay boy')",
    expect='abd efd',
    skip=['cnt = 0'],
    views=[
        dict(type='string', var='key', label='key（只取示例前几个字母；真题的 key 含全部 26 个字母）', cell=60, h=170),
        dict(type='map', var='mapping', label='mapping（黄色 = 刚加入的映射）', fmt=lambda k, v: f"'{k}' → '{v}'", h=330, font=30),
        dict(type='text', size=30, fn=_txt),
    ],
    watch=['char'],
    captions={
        'mapping = {}': '`mapping` 保存已知的「密文字母 → 明文字母」关系',
        'for char in key': _for,
        'if char != ': lambda S, B, r: (f'`{S.char!r}` 是空格 → 不参与对照表' if S.char == ' ' else
                                        (f'`{S.char!r}` 不在 `mapping` 里 → ==首次出现==，要加入' if S.char not in S.mapping else
                                         f'`{S.char!r}` 已经在 `mapping` 里 → 跳过')),
        'mapping[char] =': '新字母的顺序恰好 = 已有映射个数 `{len(mapping) - 1}` → `chr({len(mapping) - 1} + 97)` = `{mapping[char]!r}`：`{char!r}` → `{mapping[char]!r}`',
        'return': '逐个翻译 `message`：查得到的换成明文，查不到的（空格）用 `get` 的默认值 `\' \'` → =={ret!r}==',
    },
    cards=dict(
        one_liner='哈希表的长度，恰好就是下一个新字母在字母表里的位置',
        complexity='时间 `O(n + m)`，空间 `O(1)`（最多 26 个映射）',
        problem=['`key` 里 26 个字母==第一次出现的顺序==，对应 a~z，得到替换表',
                 '用它翻译 `message`，空格不变',
                 '示例：`key = "happy boy"` → `h→a, a→b, p→c, y→d, b→e, o→f`',
                 '本视频：`message = "hay boy"` → `"abd efd"`'],
        quote='若其没有出现在哈希表中，那么其对应的字母顺序恰好就是哈希表的长度，此时将char及其加密后对应的字母加入到哈希表中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历 `key`，用哈希表记录已知的对应关系',
              '遇到新字母，它是第几个新字母 = 当前表长，明文就是 `chr(表长 + 97)`',
              '空格不进表；翻译时 `get(char, \' \')` 查不到就还是空格'],
        summary=['时间 `O(n + m)`，空间 `O(1)`（映射最多 26 个）',
                 '`chr(len(mapping) + 97)`：97 是 `a` 的 ASCII 码，==先算字母再入表==，所以长度还没包含自己',
                 '要跳过 `key` 里的空格，否则空格会占掉一个字母',
                 '代码里的 `cnt = 0` 没有用到，原文如此保留',
                 '对比灵神：灵神把空格也映射到空格，翻译时不用判断；yiduobo 用 `get` 的默认值处理空格'],
    ),
)
