CONFIG = dict(
    num=1130, title='叶值的最小代价生成树', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 贪心合并最小的数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def mctFromLeafValues(self, arr):
        stack = [16]
        res = 0
        for num in arr:
            while num >= stack[-1]:
                res += stack[-1] * min(num, stack[-2])
                stack.pop()
            stack.append(num)
        
        while len(stack) > 2:
            res += stack[-1] * stack[-2]
            stack.pop()
        
        return res
''',
    call='Solution().mctFromLeafValues([6,2,4,3])',
    expect=44,
    views=[
        dict(type='array', var='arr', label='arr（叶子的值，按中序）', h=190,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='stack', var='stack', label='stack（严格递减，栈底 16 是哨兵）', h=150, font=30),
        dict(type='text', fn=lambda S: f"累计代价 `res = {S['res']}`", size=28, h=90),
    ],
    watch=[('num', 'num', 'blue'), ('stack', 'stack', 'yellow'), ('res', 'res', 'green')],
    captions={
        'stack = [16]': '栈底放哨兵 `16`（题目数值 ≤ 15）：没有左邻居时不会出错',
        'res = 0': '`res` 累计所有非叶子节点的值之和',
        'for num in arr': '扫描到 `{num}`',
        'while num >= stack[-1]': lambda S, B, ret: (
            f'`{S.num}` ≥ 栈顶 `{S.stack[-1]}`：栈顶满足 `stack[-2] > 栈顶 <= {S.num}` → 它该被合并掉'
            if S.num >= S.stack[-1] else
            f'`{S.num}` < 栈顶 `{S.stack[-1]}`：栈保持递减 → 停止合并'),
        'res += stack[-1] * min(num, stack[-2])': '栈顶和它两边较小的 `min({num}, {B.stack[-2]})` 合并：`{B.stack[-1]} × {min(num, B.stack[-2])}` → `res` = =={res}==',
        'stack.pop()': '栈顶已被合并，弹出',
        'stack.append(num)': '`{num}` 入栈',
        'while len(stack) > 2': lambda S, B, ret: (f'栈里还剩 `{S.stack[1:]}`，没合并完 → 继续' if len(S.stack) > 2 else '只剩哨兵和一个数 → 合并完成'),
        'res += stack[-1] * stack[-2]': '栈是递减的，从右往左合并：`{B.stack[-1]} × {B.stack[-2]}` → `res` = =={res}==',
        'return res': '最小代价 =={ret}==',
    },
    cards=dict(
        one_liner='最小的数最先和较小的邻居合并，用单调栈找它',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arr` 是一棵二叉树中序遍历的叶子值，每个非叶节点的值是左右子树叶子最大值的乘积',
                 '求所有非叶节点值之和的最小值',
                 '示例：`[6,2,4]` → `32`；本视频用 `[6,2,4,3]`',
                 '题意据题目与 yiduobo 题解整理'],
        quote='对于arr[i - 1] > arr[i]这种结构，我们可以使用单调栈来进行储存。方便起见，我们可以先在栈中设置边界值16。',
        quote_src='—— yiduobo 题解原文',
        idea=['dp：`f[l][r]` 枚举分割点，`O(n^2)` 可做',
              '转化：每次合并相邻两数，代价是乘积，然后删掉较小的那个',
              '若 `arr[i-1] > arr[i] <= arr[i+1]`，==直接把 arr[i] 和较小的邻居合并最优=='],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '哨兵 `16` 保证 `stack[-2]` 永远存在',
                 '扫完后栈递减，要从右往左依次合并',
                 '也可以用 dp 做，单调栈是更优的贪心写法'],
    ),
)
