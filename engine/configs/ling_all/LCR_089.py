CONFIG = dict(
    num='LCR 089', title='打家劫舍', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='线性 DP · 滚动变量',
    tags=[],
    code='''
class Solution:
    def rob(self, nums: List[int]) -> int:
        f0 = f1 = 0
        for i, x in enumerate(nums):
            f0, f1 = f1, max(f1, f0 + x)
        return f1
''',
    call='Solution().rob([2,7,9,3,1])',
    expect=12,
    skip=['f0 = f1 = 0', 'for i, x in enumerate'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前房子 x）', cell=84, h=230, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') and S.get('_line', 0) > 0 and 'x' in S else None,
             dim=lambda S, k, v: 'i' in S and k > S['i']),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"不偷：`f1 = {S['f1']}`　偷：`f0 + x = {S['f0']} + {S['x']} = {S['f0'] + S['x']}`　→ 取大 ==`{max(S['f1'], S['f0'] + S['x'])}`==" if 'x' in S and S.get('_line') == 6
                           else "`f1` = 到目前为止能偷到的最大金额，`f0` = 再往前一间时的最大金额")),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'blue'), ('f0', 'f0', 'cyan'), ('f1', 'f1', 'green')],
    captions={
        'f0, f1 = f1': lambda S, B, ret: (f'`f1 = max(f1, f0 + x) = max({B.f1}, {B.f0} + {B.x}) = {S.f1}`：'
                                           + ('偷这间更多，选偷' if B.f0 + B.x > B.f1 else '不偷更多（或一样），跳过这间')
                                           + f'；`f0` 滚动为 {S.f0}'),
        'return f1': '`f1` 就是偷完所有房子的最大金额 = =={ret}==',
    },
    cards=dict(
        one_liner='每间房两种选择：不偷继承前一间，偷则加上前前一间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小偷沿街偷窃，相邻两间房不能同时偷，否则报警',
                 '`nums[i]` 是第 `i` 间房的金额，求能偷到的最高金额',
                 '示例：`[2,7,9,3,1]` → `12`（偷 2、9、1）'],
        quote='递归搜索 + 保存计算结果 = 记忆化搜索……1:1 翻译成迭代……空间优化：只用到 f[i+1] 和 f[i]，用两个变量滚动。',
        quote_src='—— 灵茶山艾府题解（一、二、三）',
        idea=['`dfs(i)` = 前 `i` 间房的最大金额：不偷 `dfs(i-1)`，偷 `dfs(i-2) + nums[i]`',
              '把递归 1:1 翻译成数组 `f`，下标整体右移 2 位避免负数',
              '`f[i+2]` 只依赖 `f[i+1]` 和 `f[i]`，两个变量 `f0, f1` 滚动即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先记忆化搜索，再 1:1 翻译成递推，最后空间优化，是 DP 的标准思路',
                 '易错：`f0, f1 = f1, max(f1, f0 + x)` 是同时赋值，右边都用旧值',
                 '同类题：LCR 090 打家劫舍 II（环形）、740. 删除并获得点数'],
    ),
)
