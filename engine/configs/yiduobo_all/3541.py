CONFIG = dict(
    num=3541, title='找到频率最高的元音和辅音', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表计数 · 元音辅音分别取最大',
    code='''
class Solution(object):
    def maxFreqSum(self, s):
        
        freq = {}
        vowel = set(['a', 'e', 'i', 'o', 'u'])
        max_v = 0
        max_c = 0
        for char in s:
            freq[char] = freq.get(char, 0) + 1
            if char in vowel:
                max_v = max(max_v, freq[char])
            else:
                max_c = max(max_c, freq[char])
        
        return max_v + max_c
''',
    call="Solution().maxFreqSum('successes')",
    expect=6,
    skip=['freq = {}', 'max_c = 0'],
    views=[
        dict(type='string', var='s', label='s（框 = 当前字符）', cell=80, h=150,
             pointers={'(sum(freq.values()) - 1) if _line > 8 else sum(freq.values())': 'blue'},
             pointer_labels={'(sum(freq.values()) - 1) if _line > 8 else sum(freq.values())': 'char'}),
        dict(type='map', var='freq', label='freq（字符 → 次数）', fmt=lambda k, v: f"'{k}': {v}", h=250, font=30),
        dict(type='set', var='vowel', label='vowel（元音集合）', fmt=lambda x: f"'{x}'", h=130),
        dict(type='text', h=100, size=32, fn=lambda S: f"元音最大 `max_v` = =={S['max_v']}==　辅音最大 `max_c` = =={S['max_c']}==" if 'max_v' in S else ''),
    ],
    watch=['char', ('max_v', 'max_v', 'orange'), ('max_c', 'max_c', 'cyan')],
    captions={
        'vowel = set': '元音集合，判断一个字符是不是元音只要 `char in vowel`',
        'max_v = 0': '`max_v` 记元音最大频率，`max_c` 记辅音最大频率，初值 0（没有时按 0 算）',
        'for char in s': lambda S, B, r: ('遍历结束' if 'char' in S and sum(S.freq.values()) == len(S.s) else f'取字符 `{S.char!r}`'),
        'freq[char] = freq.get': '`{char!r}` 出现次数 +1 → `freq[{char!r}] = {freq[char]}`',
        'if char in vowel': lambda S, B, r: (f'`{S.char!r}` 是元音 → 去更新 `max_v`' if S.char in S.vowel else f'`{S.char!r}` 不是元音，是辅音 → 去更新 `max_c`'),
        'max_v = max': '`max_v = max({B.max_v}, {freq[char]}) = {max_v}`',
        'max_c = max': '`max_c = max({B.max_c}, {freq[char]}) = {max_c}`',
        'return max_v + max_c': '元音最大 `{max_v}` + 辅音最大 `{max_c}` = =={max_v + max_c}==',
    },
    cards=dict(
        one_liner='用哈希表计数，每数一个字符就更新它所属类别的最大频率',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小写字符串 `s`，找出现频率最高的==元音==和最高的==辅音==',
                 '返回两个频率之和，缺少某一类时按 0 计',
                 '示例：`"successes"` → 元音 `e` 2 次，辅音 `s` 4 次 → `6`'],
        quote='使用哈希表freq记录每种字符出现的次数，然后一趟遍历。对于当前字符char，先更新freq[char]，接下来若当前字符是元音，则使用freq[char]更新元音的最大频率max_v，否则使用freq[char]更新辅音的最大频率max_c。',
        quote_src='—— yiduobo 题解原文',
        idea=['先更新 `freq[char]`，得到这个字符最新的出现次数',
              '再按元音 / 辅音分别用这个次数去更新最大值',
              '一遍遍历完成，不用再扫一次哈希表'],
        summary=['时间 `O(n)`，字符集只有 26 个，空间 `O(1)`',
                 '易错：先更新 `freq`，再用更新后的值比较',
                 '没有元音（或辅音）时 `max_v`（`max_c`）保持 0，正好符合题意',
                 '原文为 Python 2 风格，本题只删去了类型说明，代码未改',
                 '对比灵神：灵神用数组 `cnt` 并用位掩码判元音，这里用字典和集合'],
    ),
)
