CFG0 = [5, 3, 4, 1, 3, 2]

CONFIG = dict(
    num=3502, title='到达每个位置的最小费用', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='两种换法取最小 · 答案末项当前缀最小值',
    tags=[],
    code='''
class Solution(object):
    def minCosts(self, cost):
        res = [cost[0]]
        for v in cost[1:]:
            res.append(min(res[-1], v))
        return res
''',
    call=f'Solution().minCosts({CFG0!r})',
    expect=[5, 3, 3, 1, 1, 1],
    views=[
        dict(type='text', fn=lambda S: (f"当前 `v = {S['v']}`，前缀最小值 `res[-1] = {S['res'][-1]}`" if 'v' in S and S['res'] else '`res` 就是前缀最小值数组'), size=28, h=70),
        dict(type='array', var=lambda S: list(CFG0), label='cost（蓝 = 当前 v）', cell=96, h=220,
             color=lambda S, k, v: 'blue' if 'v' in S and 'res' in S and k == len(S['res']) - (1 if S['_line'] == 6 else 0) else None),
        dict(type='array', var='res', label='res（新加入的为绿色）', cell=96, h=220),
    ],
    watch=[('v', 'v', 'blue'), ('res[-1]', 'res[-1]', 'green')],
    captions={
        'res = [cost[0]]': '`index = 0` 必须直接和 0 交换，`cost[0]` 一定要付：`res = {res}`',
        'for v in cost[1:]': lambda S, B, ret: (f'下一个 `v = {S.v}`（`index > 0`），当前前缀最小值是 `{S.res[-1]}`' if S.get('v') is not None and S.get('v') != B.get('v') or (S.get('v') is not None and len(S.res) != len(B.get('res', []))) else '后面的位置都算完了'),
        'res.append': lambda S, B, ret: (f'两种换法：直接换 `v = {S.v}`，或先换前缀最小 `{B.res[-1]}` 再免费走过来 → 取小 `{S.res[-1]}`'),
        'return res': '`res` 同时就是前缀最小值，无需另外维护：=={ret}==',
    },
    cards=dict(
        one_liner='两种换法取小：直接换 index，或先换前面最便宜的再免费走过去',
        complexity='时间 `O(n)`，空间 `O(n)`（结果数组）',
        problem=['队伍编号 `0..n`，你在位置 `n`，`cost[i]` 是和位置 `i` 的人交换的费用',
                 '和前面的人交换要付费，和后面的人交换免费',
                 '求到每个位置 `index` 的最小费用；示例 `[5,3,4,1,3,2]` → `[5,3,3,1,1,1]`'],
        quote='另外，由于answer数组实际上储存的就是前缀最小值，因此无需额外维护前缀最小值，使用answer数组的最后一项与cost[index]进行比较就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`index = 0`：最后一步必然是和 0 交换，所以一定付 `cost[0]`',
              '`index > 0` 方法一：直接和 `index` 交换，代价 `cost[index]`',
              '方法二：先和 `cost[0..index-1]` 里最小的交换再免费走到 `index`；两者取小，用 `res[-1]` 当前缀最小值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`res[0] = cost[0]` 是必须付的，要先单独放入',
                 '`for v in cost[1:]` 从第二个元素开始，和 `res[-1]` 比较',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神直接原地改 `cost`，空间 `O(1)`；yiduobo 新建 `res` 数组'],
    ),
)
