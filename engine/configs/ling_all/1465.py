CONFIG = dict(
    num=1465, title='切割后面积最大的蛋糕', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 相邻切口最大间隔', tags=[],
    code='''
class Solution:
    def maxArea(self, h: int, w: int, horizontalCuts: List[int], verticalCuts: List[int]) -> int:
        horizontalCuts = [0] + sorted(horizontalCuts) + [h]
        verticalCuts = [0] + sorted(verticalCuts) + [w]
        max_h = max(q - p for p, q in pairwise(horizontalCuts))
        max_w = max(q - p for p, q in pairwise(verticalCuts))
        return max_h * max_w % (10 ** 9 + 7)
''',
    call='Solution().maxArea(5, 4, [1,2,4], [1,3])',
    expect=4,
    views=[
        dict(type='array', var='horizontalCuts', label='水平切口（含边界 0 和 h）', h=170),
        dict(type='array', var='verticalCuts', label='竖直切口（含边界 0 和 w）', h=170),
        dict(type='text', fn=lambda S: ('横向间隔 `%s`，竖向间隔 `%s`' % ([b - a for a, b in zip(S['horizontalCuts'], S['horizontalCuts'][1:])], [b - a for a, b in zip(S['verticalCuts'], S['verticalCuts'][1:])])) if S.get('_line', 0) >= 5 and S['horizontalCuts'][0] == 0 else ''),
        dict(type='text', fn=lambda S: f"最大横间隔 `{S.get('max_h', '?')}` × 最大竖间隔 `{S.get('max_w', '?')}`"),
    ],
    watch=[('max_h', 'max_h', 'green'), ('max_w', 'max_w', 'orange')],
    captions={
        'horizontalCuts = [0]': '排序，并把边界 `0` 和 `h = {h}` 也当作切口：`{horizontalCuts}`',
        'verticalCuts = [0]': '竖切同理，加上 `0` 和 `w = {w}`：`{verticalCuts}`',
        'max_h = max': '相邻水平切口的最大间隔 `max_h = {max_h}`：它决定了最高的那一条蛋糕',
        'max_w = max': '相邻竖直切口的最大间隔 `max_w = {max_w}`：它决定了最宽的那一条',
        'return': '两项互相独立：`{max_h} * {max_w} = {max_h*max_w}`，对 `10^9+7` 取余 → =={ret}==',
    },
    cards=dict(
        one_liner='排序后，最大蛋糕由最大横间隔和最大竖间隔决定',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n)` 或 `O(1)`',
        problem=['蛋糕高 `h`、宽 `w`，给出水平切口和竖直切口的位置',
                 '切完后求 ==面积最大的一块==，对 `10^9+7` 取余',
                 '示例：`h=5, w=4, [1,2,4], [1,3]` → `4`'],
        quote='由于相乘的两项是互相独立的，只需要分别算出 horizontalCuts[i] - horizontalCuts[i-1] 的最大值和 verticalCuts[j] - verticalCuts[j-1] 的最大值，就得到了蛋糕面积的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，任意一块蛋糕由两个相邻的水平切口和两个相邻的竖直切口决定（边界也算切口）',
              '先横着切，间隔最大的两刀决定最大的那一条，最大蛋糕就在其中',
              '再看竖着切的最大间隔，两者相乘'],
        summary=['时间 `O(n log n + m log m)`，瓶颈在排序',
                 '易错点：要补上边界 `0`、`h`、`w`，否则漏掉两端的蛋糕',
                 '易错点：取模放在最后，Python 不会溢出',
                 '用 `pairwise` 一行求相邻差的最大值'],
    ),
)
