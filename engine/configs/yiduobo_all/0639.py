CONFIG = dict(
    num=639, title='解码方法 2', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='线性 DP · 三变量滚动',
    tags=[],
    code='''
class Solution(object):
    def numDecodings(self, s):

        l = len(s)
        mod = 10 ** 9 + 7
        a = 1
        if s[0] == '*':
            b = 9
        elif s[0] == '0':
            b = 0
        else:
            b = 1

        for index in range(1, l):
            if s[index] == '*':
                c = b * 9 % mod
                if s[index - 1] == '*':
                    c = (c + a * 15) % mod
                elif s[index - 1] == '1':
                    c = (c + a * 9) % mod
                elif s[index - 1] == '2':
                    c = (c + a * 6) % mod
            else:
                if s[index] == '0':
                    c = 0
                else:
                    c = b

                if s[index - 1] == '*':
                    if s[index] <= '6':
                        c = (c + a * 2) % mod
                    else:
                        c = (c + a) % mod
                elif s[index - 1] == '1':
                    c = (c + a) % mod
                elif s[index - 1] == '2' and s[index] <= '6':
                    c = (c + a) % mod

            a = b
            b = c

        return b
''',
    call="Solution().numDecodings('1*2*')",
    expect=288,
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, label='s（* 可以是 1~9，不含 0）', h=200),
        dict(type='text', fn=lambda S: f"`a` = =={S['a']}==（f[i-2]），`b` = =={S['b']}==（f[i-1]）" + (f"，`c` = =={S['c']}==（f[i]）" if 'c' in S and 'index' in S and S['_line'] > 20 else '') if 'a' in S and 'b' in S else '', size=32, h=110),
    ],
    watch=[('index', 'index', 'blue'), ('a', 'a', 'cyan'), ('b', 'b', 'orange'), ('c', 'c', 'green')],
    captions={
        'mod = 10': '方案数会很大，每步都对 `10^9+7` 取模',
        'a = 1': '`a` 代表 f[-1] 的“空串”：只有 1 种解码方式',
        "if s[0] == '*'": '先处理第一个字符：`*` 可以是 1~9，有 9 种',
        'b = 9': '首字符是 `*`：9 种，==不能表示 0==',
        'b = 0': '首字符是 `0`：无法单独解码，0 种',
        'b = 1': '首字符是 1~9：唯一 1 种',
        "if s[index] == '*'": lambda S, B, r: f"当前字符 `{S.s[S.index]}`：" + ('是 `*`，单独解码有 9 种' if S.s[S.index] == '*' else '是数字，分情况'),
        'c = b * 9': '`*` 单独解码：`c = b × 9 = {c}`（前一位的每种方案都能接 9 种）',
        "c = (c + a * 15)": '前面也是 `*`：`**` 组合有 11~19（9 个）和 21~26（6 个）共 15 种 → `c` += `a × 15` = {c}',
        "c = (c + a * 9)": '前一位是 1：`1*` 可以是 11~19，9 种 → `c` += `a × 9` = {c}',
        "c = (c + a * 6)": '前一位是 2：`2*` 只能是 21~26，6 种 → `c` += `a × 6` = {c}',
        'c = 0': '当前字符是 `0`：不能单独解码，`c = 0`，只能指望和前一位组合',
        'c = b': '当前字符是 1~9：单独解码，方案数沿用 `b` → `c = {c}`',
        "c = (c + a * 2)": '前面是 `*` 且当前 ≤ 6：`*` 可当 1 或 2，组合有 2 种 → `c` += `a × 2` = {c}',
        "c = (c + a) % mod": '组合解码只有 1 种方式 → `c` += `a` = {c}',
        'a = b': '滚动：`a` ← 旧的 `b` = {a}',
        'b = c': '滚动：`b` ← `c` = {b}',
        'return b': '最后一个状态就是答案：`{b}` 种',
        "if s[index - 1] == '*'": lambda S, B, r: f"前一位 `{S.s[S.index-1]}`，看能不能和当前 `{S.s[S.index]}` 组成 1~26",
        "s[index] <= '6'": lambda S, B, r: f"当前 `{S.s[S.index]}` {'≤' if S.s[S.index] <= '6' else '>'} `'6'` → " + ('`*` 可取 1、2，共 2 种' if S.s[S.index] <= '6' else '`*` 只能取 1，共 1 种'),
    },
    cards=dict(
        one_liner='f[i] 只依赖前两项：用 a、b、c 三个变量滚动',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母 A~Z 对应 1~26，字符串里的 `*` 可以代表 ==1~9==（不含 0）',
                 '求整个字符串有多少种解码方式，结果对 `10^9+7` 取模',
                 '本视频：`s = "1*2*"`'],
        quote='题目描述中说到星号可以表示1到9这些数字，那么星号是不能表示0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 表示前 i 个字符的解码方法数：先看==单独解码==当前字符，再看==和前一位组合==',
              '当前是 `*`：单独 9 种；前一位 `*` 组合 15 种、`1` 组合 9 种、`2` 组合 6 种',
              '当前是数字：`0` 不能单独；前一位 `*`、`1`、`2` 按能否凑成 ≤ 26 讨论'],
        summary=['时间 `O(n)`，空间 `O(1)`：f 只依赖前两项，用 a、b、c 滚动',
                 '`*` 不能是 0；`**` 共 15 种（11~19 与 21~26）',
                 '`0` 只能和前一位的 `1`、`2`（或 `*`）组合，否则整体为 0',
                 '每一步别忘了对 `10^9+7` 取模'],
    ),
)
