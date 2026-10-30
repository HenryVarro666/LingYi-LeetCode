def _top(S):
    if 'cnt' in S:
        return f"成对的字符都能放两侧；落单标记 `single = {S['single']}`，已累计 `res = {S['res']}`"
    if 'char_dict' in S:
        return '先统计每个字符出现的次数'
    return ''


CONFIG = dict(
    num=409, title='最长回文串', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='统计次数 · 成对放两侧',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def longestPalindrome(self, s):

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        single = 0
        res = 0
        for cnt in char_dict.values():
            if cnt % 2 == 1:
                single = 1
                res += cnt - 1
            else:
                res += cnt

        return res + single
''',
    call='Solution().longestPalindrome("abccccdd")',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='string', var='s', label='s（黄 = 正在统计的字符）', h=190, cell=80,
             color=lambda S, i, v: 'yellow' if 'char' in S and 'cnt' not in S and i == sum(S['char_dict'].values()) - (0 if S['_line'] == 5 else 1) else None),
        dict(type='map', var='char_dict', label='char_dict：字符 → 出现次数', h=300, fmt=lambda k, v: f"'{k}' → {v}"),
    ],
    watch=[('char', 'char', 'yellow'), ('cnt', 'cnt', 'blue'), ('single', 'single', 'pink'), ('res', 'res', 'green')],
    captions={
        'for char in s': lambda S, B, r: (f"取下一个字符 `char = '{S.s[sum(S.char_dict.values())]}'`" if sum(S.char_dict.values()) < len(S.s)
                                          else '`s` 扫完了，每种字符的次数都统计好了'),
        'char_dict[char] =': "`'{char}'` 又出现一次，累计：`char_dict['{char}']` = =={char_dict[char]}==",
        'single = 0': '`single` 标记是否有落单字符（能放在正中间）',
        'res = 0': '`res` 累计能放到两侧的字符数',
        'for cnt in': '看一种字符：它出现了 `{cnt}` 次',
        'if cnt % 2 == 1': lambda S, B, r: (f'`{S.cnt}` 是奇数 → 成对放完会==剩 1 个落单==' if S.cnt % 2 == 1
                                            else f'`{S.cnt}` 是偶数 → 可以==全部两两放到两侧=='),
        'single = 1': '有落单字符了，答案最后可以==在正中间再放 1 个==：`single = 1`',
        'res += cnt - 1': '落单的那 1 个先不放，其余 `{cnt - 1}` 个成对放：`res` → =={res}==',
        'res += cnt': '全部成对放：`res` += `{cnt}` → =={res}==',
        'return res + single': '`res + single` = `{res}` + `{single}` = =={res + single}==',
    },
    cards=dict(
        one_liner='字符成对放两侧，剩下的落单字符挑一个放中间',
        complexity='时间 `O(n)`，空间 `O(1)`（最多 52 种字符）',
        problem=['给定只含大小写字母的字符串 `s`，用其中的字符拼成一个回文串',
                 '返回能拼出的==最长回文串长度==',
                 '示例：`"abccccdd"` → `7`（`dccaccd`）'],
        quote='统计出串中每个字符出现的次数，那么可以将所有字符两个两个加入到答案的两侧。处理完之后，如果还剩下落单的字符，那么可以选取某一个作为答案的正中字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['回文串两侧对称：每个字符的偶数部分 `cnt // 2 * 2` 都能用上',
              '出现奇数次的字符会剩 1 个，回文串最多容纳 ==1 个落单字符放中间==',
              '所以答案 = 成对字符总数 + (有落单则 1，否则 0)'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '奇数次的字符取 `cnt - 1` 个，不是丢掉整个字符',
                 '`single` 只会是 0 或 1：不管有几种落单字符，中心位置只有一个',
                 '原文本来就能在 Python 3 运行，代码未改动'],
    ),
)
