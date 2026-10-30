CONFIG = dict(
    num=3301, title='高度互不相同的最大塔高和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='降序排序，逐个压低',
    tags=['贪心', '排序', '难度分 1448'],
    code='''
class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight.sort(reverse=True)
        for i in range(1, len(maximumHeight)):
            maximumHeight[i] = min(maximumHeight[i], maximumHeight[i - 1] - 1)
            if maximumHeight[i] <= 0:
                return -1
        return sum(maximumHeight)
''',
    call='Solution().maximumTotalSum([2,3,4,3,5])',
    expect=15,
    views=[
        dict(type='bars', var='maximumHeight', h=380, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and i <= S['i'] else None),
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 座：`min(上限, 前一座 − 1)` = ==" + str(S['maximumHeight'][S['i']]) + '==') if 'i' in S else '', size=28),
    ],
    watch=[('i', 'i', 'blue')],
    captions={
        'sort(reverse': '从大到小排序：`{maximumHeight}`，最大的那座保持不变最优（调低它只会更差）',
        'maximumHeight[i] = min': '第 `{i}` 座：不能超过自己的上限，也必须比前一座矮 `1` → `min({B.maximumHeight[i]}, {maximumHeight[i-1]} - 1)` = =={maximumHeight[i]}==',
        '<= 0': '高度 `{maximumHeight[i]}`，{"不是正整数 → 无解" if maximumHeight[i] <= 0 else "仍是正整数，继续"}',
        'return sum': '所有塔高度互不相同，求和得 =={ret}==',
    },
    cards=dict(
        one_liner='从最高的塔开始，每座塔不超过前一座减 1',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略排序栈）',
        problem=['`maximumHeight[i]` 是第 `i` 座塔的高度上限',
                 '每座塔高度为正整数且互不相同，求最大总高度，无解返回 `-1`',
                 '示例：`[2,3,4,3]` → `10`（`[1,2,4,3]`）'],
        quote='数组的最大值 m 不变是最好的。反证：如果把 m 变小是最优的，那么把 m 恢复成其原来的值，仍然满足题目要求，且我们得到了更优的答案，矛盾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从最大的元素开始想：最大值不动；次大值若等于它就变成 `m-1`，否则不动',
              '排序后第 `i` 座的实际高度 = `min(自身上限, 前一座 - 1)`',
              '出现 `≤ 0` 说明塔太多而高度不够，返回 `-1`'],
        summary=['时间 `O(n log n)`，瓶颈在排序',
                 '一定要先降序排序，再原地改写',
                 '`<= 0` 才无解，不是 `< 0`',
                 '思考题：1840 最高建筑高度；专题：贪心 §1.1'],
    ),
)
