CONFIG = dict(
    num=1903, title='字符串中的最大奇数', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='从后往前删偶数位（Go 原文转写）',
    tags=['贪心与思维', '难度分 1249'],
    code='''
class Solution:
    def largestOddNumber(self, s: str) -> str:
        while s != "" and ord(s[len(s) - 1]) & 1 == 0:
            s = s[:len(s) - 1]
        return s
''',
    call='Solution().largestOddNumber("5364280")',
    expect='53',
    views=[
        dict(type='string', var='s', label='s（最后一位决定奇偶）', cell=96,
             pointers={'len(s) - 1': 'pink'}, pointer_labels={'len(s) - 1': '末位'},
             color=lambda S, k, v: ('green' if int(v) % 2 else 'red') if k == len(S['s']) - 1 else None),
        dict(type='text', fn=lambda S: (f"末位 `{S['s'][-1]}` 是==奇数==，停下" if S['s'] and int(S['s'][-1]) % 2
                                        else (f"末位 `{S['s'][-1]}` 是偶数，删掉" if S['s'] else '')), size=30),
    ],
    watch=[('s', 's', 'blue'), ('len(s)', 'len(s)')],
    captions={
        'while s': lambda S, B, r: (f"`s` 非空，末位 `{S.s[-1]}` 是偶数 → 进入循环删掉它" if S.s and ord(S.s[-1]) & 1 == 0
                                    else (f"末位 `{S.s[-1]}` 是奇数 → 停止" if S.s else '`s` 已空 → 停止')),
        's = s[:': '删掉末位，`s` 变成 `"{s}"`',
        'return s': '剩下的 `"{ret}"` 以奇数结尾，又是最长的前缀 → 就是最大的奇数',
    },
    cards=dict(
        one_liner='奇数看末位：把末尾的偶数位全删掉',
        complexity='时间 `O(n)`，空间 `O(1)`（切片开销忽略）',
        problem=['`num` 是一个大整数字符串，在它的所有子串中找==值最大的奇数==',
                 '没有奇数则返回 `""`',
                 '示例：`"52"` → `"5"`；`"4206"` → `""`'],
        quote='由于奇数的最后一个数字是奇数，从后往前找到第一个奇数数字，删掉后面的字符，剩下的就是最大的奇数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数 ⇔ 末位是奇数；位数越多数值越大',
              '所以答案一定是 `s` 的某个前缀：取最长的、以奇数结尾的那个',
              '从末尾开始，遇到偶数就删，遇到奇数就停'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（Go 的 `s[i]&1` 写成 `ord(s[i]) & 1`，数字字符的奇偶和数字一致）',
                 '原文另有一行写法：`s[:strings.LastIndexAny(s, "13579")+1]`，思路相同',
                 '全是偶数时 `s` 删到空串，正好返回 `""`',
                 '易错：只删末尾，不能删中间，也不能转成整数（长度可达 10^5）'],
    ),
)
