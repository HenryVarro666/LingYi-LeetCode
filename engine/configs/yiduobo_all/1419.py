def _txt(S):
    if 'now' not in S:
        return '像括号匹配：c 是「左括号」，k 是「右括号」，中间字母数量不能反超前一个'
    return (f"`c={S['c']}  r={S['r']}  o={S['o']}  a={S['a']}  k={S['k']}`　未闭合 `now` = =={S['now']}==，最多同时 `res` = =={S['res']}==")


CONFIG = dict(
    num=1419, title='数青蛙', difficulty='Medium', category='字符串',
    author='yiduobo', technique='括号匹配 · 五个计数器',
    tags=[],
    code='''
class Solution(object):
    def minNumberOfFrogs(self, croakOfFrogs):

        c = r = o = a = k = 0
        now = 0
        res = 0
        for char in croakOfFrogs:
            if char == 'c':
                c += 1
                now += 1
                res = max(now, res)
            elif char == 'r':
                r += 1
                if r > c:
                    return -1
            elif char == 'o':
                o += 1
                if o > r:
                    return -1
            elif char == 'a':
                a += 1
                if a > o:
                    return -1
            elif char == 'k':
                k += 1
                if k > a:
                    return -1
                now -= 1
        
        if c == r == o == a == k:
            return res
            
        return -1
''',
    call='Solution().minNumberOfFrogs("crcoakroak")',
    expect=2,
    views=[
        dict(type='string', var='croakOfFrogs', label='croakOfFrogs（蓝箭头 = 当前字符）', cell=80, h=190,
             pointers={'c + r + o + a + k - 1': 'blue'}),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=['char', 'c', 'r', 'o', 'a', 'k', ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'c = r = o = a = k = 0': '五个计数器：分别记 c、r、o、a、k 出现的次数',
        'now = 0': '`now`：当前尚未闭合的「括号」，也就是正在叫的青蛙数',
        'res = 0': '`res` 记录 `now` 的最大值',
        "if char == 'c'": '当前字符 `{char}`',
        'c += 1': '`c` = {c}',
        'now += 1': '新起一个「括号」：新来一只青蛙，`now` = {now}',
        'res = max': '`res = max({B.res}, {now})` = =={res}==：同时叫的青蛙数峰值',
        'r += 1': '`r` = {r}',
        'if r > c': lambda S, B, r_: (f'`r = {S.r} > c = {S.c}`：r 比 c 多，没有青蛙在 c 后接 r → 不合法'
                                      if S.r > S.c else f'`r = {S.r} <= c = {S.c}`：每个 r 都有 c 在前 → 合法'),
        'o += 1': '`o` = {o}',
        'if o > r': lambda S, B, r_: (f'`o = {S.o} > r = {S.r}` → 不合法' if S.o > S.r else f'`o = {S.o} <= r = {S.r}` → 合法'),
        'a += 1': '`a` = {a}',
        'if a > o': lambda S, B, r_: (f'`a = {S.a} > o = {S.o}` → 不合法' if S.a > S.o else f'`a = {S.a} <= o = {S.o}` → 合法'),
        'k += 1': '`k` = {k}',
        'if k > a': lambda S, B, r_: (f'`k = {S.k} > a = {S.a}` → 不合法' if S.k > S.a else f'`k = {S.k} <= a = {S.a}` → 合法'),
        'now -= 1': 'k 意味着「括号」闭合：一只青蛙叫完，`now` = {now}',
        'if c == r == o == a == k': lambda S, B, r_: ('五个数相等：所有青蛙都叫完了整句 → 返回 `res`' if S.c == S.r == S.o == S.a == S.k
                                                   else '五个数不等：有「括号」没闭合 → 不合法'),
        'return res': '最少需要 `{ret}` 只青蛙',
        'return -1': '返回 `-1`',
    },
    cards=dict(
        one_liner='把青蛙当括号：c 开括号，k 闭括号，其余字母不能超前',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`croakOfFrogs` 由多只青蛙的 "croak" 混合而成，求最少需要几只青蛙',
                 '不是若干完整 croak 的混合则返回 `-1`',
                 '示例："crcoakroak" → `2`'],
        quote='与括号匹配很类似的问题，如果这里只有两个字母，那么就是一个判断括号串是否合法的问题。这里也可以使用类似的方法。',
        quote_src='—— yiduobo 题解原文',
        idea=['分别用 c、r、o、a、k 记次数，任意时刻要有 `c >= r >= o >= a >= k`',
              '遇到 c：新起一个「括号」，`now` 加一，用 `now` 刷新答案',
              '遇到 k：一个「括号」闭合，`now` 减一',
              '结束时五个数必须相等，否则有未闭合的括号'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '每个字母只需和前一个字母比较，因为前面的不等式已经保证了',
                 '答案是 `now` 的最大值，不是 c 的总数',
                 '原文 Python 2 风格，未做任何修改即可在 Python 3 运行',
                 '对比灵神：灵神用哈希表记每种「状态」的青蛙数，yiduobo 用括号匹配思路'],
    ),
)
