CONFIG = dict(
    num=910, title='最小差值 II', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 枚举分隔点',
    tags=['灵神题单', '难度分 2135'],
    code='''
class Solution(object):
    def smallestRangeII(self, A, K):

        A = sorted(A)
        res = A[-1] - A[0]
        for index in range(len(A) - 1):
            res = min(res, max(A[-1] - K, A[index] + K) - min(A[0] + K, A[index + 1] - K))
        
        return res
''',
    call='Solution().smallestRangeII([6,1,10,3], 3)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"分隔点 `index = {S['index']}`：`A[0..{S['index']}]` ==+K==，`A[{S['index']+1}..]` ==−K==" if 'index' in S and 'res' in S else '')),
        dict(type='array', var='A', h=300, pointers={'index': 'yellow'},
             color=lambda S, i, v: ('blue' if i <= S['index'] else 'pink') if 'index' in S and 'res' in S else None),
        dict(type='text', fn=lambda S: (f"最大 `max({S['A'][-1]-S['K']}, {S['A'][S['index']]+S['K']})` = =={max(S['A'][-1]-S['K'], S['A'][S['index']]+S['K'])}==；最小 `min({S['A'][0]+S['K']}, {S['A'][S['index']+1]-S['K']})` = =={min(S['A'][0]+S['K'], S['A'][S['index']+1]-S['K'])}==" if 'index' in S and 'res' in S else ''), size=28),
    ],
    watch=['K', ('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'A = sorted': '先排序：`{A}`。小的数加 `K`、大的数减 `K` 才可能让差变小',
        'res = A[-1]': '全加或全减，差都是 `max − min` = `{res}`，作为 `res` 初值',
        'for index': lambda S, B, r: (f'枚举分隔点 `index = {S.index}`：`A[0]` 到 `A[{S.index}]` 加 `K`，其后减 `K`' if S.index != B.get('index') else '分隔点都枚举完了，退出循环'),
        'res = min': '最大 `max(A[-1]-K, A[index]+K)`，最小 `min(A[0]+K, A[index+1]-K)`，差 `{max(A[-1]-K, A[index]+K)} − {min(A[0]+K, A[index+1]-K)}` = {max(A[-1]-K, A[index]+K) - min(A[0]+K, A[index+1]-K)} → `res = min({B.res}, …) = {res}`',
        'return res': '最小差值 `{res}`',
    },
    cards=dict(
        one_liner='先证明：小的数加 K、大的数减 K，再枚举分隔点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个数必须加 `K` 或减 `K`，求变化后「最大值 − 最小值」的最小值',
                 '示例：`[1,3,6], K=3` → `3`',
                 '本视频：`[6,1,10,3], K=3` → `4`'],
        quote='直观感觉上显然是小的数加上K，大的数减去K，也可以给出粗略的证明。',
        quote_src='—— yiduobo 题解原文',
        idea=['两数相差 `diff`：小加大减得 `|diff − 2K|`；同加同减仍是 `diff`；小减大加是 `diff + 2K`',
              '所以最优一定是排序后「前一段加 K，后一段减 K」',
              '枚举分隔点，最大值、最小值各取两个候选'],
        summary=['时间 `O(n log n)`，`sorted` 另开数组，空间 `O(n)`',
                 '`res` 初值对应全加或全减，不能漏',
                 '循环只到 `len(A)-2`，因为要用到 `A[index+1]`',
                 '对比灵神：思路相同，yiduobo 先用差值分情况证明贪心方向',
                 '原文为 Python 2 风格，本题无需改动'],
    ),
)
