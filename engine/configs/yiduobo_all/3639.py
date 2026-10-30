def _txt(S):
    if 'activity' not in S:
        return ''
    inn = S.get('_inner', {})
    if S['_line'] <= 15:
        inn = {}
    if 'new_left' in inn and 'new_right' in inn and S['_line'] >= 27:
        o, nl, nr = inn['o'], inn['new_left'], inn['new_right']
        a, b = o - nl, nr - o
        return (f"星号还原：左段长 `{a}`、右段长 `{b}` 合并成一段长 `{nr - nl + 1}`；"
                f"无星号子串 `+{a * (a + 1) // 2} + {b * (b + 1) // 2} − {(nr - nl + 1) * (nr - nl + 2) // 2}`")
    if 'new_left' in inn:
        return f"位置 `o = {inn['o']}` 还原成字母：先找它左右连着的无星号段的边界"
    return f"有效子串数 `activity = {S['activity']}`（= 总子串数 − 无星号子串数），目标 `k = {S['k']}`"


def _color(S, i, v):
    st = S.get('stars')
    if st is None or 'activity' not in S:
        return None
    return 'yellow' if st[i] else None


CONFIG = dict(
    num=3639, title='变为活跃状态的最小时间', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='逆向还原星号 · 合并无星号区间',
    tags=['二分答案', '逆向思维', '难度分 1853'],
    code='''
class Solution(object):
    def minTime(self, s, order, k):
        
        n = len(s)
        activity = n * (n + 1) // 2
        if activity < k:
            return -1
        
        stars = [False] * n
        for index in order:
            stars[index] = True
        left = [None] * n
        right = [None] * n
        
        for index in range(len(order) - 1, -1, -1):
            o = order[index]
            if o > 0 and not stars[o - 1]:
                new_left = left[o - 1]
            else:
                new_left = o
            
            if o + 1 < n and not stars[o + 1]:
                new_right = right[o + 1]
            else:
                new_right = o
            
            activity += (o - new_left) * (o - new_left + 1) // 2
            activity += (new_right - o) * (new_right - o + 1) // 2
            activity -= (new_right - new_left + 1) * (new_right - new_left + 2) // 2
            right[new_left] = new_right
            left[new_right] = new_left
            stars[o] = False
            if activity < k:
                return index
''',
    call='Solution().minTime("abcdef", [2,0,4,5,1,3], 15)',
    expect=2,
    skip=['for index in order', 'stars[index] = True', 'left = [None] * n', 'right = [None] * n',
          'activity += (new_right - o)', 'right[new_left] = new_right', 'left[new_right] = new_left'],
    views=[
        dict(type='text', size=22, fn=_txt),
        dict(type='string', var='s', label='s（黄 = 当前是星号；从后往前一个个还原成字母）', h=250,
             pointers={'o': 'blue', 'new_left': 'cyan', 'new_right': 'orange'}, color=_color),
        dict(type='array', var='order', label='order（从后往前扫 index）', h=250,
             pointers={'index': 'pink'}),
    ],
    watch=[('index', 'index', 'pink'), ('o', 'o', 'blue'), ('new_left', 'new_left', 'cyan'),
           ('new_right', 'new_right', 'orange'), ('activity', 'activity', 'green'), ('k', 'k')],
    captions={
        'activity = n * (n + 1) // 2': '全是星号时每个子串都有效：`activity = n(n+1)/2 = {activity}`',
        'if activity < k': lambda S, B, r: (f'`{S.activity} < {S.k}`：全变星号都不够 → 返回 -1' if S.activity < S.k
                                            else f'`{S.activity} >= {S.k}`：全变星号时够，所以一定有答案'),
        'stars = [False] * n': '`stars[i]` 记录第 `i` 位当前是不是星号；先假设全是星号（`order` 全部执行完的状态）',
        'for index in range(len(order) - 1, -1, -1)': lambda S, B, r: (f'==时间倒流==：还原 `order[{S.index}]`，看有效子串数是否掉到 `k` 以下' if B.get('index') != S.index
                                                                      else '循环结束'),
        'o = order[index]': '这一步要还原的位置 `o = {o}`（`s[{o}]` 变回字母）',
        'new_left = left[o - 1]': '左邻 `{o - 1}` 不是星号 → 它所在的无星号段左端是 `left[{o - 1}]` = `{new_left}`',
        'new_left = o': '左边没有无星号段（边界或左邻是星号）→ `new_left = o = {o}`',
        'new_right = right[o + 1]': '右邻 `{o + 1}` 不是星号 → 它所在无星号段的右端是 `right[{o + 1}]` = `{new_right}`',
        'new_right = o': '右边没有无星号段 → `new_right = o = {o}`',
        'activity += (o - new_left)': '左段长 `{o - new_left}`、右段长 `{new_right - o}`：它们原有的无星号子串 `{(o - new_left) * (o - new_left + 1) // 2} + {(new_right - o) * (new_right - o + 1) // 2}` 个先加回来',
        'activity -= ': '合并后一整段长 `{new_right - new_left + 1}`，无星号子串 `{(new_right - new_left + 1) * (new_right - new_left + 2) // 2}` 个 → 减掉；`activity = {activity}`',
        'stars[o] = False': '`s[{o}]` 还原成字母，新区间 `[{new_left}, {new_right}]` 的两端记下：`right[{new_left}] = {right[new_left]}`，`left[{new_right}] = {left[new_right]}`',
        'if activity < k': lambda S, B, r: (f'`activity = {S.activity}` < `k = {S.k}` → 还原这一位后就不活跃了，说明==时刻 {S.index} 刚好活跃==' if S.activity < S.k
                                            else f'`activity = {S.activity}` >= `k = {S.k}` → 时刻 {S.index - 1} 仍然活跃，继续往前还原'),
        'return index': '答案 `{index}`：最早的活跃时间',
    },
    cards=dict(
        one_liner='时间倒流：把星号一个个还原，合并无星号的区间，数掉到 k 以下的那一刻',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`order` 是排列，时刻 `t` 把 `s[order[t]]` 换成 `*`；含 `*` 的子串有效',
                 '有效子串数 `>= k` 时字符串「活跃」，求最小活跃时间，不可能返回 `-1`',
                 '示例：`s="cat", order=[0,2,1], k=6` → `2`',
                 '本视频：`s="abcdef", order=[2,0,4,5,1,3], k=15` → `2`'],
        quote='直接计算有效子串的数量是比较麻烦的，对于这类计算至少出现一次的问题，一种常见的处理方法是反过来计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['有效子串 = 总子串 − 一个星号都没有的子串；长 `m` 的无星号段有 `m(m+1)/2` 个',
              '正着切区间要平衡树，==倒着走==就变成「合并区间」：星号还原成字母，左右两段连起来',
              '用 `left / right` 记录每段的两端，合并时只改端点，`activity` 随之增减'],
        summary=['时间 `O(n)`，空间 `O(n)`；先特判 `n(n+1)/2 < k` 返回 `-1`',
                 '`new_left / new_right` 在邻居是星号时取 `o` 自己',
                 '返回的是还原前对应的时刻 `index`：还原后 `activity < k` 说明该时刻刚好满足',
                 '对比灵神：灵神主推二分答案，逆向版用数组模拟双向链表；yiduobo 直接维护区间端点',
                 '原文已是 Python 3 可运行写法，未做改动'],
    ),
)
