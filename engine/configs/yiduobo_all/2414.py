CONFIG = dict(
    num=2414, title='最长的字母序连续子字符串的长度', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='线性 DP · 滚动变量',
    tags=['灵神题单', '难度分 1222'],
    code='''
class Solution(object):
    def longestContinuousSubstring(self, s):

        res = 0
        now = 0
        for index, char in enumerate(s):
            if index == 0 or ord(char) != ord(s[index - 1]) + 1:
                res = max(res, now)
                now = 0
            now += 1
        
        return max(res, now)
''',
    call="Solution().longestContinuousSubstring('abcabcdea')",
    expect=5,
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, h=190),
        dict(type='text', h=90, fn=lambda S: f"f[i] = 以当前字符结尾的最长长度 = now = =={S['now']}==" if 'now' in S else ''),
        dict(type='text', h=90, fn=lambda S: f"已结束的各段里最长：res = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=['index', 'char', ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        4: '`res` 记录已经结束的各段里最长的',
        5: '`now` 就是 f[i]：以当前字符结尾的长度（滚动变量）',
        'if index == 0 or': lambda S, B, r: (f'`{S.char}` 是开头或不是前一个字母的下一个 → 一段结束，要重置' if (S.index == 0 or ord(S.char) != ord(S.s[S.index-1]) + 1)
                                              else f'`{S.char}` 紧接着 `{S.s[S.index-1]}` → 这一段继续，f[i] = f[i-1] + 1'),
        'res = max(res, now)': '先把刚结束的这一段结算：`res = max({B.res}, {now}) = {res}`',
        9: '`now` 清零，马上在下一行加一，等于重置为 1',
        'now += 1': '当前字符算进去：`now` → =={now}==',
        'return max(res, now)': '最后一段没有被结算过，要再比一次：`max({res}, {now})` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 只依赖 f[i-1]，一个变量 now 就够了',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母表中连续的字母组成的串（如 `abc`）叫字母序连续字符串',
                 '求 `s` 里最长的字母序连续子串的长度',
                 '示例：`abacaba` → `2`；本视频：`abcabcdea` → `5`'],
        quote='注意到这里的f每一轮只与上一轮有关，因此可以使用一个遍历迭代来节省空间。',
        quote_src='—— yiduobo 题解原文',
        idea=['先定义 f[i]：以 s[i] 结尾的最长长度；i=0 或断开时 f=1，否则 f[i-1]+1',
              '只和上一轮有关 → 用 `now` 滚动代替整个数组',
              '每次断开时把 `now` 结算进 `res`，再从头数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环结束后还要 `max(res, now)`，最后一段没结算',
                 '原文为 Python 2 风格，本题代码无需改动，直接可在 Python 3 运行',
                 '对比灵神：灵神每步都更新 ans，因此不需要最后补一次比较'],
    ),
)
