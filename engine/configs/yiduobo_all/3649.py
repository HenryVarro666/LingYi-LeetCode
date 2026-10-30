CONFIG = dict(
    num=3649, title='完美对的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='分类讨论化简 + 排序 + 双指针',
    tags=['滑动窗口与双指针', '数学算法', '难度分 1716'],
    code='''
class Solution(object):
    def perfectPairs(self, nums):
        
        nums.sort(key=lambda d:abs(d))
        p = 0
        res = 0
        for index, v in enumerate(nums[1:], 1):
            while abs(nums[p]) < (abs(v) + 1) // 2:
                p += 1
            
            res += index - p

        return res
''',
    call='Solution().perfectPairs([-3, 2, -1, 4, 7, -6])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"v = `{S['v']}`：可配对的 `|x|` 范围 `[{(abs(S['v']) + 1) // 2}, {abs(S['v'])}]`，下标 `[{S['p']}, {S['index'] - 1}]` 共 =={S['index'] - S['p']}== 个" if 'index' in S and 'p' in S and 'v' in S else '先按绝对值从小到大排序')),
        dict(type='array', var='nums', pointers={'p': 'blue', 'index': 'pink'}, window=('p', 'index'), h=300,
             color=lambda S, i, v: ('pink' if i == S['index'] else 'blue' if i == S['p'] else None) if 'index' in S and 'p' in S else None,
             dim=lambda S, i, v: 'index' in S and 'p' in S and not (S['p'] <= i <= S['index'])),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '拆开绝对值分四种符号情况，结论都一样：较大的 `|x|` ≤ 较小的 `|x|` 的两倍。按绝对值排序：`{nums}`',
        'p = 0': '`p`：能与当前数配对的最小下标',
        'res = 0': '`res` 累计完美对数',
        'for index, v': '`v = nums[{index}] = {v}`：只与绝对值不超过它的数配对，每一对只算一次',
        'while abs(nums[p])': lambda S, B, ret: (f'`|nums[p]| = {abs(S.nums[S.p])}` < `(|v|+1)//2 = {(abs(S.v)+1)//2}`：两倍也够不到 `|v|` → `p` 后移' if abs(S.nums[S.p]) < (abs(S.v) + 1) // 2 else f'`|nums[p]| = {abs(S.nums[S.p])}` >= `{(abs(S.v)+1)//2}`：`p` 位置合格，停'),
        'p += 1': '`p` → {p}：`index` 增大，可配对的最小下标只会右移',
        'res += index - p': '`p` 到 `index-1` 都能和 `{v}` 配对，共 `{index} - {p}` = =={index-p}== 组 → `res = {res}`',
        'return res': '完美对共 `{res}` 个',
    },
    cards=dict(
        one_liner='拆开绝对值讨论四种符号，结论统一后按绝对值排序数对',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['下标对 `(i, j)` 同时满足 `min(|a-b|,|a+b|) ≤ min(|a|,|b|)` 与 `max(...) ≥ max(...)`',
                 '求完美对的数目',
                 '本视频：`[-3,2,-1,4,7,-6]` → `8`'],
        quote='对于这类绝对值有关的问题，一种自然的想法就是拆开绝对值符号分情况讨论。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a, b` 同号、异号共四种情况，第二个式子都恒成立',
              '第一个式子都化成：绝对值小的数的两倍 ≥ 绝对值大的数',
              '`|v|` 能配的 `|x|` 在 `(|v|+1)//2` 到 `|v|`；排序后用 `p` 记最小下标，只增不减'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`(|v|+1)//2` 是向上取整的一半：`|x|×2 ≥ |v|` 的最小 `|x|`',
                 '从下标 1 开始遍历，`index - p` 就是和前面配对的个数',
                 '原文为 Python 2 风格，但 Python 3 下无需修改，已原样使用',
                 '对比灵神：灵神用数轴距离推式子并写 `abs(a)*2 < abs(b)`，yiduobo 逐符号拆开并写成 `(|v|+1)//2`'],
    ),
)
