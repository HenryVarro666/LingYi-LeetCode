CONFIG = dict(
    num=1781, title='所有子字符串美丽值之和', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举子串 + 前缀计数',
    tags=[],
    code='''
class Solution(object):
    def beautySum(self, s):

        cnt_list = [{}]
        for char in s:
            cnt_list.append(cnt_list[-1].copy())
            cnt_list[-1][char] = cnt_list[-1].get(char, 0) + 1

        n = len(s)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                ma = 0
                mi = j - i + 1
                for index in range(26):
                    char = chr(index + 97)
                    cnt = cnt_list[j + 1].get(char, 0) - cnt_list[i].get(char, 0)
                    ma = max(ma, cnt)
                    if cnt > 0:
                        mi = min(mi, cnt)
                
                res += ma - mi
        
        return res
''',
    call='Solution().beautySum("aabcb")',
    expect=5,
    views=[
        dict(type='string', var='s', label='s', h=170,
             window=('i', 'j'),
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='table', var=lambda S: [[v for v in (d.get(chr(97 + k), 0) for k in range(4))] for d in S['cnt_list']],
             label='前缀计数：第 k 行 = s[0:k] 中 a / b / c / d 的个数', h=300,
             cols=['a', 'b', 'c', 'd'],
             color=lambda S, i, j, v: 'blue' if 'i' in S and i == S['i'] and 'j' in S else ('pink' if 'j' in S and i == S['j'] + 1 else None)),
    ],
    watch=['i', 'j', ('ma', 'ma', 'green'), ('mi', 'mi', 'orange'), ('res', 'res', 'cyan')],
    skip=['char = chr', 'cnt_list.append'],
    max_steps=90,
    captions={
        'cnt_list = [{}]': '`cnt_list[k]` 存 `s[0:k]` 里每个字符的个数，开头是空前缀',
        'cnt_list[-1][char] =': '读入 `{char}`，在上一个前缀的拷贝上给它加一',
        'for i in range': '枚举子串左端点 `i`（长度至少为 2 才可能有差值）',
        'for j in range': '枚举右端点 `j`，子串是 `s[{i}..{j}]`',
        'ma = 0': '`ma` 记最多出现次数，`mi` 先设成子串长度 `{mi}`（上界）',
        'cnt = cnt_list': '区间计数 = 前缀 `j+1` 减前缀 `i`：字符 `{char}` 出现 `{cnt}` 次',
        'ma = max': '最大次数 `ma = {ma}`',
        'if cnt > 0': '`cnt = {cnt}`：只有出现过的字符才参与最小值',
        'mi = min': '最小次数 `mi = {mi}`',
        'res += ma - mi': '这个子串美丽值 = `{ma} - {mi}` = {ma - mi}，累计 `res = {res}`',
        'return res': '所有子串美丽值之和 = `{res}`',
    },
    cards=dict(
        one_liner='字符串不长，直接枚举子串，用前缀计数求区间频次',
        complexity='时间 `O(26·n²)`，空间 `O(26·n)`',
        problem=['美丽值 = 子串中出现次数最多的字符次数 − 最少的字符次数',
                 '求 `s` 所有子串的美丽值之和',
                 '示例：`"aabcb"` → `5`'],
        quote='因此可以直接枚举所有的子字符串，然后计算字符串中各个字符的数量从而得出该字符串的美丽值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt_list[k]` 保存前 k 个字符的计数字典',
              '`[l, r]` 中某字符个数 = `[0, r]` 的个数 − `[0, l-1]` 的个数',
              '枚举 `(i, j)`，再扫 26 个字母得 `ma` 与 `mi`，累加差值'],
        summary=['时间 `O(26·n²)`，空间 `O(26·n)`',
                 '`mi` 初值取子串长度，作为 “最小值” 的上界',
                 '只有 `cnt > 0` 的字符才能更新 `mi`，否则最小值会变成 0',
                 '长度为 1 的子串美丽值恒为 0，所以 `i` 只需枚举到 `n-2`',
                 '原文为 Python 2 风格，在 Python 3 下可直接运行，代码未改'],
    ),
)
