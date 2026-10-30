def _cnts(S):
    return [(S['total'] - S['cost1'] * i) // S['cost2'] + 1 for i in range(S['total'] // S['cost1'] + 1)]


def _text(S):
    t, c1, c2 = S['total'], S['cost1'], S['cost2']
    if 'cnt1' not in S:
        return f'`total={t}`：枚举钢笔数 `cnt1`，累加铅笔的 `k + 1` 种选法'
    c = S['cnt1']
    if c * c1 > t:
        return f'`{c} × {c1} = {c * c1} > {t}`：钢笔买不起了，停止'
    k = (t - c * c1) // c2
    return f'买 `{c}` 支钢笔：剩 `{t} − {c * c1} = {t - c * c1}` 元，铅笔 0 到 `{k}` 共 =={k + 1}== 种'


CONFIG = dict(
    num=2240, title='买钢笔和铅笔的方案数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举一种笔 · 累加另一种',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def waysToBuyPensPencils(self, total, cost1, cost2):

        res = 0
        cnt1 = 0
        while cnt1 * cost1 <= total:
            res += (total - cnt1 * cost1) // cost2 + 1
            cnt1 += 1
        
        return res
''',
    call='Solution().waysToBuyPensPencils(20, 10, 5)',
    expect=9,
    views=[
        dict(type='text', fn=_text, h=110),
        dict(type='array', var=_cnts, label='每个 cnt1 对应的铅笔方案数 k + 1', h=260),
    ],
    watch=['cnt1', ('res', 'res', 'green')],
    captions={
        'while cnt1': lambda S, B, r: (f'`{S.cnt1} × {S.cost1} = {S.cnt1 * S.cost1} <= {S.total}`：钢笔还买得起，继续' if S.cnt1 * S.cost1 <= S.total
                                      else f'`{S.cnt1} × {S.cost1} = {S.cnt1 * S.cost1} > {S.total}`：买不起了，退出循环'),
        'res +=': '剩余 `{total - (cnt1) * cost1}` 元买铅笔，最多 `k = {(total - cnt1 * cost1) // cost2}` 支，0 到 k 共 `k + 1` 种 → `res = {res}`',
        'cnt1 += 1': '再多买一支钢笔：`cnt1 = {cnt1}`',
        'return res': '全部累加完，答案 `{res}`',
    },
    cards=dict(
        one_liner='只有两种笔：枚举钢笔数量，铅笔的方案数直接算',
        complexity='时间 `O(total / cost1)`，空间 `O(1)`',
        problem=['有 `total` 元，钢笔 `cost1` 元、铅笔 `cost2` 元，求不同的购买方案数',
                 '示例：`total=20, cost1=10, cost2=5` → `9`'],
        quote='完全可以枚举其中一种的数量，然后计算选择另一种笔的可能方案数。',
        quote_src='—— yiduobo 题解原文',
        idea=['设买了 `x` 支钢笔，剩 `total - cost1 * x`',
              '铅笔最多 `k = (total - cost1 * x) // cost2` 支，0 到 `k` 共 `k + 1` 种',
              '用 `while` 一直试到 `cost1 * x > total` 为止'],
        summary=['时间 `O(total / cost1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去了类型文档',
                 '易错点：每次是加 `k + 1`，不是 `k`（买 0 支铅笔也算）',
                 '对比灵神：灵神把所有 `+1` 合并成 `n`，用一个 `sum` 写完'],
    ),
)
