def _info(S):
    if 'v' not in S:
        return '先把非零数乘起来，同时数负数、记下绝对值最小的负数'
    return (f"乘积 `res` = =={S.get('res')}==；负数 `{S.get('neg')}` 个；零 `{S.get('zero')}` 个；"
            f"绝对值最小的负数 = `{S.get('max_neg')}`")


CONFIG = dict(
    num=2708, title='一个小组的最大实力值', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='分类讨论 · 排除绝对值最小的负数',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def maxStrength(self, nums):

        res = None
        neg = 0
        zero = 0
        max_neg = None
        for v in nums:
            if v == 0:
                zero += 1
            else:
                if res is None:
                    res = v
                else:
                    res *= v
                if v < 0:
                    neg += 1
                    if max_neg is None or max_neg < v:
                        max_neg = v

        if res is None:
            res = 0
        elif res < 0 and len(nums) > 1:
            if neg == 1 and neg + zero == len(nums):
                res = 0
            else:
                res //= max_neg
        
        return res
''',
    call='Solution().maxStrength([3,-1,-5,2,5,-9])',
    expect=1350,
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=96,
             color=lambda S, i, v: ('green' if v > 0 else 'pink' if v < 0 else 'yellow') if 'v' in S and i == S['nums'].index(S['v']) else None),
        dict(type='text', fn=_info, size=26, h=90),
    ],
    watch=[('v', 'v', 'blue'), ('res', 'res', 'green'), ('neg', 'neg', 'pink'), ('zero', 'zero', 'yellow'), ('max_neg', 'max_neg', 'orange')],
    captions={
        'res = None': '`res` 还没有数，记为 `None`（区分“没选过”和“乘积为 0”）',
        'max_neg = None': '`max_neg`：目前绝对值==最小==的负数（即最接近 0 的那个）',
        'if v == 0': lambda S, B, r: ('`v = 0`：零先不乘进去，只计数' if S.v == 0 else f'`v = {S.v}` 不是 0，乘进乘积'),
        'zero += 1': '零不加入小组，`zero` → {zero}',
        'res = v': '第一个非零数，`res = {res}`',
        'res *= v': '正数全要、负数先全乘：`res` → =={res}==',
        'neg += 1': '又一个负数，`neg` → {neg}',
        'max_neg = v': '更新绝对值最小的负数：`max_neg = {max_neg}`',
        12: '`res` 还是 `None` 吗？{"是，这是第一个非零数，直接赋值" if res is None else "否，已经有乘积了，直接相乘"}',
        21: '`res is None` 吗？{"是，全是 0，答案只能是 0" if res is None else "否，有非零数"}',
        'elif res < 0': lambda S, B, r: (f'`res = {S.res} < 0`：负数个数为奇数，要排除一个' if S.res < 0 and len(S.nums) > 1 else f'`res = {S.res} ≥ 0`：负数成对，直接用'),
        'if neg == 1': '只有一个负数且其余全是 0：选 0 更大 → 答案 0（条件{"成立" if neg == 1 and neg + zero == len(nums) else "不成立"}）',
        'res //= max_neg': '奇数个负数：除掉绝对值最小的 `{max_neg}`，剩下的乘积最大 → ==`res = {res}`==',
        'return res': '最大实力值 `{res}`',
    },
    cards=dict(
        one_liner='正数全要，负数成对要，奇数个负数就扔掉绝对值最小的那个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选一个非空小组，使成员成绩的乘积最大',
                 '示例：`[3,-1,-5,2,5,-9]` → `1350`',
                 '难点：0 和负数怎么处理'],
        quote='当数组中存在奇数个负数时，应该将其中绝对值最小的那个排除出去，这样才能使得其他负数的乘积最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['有正数或 2 个以上负数时，==不要 0==，否则乘积必为 0',
              '负数要成对出现；奇数个就排除绝对值最小的',
              '正数全选。特判：只有一个负数且其余全是 0 → 选 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（此处恰好整除）',
                 '易错：只有一个数且为负数时只能选它；负数加 0 时选 0',
                 '对比灵神：灵神 DP 维护 mn/mx，不用分类；这里直接数学分类'],
    ),
)
