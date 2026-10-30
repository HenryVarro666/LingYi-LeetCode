EV, ST, ET = 10, [0, 3, 7, 9], [1, 4, 8, 10]


def _gaps():
    return [ST[0]] + [ST[i] - ET[i - 1] for i in range(1, len(ST))] + [EV - ET[-1]]


def _gcol(S, i, v):
    if 'left' in S and 'index' in S and S['index'] in (i, i - 1) and S['_line'] >= 30:
        return 'yellow'
    return None


def _txt(S):
    g = _gaps()
    if 'first' not in S:
        return f'空位长度 `{g}`，会议长度 `{[e - s for s, e in zip(ST, ET)]}`'
    t = f"前三大空位：first=={S['first']}==，second=={S['second']}==，third=={S['third']}=="
    if 'move_length' in S and 'left' in S and S['_line'] >= 30:
        t += f"　|　会议 {S['index']}：left={S['left']} right={S['right']} 长={S['move_length']}"
    return t


CONFIG = dict(
    num=3440, title='重新安排会议得到最多空余时间 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='前三大空闲 · 三条件判断能否插入',
    tags=['灵神题单', '思维题', '难度分 1998'],
    code='''
class Solution(object):
    def maxFreeTime(self, eventTime, startTime, endTime):
        
        first, second, third = 0, 0, 0
        pre = 0
        
        for start, end in zip(startTime, endTime):
            length = start - pre
            if length > first:
                first, second, third = length, first, second
            elif length > second:
                second, third = length, second
            elif length > third:
                third = length
            pre = end
        
        length = eventTime - pre
        if length > first:
            first, second, third = length, first, second
        elif length > second:
            second, third = length, second
        elif length > third:
            third = length
        
        startTime.append(eventTime)
        endTime.append(eventTime)

        pre = 0
        res = 0
        for index in range(len(startTime) - 1):
            move_length = endTime[index] - startTime[index]
            left = startTime[index] - pre
            right = startTime[index + 1] - endTime[index]
            res = max(res, left + right)

            if max(left, right) < first and move_length <= first:
                res = max(res, left + right + move_length)
            elif min(left, right) < second and move_length <= second:
                res = max(res, left + right + move_length)
            elif move_length <= third:
                res = max(res, left + right + move_length)

            pre = endTime[index]

        return res
''',
    call=f'Solution().maxFreeTime({EV}, {ST}, {ET})',
    expect=6,
    skip=['first, second, third = 0', 'pre = 0', 'pre = end', 'pre = endTime', 'startTime.append', 'endTime.append', 'res = 0'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var=lambda S: _gaps(), label='空闲时间（下标 0..n）：黄 = 当前会议左右两侧', cell=96, color=_gcol, h=300),
    ],
    watch=[('first', 'first', 'blue'), ('second', 'second', 'pink'), ('third', 'third', 'purple'), ('res', 'res', 'green')],
    captions={
        'for start, end in zip': '第一趟遍历：统计相邻会议之间的空闲时间，保留前三大',
        'length = start - pre': '空闲 `length = {start} - {pre} = {length}`（上一个会议结束到这个会议开始）',
        'if length > first': '`{length}` 与最大空闲 `{first}` 比：{"更大 → 成为 first，原 first、second 顺位降级" if B.length > B.first else "不更大，看 second"}',
        'elif length > second': '`{length}` 与 second `{second}` 比：{"更大 → 成为 second" if B.length > B.second else "不更大，看 third"}',
        'elif length > third': '`{length}` 与 third `{third}` 比：{"更大 → 成为 third" if B.length > B.third else "不更大，丢弃"}',
        'first, second, third = length': '更新：`first={first}, second={second}, third={third}`',
        'second, third = length': '更新：`second={second}, third={third}`',
        'third = length': '更新：`third={third}`',
        'length = eventTime - pre': '最后一个会议右侧的空闲：`{eventTime} - {pre} = {length}`，同样参与前三大',
        'if length > first:\n': '最后一段空闲也和 first 比',
        'for index in range': '第二趟：枚举要移动的会议 `{index}`',
        'move_length =': '会议 `{index}` 的长度 `move_length = {move_length}`',
        'left =': '它左边的空闲 `left = {left}`',
        'right =': '它右边的空闲 `right = {right}`',
        34: '方案一：会议紧贴邻居，左右空闲合并：`{left} + {right} = {left + right}`，`res = {res}`',
        'if max(left, right) < first': lambda S, B, r: (f'条件 1：`max(left, right) = {max(B.left, B.right)} < first = {B.first}` 且 `move_length = {B.move_length} <= first`'
                                                       f'：{"==成立，可以移进 first 那段空闲==" if (max(B.left, B.right) < B.first and B.move_length <= B.first) else "不成立"}'),
        'elif min(left, right) < second': lambda S, B, r: (f'条件 2：`min(left, right) = {min(B.left, B.right)} < second = {B.second}` 且 `move_length = {B.move_length} <= second`'
                                                           f'：{"==成立，first、second 至少一个不挨着它==" if (min(B.left, B.right) < B.second and B.move_length <= B.second) else "不成立"}'),
        'elif move_length <= third': '条件 3：`move_length = {move_length} <= third = {third}`：{"==成立，三段里总有一段不挨着它==" if B.move_length <= B.third else "不成立，只能贴邻居"}',
        'res = max(res, left + right + move_length)': '方案二：移到别处，空出 `{left} + {move_length} + {right} = {left + move_length + right}`，`res = {res}`',
        'pre = endTime': '`pre` 更新为本会议的结束时间',
        'return res': '最大空余时间 `{res}`',
    },
    cards=dict(
        one_liner='先找前三大空闲，再判断每个会议能不能搬进去',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['总时长 `eventTime`，`n` 个不重叠会议；可以把一个会议平移（时长不变），不能出活动范围',
                 '求移动后最长的连续空闲时间',
                 '示例：`eventTime=10, start=[0,3,7,9], end=[1,4,8,10]` → `6`'],
        quote='需要计算前三大而不是最大的理由是left或者right可能就是前三大空余时间之一或者之二，那么此时移动move_length相当于是第一种移动方案而不是第二种。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个会议两种方案：贴邻居得 `left + right`；搬到别处得 `left + move_length + right`',
              '第一趟遍历求 `first / second / third` 三个最大空闲',
              '第二趟用三个条件判断：能插进 first、second 或 third 之一，且不挨着自己'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：末尾要补 `[eventTime, eventTime]`，否则最后一个会议的 `right` 算不出',
                 '三个条件的顺序：先 `max(left,right) < first`，再 `min(...) < second`，最后 `third`',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神记下标并检查是否相邻；yiduobo 只记长度，用大小比较判断'],
    ),
)
