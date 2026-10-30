CONFIG = dict(
    num=2498, title='青蛙过河 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='两条路径交替分配落脚点',
    tags=['灵神题单', '难度分 1759'],
    code='''
class Solution(object):
    def maxJump(self, stones):

        if len(stones) <= 3:
            return stones[-1]
        
        p1 = p2 = 0
        res = 0
        for index in range(1, len(stones) - 1, 2):
            res = max(res, stones[index] - stones[p1], stones[index + 1] - stones[p2])
            p1 = index
            p2 = index + 1
        
        return max(res, stones[-1] - stones[p1], stones[-1] - stones[p2])
''',
    call='Solution().maxJump([0,2,5,6,7])',
    expect=5,
    views=[
        dict(type='text', size=26, h=90, fn=lambda S: (
            f"路径 A 在 `{S['stones'][S['p1']]}`，路径 B 在 `{S['stones'][S['p2']]}`" if 'p1' in S else '两条路径都从第 0 块石头出发')),
        dict(type='array', var='stones', label='stones（蓝 = p1 路径当前所在，粉 = p2 路径当前所在）', h=250,
             pointers={'p1': 'blue', 'p2': 'pink'},
             color=lambda S, i, v: 'blue' if 'p1' in S and i == S['p1'] else 'pink' if 'p2' in S and i == S['p2'] else None),
    ],
    watch=['p1', 'p2', 'index', ('res', 'res', 'green')],
    captions={
        'if len(stones) <= 3': '`len(stones) = {len(stones)}`：{"石头太少，只能直接跳到终点再跳回" if len(stones) <= 3 else "石头够多，需要两条路径交替"}',
        'return stones[-1]': '最远一跳就是起点到终点：`{ret}`',
        'p1 = p2 = 0': '去程和回程看作两条从起点出发的路径，`p1`、`p2` 是它们当前所在的石头',
        'res = 0': '`res` 记录目前最大的一跳',
        'for index': '下一对落脚点：`stones[{index}]` 和 `stones[{index + 1}]`',
        'res = max': '`stones[{index}] − stones[{p1}]` = {stones[index] - stones[p1]}，`stones[{index+1}] − stones[{p2}]` = {stones[index + 1] - stones[p2]}，`res` → =={res}==',
        'p1 = index': '较近的石头 `{index}` 分给上一个落脚点较近的路径 p1',
        'p2 = index + 1': '下一块 `{index + 1}` 分给另一条路径 p2',
        'return max': '最后两条路径都要跳到终点：`max(res, {stones[-1]}-{stones[p1]}, {stones[-1]}-{stones[p2]})` = =={ret}==',
    },
    cards=dict(
        one_liner='所有石头都用上，两条路径交替领取下一块石头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['青蛙从第一块石头跳到最后一块，再跳回来，每块石头至多到达一次',
                 '代价 = 最大跳跃长度，求最小代价',
                 '示例：`[0,2,5,6,7]` → `5`'],
        quote='将下一个最近的落脚点分给上一个落脚点离起点较近的那条路径，理由也很简单，因为如果分配给另一条路径，那么落脚点较近的那条路径到其下一个落脚点的距离只会更远。',
        quote_src='—— yiduobo 题解原文',
        idea=['往返两条不相交路径，等价于两条从起点到终点的不相交路径',
              '落脚点全用上，距离才能最短',
              '每次把相邻两块石头分给两条路径，更新最大跳跃，最后两条路径各跳向终点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`len(stones) <= 3` 要特判，直接返回 `stones[-1]`',
                 '循环到 `len-2` 为止，终点留到最后单独处理',
                 '对比灵神：灵神一行 `stones[i] - stones[i-2]` 取最大；yiduobo 显式维护两条路径的当前位置，结果相同'],
    ),
)
