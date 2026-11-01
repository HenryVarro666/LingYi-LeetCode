CONFIG = dict(
    num=1864, title='构成交替字符串需要的最小交换次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='统计 1 的个数与偶数位上的 1',
    tags=['灵神题单', '贪心算法', '难度分 1601'],
    code='''
class Solution(object):
    def minSwaps(self, s):

        cnt_one = 0
        even_one = 0
        for index, char in enumerate(s):
            if char == '1':
                cnt_one += 1
                if index % 2 == 0:
                    even_one += 1

        if abs(cnt_one - (len(s) - cnt_one)) >= 2:
            return -1
        
        res = cnt_one

        if cnt_one >= len(s) - cnt_one:
            res = min(res, cnt_one - even_one)
        
        if cnt_one <= len(s) - cnt_one:
            res = min(res, even_one)
        
        return res
''',
    call='Solution().minSwaps("111000")',
    expect=1,
    views=[
        dict(type='string', var='s', label='s（红 = 偶数下标上的 1）', pointers={'index': 'blue'},
             color=lambda S, i, v: 'red' if (v == '1' and i % 2 == 0 and 'index' in S and i <= S['index']) else None, h=240),
        dict(type='text', fn=lambda S: (f"1 共 `{S['cnt_one']}` 个，0 共 `{len(S['s']) - S['cnt_one']}` 个；偶数位上的 1 有 ==%d== 个" % S['even_one']) if 'even_one' in S else '', size=30),
        dict(type='text', fn=lambda S: (f"1 放偶数位：需移走 `cnt_one − even_one` = ==%d==；0 放偶数位：需 `even_one` = ==%d==" % (S['cnt_one'] - S['even_one'], S['even_one'])) if S.get('_line', 0) >= 17 else '', size=28),
    ],
    watch=['cnt_one', 'even_one', ('res', 'res', 'green')],
    captions={
        'cnt_one = 0': '`cnt_one` 统计 1 的个数',
        'even_one = 0': '`even_one` 统计偶数下标上 1 的个数',
        'if char ==': lambda S, B, ret: f'`s[{S.index}] = {S.char}`' + ('，是 1，计数' if S.char == '1' else '，是 0，跳过'),
        'cnt_one += 1': '1 的总数 `cnt_one` = {cnt_one}',
        'if index % 2': lambda S, B, ret: f'下标 `{S.index}` 是' + ('==偶数位==' if S.index % 2 == 0 else '奇数位，不计'),
        'even_one += 1': '偶数位上的 1：`even_one` = {even_one}',
        'if abs': lambda S, B, ret: f'0 与 1 个数之差 `|{S.cnt_one} − {len(S.s) - S.cnt_one}|` = {abs(S.cnt_one - (len(S.s) - S.cnt_one))}' + ('，>= 2 → 交替串里不可能，返回 -1' if abs(S.cnt_one - (len(S.s) - S.cnt_one)) >= 2 else '，< 2 → 有解'),
        'res = cnt_one': '`res` 先取一个上界 `cnt_one` = {res}',
        'if cnt_one >= len': lambda S, B, ret: ('1 不少于 0 → 可以把 ==1 放在偶数位==' if S.cnt_one >= len(S.s) - S.cnt_one else '1 比 0 少，不能把 1 放偶数位'),
        'res = min(res, cnt_one - even_one)': '要在偶数位放 1：不在偶数位的 1 都得换，共 `{cnt_one} − {even_one}`，`res` = {res}',
        'if cnt_one <= len': lambda S, B, ret: ('1 不多于 0 → 可以把 ==0 放在偶数位==' if S.cnt_one <= len(S.s) - S.cnt_one else '1 比 0 多，不能把 0 放偶数位'),
        'res = min(res, even_one)': '要在偶数位放 0：偶数位上的 1 都得换走，共 `{even_one}`，`res` = {res}',
        'return res': '最少交换 `{res}` 次',
    },
    cards=dict(
        one_liner='先数 1，再数偶数位上的 1，答案就出来了',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`，任意两字符可交换，求变成交替串的最少交换次数，不行返回 `-1`',
                 '示例：`"111000"` → `1`；`"1110"` → `-1`'],
        quote='若需要将1放在偶数位上，那么交换的次数就是不在偶数位上的1的个数，而如果要将0放在偶数位上，那么交换的次数就是在偶数位上的1的个数',
        quote_src='—— yiduobo 题解原文',
        idea=['合法串只有两种：偶数位全 1 或偶数位全 0，所以 0、1 个数最多差 1',
              '1 不少于 0 时可试「1 放偶数位」；0 不少于 1 时可试「0 放偶数位」',
              '一趟遍历同时数出 1 的个数和偶数位上 1 的个数，0 的个数用 `n − cnt_one` 得到'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '个数相等时两种方案都要试，取较小',
                 '原文第二句 `res = cnt_one` 只是上界，真正的值由两个 `if` 给出',
                 '对比灵神：灵神枚举两个目标串逐位比较，这里只数两个数'],
    ),
)
