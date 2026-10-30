CONFIG = dict(
    num=1785, title='构成特定和需要添加的最少元素', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='顶着 limit 添加',
    code='''
class Solution(object):
    def minElements(self, nums, limit, goal):

        delta = abs(sum(nums) - goal)
        res = delta // limit
        if delta % limit != 0:
            res += 1
        
        return res
''',
    call='Solution().minElements([1,-1,1], 3, -4)',
    expect=2,
    views=[
        dict(type='array', var='nums', h=200, label='nums（和 = 1）'),
        dict(type='text', size=34, h=120, fn=lambda S: (
            f"`goal = {S['goal']}`，当前和 `{sum(S['nums'])}`，差距 `delta = {S['delta']}`" if 'delta' in S
            else f"`goal = {S['goal']}`，当前和 `{sum(S['nums'])}`")),
        dict(type='text', size=34, h=120, fn=lambda S: (
            f"每个新数最多 `{S['limit']}`：`{S['delta']} // {S['limit']} = {S['delta'] // S['limit']}` 个满额" if 'delta' in S else '')),
    ],
    watch=['limit', 'goal', ('delta', 'delta', 'yellow'), ('res', 'res', 'green')],
    captions={
        'delta = abs': '当前和 `{sum(nums)}`，目标 `{goal}`，差距 `delta = |{sum(nums)} − ({goal})|` = =={delta}==。正负方向无关，取绝对值',
        'res = delta': '每个新数的绝对值最多 `{limit}`，==顶着 limit 加==最省：`{delta} // {limit}` = =={res}== 个',
        'if delta % limit': lambda S, B, r: (f'`{S.delta} % {S.limit} = {S.delta % S.limit}` ≠ 0：还差一截，不够 limit 也得再加一个数' if S.delta % S.limit != 0
                                           else f'`{S.delta} % {S.limit} = 0`：刚好凑齐，不用多加'),
        'res += 1': '补上那个不满额的数：`res` → =={res}==',
        'return res': '最少需要添加 `{res}` 个元素',
    },
    cards=dict(
        one_liner='每个新数都顶着 limit，差距除以 limit 向上取整',
        complexity='时间 `O(n)`（求和），空间 `O(1)`',
        problem=['给整数数组 `nums`，每个元素绝对值 `<= limit`；再添加最少的元素（绝对值也 `<= limit`），使总和等于 `goal`',
                 '示例：`nums=[1,-1,1]`，`limit=3`，`goal=-4` → `2`（加 `-2`、`-3`）'],
        quote='为了使得添加的元素最少，那么就应该顶着limit来添加数字，那么可以先计算出当前数组和与goal的差距delta',
        quote_src='—— yiduobo 题解原文',
        idea=['先算差距 `delta = |sum(nums) − goal|`，方向（正负）不影响个数',
              '每个新数最多贡献 `limit`，所以先用 `delta // limit` 个满额的数',
              '余数不为 0，还要再加一个数补齐：即向上取整'],
        after=[dict(heading='向上取整的写法', lines=['`delta // limit` 个满额数，余数非 0 再加一个', '等价于 `ceil(delta / limit)`', '例：`delta=5, limit=3` → 一个 `3`，再补一个 `2`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：要取 `abs`，差距为负时同样靠加负数补',
                 '易错：余数不为 0 要 `+1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
