CONFIG = dict(
    num=984, title='不含 AAA 或 BBB 的字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心：多的字符 aab / bba 抹平差距',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def strWithout3a3b(self, a, b):

        res = ''
        while a > 0 and b > 0 and a != b:
            if a > b:
                res += 'aab'
                a -= 2
                b -= 1
            else:
                res += 'bba'
                a -= 1
                b -= 2
        
        if a == b:
            if len(res) > 0 and res[-1] == 'a':
                tmp = 'ba'
            else:
                tmp = 'ab'
            res += tmp * a
        elif a > 0:
            res += 'a' * a
        else:
            res += 'b' * b

        return res
''',
    call='Solution().strWithout3a3b(4, 3)',
    expect='aababab',
    views=[
        dict(type='string', var=lambda S: S['res'] if 'res' in S else '', label='res（已构造的字符串）', cell=84, h=200,
             color=lambda S, i, v: 'blue' if v == 'a' else 'pink'),
        dict(type='text', h=130, fn=lambda S: (f"还剩 `a = {S['a']}`，`b = {S['b']}`" + ('，数量相同可以交替' if S['a'] == S['b'] else '')) if 'a' in S and 'b' in S else ''),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), 'tmp'],
    skip=["res = ''"],
    captions={
        'while a > 0': lambda S, B, r: (f'`a = {S.a}`、`b = {S.b}` 都有剩余且数量不等 → 继续抹平差距' if S.a > 0 and S.b > 0 and S.a != S.b
                                        else '两种字符数量相等或有一种用完了 → 结束循环'),
        'if a > b': lambda S, B, r: (f'`a = {S.a} > b = {S.b}`：a 多，用 `aab` 消耗' if S.a > S.b else f'`a = {S.a} < b = {S.b}`：b 多，用 `bba` 消耗'),
        "res += 'aab'": '`aab`：中间的 b 把两个 a 隔开，a 少 2、b 少 1，差距缩小 → `res = {res}`',
        'b -= 1': '`b` 用掉 1 个 → {b}',
        'a -= 1': '`a` 用掉 1 个 → {a}',
        'a -= 2': '`a` 用掉 2 个 → {a}',
        'res += \'bba\'': '`bba`：a 把两个 b 隔开，b 少 2、a 少 1 → `res = {res}`',
        'b -= 2': '`b` 用掉 2 个 → {b}',
        'if a == b': lambda S, B, r: (f'`a = b = {S.a}`：数量相同，可以交替拼接' if S.a == S.b else f'`a = {S.a}`，`b = {S.b}`：有一方用完了，剩下的直接接在末尾'),
        'if len(res) > 0': lambda S, B, r: ('末尾是 `a` → 接 `ba` 避免连成 aaa' if S.res and S.res[-1] == 'a' else '末尾是 `b`（或为空） → 接 `ab`'),
        'tmp * a': '重复 `{tmp}` 共 `{a}` 次 → `res = {res}`',
        "'a' * a": '只剩 a：直接接在末尾（前面是 bba 形式，不会连成 aaa）→ `res = {res}`',
        "'b' * b": '只剩 b：直接接在末尾 → `res = {res}`',
        'return res': '得到 ==`{res}`==',
    },
    cards=dict(
        one_liner='谁多就先用 aab / bba 把多出来的那个吃掉',
        complexity='时间 `O(a + b)`，空间 `O(a + b)`',
        problem=['给定 `a` 个 `a` 和 `b` 个 `b`，拼成长度 `a+b` 的字符串，不能出现 `aaa` 或 `bbb`',
                 '返回任意一个合法字符串（题目保证有解）',
                 '本视频：`a = 4, b = 3` → `aababab`'],
        quote='当a比较多时，由于不能出现连续的三个a，那么我们需要使用两个a一个b的组合，通过b来分割这两个a与其他的a，同时也达到了来减少a的数量的目的。',
        quote_src='—— yiduobo 题解原文',
        idea=['数量相同：交替放 `ab` 即可，所以只需抹平差距',
              'a 多用 `aab`，b 多用 `bba`，差距每次缩小 1',
              '结束后三种情况：只剩 a、只剩 b，或数量相同（看末尾字符决定接 `ba` 还是 `ab`）'],
        summary=['时间 `O(a + b)`，空间 `O(a + b)`',
                 '用 `aab` 而非 `baa`，保证后面还有机会用掉多出的 a',
                 '数量相同收尾要看末尾字符：以 a 结尾接 `ba`',
                 '原文为 Python 2 写法，本题代码无需修改'],
    ),
)
