W1, W2 = 'abcdeef', 'abaaacc'

CONFIG = dict(
    num=2068, title='检查两个字符串是否几乎相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表记录次数之差',
    tags=[],
    code='''
class Solution(object):
    def checkAlmostEquivalent(self, word1, word2):

        char_diff = {}
        for char in word1:
            char_diff[char] = char_diff.get(char, 0) + 1
        
        for char in word2:
            char_diff[char] = char_diff.get(char, 0) - 1

        for diff in char_diff.values():
            if abs(diff) > 3:
                return False

        return True
''',
    call=f'Solution().checkAlmostEquivalent({W1!r}, {W2!r})',
    expect=True,
    views=[
        dict(type='string', var='word1', label='word1（蓝 = 正在计入的字符）', cell=84, h=150,
             color=lambda S, i, v: 'blue' if S.get('_line') in (5, 6) and S.get('char') == v else None),
        dict(type='string', var='word2', label='word2（粉 = 正在扣除的字符）', cell=84, h=150,
             color=lambda S, i, v: 'pink' if S.get('_line') in (8, 9) and S.get('char') == v else None),
        dict(type='map', var='char_diff', label='char_diff（字符 → word1 次数 − word2 次数）',
             fmt=lambda k, v: f"'{k}': {v}", h=190, font=32),
    ],
    watch=[('char', 'char', 'blue'), ('diff', 'diff', 'orange')],
    captions={
        'char_diff = {}': '用一个哈希表记录每个字符在两个字符串中的次数之差',
        'for char in word1': '看 word1 的下一个字符',
        'for char in word2': '看 word2 的下一个字符',
        'char_diff[char] = char_diff.get(char, 0) + 1': "word1 里的 `'{char}'`：差值 +1 → `{char_diff[char]}`",
        'char_diff[char] = char_diff.get(char, 0) - 1': "word2 里的 `'{char}'`：差值 -1 → `{char_diff[char]}`",
        'for diff in char_diff.values()': '两个字符串都统计完，逐个检查每种字符的差值',
        'if abs(diff) > 3': lambda S, B, r: (f'`|{S.diff}| > 3` → 频率差太大，不是几乎相等' if abs(S.diff) > 3
                                           else f'`|{S.diff}| = {abs(S.diff)}`，不超过 3 → 这种字符没问题'),
        'return False': '有字符频率差超过 3 → 返回 `False`',
        'return True': '所有字符频率差都不超过 3 → 返回 `True`',
    },
    cards=dict(
        one_liner='一个哈希表：word1 里加一，word2 里减一，看差的绝对值',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 26 种字符）',
        problem=['两个字符串中，每个字母出现次数之差都 ==不超过 3== 就叫几乎相等',
                 '返回 `word1`、`word2` 是否几乎相等',
                 '示例：`"abcdeef"` 与 `"abaaacc"` → `True`'],
        quote='使用哈希表记录每个字符在word1中出现次数与word2中出现次数之差，接下来遍历每种字符出现次数之差，如果有差值大于3次的字符，那么答案就是false，否则答案就是true。',
        quote_src='—— yiduobo 题解原文',
        idea=['`word1` 的字符让差值 +1，`word2` 的字符让差值 -1',
              '最后每个键的值就是该字母两边次数之差',
              '只要有一个 `|差| > 3`，答案就是 `False`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：差值可能为负，必须取绝对值再和 3 比',
                 '只出现在一个单词里的字母也要算（另一边次数为 0）',
                 '代码与原文一致，只保留了 Python 3 可运行的写法'],
    ),
)
