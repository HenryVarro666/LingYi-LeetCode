def _q(S):
    if 'index' not in S or 'l' not in S:
        return ''
    i = S['index']
    seg = S['nums'][S['l'][i]:S['r'][i] + 1]
    return f"第 `{i}` 个询问：区间 `[{S['l'][i]}, {S['r'][i]}]` = `{seg}`"


def _mm(S):
    if 'm1' not in S:
        return ''
    d = ''
    if S.get('m2') is not None and S.get('m1') is not None:
        d = f"，公差 `delta = {S['m2']} − {S['m1']} = {S['m2'] - S['m1']}`"
    return f"最小 `m1 = {S['m1']}`，第二小 `m2 = {S['m2']}`" + d


CONFIG = dict(
    num=1630, title='等差子数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找最小两数 + 哈希集合',
    tags=[],
    code='''
class Solution(object):
    def checkArithmeticSubarrays(self, nums, l, r):

        m = len(l)
        res = []
        for index in range(m):
            m1 = m2 = None
            num_set = set()
            for num in nums[l[index]: r[index] + 1]:
                if m1 is None or num < m1:
                    m1, m2 = num, m1
                elif m2 is None or num < m2:
                    m2 = num
            
                num_set.add(num)

            delta = m2 - m1
            if delta == 0:
                res.append(len(num_set) == 1)
            else:
                flag = True
                for multi in range(r[index] - l[index] + 1):
                    tmp = m1 + delta* multi
                    if tmp not in num_set:
                        flag = False
                        break
                res.append(flag)
        
        return res
''',
    call='Solution().checkArithmeticSubarrays([4,6,5,9,3,7], [0,0,2], [2,3,5])',
    expect=[True, False, True],
    views=[
        dict(type='text', fn=_q, size=26, h=60),
        dict(type='array', var='nums', h=170, cell=80, label='nums',
             window=(lambda S: S['l'][S['index']], lambda S: S['r'][S['index']])),
        dict(type='set', var='num_set', h=130, fmt=lambda x: str(x), label='num_set'),
        dict(type='text', fn=_mm, size=26, h=60),
        dict(type='array', var='res', h=130, cell=80, label='res'),
    ],
    watch=['index', 'm1', 'm2', 'delta', 'multi', 'tmp', 'flag'],
    captions={
        'm1 = m2 = None': '新询问：先把最小值 `m1`、次小值 `m2` 清空',
        'num_set = set()': '准备一个集合，记下区间里出现过的所有数',
        'if m1 is None or num < m1': lambda S, B, r: f"`{S.num}` 比当前最小 `{B.m1}` 还小吗？" + ('是 → 它成为新的最小，旧最小退为次小' if (B.m1 is None or S.num < B.m1) else '不是'),
        'm1, m2 = num, m1': '新最小 `m1 = {m1}`，原最小顺位成为次小 `m2 = {m2}`',
        'elif m2 is None or num < m2': lambda S, B, r: f"`{S.num}` 比次小 `{B.m2}` 更小吗？" + ('是 → 更新次小' if (B.m2 is None or S.num < B.m2) else '不是，不影响最小两数'),
        'm2 = num': '次小更新为 `m2 = {m2}`',
        'num_set.add': '`{num}` 放进集合：后面用它判断某项是否存在',
        'delta = m2 - m1': '公差 `delta = m2 − m1 = {delta}`：首项 + 公差就确定了整个数列',
        'if delta == 0': lambda S, B, r: ('`delta = 0`：只有区间里全是同一个数才是等差' if S.delta == 0 else '`delta ≠ 0`：逐项检查 `m1 + delta × k` 是否都在集合里'),
        'res.append(len(num_set) == 1)': '集合大小 `{len(num_set)}`，全相同才成立 → 追加 `{res[-1]}`',
        'flag = True': '先假设能构成等差',
        'tmp = m1': '第 `{multi}` 项应为 `{m1} + {delta} × {multi}` = =={tmp}==',
        'if tmp not in num_set': lambda S, B, r: (f"`{S.tmp}` 不在集合里 → 缺项，不是等差" if S.tmp not in S.num_set else f"`{S.tmp}` 在集合里，这一项没问题"),
        'flag = False': '缺项，`flag = False`',
        'break': '已经确定不行，跳出检查',
        'res.append(flag)': '本次询问结果 `{res[-1]}`',
        'return res': '三个询问的结果：`{res}`',
    },
    cards=dict(
        one_liner='等差数列由首项和公差决定：找最小两数，再查缺项',
        complexity='时间 `O(Σ区间长度)`，空间 `O(n)`',
        problem=['给数组 `nums` 和若干区间 `[l[i], r[i]]`，判断区间内的数==重新排列后==能否组成等差数列',
                 '示例：`nums=[4,6,5,9,3,7]`，区间 `[0,2]`、`[0,3]`、`[2,5]`',
                 '结果 `[True, False, True]`'],
        quote='首项自然是区间中的最小值，而公差则可以通过找到区间中第二小的值，与最小值作差得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描同时找出最小的两个数 `m1`、`m2`，公差 `delta = m2 − m1`',
              '扫描时把所有数放进哈希集合',
              '再检查 `m1 + delta×k` 是否都在集合里；`delta = 0` 要单独判断'],
        summary=['每个询问 `O(区间长度)`，总共 `O(Σ长度)`',
                 '易错点：公差为 0 时只有全部相同才成立',
                 '区间内有重复数且公差不为 0 时，集合长度不足，检查会发现缺项',
                 '原文为 Python 2 风格，代码未改动'],
    ),
)
