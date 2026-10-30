def _txt(S):
    if 'p' not in S or 'index' not in S:
        return '先排序，再用单调性：便宜的零件涨价，贵的那个只能更便宜'
    i, p, t = S['index'], S['p'], S['target']
    n = S['nums']
    if p <= i:
        return f'`p = {p} <= index = {i}`：没有更贵的零件可配了'
    return f'`{n[i]} + {n[p]} = {n[i]+n[p]}`，预算 `{t}`；`index` 与 `({i+1}..{p})` 都可行：=={p-i}== 种'


CONFIG = dict(
    num='LCP 28', title='采购方案', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 相向双指针',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def purchasePlans(self, nums, target):

        nums.sort()
        p = len(nums) - 1
        res = 0
        mod = 10 ** 9 + 7
        for index in range(len(nums)):
            while p > index and nums[p] + nums[index] > target:
                p -= 1
            if p == index:
                break
            res += p - index
            if res >= mod:
                res -= mod
        
        return res
''',
    call='Solution().purchasePlans([2,1,3,5,4,3], 6)',
    expect=9,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'}, h=300,
             color=lambda S, i, v: ('blue' if i == S['index'] else 'pink' if i == S['p'] else None) if 'p' in S and 'index' in S else None,
             dim=lambda S, i, v: 'p' in S and 'index' in S and i > S['p']),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), 'target', ('res', 'res', 'green')],
    captions={
        'nums.sort()': '价格从小到大排序：`{nums}`',
        'p = len': '`p` 指向最贵的零件，下标 {p}',
        'res = 0': '`res` 累计方案数',
        'mod = ': '答案要对 `10^9 + 7` 取模',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：枚举较便宜的零件 `{S.nums[S.index]}`' if 'index' not in B or B['index'] != S.index else '枚举完了'),
        'while p > index': lambda S, B, r: (f'`{S.nums[S.p]} + {S.nums[S.index]} = {S.nums[S.p]+S.nums[S.index]} > {S.target}`：太贵，`p` 左移' if S.p > S.index and S.nums[S.p] + S.nums[S.index] > S.target
                                              else (f'`p = {S.p}` 已到 index，停' if S.p <= S.index else f'`{S.nums[S.p]} + {S.nums[S.index]} = {S.nums[S.p]+S.nums[S.index]} <= {S.target}`：p 就是能配的最贵零件')),
        'p -= 1': '较贵的零件只能越来越便宜：`p` → {p}',
        'if p == index': lambda S, B, r: ('`p == index`：找不到更贵的配对了，直接退出' if S.p == S.index else f'`p = {S.p} > index = {S.index}`：还有配对，继续'),
        'res += p - index': '`index` 与 `index+1 .. p` 共 `{p} - {index}` = {p-index} 种都可行，`res` = =={res}==',
        'if res >= mod': '`res = {res}`，未超过 `mod`' ,
        'return res': '一共 =={res}== 种方案',
    },
    cards=dict(
        one_liner='便宜的涨价，贵的只能降价：双指针一次数一批',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`nums` 是各零件价格，`target` 是预算；买两种不同零件，总价不超过预算',
                 '求方案数，对 `10^9 + 7` 取模',
                 '示例：`nums=[2,5,3,5]`，`target=6` → `1`',
                 '本视频：`[2,1,3,5,4,3]`，`target=6` → `9`'],
        quote='随着便宜零件价格的上涨，比较贵的那个零件的价格只能是越来越便宜，因此在这里利用单调性就可以在均摊O(1)的时间内找出比较贵的那个零件的最大下标p。',
        quote_src='—— yiduobo 题解原文',
        idea=['两数之和的变种：排序后枚举较便宜的 `index`',
              '`p` 只会左移不会回头；`index` 与 `index+1 .. p` 共 `p - index` 种',
              '`p <= index` 说明没有更贵的可配，直接退出'],
        summary=['时间 `O(n log n)`（排序），双指针部分 `O(n)`，空间 `O(1)`',
                 '`p == index` 时必须 `break`，否则会把自己和自己配',
                 '条件是总价 ==不超过== 预算：`> target` 才左移',
                 '本题难度库里未标注；原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
