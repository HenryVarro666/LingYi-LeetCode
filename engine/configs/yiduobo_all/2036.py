CONFIG = dict(
    num=2036, title='最大交替子数组和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='以加号项 / 减号项结尾的两个状态',
    tags=[],
    code='''
class Solution(object):
    def maximumAlternatingSubarraySum(self, nums):

        n = len(nums)
        
        res = f = nums[0]
        g = None
        for v in nums[1:]:
            last_f = f
            if g is None:
                f = v
            else:
                f = g + v
            
            if last_f - v < 0:
                g = None
            else:
                g = last_f - v
            
            res = max(res, f)
            if g is not None:
                res = max(res, g)
        
        return res
''',
    call='Solution().maximumAlternatingSubarraySum([3, -1, 1, 2])',
    expect=5,
    max_steps=60,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前元素 v；绿 = 已处理）', h=210, cell=110,
             color=lambda S, i, v: ('blue' if 'v' in S and i == S['nums'].index(S['v']) else
                                    ('green' if 'v' in S and i < S['nums'].index(S['v']) else None)) if 'f' in S else None),
        dict(type='text', size=28, h=70,
             fn=lambda S: (f"`f` = 以 + 号项结尾 = =={S['f']}==　`g` = 以 − 号项结尾 = =={'空' if S.get('g') is None else S['g']}==" if 'f' in S else '')),
    ],
    watch=[('v', 'v', 'blue'), ('f', 'f', 'cyan'), ('g', 'g', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = f = nums[0]': '第 0 个数只能是 + 号项：`f = res = {f}`',
        7: '`g[0]` 为空：减号项前面必须有加号项，第 0 个位置没有',
        'for v in nums': lambda S, B, r: (f'处理 `v = {S.v}`' if 'v' in S else '处理完毕'),
        'last_f = f': '先存下旧的 `f = {last_f}`，因为下面会覆盖 `f`',
        'if g is None': lambda S, B, r: ('`g` 为空：没有可接的减号项 → `v` 自己当新的开头，`f = v`' if S.get('g') is None
                                         else f'`g = {S.g}` 非空：可以接在减号项后面再加 `v`'),
        'f = v': '`g` 为空，从 `v` 重新开始：`f = {f}`',
        'f = g + v': '`f = g + v` = {B.g} + {v} = =={f}==：减号项后面接加号项',
        'if last_f - v < 0': lambda S, B, r: (f'`last_f - v = {S.last_f} - {S.v} = {S.last_f - S.v}` < 0 → 放弃这段，`g` 置空' if S.last_f - S.v < 0
                                              else f'`last_f - v = {S.last_f} - {S.v} = {S.last_f - S.v}` ≥ 0 → 保留'),
        16: '亏本的减号项不要：`g` 置为空',
        'g = last_f - v': '`g = last_f - v` = {last_f} − ({v}) = =={g}==：以 `v` 为减号项',
        'res = max(res, f)': '`res = max({B.res}, f = {f})` = =={res}==',
        'res = max(res, g)': '`g` 非空也算：`res = max({B.res}, g = {g})` = =={res}==',
        'return res': '最大交替子数组和 = =={ret}==',
    },
    cards=dict(
        one_liner='子段按 + − + − 交替取符号，f/g 分别记加号项、减号项结尾',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组的交替和：`a0 − a1 + a2 − …`（第一项取正）',
                 '求 `nums` 所有非空子数组中交替和的最大值',
                 '示例：`[3,-1,1,2]` → `5`（`3 − (−1) + 1`）'],
        quote='令f[i]表示以nums[i]结尾的最大的以加号项结尾的子段和，g[i]则表示以nums[i]结尾的最大的以减号项结尾的子段和。',
        quote_src='—— yiduobo 题解原文',
        idea=['加号项可以另起一段，也可以接在减号项后：`f = v` 或 `g + v`',
              '减号项必须接在加号项后：`g = last_f − v`，亏本（小于 0）就置空',
              '`f` 和非空的 `g` 都可能是答案，每步更新 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`g` 用 `None` 表示放弃；不能用 0 代替，否则会把没有的段当成 0',
                 '`last_f` 要先存：`f` 更新后 `g` 还要用旧 `f`',
                 '结尾可以是加号项，也可以是减号项'],
    ),
)
