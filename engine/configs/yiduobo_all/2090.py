def _win(S):
    if 'now' not in S:
        return None
    idx = S.get('index')
    if idx is None:
        idx = S['k']
    return (idx - S['k'], idx + S['k'])


def _ctr(S):
    if 'now' not in S:
        return None
    return S.get('index', S['k'])


CONFIG = dict(
    num=2090, title='半径为 k 的子数组平均值', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举窗口中心的滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1358'],
    code='''
class Solution(object):
    def getAverages(self, nums, k):

        n = len(nums)
        res = [-1] * n
        if k + k + 1 > n:
            return res
        
        now = sum(nums[:k + k + 1])
        res[k] = now // (k + k + 1)
        for index in range(k + 1, n - k):
            now += nums[index + k] - nums[index - k - 1]
            res[index] = now // (k + k + 1)
        
        return res
''',
    call='Solution().getAverages([7,4,3,9,1,8,5,2,6], 2)',
    expect=[-1, -1, 4, 5, 5, 5, 4, -1, -1],
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [中心−k, 中心+k]）', h=250, cell=96,
             pointers={_ctr: 'orange'}, pointer_labels={_ctr: '中心'},
             window=(lambda S: (_win(S) or (None,))[0], lambda S: (_win(S) or (None, None))[1]),
             color=lambda S, i, v: 'orange' if _ctr(S) == i else None),
        dict(type='array', var='res', label='res', h=200, cell=96,
             color=lambda S, i, v: 'green' if v != -1 else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"窗口和 `now = {S['now']}`，窗口长 `k + k + 1 = {2 * S['k'] + 1}`" if 'now' in S
                           else '中心只能取 ==k .. n−k−1==，否则窗口不完整')),
    ],
    watch=[('n', 'n'), ('index', 'index', 'orange'), ('now', 'now', 'cyan')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'res = [-1] * n': '先全部填 `-1`',
        'if k + k + 1 > n': lambda S, B, r: (f'`{2 * S.k + 1} > {S.n}`：一个完整窗口都没有' if 2 * S.k + 1 > S.n
                                             else f'`k + k + 1 = {2 * S.k + 1} ≤ n = {S.n}`：至少有一个完整窗口'),
        'return res': lambda S, B, r: f'返回 `{r}`',
        'now = sum(nums[:k + k + 1])': '第一个窗口中心为 `k = {k}`：`now = sum({nums[:2 * k + 1]}) = {now}`',
        'res[k] = now': '`res[{k}] = {now} // {2 * k + 1} = {res[k]}`',
        'for index in range(k + 1, n - k)': lambda S, B, r: (f'中心移到 `index = {S.index}`（中心最大到 `n−k−1 = {S.n - S.k - 1}`）'
                                                             if 'index' not in B or S.index != B.index else '中心已到 `n−k−1`，结束'),
        'now += nums[index + k]': '右侧 `nums[{index + k}] = {nums[index + k]}` 纳入、左侧 `nums[{index - k - 1}] = {nums[index - k - 1]}` 移出：`now = {now}`',
        'res[index] = now': '`res[{index}] = {now} // {2 * k + 1} = {res[index]}`',
    },
    cards=dict(
        one_liner='记录窗口中心，中心只在 k 到 n−k−1 之间移动',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['对每个 `i` 求 `nums[i−k..i+k]` 的整除平均值，不足 k 个邻居则为 `-1`',
                 '示例：`nums = [7,4,3,9,1,8,5,2,6], k = 3` → `[-1,-1,-1,5,4,4,-1,-1,-1]`',
                 '本视频用 `k = 2` → `[-1,-1,4,5,5,5,4,-1,-1]`'],
        quote='我在这里采用的是记录窗口中心位置的做法。……当窗口中心从index - 1移动到index时，右侧元素nums[index + k]将被纳入到窗口中，而左侧元素nums[index - k - 1]则将被移出窗口。',
        quote_src='—— yiduobo 题解原文',
        idea=['特判：`k + k + 1 > n` 时一个完整窗口都没有，直接返回全 -1',
              '中心为 `k` 的窗口先 `sum` 出来，然后中心逐个右移',
              '纳入 `nums[index + k]`、移出 `nums[index − k − 1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '中心范围是 `[k, n−k−1]`，所以 `range(k + 1, n - k)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神枚举右端点、答案写到 `i−k`；yiduobo 直接枚举中心'],
    ),
)
