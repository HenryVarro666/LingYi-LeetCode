STR = 'abacabd'


def _color(S, i, v):
    d = S.get('char_dict') or {}
    if 'index' in S and i == S['index'] and S.get('res') is None:
        return 'yellow'
    if S.get('res') is not None and i == S['res']:
        return 'green'
    if v in d and d[v] == len(S['s']) and i <= S.get('index', -1):
        return 'red'
    return None


CONFIG = dict(
    num=387, title='字符串中的第一个唯一字符', difficulty='Easy', category='哈希',
    author='yiduobo', technique='一边扫描统计 · 重复字符的位置记为 len(s)',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def firstUniqChar(self, s):
        if not s:
            return -1

        char_dict = {}
        for index, char in enumerate(s):
            if char not in char_dict:
                char_dict[char] = index
            else:
                char_dict[char] = len(s)

        res = min(char_dict.values())
        if len(s) == res:
            return -1
        return res
''',
    call=f'Solution().firstUniqChar({STR!r})',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (
            f"`min(char_dict.values())` = `min({list(S['char_dict'].values())})` = =={S['res']}=="
            if S.get('res') is not None else
            f"`char_dict[c]`：只出现一次 → ==它的下标==；重复出现 → `len(s) = {len(S['s'])}`"), size=28),
        dict(type='string', var='s', pointers={'index': 'yellow'}, color=_color, h=200),
        dict(type='map', var='char_dict', label='char_dict（字符 → 唯一时的下标 / 重复时记 len(s)）', h=150, font=30,
             fmt=lambda k, v: f"'{k}': {v}" + ('（重复）' if v == len(STR) else '')),
    ],
    watch=[('index', 'index', 'yellow'), ('char', 'char'), ('len(s)', 'len(s)'), ('res', 'res', 'green')],
    captions={
        'if not s': '空串没有任何字符 → 直接返回 `-1`；`s = "{s}"` 非空，继续',
        'char_dict = {}': '`char_dict`：记录每个字符==第一次出现的位置==',
        'for index, char in enumerate': lambda S, B, ret: (
            f"扫描 `s[{S.index}] = '{S.char}'`" if S.get('index') != B.get('index') or 'index' not in B
            else '扫描结束，每个字符都统计好了'),
        'if char not in char_dict': lambda S, B, ret: (
            f"`'{S.char}'` 第一次出现" if S.char not in B.char_dict
            else f"`'{S.char}'` ==之前出现过==（记录为 {S.char_dict[S.char]}）"),
        'char_dict[char] = index': "记下位置：`char_dict['{char}'] = {index}`",
        'char_dict[char] = len(s)': lambda S, B, ret: (
            f"重复了 → `char_dict['{S.char}'] = len(s) = {len(S.s)}`：==比任何下标都大==，取最小值时不会选到它"
            if list(B.char_dict.values()).count(len(S.s)) == 0
            else f"`'{S.char}'` 重复了 → `char_dict['{S.char}'] = {len(S.s)}`" if B.char_dict[S.char] != len(S.s)
            else f"`'{S.char}'` 又重复 → 仍记 `{len(S.s)}`"),
        'res = min': '所有值里最小的：`res = {res}` → 下标最小的唯一字符',
        'if len(s) == res': lambda S, B, ret: (
            '最小值都是 `len(s)`：所有字符都重复 → 返回 `-1`' if S.res == len(S.s)
            else f'`res = {S.res} ≠ len(s) = {len(S.s)}`：存在唯一字符'),
        'return res': "第一个唯一字符是 `s[{res}] = '{s[res]}'`，返回 =={res}==",
    },
    max_steps=50,
    cards=dict(
        one_liner='一趟扫描：首次出现记下标，再次出现改成 len(s)，最后取最小值',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（字符集大小）',
        problem=['给定字符串 `s`，找到它的==第一个不重复的字符==，返回它的下标；不存在则返回 `-1`',
                 '示例：`"leetcode"` → `0`，`"loveleetcode"` → `2`，`"aabb"` → `-1`',
                 f'本视频：`"{STR}"` → `3`（`\'c\'`）'],
        quote='比较基础的题目，==一边扫描统计即可==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`char_dict[c]`：`c` 只出现过一次时存它的下标',
              '再次出现就改成 `len(s)`：一个==比所有下标都大==的「无效值」',
              '最后 `min(values)` 就是第一个唯一字符；等于 `len(s)` 说明没有'],
        summary=['时间 `O(n)`；字典最多 26 个键，取 `min` 很快',
                 '用 `len(s)` 当「重复」标记，省去第二趟按原串扫描',
                 '别忘了判断 `res == len(s)`（全部重复）→ 返回 `-1`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '常见写法：先 `Counter(s)` 计数，再扫一遍找第一个次数为 1 的'],
    ),
)
