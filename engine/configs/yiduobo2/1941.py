S_IN = 'abacbc'


def _done(S):
    return sum((S.get('char_dict') or {}).values())


def _pos(S):
    if 'char_dict' not in S or S.get('char_cnt') is not None:
        return None
    k = _done(S)
    if S.get('_line') == 4:
        return k if k < len(S_IN) else None
    return k - 1


def _s_color(S, i, v):
    return 'green' if i < _done(S) else None


def _cnt_color(S, i, v):
    if S.get('char_cnt') is None:
        return None
    if i == 0:
        return 'purple'
    idx = S.get('index')
    if idx is None:
        return None
    if i < idx:
        return 'green'
    if i == idx and S.get('_line') in (9, 10):
        return 'green' if S['char_cnt'][i] == S['char_cnt'][0] else 'red'
    return None


def _cap_for_char(S, B, ret):
    k = _done(B)
    if k == len(S_IN):
        return '整串扫描完毕，计数完成'
    return f"读 `s[{k}] = '{S.char}'`"


def _cap_add(S, B, ret):
    c = S.char
    old = B['char_dict'].get(c)
    if old is None:
        return f"`'{c}'` 第一次出现：`get` 返回默认值 0 → `char_dict['{c}'] = 1`"
    return f"`'{c}'` 之前出现过 `{old}` 次 → `char_dict['{c}'] = {old + 1}`"


def _cap_for_idx(S, B, ret):
    if S.get('index') == B.get('index'):
        return '所有次数都和第一个相同'
    return f'拿第 `{S.index}` 种字符的次数和第 0 种比'


def _cap_cmp(S, B, ret):
    a, b = S.char_cnt[S.index], S.char_cnt[0]
    if a != b:
        return f'`{a} != {b}`：出现次数==不同== → 不是好字符串'
    return f'`{a} == {b}`：相同，继续'


CONFIG = dict(
    num=1941, title='检查是否所有字符出现次数相同', difficulty='Easy', category='哈希',
    author='yiduobo', technique='dict 计数 · 和第一个比较',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def areOccurrencesEqual(self, s):
        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1

        char_cnt = list(char_dict.values())
        for index in range(1, len(char_cnt)):
            if char_cnt[index] != char_cnt[0]:
                return False

        return True
''',
    call=f'Solution().areOccurrencesEqual({S_IN!r})',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（绿 = 已统计）', cell=84, h=210,
             pointers={'char': _pos}, color=_s_color),
        dict(type='map', var='char_dict', label='char_dict（字符 → 出现次数）', h=150,
             fmt=lambda k, v: f"'{k}': {v}"),
        dict(type='array', var='char_cnt', label='char_cnt（紫 = 基准 char_cnt[0]，绿 = 已比较且相同）', cell=84, h=210,
             pointers={'index': 'blue'}, color=_cnt_color),
        dict(type='text', fn=lambda S: (f"比较 `char_cnt[{S['index']}] = {S['char_cnt'][S['index']]}` 和 `char_cnt[0] = {S['char_cnt'][0]}`"
                                        if S.get('index') is not None else ''), h=70),
    ],
    watch=[('char', 'char', 'blue'), ('index', 'index', 'blue')],
    captions={
        'char_dict = {}': '用 dict 统计==每种字符出现的次数==',
        'for char in s': _cap_for_char,
        'char_dict[char] = ': _cap_add,
        'char_cnt = list(': '只关心次数：取出所有 value → `char_cnt = {char_cnt}`',
        'for index in range': _cap_for_idx,
        'if char_cnt[index]': _cap_cmp,
        'return False': '有一种字符次数不同 → 返回 `False`',
        'return True': '每种出现过的字符次数都等于第一种 → 是好字符串，返回 =={ret}==',
    },
    max_steps=40,
    cards=dict(
        one_liner='一趟计数，再看所有次数是否都等于第一个',
        complexity='时间 `O(n)`，空间 `O(Σ)`（Σ = 26）',
        problem=['给字符串 `s`，如果 `s` 中出现过的==所有字符出现次数相同==，返回 `true`',
                 '示例 1：`s = "abacbc"` → `true`（a、b、c 各出现 2 次）',
                 '示例 2：`s = "aaabb"` → `false`（a 出现 3 次，b 出现 2 次）'],
        quote='比较基础的题目，==一趟遍历==，使用dict统计每种字符出现的次数，然后判断每种出现过的字符其出现次数是否相同即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['第一遍：`char_dict[c] = get(c, 0) + 1`，没出现过的字符默认 0',
              '只看==出现过的==字符：没出现的字母不在 dict 里，不参与比较',
              '「全部相同」⇔「全部等于第一个」：从下标 1 开始和 `char_cnt[0]` 比'],
        summary=['时间 `O(n)`，空间 `O(Σ)`：dict 最多 26 个键',
                 '原文为 Python 2 写法：`dict.values()` 在 Python 3 不能下标访问，已改为 `list(char_dict.values())`；另删去类型说明文档字符串',
                 '易错：不要用长度 26 的数组直接比，次数为 0 的字母要排除',
                 '更短的写法：`len(set(Counter(s).values())) == 1`'],
    ),
)
