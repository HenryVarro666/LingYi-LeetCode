CONFIG = dict(
    num=1864, title='构成交替字符串需要的最小交换次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='统计 1 的个数与偶数位上的 1',
    tags=['灵神题单', '难度分 1601'],
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
        dict(type='string', var='s', label='s（蓝 = 1，偶数下标的 1 记入 even_one）', h=250, cell=100,
             pointers={'index': 'pink'},
             color=lambda S, i, v: ('green' if (v == '1' and i % 2 == 0) else 'blue') if v == '1' else None),
        dict(type='text', size=26, h=90, fn=lambda S: (
            f"1 共 `{S['cnt_one']}` 个，0 共 `{len(S['s'])-S['cnt_one']}` 个；偶数位上的 1 有 `{S['even_one']}` 个")
            if 'cnt_one' in S and 'even_one' in S else ''),
    ],
    watch=['cnt_one', 'even_one', 'res'],
    captions={
        'cnt_one = 0': '`cnt_one` 统计 1 的个数；0 的个数 = `len(s) - cnt_one`，不用单独数',
        'even_one = 0': '`even_one` 统计==偶数下标==上 1 的个数',
        'for index, char': '看下标 `{index}`，字符 `{char}`',
        "if char == '1'": lambda S, B, r: f"`char = '{S.char}'`" + (' 是 1，要统计' if S.char == '1' else ' 是 0，跳过'),
        'cnt_one += 1': '`cnt_one` → {cnt_one}',
        'if index % 2 == 0': '下标 `{index}` 是{"偶数位" if index % 2 == 0 else "奇数位"}',
        'even_one += 1': '偶数位上又多一个 1：`even_one` → {even_one}',
        'abs(cnt_one': '1 有 `{cnt_one}` 个，0 有 `{len(s) - cnt_one}` 个，差 `{abs(cnt_one - (len(s) - cnt_one))}`：'
                       '{"差 ≥ 2 → 不可能交替 → -1" if abs(cnt_one - (len(s) - cnt_one)) >= 2 else "差 ≤ 1，可以交替"}',
        'res = cnt_one': '先给 `res` 一个上界 `cnt_one = {res}`',
        'if cnt_one >= len(s)': lambda S, B, r: (f'`{S.cnt_one} ≥ {len(S.s) - S.cnt_one}`：1 不比 0 少 → ==可以让 1 占偶数位=='
                                                  if S.cnt_one >= len(S.s) - S.cnt_one else '1 比 0 少，不能让 1 占偶数位'),
        'res = min(res, cnt_one - even_one)': '1 放偶数位：只需把不在偶数位的 1 换进来 → `{cnt_one} − {even_one} = {cnt_one - even_one}`，`res` = =={res}==',
        'if cnt_one <= len(s)': lambda S, B, r: (f'`{S.cnt_one} ≤ {len(S.s) - S.cnt_one}`：0 不比 1 少 → ==可以让 0 占偶数位=='
                                                  if S.cnt_one <= len(S.s) - S.cnt_one else '0 比 1 少，不能让 0 占偶数位'),
        'res = min(res, even_one)': '0 放偶数位：偶数位上的 1 都要换走 → `even_one = {even_one}`，`res` = =={res}==',
        'return res': '最少交换 `res` = =={res}==',
    },
    cards=dict(
        one_liner='只数 1 的个数和偶数位上的 1，就能算出交换次数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，任意两个字符可以交换（不必相邻）',
                 '求变成交替字符串（如 `1010`）的最少交换次数，不可能则 `-1`',
                 '示例：`"111000"` → `1`'],
        quote='若需要将1放在偶数位上，那么交换的次数就是不在偶数位上的1的个数，而如果要将0放在偶数位上，那么交换的次数就是在偶数位上的1的个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['合法串只有两种：1 占偶数位，或 0 占偶数位',
              '0 和 1 的个数差 ≥ 2 无解；否则个数多（或相等）的那个可以占偶数位',
              '1 占偶数位：换进 `cnt_one - even_one` 次；0 占偶数位：换走 `even_one` 次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：个数相等时两种方案都要试，取较小',
                 '0 的个数 = 长度 − 1 的个数，不用单独统计',
                 '因为可以任意交换，所以每次交换纠正两个错位字符，次数 = 错位的 1 的个数'],
    ),
)
