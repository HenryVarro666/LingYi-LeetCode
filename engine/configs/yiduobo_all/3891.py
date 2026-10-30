CONFIG = dict(
    num=3891, title='最大化特殊下标数目的最少增加次数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='奇偶分类 · 正反两趟前缀和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1953'],
    code='''
class Solution(object):
    def minIncrease(self, nums):

        n = len(nums)

        if n % 2 == 1:
            res = 0
            for index in range(1, n - 1, 2):
                res += max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)
            return res
        
        left = [0]
        for index in range(1, n - 1, 2):
            v = max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)
            left.append(left[-1] + v)
        
        right = [0]
        for index in range(n - 2, 0, -2):
            v = max(max(nums[index - 1], nums[index + 1]) + 1 - nums[index], 0)
            right.append(right[-1] + v)
        
        res = None
        for cnt in range(n // 2):
            cost = left[cnt] + right[n // 2 - 1 - cnt]
            if res is None or res > cost:
                res = cost
        return res
''',
    call='Solution().minIncrease([4, 6, 5, 2, 5, 5])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前正在算代价的下标）', h=230, cell=84, pointers={'index': 'blue'},
             color=lambda S, k, v: 'yellow' if S.get('index') == k and S.get('_line', 0) in (15, 16, 20, 21) else None),
        dict(type='array', var='left', label='left[c]：前缀改 c 个奇数下标的总代价', h=170, cell=84,
             color=lambda S, k, v: 'cyan' if 'cnt' in S and 'right' in S and S.get('_line', 0) >= 23 and k == S['cnt'] else None),
        dict(type='array', var='right', label='right[c]：后缀改 c 个偶数下标的总代价', h=170, cell=84,
             color=lambda S, k, v: 'pink' if 'cnt' in S and S.get('_line', 0) >= 23 and k == S['n'] // 2 - 1 - S['cnt'] else None),
        dict(type='text', h=70, size=26, fn=lambda S: (
            f"前缀 `{S['cnt']}` 个 + 后缀 `{S['n'] // 2 - 1 - S['cnt']}` 个：`{S['left'][S['cnt']]} + {S['right'][S['n'] // 2 - 1 - S['cnt']]}` = =={S['left'][S['cnt']] + S['right'][S['n'] // 2 - 1 - S['cnt']]}==") if 'cnt' in S and 'right' in S else '先分奇偶：奇数时改全部奇数下标；偶数时前缀奇数 + 后缀偶数'),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'cyan'), ('cost', 'cost', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'if n % 2 == 1': 'n 是偶数 → 多出一个空位：前缀改奇数下标，后缀改偶数下标（前缀、后缀都可以为空）',
        'left = [0]': '`left[c]`：前缀改 `c` 个奇数下标的总代价，`left[0] = 0` 是前缀为空',
        'for index in range(1, n - 1, 2)': lambda S, B, r: (f'正着枚举奇数下标 `index = {S.index}`' if S.get('index') != B.get('index') else '奇数下标都算完了'),
        'right = [0]': '`right[c]`：后缀改 `c` 个偶数下标的总代价',
        'for index in range(n - 2': lambda S, B, r: (f'倒着枚举偶数下标 `index = {S.index}`' if S.get('index') != B.get('index') else '偶数下标都算完了'),
        'v = max': '`nums[{index}]` 要大于 `max({nums[index-1]}, {nums[index+1]}) = {max(nums[index-1], nums[index+1])}`，目标值 +1，代价 `max(.. - {nums[index]}, 0)` = =={v}==',
        'left.append': '`left` 累加：`left = {left}`',
        'right.append': '`right` 累加：`right = {right}`',
        'res = None': '`res` 记录最小总代价，先设为空',
        'for cnt in range': lambda S, B, r: (f'枚举前缀改 `cnt = {S.cnt}` 个奇数下标，后缀就改 `{S.n // 2 - 1 - S.cnt}` 个偶数下标' if S.get('cnt') != B.get('cnt') else '所有分配方式都试完了'),
        'cost = left': '`cost = left[{cnt}] + right[{n // 2 - 1 - cnt}] = {left[cnt]} + {right[n // 2 - 1 - cnt]}` = =={cost}==',
        'if res is None': lambda S, B, r: (('`res` 还是空 → 成立，先记下这个代价' if S.res is None else f'`res = {S.res} > cost = {S.cost}` → 成立，更新') if (B.get('res') is None or B.get('res') > S.cost) else f'`res = {S.res}` 已经不比 `cost = {S.cost}` 大 → 不更新'),
        'res = cost': '`res` 更新为 =={res}==',
        'return res': '最少操作数 =={ret}==',
    },
    cards=dict(
        one_liner='特殊下标不相邻：偶数长度时，前面改奇数下标、后面改偶数下标',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums[i]` 比左右邻居都大，下标 `i` 就是特殊的（不含两端）',
                 '每次操作可以让某个数 +1',
                 '先让特殊下标尽量多，再让操作数最少',
                 '本视频：`[4,6,5,2,5,5]` → `1`'],
        quote='特殊下标对应的元素必须大于两侧相邻元素的特性，意味着特殊下标不能出现在数组的两侧，同时两个特殊下标也不可能连续出现。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 为奇数：必须改全部奇数下标，一趟累加代价',
              'n 为偶数：最终是「前缀的奇数下标 + 后缀的偶数下标」，长 8 的例子有 4 种配对',
              '正反两趟算出 `left`、`right`，枚举前缀个数 `cnt` 取最小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '代价 `max(max(左, 右) + 1 − 当前, 0)`：已经特殊就不用改，所以要和 0 取最大',
                 '`right[n//2-1-cnt]`：前缀 `cnt` 个，后缀就是剩下的个数',
                 '原文已是 `//` 写法，代码未改动',
                 '对比灵神：灵神用 `suf -= ...` 原地撤销，yiduobo 用两个前缀和数组'],
    ),
)
