PATTERN, STR = 'abba', 'dog cat cat fish'


def _color(S, i, v):
    idx = S.get('index')
    if idx is None:
        return None
    if i < idx:
        return 'green'
    if i == idx:
        ln = S.get('_line')
        if ln in (11, 15):
            return 'red'
        if ln in (12, 13):
            return 'green'
    return None


def _for_cap(S, B, ret):
    if B.get('index') != S.get('index') or 'index' not in B:
        return f'第 `index = {S.index}` 个：字母 `\'{S.char}\'` ↔ 单词 `"{S.words[S.index]}"`'
    return '全部对应完毕，没有冲突'


def _not_in(S, B, ret):
    c = S.char
    if c not in S.word_dict:
        return f'`\'{c}\'` 还不在 `word_dict` 里 → 第一次出现，准备建立映射'
    return f'`\'{c}\'` 已经映射到 `"{S.word_dict[c]}"`'


def _used(S, B, ret):
    w = S.words[S.index]
    if w in S.used_set:
        return f'`"{w}"` 已经被别的字母用过 → 违反一一对应'
    return f'`"{w}"` 没被用过 → 可以分配给 `\'{S.char}\'`'


def _neq(S, B, ret):
    c, w = S.char, S.words[S.index]
    if S.word_dict[c] != w:
        return f'`word_dict[\'{c}\'] = "{S.word_dict[c]}"` ≠ `"{w}"`：同一个字母对应了两个单词 → ==不符合规律=='
    if S.pattern.index(c) == S.index:
        return '刚建好的映射，这里必然相等 → 继续'
    return f'`word_dict[\'{c}\'] = "{w}"`，和当前单词一致 → 继续'


CONFIG = dict(
    num=290, title='单词规律', difficulty='Easy', category='哈希',
    author='yiduobo', technique='字母→单词映射 + 已用单词集合',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def wordPattern(self, pattern, str):
        words = str.split(' ')
        if len(pattern) != len(words):
            return False
        word_dict = {}
        used_set = set()
        for index, char in enumerate(pattern):
            if char not in word_dict:
                if words[index] in used_set:
                    return False
                word_dict[char] = words[index]
                used_set.add(words[index])
            if word_dict[char] != words[index]:
                return False

        return True
''',
    call=f'Solution().wordPattern({PATTERN!r}, {STR!r})',
    expect=False,
    views=[
        dict(type='string', var='pattern', label='pattern', pointers={'index': 'blue'}, color=_color, cell=110),
        dict(type='array', var='words', label='words = str.split(\' \')', pointers={'index': 'pink'}, color=_color, cell=110),
        dict(type='map', var='word_dict', label='word_dict（字母 → 单词）', h=130, fmt=lambda k, v: f"'{k}' → \"{v}\""),
        dict(type='set', var='used_set', label='used_set（已经被用过的单词）', h=120, fmt=lambda x: f'"{x}"'),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('words[index]', lambda S: S['words'][S['index']] if 'index' in S else None, 'pink')],
    captions={
        'words = str.split': '按空格切出单词：`words = {words}`',
        'if len(pattern) != len(words)': '字母 {len(pattern)} 个、单词 {len(words)} 个：要一一对应，==数量必须一致==',
        'word_dict = {}': '`word_dict` 维护每个字母到单词的映射',
        'used_set = set()': '`used_set` 记录已经被某个字母占用的单词',
        'for index, char in': _for_cap,
        'if char not in word_dict': _not_in,
        'if words[index] in used_set': _used,
        'word_dict[char] = words[index]': "建立映射 `'{char}' → \"{words[index]}\"`",
        'used_set.add': '`"{words[index]}"` 被 `\'{char}\'` 占用',
        'if word_dict[char] != words[index]': _neq,
        11: '单词已被占用 → 返回 `False`',
        15: '映射不一致 → 返回 `False`',
        'return True': '每个字母和单词都一一对应 → 返回 `True`',
    },
    cards=dict(
        one_liner='一个 dict 管字母→单词，一个 set 保证单词不被两个字母共用',
        complexity='时间 `O(n + m)`，空间 `O(m)`（`m` 为 str 长度）',
        problem=['`pattern` 是字母串，`s` 是空格分隔的单词串',
                 '判断 `s` 是否遵循 `pattern`：字母与单词==一一对应==（双向）',
                 '示例：`"abba","dog cat cat dog"` → `true`',
                 '示例：`"abba","dog cat cat fish"` → `false`'],
        quote='需要注意每个字母与单词必须一一对应，因此首先二者的数量必须一致，另外当某个字母不在dict中时，其对应的单词也必须没有被使用过。',
        quote_src='—— yiduobo 知乎题解',
        idea=['数量不一致 → 直接 `False`',
              '字母第一次出现：单词若已被占用 → `False`，否则建立映射',
              '每一步都检查 `word_dict[char]` 是否等于当前单词'],
        summary=['时间 `O(n + m)`：切分单词 + 一次遍历',
                 '易错：只用 dict 会漏掉 `"ab","dog dog"`，所以要 `used_set`',
                 '新映射建立后会顺带再比较一次，必然相等，写法更统一',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（参数名 `str` 原样保留）',
                 '同类题：205 同构字符串（字符 ↔ 字符）'],
    ),
)
