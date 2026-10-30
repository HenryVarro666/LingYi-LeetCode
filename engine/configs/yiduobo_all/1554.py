CONFIG = dict(
    num=1554, title='只有一个不同字符的字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='抹去一位 + 双模数哈希',
    tags=['字符串哈希'],
    code='''
class Solution(object):
    def differByOne(self, dict):

        mod1 = 10**9 + 7
        mod2 = 2147483647

        pow1 = [1]
        pow2 = [1]

        m = len(dict)
        n = len(dict[0])

        for index in range(n):
            pow1.append(pow1[-1] * 27 % mod1)
            pow2.append(pow2[-1] * 27 % mod2)
        
        h = set()
        for word in dict:
            v1 = v2 = 0
            for index, char in enumerate(word):
                v1 = (v1 + (ord(char) - 96) * pow1[n - index - 1]) % mod1
                v2 = (v2 + (ord(char) - 96) * pow2[n - index - 1]) % mod2
            
            for index, char in enumerate(word):
                t1 = v1 - (ord(char) - 96) * pow1[n - index - 1] % mod1
                if t1 < 0:
                    t1 += mod1
                
                t2 = v2 - (ord(char) - 96) * pow2[n - index - 1] % mod2
                if t2 < 0:
                    t2 += mod2
                
                if (t1, t2) in h:
                    return True
                
                h.add((t1, t2))
        
        return False
''',
    call='Solution().differByOne(["abcd", "acbd", "aacd"])',
    expect=True,
    views=[
        dict(type='array', var='dict', h=120, cell=100, label='dict（字符串列表）',
             pointers={}),
        dict(type='string', var='word', h=190, pointers={'index': 'blue'}),
        dict(type='text', fn=lambda S: (f"抹去第 {S['index']} 位 → `{S['word'][:S['index']]}_{S['word'][S['index']+1:]}`，`h` 里已有 {len(S['h'])} 个哈希") if 'word' in S and 'index' in S else ''),
        dict(type='set', var='h', h=200, fmt=lambda x: f'({x[0] % 1000}, {x[1] % 1000})…'),
    ],
    watch=['n', ('word', 'word', 'blue'), 'index', 't1', 't2', 'v1'],
    skip=['pow2.append'],
    captions={
        'mod2 = ': '第二个模数：两套哈希同时撞才算相同',
        'pow2 = [1]': '`pow2` 同理，对应第二个模数',
        'mod1 = ': '准备两个模数，两套哈希一起比，降低冲突风险',
        'pow1 = [1]': '`pow1[k] = 27^k`：把字符串当 27 进制数',
        'n = len(dict[0])': '`n = {n}`：每个字符串等长；`a~z` 占 `1~26`，`0` 留给被抹去的位置',
        'pow1.append': '`pow1` 长度 → {len(pow1)}',
        'h = set()': '`h` 存所有「抹去一位」后字符串的哈希',
        'v1 = v2 = 0': '开始处理 `{word}`，哈希清零',
        'v1 = (v1 + ': '把 `{char}` 的值 `{ord(char) - 96}` 乘上位权加进整体哈希：`v1 = {v1}`',
        'v2 = (v2 + ': '另一个模数同样累加：`v2 = {v2}`',
        't1 = v1 - ': '抹去第 `{index}` 位（`{char}`）：整体哈希减去它的贡献 → `t1 = {t1}`',
        't2 = v2 - ': '另一个模数同样减 → `t2 = {t2}`',
        'if t1 < 0': '减完可能为负，`t1 = {t1}`',
        'if t2 < 0': '`t2 = {t2}`',
        't1 += mod1': '补回模数，保证非负：`t1 = {t1}`',
        't2 += mod2': '补回模数：`t2 = {t2}`',
        'if (t1, t2) in h': lambda S, B, r: '`(t1, t2)` 在 h 里吗？' + ('在 → 之前有个字符串抹去某一位后和它一样！' if (S.t1, S.t2) in S.h else '不在 → 把它记下来'),
        'return True': '找到只差一个字符的两个字符串 → 返回 `True`',
        'h.add': '记下 `{word}` 抹去第 `{index}` 位的哈希，`h` 共 {len(h)} 个',
        'return False': '所有字符串都没有撞上 → `False`',
    },
    cards=dict(
        one_liner='把每个字符「抹成空」，两个字符串抹同一位后相同，就只差一个字符',
        complexity='时间 `O(m·n)`，空间 `O(m·n)`',
        problem=['给一组等长小写字符串 `dict`，问是否存在两个串，恰好只有一个位置字符不同',
                 '示例：`["abcd","acbd","aacd"]` → `True`',
                 '`abcd` 与 `aacd` 只有第 1 位不同'],
        quote='这里的抹去指的是用一个空值来填充这个位置而不是直接从字符串中删去。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个长 `n` 的字符串有 `n` 种抹法；抹去同一位后相同 ⇔ 只差这一位',
              '作者把字符串看成 27 进制数（`a~z` 为 `1~26`，`0` 代表空），整体哈希减去一位的贡献就得到抹去后的哈希',
              '哈希进集合；用两个模数分别算，降低冲突'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '关键：先查再加，同一个字符串自己的抹法不会互相命中',
                 '哈希有极小冲突概率，所以用了双模数',
                 '题意说明：库里无题面，按 yiduobo 文章与 LeetCode 原题整理'],
    ),
)
