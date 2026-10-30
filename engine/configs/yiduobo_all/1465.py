CONFIG = dict(
    num=1465, title='切割后面积最大的蛋糕', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序后扫描最大间隔', tags=[],
    code='''
class Solution(object):
    def maxArea(self, h, w, horizontalCuts, verticalCuts):

        last = 0
        max_h = 0
        for now in sorted(horizontalCuts):
            max_h = max(max_h, now - last)
            last = now
        
        max_h = max(max_h, h - now)

        last = 0
        max_v = 0
        for now in sorted(verticalCuts):
            max_v = max(max_v, now - last)
            last = now
        
        max_v = max(max_v, w - now)

        return max_h * max_v % (10 ** 9 + 7)
''',
    call='Solution().maxArea(5, 4, [1,2,4], [1,3])',
    expect=4,
    views=[
        dict(type='array', var=lambda S: [0] + sorted(S['horizontalCuts']) + [S['h']], label='水平切口（含 0 和 h）', h=170,
             pointers={'_hi': 'blue'} if False else {}),
        dict(type='array', var=lambda S: [0] + sorted(S['verticalCuts']) + [S['w']], label='竖直切口（含 0 和 w）', h=170),
        dict(type='text', fn=lambda S: f"上一刀 `last = {S.get('last')}`，当前刀 `now = {S.get('now')}`，最大间隔 横 ==`{S.get('max_h')}`== 竖 ==`{S.get('max_v', '?')}`=="),
    ],
    watch=[('last', 'last', 'cyan'), ('now', 'now', 'blue'), ('max_h', 'max_h', 'green'), ('max_v', 'max_v', 'orange')],
    captions={
        'last = 0': '蛋糕边缘就是第 0 刀：`last = 0`',
        'max_h = 0': '`max_h` 记录横切相邻两刀的最大间隔',
        'max_v = 0': '`max_v` 记录竖切相邻两刀的最大间隔',
        'for now in sorted(horizontalCuts)': '横切按从小到大排序，当前这刀在 `{now}`',
        'for now in sorted(verticalCuts)': '竖切按从小到大排序，当前这刀在 `{now}`',
        'max_h = max(max_h, now - last)': '间隔 `{now} - {last} = {now-last}`，`max_h = max({B.max_h}, {now-last}) = {max_h}`',
        'max_v = max(max_v, now - last)': '间隔 `{now} - {last} = {now-last}`，`max_v = max({B.max_v}, {now-last}) = {max_v}`',
        'last = now': '当前刀成为下一段的起点：`last = {last}`',
        'max_h = max(max_h, h - now)': '别忘了最后一段：蛋糕下边缘 `h = {h}` 到最后一刀 `{now}` → 间隔 `{h-now}`，`max_h = {max_h}`',
        'max_v = max(max_v, w - now)': '最后一段：右边缘 `w = {w}` 到最后一刀 `{now}` → 间隔 `{w-now}`，`max_v = {max_v}`',
        'return': '长 × 宽互相独立：`{max_h} * {max_v}` = {max_h*max_v}，对 `10^9+7` 取余 → =={ret}==',
    },
    cards=dict(
        one_liner='长和宽互相独立，各自找最大间隔，相乘即最大面积',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n + m)`',
        problem=['蛋糕高 `h`、宽 `w`，给出所有水平切口和竖直切口的位置',
                 '切完后求 ==面积最大的一块==，结果对 `10^9+7` 取余',
                 '示例：`h=5, w=4, [1,2,4], [1,3]` → `4`'],
        quote='注意到矩形的长和宽是互相独立的，于是可以将横切位置和纵切位置分别排序，然后一趟扫描，找出两条横切以及两条纵切之间的最大间隔，二者相乘即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['切完后每一块都是矩形，面积 = 横向间隔 × 竖向间隔',
              '两个间隔互相独立，所以分别取最大即可',
              '排序后扫描相邻差，并用 `last` 记前一刀；最后补上到边缘的一段'],
        summary=['时间 `O(n log n + m log m)`，瓶颈在排序',
                 '易错点：必须补上最后一刀到边缘 `h - now` 的一段，开头从 0 开始',
                 '易错点：Python 整数不会溢出，最后再取模即可',
                 '原文用 `now` 在循环外取最后一刀（切口至少 1 个，所以安全）'],
    ),
)
