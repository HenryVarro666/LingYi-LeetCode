def _col(S, i, v):
    if 'i' not in S or 'k' not in S:
        return None
    n = len(S['nums'])
    if i == S['i']:
        return 'blue'
    if i in (S['i'] - S['k'], S['i'] + S['k']) and 0 <= i < n:
        return 'pink'
    return None


CONFIG = dict(
    num=3452, title='好数字之和', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='一次遍历 + 越界当作符合', tags=[],
    code='''
class Solution:
    def sumOfGoodNumbers(self, nums: List[int], k: int) -> int:
        ans = 0
        for i, x in enumerate(nums):
            if (i < k or x > nums[i - k]) and (i + k >= len(nums) or x > nums[i + k]):
                ans += x
        return ans
''',
    call='Solution().sumOfGoodNumbers([1,3,2,1,5,4], 2)',
    expect=12,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 x，粉 = i-k 和 i+k 处的元素）', cell=100, h=240,
             pointers={'i': 'blue'}, color=_col),
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"累计好数字之和 ==`{S['ans']}`==" if 'ans' in S else '')),
    ],
    watch=['i', 'x', 'k', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累加所有好数字',
        'for i, x': '枚举 `nums[{i}] = {x}`',
        'if (i < k': lambda S, B, r: (
            f"左边 `i-k={S.i-S.k}` " + ("越界，视为满足" if S.i < S.k else f"`{S.x} > nums[{S.i-S.k}]={S.nums[S.i-S.k]}` " + ("成立" if S.x > S.nums[S.i-S.k] else "不成立"))
            + "；右边 `i+k=" + str(S.i+S.k) + "` " + ("越界，视为满足" if S.i + S.k >= len(S.nums) else f"`{S.x} > nums[{S.i+S.k}]={S.nums[S.i+S.k]}` " + ("成立" if S.x > S.nums[S.i+S.k] else "不成立"))
            + " → " + ("==是好数字==" if ((S.i < S.k or S.x > S.nums[S.i-S.k]) and (S.i + S.k >= len(S.nums) or S.x > S.nums[S.i+S.k])) else "不是好数字")),
        'ans += x': '`{x}` 是好数字，累加：`ans = {B.ans} + {x} = {ans}`',
        'return ans': '所有好数字之和 =={ret}==',
    },
    cards=dict(
        one_liner='越界的一侧当作“符合”，剩下的直接比大小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums[i]` 严格大于下标 `i-k` 和 `i+k` 处的元素（存在的话）就是好数字',
                 '两侧下标都不存在也算好；求所有好数字之和',
                 '示例：`[1,3,2,1,5,4]`，`k=2` → `3+5+4=12`'],
        quote='把 $i-k<0$ 或者 $i+k\\ge n$ 的情况当作「符合要求」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历 `nums`，累加符合要求的元素值',
              '`i < k` 表示左边没有元素，`i + k >= len(nums)` 表示右边没有',
              '用 `or` 短路：越界时不会去访问 `nums[i-k]`、`nums[i+k]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '必须==严格==大于，相等的不算好数字',
                 '`or` 的顺序不能反：先判越界，再取下标，否则会越界或访问到负下标',
                 '另有写法二：同样的条件写成一行 `sum(...)` 生成器'],
    ),
)
