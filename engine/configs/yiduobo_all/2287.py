CONFIG = dict(
    num=2287, title='重排字符形成目标字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='手写计数字典 · 取最小',
    tags=[],
    code='''
class Solution(object):
    def rearrangeCharacters(self, s, target):

        char_cnt_s = {}
        for char in s:
            char_cnt_s[char] = char_cnt_s.get(char, 0) + 1
        
        char_cnt_target = {}
        for char in target:
            char_cnt_target[char] = char_cnt_target.get(char, 0) + 1
        
        res = len(s)
        for char, target_cnt in char_cnt_target.items():
            res = min(res, char_cnt_s.get(char, 0) // target_cnt)

        return res
''',
    call="Solution().rearrangeCharacters('aabbbcc', 'abb')",
    expect=1,
    views=[
        dict(type='string', var='s', label='s', cell=90, h=140, pointers={}),
        dict(type='string', var='target', label='target', cell=90, h=140),
        dict(type='map', var='char_cnt_s', label='char_cnt_s', fmt=lambda k, v: f"'{k}': {v}", h=140, font=32),
        dict(type='map', var='char_cnt_target', label='char_cnt_target', fmt=lambda k, v: f"'{k}': {v}", h=140, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"目前最多 `res = {S['res']}` 份" if 'res' in S else '')),
    ],
    watch=[('char', 'char', 'blue'), ('target_cnt', 'target_cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'char_cnt_s[char] =': '`s` 里 `{char!r}` 又多一个：`char_cnt_s[{char!r}] = {char_cnt_s[char]}`',
        'char_cnt_target[char] =': '`target` 里 `{char!r}` 又多一个：`char_cnt_target[{char!r}] = {char_cnt_target[char]}`',
        'res = len(s)': '`res` 先取一个足够大的数（`len(s)`），后面只会变小',
        'res = min': '`{char!r}`：s 里有 `{char_cnt_s.get(char, 0)}` 个，一份要 `{target_cnt}` 个 → 够 `{char_cnt_s.get(char, 0) // target_cnt}` 份；`res = min({B.res}, …)` = =={res}==',
        'return res': '最缺的字母限制了份数，答案 `{res}`',
    },
    cards=dict(
        one_liner='字符数量够不够，决定能拼几份',
        complexity='时间 `O(n+m)`，空间 `O(|Σ|)`',
        problem=['从 `s` 里取字符并重排，最多能拼出几份 `target`',
                 '示例：`s = "abcba", target = "abc"` → `1`',
                 '本视频：`s = "aabbbcc", target = "abb"` → `1`'],
        quote='只需要需要的字符数量足够，就能拼凑出目标字符串。……计算s中相同的字符足够几个target使用，取其中的最小值就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['可以随意选、随意排，所以只比较字符数量',
              '先用字典分别数出 s 和 target 的字符个数',
              '遍历 target 的每个字符，算 s 够用几份，==取最小值=='],
        summary=['时间 `O(n+m)`，空间 `O(|Σ|)`',
                 '`char_cnt_s.get(char, 0)`：s 里没有的字符按 0 个算，结果就是 0 份',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：他用 `Counter`，一行写完；这里手写计数字典'],
    ),
)
