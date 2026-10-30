def _txt(S):
    if 'now' not in S:
        return ''
    return f"当前段的值 `now = {S['now']}`，下标 `p = {S['p']}`，上限 `k = {S['k']}`"


CONFIG = dict(
    num=2522, title='将字符串分割成值不超过 K 的子字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先判无解 · 每段尽量多吞字符',
    tags=['灵神题单', '贪心算法', '难度分 1605'],
    code='''
class Solution(object):
    def minimumPartition(self, s, k):

        if k < 10:
            if int(max(list(s))) > k:
                return -1
            else:
                return len(s)
        else:
            cnt = 0
            p = 0
            now = 0
            while p < len(s):
                while p < len(s) and now * 10 + int(s[p]) <= k:
                    now = now * 10 + int(s[p])
                    p += 1
                
                cnt += 1
                now = 0
            
            return cnt
''',
    call="Solution().minimumPartition('165462', 60)",
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=32, h=90),
        dict(type='string', var='s', h=300, pointers={'p': 'blue'}, label='s（p 指向下一个要吞的字符）'),
    ],
    watch=[('p', 'p', 'blue'), ('now', 'now', 'pink'), ('k', 'k'), ('cnt', 'cnt', 'green')],
    captions={
        'if k < 10': '`k = {k}`：{\'k 是个位数，要单独判断\' if k < 10 else \'k 至少两位，逐位拆开一定有解，不用判无解\'}',
        'cnt = 0': '`cnt` 记录已经分出的段数',
        'p = 0': '`p` 从字符串头部开始，指向当前段的起点',
        'now = 0': lambda S, B, r: ('`now` 是当前这一段的数值' if S['_line'] < 19 else f"这一段结束，`now` 归零，`p = {S.p}` 作为下一段的起点"),
        'while p < len(s):': lambda S, B, r: (f"`p = {S.p}` 还没到末尾，开始分出一段新的" if S.p < len(S.s) else f"`p = {S.p} == len(s)`：整个字符串分完了"),
        'while p < len(s) and now': lambda S, B, r: ((f"试着吞下 `s[{S.p}] = {S.s[S.p]}`：`{S.now}×10 + {S.s[S.p]} = {S.now * 10 + int(S.s[S.p])}` {'<=' if S.now * 10 + int(S.s[S.p]) <= S.k else '>'} `{S.k}` → {'能吞，继续' if S.now * 10 + int(S.s[S.p]) <= S.k else '吞不下，这一段结束'}") if S.p < len(S.s) else '字符串到头了，这一段结束'),
        'now = now * 10': '吞下：`now` = =={now}==',
        'p += 1': '`p` 右移到 {p}',
        'cnt += 1': '这一段分好了：`cnt` = =={cnt}==',
        'return cnt': '一共分出 `{cnt}` 段',
    },
    cards=dict(
        one_liner='每一段尽量多吞字符，后面的分割才更容易',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 每位是 1~9，分成若干子串使每个子串的数值 `≤ k`',
                 '求最少段数，不可能就返回 `-1`',
                 '示例：`s = "165462", k = 60` → `4`'],
        quote='由于字符串中的每一位都必须使用，因此对于每个子字符串的划分就应该尽量将可以包含的字符包含进来，这样一来才能让后续的分割更加容易。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看无解：`k` 为两位数时逐位拆总有解；个位数时有数位 `> k` 才无解',
              '`k` 为个位数且有解，每位都得单独成段，答案 `len(s)`',
              '`k >= 10`：用 `p` 往后扫，每段吞到不能吞为止'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串',
                 '易错：内层 `while` 要同时判断 `p < len(s)`，避免越界',
                 '对比灵神：灵神一个循环搞定，遇到 `v > k` 返回 -1；这里把无解单独拆出来'],
    ),
)
