def _top(S):
    if 'cnt' not in S:
        return ''
    return f"偶数位的 `0`、奇数位的 `1` 记为 `cnt = {S['cnt']}`（变成 `1010…` 的代价），另一种是 `{len(S['s'])} − cnt`"


CONFIG = dict(
    num=1758, title='生成交替二进制字符串的最少操作数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='统计偶数位 0 与奇数位 1',
    code='''
class Solution(object):
    def minOperations(self, s):

        cnt = 0
        for index in range(len(s)):
            if index % 2 == 0 and s[index] == '0':
                cnt += 1
            elif index % 2 == 1 and s[index] == '1':
                cnt += 1
        
        return min(cnt, len(s) - cnt)
''',
    call='Solution().minOperations("010011")',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（红 = 需要翻转成 1010… 的位置）', cell=90, pointers={'index': 'pink'},
             color=lambda S, i, v: (('red' if (i % 2 == 0 and v == '0') or (i % 2 == 1 and v == '1') else 'green')
                                    if 'index' in S and i <= S['index'] else None)),
    ],
    watch=[('index', 'index', 'pink'), ('cnt', 'cnt', 'red')],
    captions={
        'cnt = 0': '`cnt`：想变成「偶数位全 1、奇数位全 0」需要翻转的个数',
        'for index in range': '看下标 `{index}`（{"偶" if index % 2 == 0 else "奇"}数位），字符 `{s[index]}`',
        "index % 2 == 0 and": lambda S, B, r: ("偶数位却是 `0` → 要翻成 1" if S.index % 2 == 0 and S.s[S.index] == '0'
                                               else '偶数位是 `1` 或这是奇数位，先不算'),
        "index % 2 == 1 and": lambda S, B, r: ('偶数位，已在上一行判断过' if S.index % 2 == 0 else
                                               "奇数位却是 `1` → 要翻成 0" if S.s[S.index] == '1'
                                               else '奇数位是 `0` → 不用翻'),
        'cnt += 1': '要翻转 → `cnt` = {cnt}',
        'return min': lambda S, B, ret: (f'反过来变成「偶数位全 0、奇数位全 1」恰好是 `{len(S.s)} − {S.cnt} = {len(S.s) - S.cnt}`；'
                                         f'取小 → =={ret}=='),
    },
    cards=dict(
        one_liner='两种目标互为镜像：统计一种，另一种用总长减去',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 只含 `0`/`1`，每步翻转一个字符，使相邻字符都不同',
                 '求最少操作次数',
                 '本视频：`"010011"` → `2`'],
        quote='最终答案的字符串上要么偶数位全1，奇数位全0，要么正好反过来。……那么最终答案就是min(cnt, len(s) - cnt)',
        quote_src='—— yiduobo 题解原文',
        idea=['目标 A：偶数位全 1、奇数位全 0；要翻的是偶数位上的 `0` 和奇数位上的 `1`，个数记为 `cnt`',
              '目标 B 与 A 逐位相反：A 里要翻的，B 不用翻；A 不用翻的，B 要翻 → `len(s) - cnt`',
              '一趟统计 `cnt` 就够了，答案取两者较小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`cnt` 统计的是目标 `1010…`（偶数位 1），不是 `0101…`；两种互补，取 min 即可',
                 '原文为 Python 2 风格，类名 `Solution(object)` 在 Python 3 同样可用，代码未改',
                 '对比灵神：灵神直接数和 `0101…` 不同的位置，yiduobo 数和 `1010…` 不同的位置'],
    ),
)
