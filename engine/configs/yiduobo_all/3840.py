CONFIG = dict(
    num=3840, title='打家劫舍 V', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='偷 / 不偷 两个状态 f, g',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1619'],
    code='''
class Solution(object):
    def rob(self, nums, colors):
        
        f, g = nums[0], 0
        for index in range(1, len(nums)):
            if colors[index] != colors[index - 1]:
                f, g = max(f, g) + nums[index], max(f, g)
            else:
                f, g = g + nums[index], max(f, g)
        
        return max(f, g)
''',
    call='Solution().rob([4,1,5,2,6,3], [1,1,2,2,2,3])',
    expect=18,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=200, label='nums（金额）',
             color=lambda S, k, v: 'green' if 'index' in S and k == S['index'] else None,
             dim=lambda S, k, v: 'index' in S and k > S['index']),
        dict(type='array', var='colors', h=170, label='colors（颜色码）',
             color=lambda S, k, v: {1: 'blue', 2: 'orange', 3: 'purple'}.get(v)),
        dict(type='text', size=30, fn=lambda S: (f"`f` 偷当前房 = =={S['f']}==　　`g` 不偷当前房 = =={S['g']}==" if 'g' in S else '')),
    ],
    watch=['index', ('f', 'f', 'green'), ('g', 'g', 'cyan')],
    captions={
        'f, g = nums[0]': '第 0 间：偷则 `f = nums[0] = {f}`，不偷则 `g = 0`',
        'for index': lambda S, B, r: (f'看第 `{S.index}` 间房：金额 `{S.nums[S.index]}`，颜色 `{S.colors[S.index]}`' if B.get('index') != S.index else '所有房屋处理完'),
        'if colors[index] != colors[index - 1]': lambda S, B, r: (f"颜色 `{S.colors[S.index]}` ≠ 前一间的 `{S.colors[S.index - 1]}`：偷本间不受前一间限制" if S.colors[S.index] != S.colors[S.index - 1] else f"颜色 `{S.colors[S.index]}` == 前一间：偷本间时前一间必须不偷"),
        'f, g = max(f, g) +': '`f = max({B.f}, {B.g}) + {nums[index]} = {f}`（前一间偷不偷都行）；`g = max({B.f}, {B.g}) = {g}`',
        'f, g = g +': '`f = g + {nums[index]} = {B.g} + {nums[index]} = {f}`（前一间只能不偷）；`g = max({B.f}, {B.g}) = {g}`（不偷本间，前一间随意）',
        'return max': '最后一间偷或不偷取较大者：`max({f}, {g}) = {ret}`',
    },
    cards=dict(
        one_liner='f 记「偷了这间」，g 记「没偷这间」，颜色相同时 f 只能接 g',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums[i]` 是第 `i` 间房的金额，`colors[i]` 是它的颜色码',
                 '相邻且颜色相同的两间房不能同时偷，求最大金额',
                 '本视频：`nums=[4,1,5,2,6,3], colors=[1,1,2,2,2,3]` → `18`'],
        quote='令f[index]表示对于第0到第index间房屋，偷窃了第index间房屋的最大收益，而g[index]则表示不偷窃第index间房屋的最大收益',
        quote_src='—— yiduobo 题解原文',
        idea=['颜色相同：`f = g_前 + nums[index]`，前一间必须不偷',
              '颜色不同：`f = max(f_前, g_前) + nums[index]`，不受限制',
              '`g = max(f_前, g_前)`：不偷本间，前一间随意；两个状态只依赖上一轮 → 变量滚动'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：==元组赋值右边用的都是旧的 f、g==，不会互相覆盖',
                 '最后答案是 `max(f, g)`：最后一间可偷可不偷',
                 '对比灵神：灵神只用一个 f 序列，颜色不同时直接必偷；这里显式分偷/不偷两个状态',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
