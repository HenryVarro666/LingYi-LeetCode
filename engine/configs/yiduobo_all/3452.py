def _col(S, i, v):
    if 'index' not in S or 'k' not in S:
        return None
    n = len(S['nums'])
    if i == S['index']:
        return 'blue'
    if i in (S['index'] - S['k'], S['index'] + S['k']) and 0 <= i < n:
        return 'pink'
    return None


CONFIG = dict(
    num=3452, title='好数字之和', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按定义一趟遍历', tags=[],
    code='''
class Solution(object):
    def sumOfGoodNumbers(self, nums, k):
        
        res = 0
        for index, v in enumerate(nums):
            if (index - k < 0 or nums[index - k] < v) and (index + k >= len(nums) or nums[index + k] < v):
                res += v
        
        return res
''',
    call='Solution().sumOfGoodNumbers([1,3,2,1,5,4], 2)',
    expect=12,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前元素，粉 = 左右相距 k 的元素）', cell=100, h=240,
             pointers={'index': 'blue'}, color=_col),
        dict(type='text', h=90, size=30, fn=lambda S: f"已累加 ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=['index', 'v', 'k', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累加好元素',
        'for index, v': '看 `nums[{index}] = {v}`',
        'if (index - k': lambda S, B, r: (
            f"左侧：`index-k={S.index-S.k}` " + ("不存在 → 满足" if S.index - S.k < 0 else f"`nums[{S.index-S.k}]={S.nums[S.index-S.k]}` " + ("< " if S.nums[S.index-S.k] < S.v else ">= ") + f"`{S.v}`")
            + f"；右侧：`index+k={S.index+S.k}` " + ("不存在 → 满足" if S.index + S.k >= len(S.nums) else f"`nums[{S.index+S.k}]={S.nums[S.index+S.k]}` " + ("< " if S.nums[S.index+S.k] < S.v else ">= ") + f"`{S.v}`")
            + " → " + ("==两边都满足，是好元素==" if ((S.index - S.k < 0 or S.nums[S.index-S.k] < S.v) and (S.index + S.k >= len(S.nums) or S.nums[S.index+S.k] < S.v)) else "不是好元素")),
        'res += v': '累加 `{v}`：`res` = {res}',
        'return res': '好元素之和 =={ret}==',
    },
    cards=dict(
        one_liner='两边“不存在或更小”都成立，就累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums[index]` 在 `index-k`、`index+k` 处的元素（若存在）都严格更小，就是好的',
                 '两处都不存在也算好，求好元素之和',
                 '本视频：`[1,3,2,1,5,4]`，`k=2` → `12`'],
        quote='直接对nums进行一趟遍历，对于nums[index]，按照题目描述中关于好元素的定义，检测index - k是否不存在，或者nums[index]严格大于nums[index - k]',
        quote_src='—— yiduobo 题解原文',
        idea=['完全按题意翻译：左边“不存在或更小”，右边“不存在或更小”',
              '“不存在”用 `index - k < 0`、`index + k >= len(nums)` 判断',
              '两边同时满足才把 `v` 累加进 `res`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '“严格大于”：相等不算，所以用 `<` 而不是 `<=`',
                 '先判越界再取下标，靠 `or` 短路避免越界',
                 '原文已是 Python 3 可运行写法'],
    ),
)
