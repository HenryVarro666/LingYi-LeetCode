def _cur(S):
    if 'string' not in S:
        return None
    return S['strs'].index(S['string'])


def _cnt_color(S, i, v):
    return 'cyan' if v else None


def _key_text(S):
    if 'str_list' not in S:
        return '每个字符串：数字母 → 拼 key → 分组'
    letters = '  '.join(f"`{chr(i + 97)}:{c}`" for i, c in enumerate(S['str_list']) if c)
    k = S.get('key')
    tail = f"  →  key = `\"{k}\"`" if k is not None else ''
    return f"非零计数 {letters}{tail}"


def _check(S, B, ret):
    if S.key not in S.res_dict:
        return f'key `"{S.key}"` 第一次出现：还没有对应的 list'
    return f'key `"{S.key}"` 已存在：`{S.res_dict[S.key]}` 和它是异位词'


CONFIG = dict(
    num=49, title='字母异位词分组', difficulty='Medium', category='哈希',
    author='yiduobo', technique='字母计数作 key · 哈希表分组',
    code='''
class Solution(object):
    def groupAnagrams(self, strs):
        res_dict = {}

        for string in strs:
            str_list = [0] * 26
            for char in string:
                str_list[ord(char) - 97] += 1
            key = ''
            for index, count in enumerate(str_list):
                if count > 0:
                    key = key + chr(index + 97) + str(count)
            if key not in res_dict:
                res_dict[key] = []
            res_dict[key].append(string)

        return list(res_dict.values())
''',
    call='Solution().groupAnagrams(["eat", "tea", "ana", "naa"])',
    expect=[['eat', 'tea'], ['ana', 'naa']],
    skip=['for char in string', 'for index, count', 'if count > 0'],
    views=[
        dict(type='array', var='strs', pointers={_cur: 'yellow'}, pointer_labels={_cur: 'string'}, h=230, cell=100,
             color=lambda S, i, v: 'green' if 'res_dict' in S and any(v in g for g in S['res_dict'].values()) else None,
             label='strs（绿 = 已分组）'),
        dict(type='array', var='str_list', color=_cnt_color, cell=37, h=150,
             label='str_list：26 个计数器（下标 = ord(char) − 97，0 是 a，25 是 z）'),
        dict(type='text', fn=_key_text, size=27),
        dict(type='map', var='res_dict', font=28, h=200,
             fmt=lambda k, v: f'"{k}" → [{", ".join(v)}]',
             label='res_dict：计数 key → 同组字符串'),
    ],
    watch=[('string', 'string', 'yellow'), 'char', ('key', 'key', 'cyan')],
    captions={
        'res_dict = {}': '`res_dict`：==key 是"字母+次数"拼成的串，value 是这一组的字符串==',
        'for string in strs': lambda S, B, r: (f'处理下一个字符串 `"{S.string}"`' if 'string' not in B or B.string != S.string
                                               else 'for 循环结束：全部分组完毕'),
        'str_list = [0] * 26': lambda S, B, r: ('26 个计数器清零：题目只包含小写字母，26 个就够' if S.string == S.strs[0] else '计数器清零'),
        'str_list[ord(char) - 97] += 1': lambda S, B, r: (f'`"{S.char}"` → 下标 `ord("{S.char}") − 97 = {ord(S.char) - 97}`，计数 +1 → `{S.str_list[ord(S.char) - 97]}`'
                                                          if S.string == S.strs[0] else f'`"{S.char}"` → 下标 `{ord(S.char) - 97}`，计数 → `{S.str_list[ord(S.char) - 97]}`'),
        "key = ''": lambda S, B, r: ('按 a→z 扫 26 个计数器，把出现过的字母连同次数拼进 key' if S.string == S.strs[0] else '重新拼 key'),
        'key = key + chr': '`{chr(index + 97)}` 出现 `{count}` 次 → key 拼成 `"{key}"`',
        'if key not in res_dict': _check,
        'res_dict[key] = []': '为新 key `"{key}"` 建一个空 list',
        'res_dict[key].append(string)': '`"{string}"` 加入 key `"{key}"` 对应的 list → `{res_dict[key]}`',
        'return list(': '按 key 输出对应的 list：共 =={len(res_dict)} 组==',
    },
    cards=dict(
        one_liner='数一数每个字母出现几次，拼成 key 来分组',
        complexity='时间 `O(n(m+26))`，空间 `O(nm)`',
        problem=['把==字母异位词==（字母相同、只是顺序不同）分到同一组，组的顺序随意',
                 '示例：`["eat","tea","tan","ate","nat","bat"]`',
                 '→ `[["bat"],["nat","tan"],["ate","eat","tea"]]`',
                 '本视频：`["eat","tea","ana","naa"]` → 两组'],
        quote='对于strs中的每个字符串，可以先==统计出当前字符串中每个字母出现的次数==，然后用这个次数作为dict的key来将异位词加入到key所对应的list当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['异位词 ⇔ ==每个字母的出现次数都相同==',
              '`ord(char) − 97` 把 a–z 映射到 0–25（97 是 a 的 ASCII 码）',
              '计数拼成 `"a1e1t1"` 这样的串作 key：不用排序'],
        summary=['时间 `O(n·(m+26))`：每个串计数 `O(m)`，拼 key 扫 26 个计数器',
                 'key 必须带上字母：只拼次数的话，`"ab"` 和 `"cd"` 都会变成 `"11"`',
                 '原文为 Python 2：返回的 `.values()` 已改为 `list(...)`；删去了文档字符串',
                 '对比灵神：灵神用==排序后的串==作 key，yiduobo 用==字母计数==作 key'],
    ),
)
