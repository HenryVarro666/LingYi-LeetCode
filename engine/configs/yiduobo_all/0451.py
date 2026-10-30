CONFIG = dict(
    num=451, title='根据字符出现频率排序', difficulty='Medium', category='字符串',
    author='yiduobo', technique='计数 + 按频次排序',
    code='''
class Solution(object):
    def frequencySort(self, s):

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        res = ''
        for char, cnt in sorted(char_dict.items(), key=lambda d:d[1], reverse=True):
            res += char * cnt
        return res
''',
    call="Solution().frequencySort('cacbbb')",
    expect='bbbcca',
    views=[
        dict(type='string', var='s', label='s（输入字符串）', h=150, pointers={}),
        dict(type='map', var='char_dict', fmt=lambda k, v: f"'{k}': {v}", label='char_dict：字符 → 出现次数', h=220, font=34),
        dict(type='text', fn=lambda S: f"结果 res = `'{S['res']}'`" if 'res' in S else '', size=36, h=80),
    ],
    watch=['char', 'cnt', ('res', 'res', 'green')],
    captions={
        'char_dict = {}': '先准备一个字典，记录每个字符出现的次数',
        'char_dict[char] =': '`char_dict[{char!r}]` = =={char_dict[char]}==：{char!r} 目前出现了 {char_dict[char]} 次',
        'res = ': '`res` 用来拼最终字符串',
        'sorted(': '按次数从高到低排序：次数相同的保持原来的先后顺序（排序是稳定的）',
        'res += char * cnt': '字符 `{char!r}` 出现 `{cnt}` 次，连续写 `{cnt}` 遍 → `res = {res!r}`',
        'return res': '次数多的字符排在前面，返回 `{res!r}`',
    },
    cards=dict(
        one_liner='数出每个字符的次数，按次数从多到少重复拼接',
        complexity='时间 `O(n + k log k)`，空间 `O(n)`',
        problem=['给定字符串 `s`，把字符按==出现频率降序==重新排列',
                 '同一个字符必须连在一起；频率相同的字符顺序任意',
                 '本视频：`s = "cacbbb"` → `"bbbcca"`'],
        quote='比较基础的题目。统计每个字符出现的次数，排序后输出即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍扫描：用字典 `char_dict` 记录每个字符的次数',
              '把字典的 `(字符, 次数)` 按次数降序排序',
              '依次把 `char * cnt` 拼进结果，次数大的先拼'],
        summary=['时间 `O(n + k log k)`，`k` 是不同字符的个数',
                 '排序的 `key` 是次数 `d[1]`，不是字符本身',
                 '次数相同的字符顺序题目不限制，任意一种都对',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改'],
    ),
)
