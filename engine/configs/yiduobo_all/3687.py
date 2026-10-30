CONFIG = dict(
    num=3687, title='图书馆逾期罚款计算器', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历按规则累加',
    code='''
class Solution(object):
    def lateFee(self, daysLate):
        
        res = 0
        for d in daysLate:
            if d == 1:
                res += 1
            elif 2 <= d <= 5:
                res += d * 2
            else:
                res += d * 3
        
        return res
''',
    call='Solution().lateFee([1,5,6,3,9])',
    expect=1+10+18+6+27,
    views=[
        dict(type='array', var='daysLate', label='daysLate', h=170,
             color=lambda S, i, v: ('green' if v == 1 else 'blue' if v <= 5 else 'pink') if 'd' in S and S.get('d') == v else None),
        dict(type='text', fn=lambda S: '规则：1天 罚 1；2到5天 罚 2×天数；超过5天 罚 3×天数', size=26, h=60),
        dict(type='text', fn=lambda S: f"累计罚款 res = =={S['res']}==" if 'res' in S else '', size=32, h=60),
    ],
    watch=['d', ('res', 'res', 'green')],
    captions={
        'res = 0': '总罚款从 0 开始累加',
        'for d': '取下一本书，逾期 `d = {d}` 天',
        'if d == 1': '`d == 1`？{"是，罚款 1" if d == 1 else "不是，看下一档"}',
        'elif 2 <= d <= 5': '`2 <= {d} <= 5`？{"是，每天罚 2" if 2 <= d <= 5 else "不是，超过 5 天"}',
        'res += 1': '逾期 1 天罚 1：`res = {B.res} + 1 = {res}`',
        'res += d * 2': '2 到 5 天，每天 2：`res = {B.res} + {d}×2 = {res}`',
        'res += d * 3': '超过 5 天，每天 3：`res = {B.res} + {d}×3 = {res}`',
        'return': '所有书的罚款之和为 =={ret}==',
    },
    cards=dict(
        one_liner='每本书按档位算罚款，累加起来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`daysLate[i]` 是第 i 本书逾期天数', '罚款：1 天罚 1；2 到 5 天罚 `2 × 天数`；超过 5 天罚 `3 × 天数`',
                 '求所有书的总罚款，示例：`[1,5,6,3,9]` → `62`'],
        quote='一趟遍历，按照题目的规则计算每本书的罚款金额，然后累加起来即为最终答案。',
        quote_src='—— yiduobo 题解',
        idea=['三档规则互斥，用 if / elif / else 分档', '`elif 2 <= d <= 5` 利用链式比较，else 即超过 5 天'],
        summary=['时间 `O(n)`，空间 `O(1)`', '易错点：1 天罚款是 1 而不是 2×1',
                 '原文为 Python 2 写法，本题无需改动'],
    ),
)
