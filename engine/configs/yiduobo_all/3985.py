def _top(S):
    if 'right' not in S:
        return '`f`：数之间插入 `0`（解决偶回文），首尾放 `-1`、`-2`（扩展时自然停下）'
    if 'index' not in S:
        return ''
    return f"遍历中心 `f[{S['index']}]`；`mid = {S['mid']}`，`right = {S['right']}`（已扩展到的最右边界）"


CONFIG = dict(
    num=3985, title='回文子数组求和', difficulty='Hard', category='字符串',
    author='yiduobo', technique='马拉车 + 前缀和',
    tags=['灵神题单', '字符串', '难度分 2202'],
    code='''
class Solution(object):
    def getSum(self, nums):
        
        f = [-1]
        for v in nums:
            f.append(v)
            f.append(0)
        f[-1] = -2

        s = [0]
        for v in f[1:]:
            s.append(s[-1] + v)
        
        mid = 0
        right = 0
        r = [0]
        res = 0
        for index in range(1, len(f) - 1):
            if index < right:
                r.append(min(right - index, r[mid * 2 - index]))
            else:
                r.append(1)

            while f[index - r[index]] == f[index + r[index]]:
                r[index] += 1

            res = max(res, s[index + r[index] - 1] - s[index - r[index]])

            if right < index + r[index]:
                mid = index
                right = index + r[index]

        return res
''',
    call='Solution().getSum([3,1,3,2])',
    expect=7,
    skip=['f.append', 'for v in nums', 'for v in f[1:]', 'r = [0]', 'for index in range', 's.append(s[-1]', 'right = 0', 'res = 0', 'mid = index', 'right = index'],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='array', var='f', label='f（0 = 插入的间隔，-1/-2 = 边界）', cell=60, pointers={'index': 'blue', 'mid': 'pink'}, h=190,
             color=lambda S, k, v: 'green' if 'index' in S and 'r' in S and len(S['r']) > S['index'] and S['index'] - S['r'][S['index']] < k < S['index'] + S['r'][S['index']] else None),
        dict(type='array', var='r', label='r（回文半径）', cell=60, h=150),
        dict(type='array', var='s', label='s（f 的前缀和）', cell=60, h=150),
    ],
    watch=[('index', 'index', 'blue'), ('mid', 'mid', 'pink'), ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        's = [0]': '前缀和 `s[k]` = `f` 前 `k` 个数之和，稍后用它一次算出回文子数组的和',
        'mid = 0': '`mid` 是最右回文的中心，`right` 是它的右边界',
        'if index < right': lambda S, B, r: (f'`index = {S.index} < right = {S.right}`：落在最右回文里 → 用关于 `mid` 的对称点初始化'
                                             if S.index < S.right else
                                             f'`index = {S.index} >= right = {S.right}`：在最右回文外，前面的信息没用 → 半径从 1 开始'),
        'r.append(min': '对称中心 `{mid*2-index}`，半径 `{r[mid*2-index]}`；右侧只到 `right - index = {right-index}` → 取小：`r[{index}] = {r[index]}`',
        'r.append(1)': '`r[{index}]` 初始为 1',
        'while f[index': lambda S, B, ret: (f'`f[{S.index-S.r[S.index]}] = {S.f[S.index-S.r[S.index]]}` == `f[{S.index+S.r[S.index]}] = {S.f[S.index+S.r[S.index]]}` → ==继续向两侧扩展=='
                                            if S.f[S.index-S.r[S.index]] == S.f[S.index+S.r[S.index]] else
                                            f'`f[{S.index-S.r[S.index]}] = {S.f[S.index-S.r[S.index]]}` ≠ `f[{S.index+S.r[S.index]}] = {S.f[S.index+S.r[S.index]]}` → 扩展结束（负数边界一定停）'),
        'r[index] += 1': '半径加一：`r[{index}] = {r[index]}`',
        'res = max': '半径 `{r[index]}` 的子数组和 = `s[{index+r[index]-1}] - s[{index-r[index]}]` = `{s[index+r[index]-1] - s[index-r[index]]}`；`res` = =={res}==',
        'if right < index': lambda S, B, r: (f'`right = {S.right} < index + r[index] = {S.index + S.r[S.index]}` → 回文伸得更远：`mid` → {S.index}，`right` → {S.index + S.r[S.index]}'
                                             if S.right < S.index + S.r[S.index] else
                                             f'`right = {S.right} >= {S.index + S.r[S.index]}`：没超过原边界，不更新'),
        'return res': '全是正数，每个中心取最大半径，最大和为 `{res}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='正数 → 半径越大和越大：马拉车求半径，同步用前缀和算答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给正整数数组 `nums`，找和最大的==回文子数组==',
                 '本视频：`[3,1,3,2]` → `7`（子数组 `[3,1,3]`）'],
        quote='由于nums中都是正整数，且题目的目标是使得回文子数组的元素和最大，那么当确定了回文子数组的中心后，就应该让这个子数组的回文半径尽可能大，于是问题就变成了枚举回文中心，计算对应的最大回文半径的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['原数组相邻元素间插入 `0`：偶数长度回文也有中心，且不影响和',
              '两侧放 `-1`、`-2`：向外扩展时一定停下，不会越界',
              '`mid`/`right` 记录最右回文，`index` 落在里面就用对称点的半径起步，再暴力扩展'],
        summary=['时间 `O(n)`：`right` 只向右移，扩展总次数是线性的',
                 '前缀和 `s[index + r - 1] - s[index - r]` 就是半径 `r` 的回文子数组和',
                 '`f[-1] = -2`：把最后插入的 `0` 换成边界，两端边界不同，不会匹配',
                 '对比灵神：他用 `t` 的 `-2 -1 ... -1 -3` 哨兵，yiduobo 是插 `0` + `-1/-2`，同步算答案'],
    ),
)
