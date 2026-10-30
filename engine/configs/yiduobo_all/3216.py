def _txt(S):
    if 'i' not in S:
        return '从头扫描，遇到的第一对可交换的相邻数字就交换并返回'
    return f"看相邻两位 `s[{S['i'] - 1}] = {S['s'][S['i'] - 1]}`、`s[{S['i']}] = {S['s'][S['i']]}`"


CONFIG = dict(
    num=3216, title='交换后字典序最小的字符串', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='高位优先 · 一趟遍历交换',
    tags=['灵神题单', '贪心与思维', '难度分 1243'],
    code='''
class Solution(object):
    def getSmallestString(self, s):

        for i in range(1, len(s)):
            if (int(s[i]) + int(s[i - 1])) % 2 == 0 and s[i] < s[i - 1]:
                return s[:i - 1] + s[i] + s[i - 1] + s[i + 1:]
        
        return s
''',
    call='Solution().getSmallestString("2457320")',
    expect='2453720',
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='s', pointers={'i-1': 'blue', 'i': 'pink'}, window=('i-1', 'i'), label='s（蓝 = 前一位，粉 = 当前位）', h=240),
    ],
    watch=[('i', 'i', 'cyan')],
    captions={
        'for i in range': '`i = {i}`：比较 `s[{i-1}] = {s[i-1]}` 和 `s[{i}] = {s[i]}`',
        'if (int': lambda S, B, r: (
            f'两数之和 `{int(S["s"][S["i"]]) + int(S["s"][S["i"] - 1])}` 是偶数（奇偶相同），且 `{S["s"][S["i"]]} < {S["s"][S["i"] - 1]}` → ==在高位换，字典序变小=='
            if (int(S['s'][S['i']]) + int(S['s'][S['i'] - 1])) % 2 == 0 and S['s'][S['i']] < S['s'][S['i'] - 1]
            else ('奇偶不同（和为奇数）：不能交换' if (int(S['s'][S['i']]) + int(S['s'][S['i'] - 1])) % 2 else
                  f'奇偶相同，但 `{S["s"][S["i"]]}` 不比 `{S["s"][S["i"] - 1]}` 小：换了不会变小')),
        'return s[:i': '拼出交换后的串，直接返回：只能换一次，且越靠左越好',
        'return s': '没找到可交换的一对，原样返回 `{s}`',
    },
    cards=dict(
        one_liner='尽量在高位上交换，找到就返回',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数字字符串 `s`，至多交换一次==相邻且奇偶相同==的两位',
                 '返回字典序最小的结果',
                 '本视频：`"2457320"` → `"2453720"`'],
        quote='又只能交换一次，那么就应该尽量在高位上进行交换。于是只需从头开始向后一趟遍历，若当前数字与下一位数字奇偶性相同，且当前数字更小，那么就进行交换并返回答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['只能换一次：换在越高位，对字典序影响越大',
              '一趟遍历，两数之和为偶数 ⇔ 奇偶相同',
              '同时要求后一位更小，才会让字典序变小；找到就直接返回'],
        summary=['时间 `O(n)`，空间 `O(n)`（切片拼接新字符串）',
                 '易错点：别忘了「后一位更小」这个条件，奇偶相同但递增的对交换只会变大',
                 '没有可交换的对就返回原串',
                 '原文把结果说成「最大数字」，实为字典序最小；代码只删去了类型说明文档字符串',
                 '对比灵神：灵神用列表原地交换 + `break`，yiduobo 直接切片拼接 + `return`'],
    ),
)
