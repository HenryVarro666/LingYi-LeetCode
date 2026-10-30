CFG0 = [5, 3, 4, 1, 3, 2]

CONFIG = dict(
    num=3502, title='到达每个位置的最小费用', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='前缀最小值 · 原地修改',
    tags=[],
    code='''
class Solution:
    def minCosts(self, cost: List[int]) -> List[int]:
        for i in range(1, len(cost)):
            cost[i] = min(cost[i], cost[i - 1])
        return cost
''',
    call=f'Solution().minCosts({CFG0!r})',
    expect=[5, 3, 3, 1, 1, 1],
    views=[
        dict(type='text', fn=lambda S: (f"`answer[{S['i']}]` = `[0, {S['i']}]` 里 cost 的最小值 = =={S['cost'][S['i']]}==" if 'i' in S
                                         else '`answer[i]` = `cost[0..i]` 的最小值（前缀最小值）'), size=28, h=70),
        dict(type='array', var='cost', label='cost（原地改成前缀最小值，绿 = 已算好）', cell=96, h=240, pointers={'i': 'blue'},
             color=lambda S, k, v: 'green' if 'i' in S and k < S['i'] else ('blue' if 'i' in S and k == S['i'] else None)),
        dict(type='text', fn=lambda S: '先付最小的那个人的钱换到前面，再==免费==和右边的人换到 `i`', size=26, h=60),
    ],
    watch=[('i', 'i', 'blue')],
    captions={
        'for i in range': lambda S, B, ret: (f'`i = {S.i}`：算 `answer[{S.i}]`，`cost[0..{S.i - 1}]` 已经是前缀最小值' if S.get('i') != B.get('i') or 'i' not in B else '遍历完了，`cost` 已经是答案'),
        'cost[i] = min': '`min(cost[{i}], cost[{i-1}])`：直接买 `i`，或者买前面最便宜的再免费走过来 → =={cost[i]}==',
        'return cost': '`cost` 现在就是 `answer`：=={ret}==',
    },
    cards=dict(
        one_liner='到 i 的最小费用 = cost[0..i] 的前缀最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['你在队尾（位置 `n`），要换到前面的位置 `i`',
                 '和前面的人 `i` 交换要付 `cost[i]`，和后面的人交换==免费==',
                 '示例：`[5,3,4,1,3,2]` → `[5,3,3,1,1,1]`'],
        quote='先找一个 [0,i] 中 cost 最小的人，和他交换，然后再和右边的人免费交换，直到到达 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['想到 `i`：先花钱换到 `[0,i]` 里最便宜的那个人的位置',
              '之后每次和右边的人交换都免费，一路换到 `i`',
              '所以 `answer[i]` 就是前缀最小值，从左往右一遍算出，直接改在 `cost` 上'],
        summary=['时间 `O(n)`，空间 `O(1)`（原地修改 `cost`）',
                 '易错：循环从 `i = 1` 开始，`answer[0] = cost[0]` 不用动',
                 '题解还给了一行写法：`list(accumulate(cost, min))`',
                 '同类：前缀最小值 / 前缀最大值的递推'],
    ),
)
