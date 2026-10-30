CONFIG = dict(
    num=2498, title='青蛙过河 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='间隔跳',
    tags=['灵神题单', '难度分 1759'],
    code='''
class Solution:
    def maxJump(self, stones: List[int]) -> int:
        ans = stones[1] - stones[0]
        for i in range(2, len(stones)):
            ans = max(ans, stones[i] - stones[i - 2])
        return ans
''',
    call='Solution().maxJump([0,2,5,6,7,10])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"这一跳：`stones[{S['i']}] − stones[{S['i']-2}] = {S['stones'][S['i']]} − {S['stones'][S['i']-2]}` = =={S['stones'][S['i']]-S['stones'][S['i']-2]}=="
                                        if 'i' in S else '间隔跳：去程和回程各占一半石头'), size=28, h=90),
        dict(type='array', var='stones', label='stones（石头位置）', h=250,
             pointers={'i': 'pink', 'i - 2': 'blue'}, pointer_labels={'i': 'i', 'i - 2': 'i-2'},
             window=('i - 2', 'i')),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'ans = stones[1]': '第一步：`ans = stones[1] - stones[0] = {ans}`（前两块石头之间必有一跳）',
        'for i in range': '枚举 `i`，比较隔一块石头的两块：`stones[i]` 和 `stones[i-2]`',
        'ans = max': '间隔跳时相邻两跳最长是 `stones[i] - stones[i-2]`：`max({B.ans}, {stones[i] - stones[i-2]})` → =={ans}==',
        'return ans': '最大跳跃长度最小就是 =={ans}==',
    },
    cards=dict(
        one_liner='所有石头都用上，隔一块跳，答案是隔一块的最大间距',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['青蛙从第一块石头跳到最后一块再跳回来，每块石头至多到达一次',
                 '路径代价 = 最大跳跃长度，求最小代价',
                 '示例：`[0,2,5,6,7]` → `5`'],
        quote='比如四块石头 a-b-c-d：不采用间隔跳，路径为 a-d-c-b-a；采用间隔跳，路径为 a-c-d-b-a；由于 a-d 必然比 a-c 和 b-d 大，从这点可以看出，间隔跳是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每块石头都选，才能让最大距离尽量小',
              '去程走偶数下标、回程走奇数下标，每一跳都是跨一块石头',
              '答案 = 前两块的间距 与 所有 `stones[i]-stones[i-2]` 的最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：别忘了 `stones[1]-stones[0]` 这一跳（只有两块石头时即为答案）',
                 '下标从 2 开始枚举，避免越界'],
    ),
)
