NUMS = [51, 71, 17, 24, 42, 93, 39]


def _T(S):
    ma = S.get('ma')
    if not isinstance(ma, list) or len(ma) != 10:
        return None
    return [[r[0] for r in ma], [r[1] for r in ma]]


def _col(S, i, j, v):
    d = S.get('digit') if 'res' in S else S.get('max_digit')
    if d is not None and j == d:
        return 'green' if 'res' in S else 'pink'
    return None


CONFIG = dict(
    num=2815, title='数组中的最大数对和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='每种最大数位记最大值与次大值',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maxSum(self, nums):

        ma = [[None] * 2 for _ in range(10)]
        for v in nums:
            max_digit = int(max(list(str(v))))
            if ma[max_digit][0] is None or ma[max_digit][0] < v:
                ma[max_digit] = [v, ma[max_digit][0]]
            elif ma[max_digit][1] is None or ma[max_digit][1] < v:
                ma[max_digit][1] = v
        
        res = -1
        for digit in range(1, 10):
            if ma[digit][1] is not None:
                res = max(res, ma[digit][0] + ma[digit][1])

        return res
''',
    call=f'Solution().maxSum({NUMS})',
    expect=132,
    views=[
        dict(type='array', var='nums', label='nums', h=180,
             color=lambda S, i, v: 'blue' if 'v' in S and 'res' not in S and S['nums'].index(S['v']) == i else None,
             dim=lambda S, i, v: 'v' in S and 'res' not in S and i > S['nums'].index(S['v'])),
        dict(type='table', var=_T, label='ma[d]（列 = 最大数位 d；· 表示还没有）', rows=['最大', '次大'], cols=list(range(10)),
             color=_col, cell=74, h=250),
    ],
    watch=[('v', 'v', 'blue'), ('max_digit', 'max_digit', 'pink'), ('digit', 'digit'), ('res', 'res', 'green')],
    captions={
        'ma = [[None]': '`ma[d] = [最大值, 次大值]`：每种最大数位各存两个数，`None` 表示还没有',
        'for v in nums': lambda S, B, r: (f'看下一个数 `v = {S.v}`' if B.get('v') != S.v or 'max_digit' not in B else '所有数都放好了'),
        'max_digit = int(': '`{v}` 的最大数位是 `{max_digit}`',
        'if ma[max_digit][0] is None': lambda S, B, r: (
            (f'`ma[{S.max_digit}]` 还没有最大值 → `{S.v}` 当最大值' if S.ma[S.max_digit][0] is None
             else f'`{S.v} > {S.ma[S.max_digit][0]}`：比当前最大值还大 → 成为新的最大值')
            if S.ma[S.max_digit][0] is None or S.ma[S.max_digit][0] < S.v
            else f'`{S.v} ≤ 最大值 {S.ma[S.max_digit][0]}`，再看能不能当次大值'),
        'ma[max_digit] = [v,': lambda S, B, r: (f'原来的最大值 `{S.ma[S.max_digit][1]}` ==退位成次大值==：`ma[{S.max_digit}] = {S.ma[S.max_digit]}`' if S.ma[S.max_digit][1] is not None
                                               else f'`ma[{S.max_digit}] = {S.ma[S.max_digit]}`（次大值仍为空）'),
        'elif ma[max_digit][1]': lambda S, B, r: (f'次大值是 `{S.ma[S.max_digit][1]}`，`{S.v}` 比它大 → 替换' if S.ma[S.max_digit][1] is not None and S.ma[S.max_digit][1] < S.v
                                                 else (f'还没有次大值 → `{S.v}` 当次大值' if S.ma[S.max_digit][1] is None
                                                       else f'`{S.v}` 不比次大值 `{S.ma[S.max_digit][1]}` 大，丢掉')),
        'ma[max_digit][1] = v': '`ma[{max_digit}] = {ma[max_digit]}`',
        'res = -1': '第二趟：每种数位里“最大 + 次大”就是这一类的最佳数对',
        'for digit in range': lambda S, B, r: (f'看最大数位 `{S.digit}`' if B.get('digit') != S.digit else '九种数位都看完了'),
        'if ma[digit][1] is not None': lambda S, B, r: (f'数位 {S.digit} 有两个数 → 数对和 `{S.ma[S.digit][0]} + {S.ma[S.digit][1]} = {S.ma[S.digit][0] + S.ma[S.digit][1]}`' if S.ma[S.digit][1] is not None
                                                       else f'数位 {S.digit} 不足两个数，组不成数对'),
        'res = max(res': '`res = max({B.res}, {ma[digit][0] + ma[digit][1]})` = =={res}==',
        'return res': '最大数对和为 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='按最大数位分组，每组只留最大和次大两个数',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['找一对数，它们==数位上最大的数字相等==，求最大的和；不存在返回 `-1`',
                 '示例：`[51,71,17,24,42]` → `88`（71 + 17）',
                 f'本视频：`{NUMS}` → `132`（93 + 39）'],
        quote='我的做法是一趟遍历，利用哈希表储存每种最大数位对应的==最大值以及次大值==，然后再从中选出和最大的那一组就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一组（最大数位相同）里和最大的一对，一定是==最大 + 次大==',
              '遍历时维护每组前两名：比最大还大 → 最大退位成次大',
              '最后扫 1~9 九组，有次大值的才能组成数对'],
        summary=['时间 `O(n log U)`，空间 `O(1)`（只有 10 组）',
                 '新最大值出现时，==旧最大值要降为次大==，不能直接丢掉',
                 '数据小也可以二重循环暴力枚举，原文也提到了',
                 '原文为 Python 2 风格，代码无需改动即可运行',
                 '对比「枚举右，维护左」：每组只存一个最大值，边遍历边更新答案'],
    ),
)
