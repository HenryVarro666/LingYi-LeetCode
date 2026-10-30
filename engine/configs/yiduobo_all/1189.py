CONFIG = dict(
    num=1189, title='“气球” 的最大数量', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表计数 · 取最小',
    code='''
class Solution(object):
    def maxNumberOfBalloons(self, text):

        char_dict = {}
        for char in text:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        res = char_dict.get('b', 0)
        res = min(res, char_dict.get('a', 0))
        res = min(res, char_dict.get('l', 0) // 2)
        res = min(res, char_dict.get('o', 0) // 2)
        res = min(res, char_dict.get('n', 0))

        return res
''',
    call='Solution().maxNumberOfBalloons("loonbalxballpoon")',
    expect=2,
    views=[
        dict(type='string', var='text', label='text', cell=60, h=170, pointers={'__i': 'blue'}),
        dict(type='map', var='char_dict', label='char_dict', fmt=lambda k, v: f"'{k}': {v}", h=200, font=30),
        dict(type='text', h=100, size=34, fn=lambda S: f"当前 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=[('char', 'char', 'blue'), ('res', 'res', 'green')],
    captions={
        'char_dict = {}': '空字典，用来数每个字母出现几次',
        'for char in text': lambda S, B, r: ('字符都数完了' if sum(S.char_dict.values()) == len(S.text) else f'取下一个字符 `{S.char!r}`'),
        'char_dict[char] =': '`{char!r}` 次数加一 → `{char_dict[char]}`',
        "res = char_dict.get('b'": '先用 b 初始化：1 个气球要 1 个 b → `res = {res}`',
        "min(res, char_dict.get('a'": '1 个气球要 1 个 a，有 `{char_dict.get("a", 0)}` 个 → `res = min({B.res}, {char_dict.get("a", 0)}) = {res}`',
        "min(res, char_dict.get('l'": '1 个气球要 2 个 l，有 `{char_dict.get("l", 0)}` 个，够 `{char_dict.get("l", 0)//2}` 个 → `res = {res}`',
        "min(res, char_dict.get('o'": '1 个气球要 2 个 o，有 `{char_dict.get("o", 0)}` 个，够 `{char_dict.get("o", 0)//2}` 个 → `res = {res}`',
        "min(res, char_dict.get('n'": '1 个气球要 1 个 n，有 `{char_dict.get("n", 0)}` 个 → `res = {res}`',
        'return res': '各字母能供的气球数取最小 → ==`{res}`==',
    },
    cards=dict(
        one_liner='每个字母最多供几个气球，取其中最小的',
        complexity='时间 `O(n)`，空间 `O(1)`（字母表大小）',
        problem=['用 `text` 里的字母拼尽可能多的 `"balloon"`，每个字母最多用一次',
                 '示例：`"loonbalxballpoon"` → `2`',
                 '一个气球：1 个 b、1 个 a、2 个 l、2 个 o、1 个 n'],
        quote='可以统计各个字母出现的次数，并计算该字母最多可以供几个气球使用，然后取其中的最小值即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典数出每个字母的次数',
              '再逐个字母算“最多供几个”：l、o 要除以 2',
              '`res` 从 b 起步，依次和其他字母取 `min`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：l、o 要除以 2；用 `.get(x, 0)` 防止字母缺失',
                 '原文为 Python 2 写法，整数除法 `/ 2` 已改为 `// 2`',
                 '与灵神对比：灵神用 Counter 一行 min，yiduobo 逐个字母更新 res'],
    ),
)
