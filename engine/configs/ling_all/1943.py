CONFIG = dict(
    num=1943, title='描述绘画结果', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分思想：端点排序 + 累加颜色（Go 原文转写）',
    tags=['灵神题单', '常用数据结构', '难度分 1969'],
    setup='''
from collections import namedtuple
event = namedtuple('event', 'pos color')  # 对应 Go 的 type event struct{ pos, color int }
''',
    code='''
class Solution:
    def splitPainting(self, segments: List[List[int]]) -> List[List[int]]:
        ans = []
        events = []
        for seg in segments:
            events.append(event(seg[0], seg[2]))
            events.append(event(seg[1], -seg[2]))  # 记录每个区间左右端点及颜色
        events.sort(key=lambda e: e.pos)  # 按位置排序

        sum = 0
        for i, e in enumerate(events[:-1]):
            sum += e.color
            if sum > 0 and e.pos < events[i + 1].pos:
                ans.append([e.pos, events[i + 1].pos, sum])
        return ans
''',
    call='Solution().splitPainting([[1,4,5],[4,7,7],[1,7,9]])',
    expect=[[1, 4, 14], [4, 7, 16]],
    views=[
        dict(type='text', fn=lambda S: (f"累加到下标 `{S['i']}`：当前颜色和 `sum` = =={S['sum']}==，下一个端点在 `{S['events'][S['i']+1].pos}`" if 'i' in S and 'sum' in S and 'events' in S and S['i'] + 1 < len(S['events']) else '每个端点只改变颜色和：左端点 +color，右端点 −color')),
        dict(type='array', var='events', label='events（pos, color）', h=240, cell=130, pointers={'i': 'blue'},
                  color=lambda S, i, v: 'green' if v[1] > 0 else 'pink'),
        dict(type='array', var='ans', label='ans：[左端点, 右端点, 颜色和]', h=170, cell=170),
        dict(type='array', var='segments', label='segments：[start, end, color]', h=170, cell=150),
    ],
    watch=[('i', 'i', 'blue'), ('sum', 'sum', 'green')],
    captions={
        'events.append(event(seg[0]': '区间 `{seg}` 的左端点 `{seg[0]}`：颜色 `+{seg[2]}`',
        'events.append(event(seg[1]': '右端点 `{seg[1]}`：颜色 `-{seg[2]}`，到这里它就不再混合了',
        'events.sort': '按位置排序：同一位置的端点挨在一起，之后只需顺着扫一遍',
        'sum = 0': '`sum` 记录当前位置混合颜色的和',
        'for i, e in enumerate': lambda S, B, r: ('除最后一个端点外都处理完了（最后一个端点后面没有区间）' if 'i' in B and B['i'] == S['i'] and S['i'] == len(S['events']) - 2 else f"处理端点 `{S['e'].pos}`（颜色 `{S['e'].color:+d}`）") if 'e' in S else '遍历除最后一个以外的端点（最后一个端点后面没有区间）',
        'sum += e.color': '`sum += {e.color}` → `{sum}`：端点处颜色和发生变化',
        'if sum > 0': lambda S, B, r: (f"`sum = {S['sum']} > 0` 且 `{S['e'].pos} < {S['events'][S['i']+1].pos}`：[{S['e'].pos}, {S['events'][S['i']+1].pos}) 这一段有颜色 → 记入答案" if S['sum'] > 0 and S['e'].pos < S['events'][S['i']+1].pos else (f"下一个端点也在 `{S['e'].pos}`，这一段长度为 0 → 不记" if S['sum'] > 0 else "`sum = 0`：这一段没有被涂色 → 不记")),
        'ans.append': '记录 `[{e.pos}, {events[i+1].pos}, {sum}]`',
        'return ans': '扫完所有端点，返回 `{ans}`',
    },
    cards=dict(
        one_liner='颜色只在端点处变化，端点排序后一趟累加',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个线段 `[start, end, color]` 是半开区间，重叠处颜色相加',
                 '返回最少数目的不重叠区间及其颜色和；颜色集合不同的段不能合并',
                 '示例：`[[1,4,5],[4,7,7],[1,7,9]]` → `[[1,4,14],[4,7,16]]`'],
        quote='由于只有在区间端点处才会改变颜色（增加或减少），我们可以统计所有区间端点并按位置从小到大排序，然后遍历这些端点，在每个端点处累加颜色并记录答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个线段拆成两个事件：左端点 `+color`，右端点 `-color`',
              '事件按位置排序，`sum` 累加就是当前位置的颜色和',
              '相邻两个端点之间颜色不变：`sum > 0` 且位置不同，就记一段'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python；`event` 用 `namedtuple` 对应 Go 的结构体（在 setup 中定义）',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：同一位置的多个端点要全部累加后才算一段，所以要判断 `e.pos < events[i + 1].pos`',
                 '颜色互不相同，所以 `sum > 0` 就表示这段有颜色，不会出现总和相抵',
                 '同类题：253 会议室 II、2406 分割区间'],
    ),
)
