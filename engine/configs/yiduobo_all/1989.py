CONFIG = dict(
    num=1989, title='捉迷藏中可捕获的最大人数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='人、鬼位置分开 · 贪心配对双指针',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def catchMaximumAmountofPeople(self, team, dist):

        h = []
        g = []
        for index, v in enumerate(team):
            if v == 0:
                h.append(index)
            else:
                g.append(index)
        
        res = 0
        p = 0
        for index in h:
            while p < len(g) and g[p] < index - dist:
                p += 1
            
            if p == len(g):
                break
            
            if abs(g[p] - index) <= dist:
                res += 1
                p += 1
        
        return res
''',
    call='Solution().catchMaximumAmountofPeople([1,1,0,0,0,1], 1)',
    expect=2,
    views=[
        dict(type='text', size=28, h=80, fn=lambda S: (
            f"人 `{S['index']}` 看鬼 `{S['g'][S['p']]}`：距离 `{abs(S['g'][S['p']]-S['index'])}` vs dist `{S['dist']}`"
            if 'p' in S and 'g' in S and 'index' in S and isinstance(S.get('index'), int) and S['p'] < len(S['g']) and S.get('res') is not None
            else '先把人（0）和鬼（1）的位置分别收集起来')),
        dict(type='array', var='team', h=220, label='team（0 = 人，1 = 鬼）',
             pointers={'index': 'blue', 'g[p]': 'pink'},
             color=lambda S, k, v: ('pink' if v == 1 else None)),
        dict(type='array', var='h', h=150, label='h：人的位置（有序）'),
        dict(type='array', var='g', h=150, label='g：鬼的位置（有序），p 指向当前候选', pointers={'p': 'pink'}),
    ],
    watch=['h', 'g', ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'h = []': '`h` 存「人」（0）的下标',
        'g = []': '`g` 存「鬼」（1）的下标',
        'for index, v in enumerate(team)': lambda S, B, r: (f"`team[{S.index}] = {S.v}`，位置 {S.index} 已看完，收集结束：人 `h` = {S.h}，鬼 `g` = {S.g}" if 'index' in B and B.index == S.index and S.index == len(S.team) - 1 else f"依次看每个位置：`team[{S.index}] = {S.v}`"),
        'if v == 0': lambda S, B, r: f"`v == 0` → 是人，记进 `h`" if S.v == 0 else "`v == 0` 不成立 → 是鬼，记进 `g`",
        'h.append': '人的位置 `{index}` 入 `h` → {h}',
        'g.append': '鬼的位置 `{index}` 入 `g` → {g}',
        'res = 0': '`res` 统计配对数',
        'p = 0': '`p` 指向「最左边还能抓人的鬼」，从 `g[0]` 开始',
        'for index in h': lambda S, B, r: ("人都处理完了，循环结束" if 'index' in B and B.index == S.index else f"从左到右处理每个人：当前人在位置 `{S.index}`"),
        'while p < len(g)': lambda S, B, r: (f"`g[{S.p}] = {S.g[S.p]} < {S.index} - {S.dist} = {S.index - S.dist}` 成立 → 这只鬼太靠左，后面的人更靠右，更够不到它，==永久跳过==" if S.p < len(S.g) and S.g[S.p] < S.index - S.dist else (f"鬼 `g[{S.p}] = {S.g[S.p]}` 不再太靠左，停在这里" if S.p < len(S.g) else "鬼用完了")),
        'p += 1': lambda S, B, r: f"`p` → {S.p}，看下一只鬼",
        'if p == len(g)': lambda S, B, r: ("`p == len(g)`：没有鬼了，后面的人更靠右，也抓不到 → 结束" if S.p == len(S.g) else f"`p = {S.p}` 还有鬼，继续判断"),
        'break': '鬼已用完，跳出循环',
        'if abs(g[p] - index) <= dist': lambda S, B, r: (f"`|{S.g[S.p]} - {S.index}| = {abs(S.g[S.p]-S.index)} <= {S.dist}` 成立 → 能抓到" if abs(S.g[S.p]-S.index) <= S.dist else f"`|{S.g[S.p]} - {S.index}| = {abs(S.g[S.p]-S.index)} <= {S.dist}` 不成立 → 鬼太靠右，抓不到这个人；鬼留着，换下一个人"),
        'res += 1': '配对成功：`res` → =={res}==',
        'p += 1\n': '这只鬼已抓人，`p` → {p}',
        'return res': '最多能抓到 =={res}== 个人',
    },
    cards=dict(
        one_liner='人从左到右排队，每人配「最左边够得着」的鬼',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`team[i] = 0` 是「不是鬼」的人，`1` 是「鬼」',
                 '每只鬼能抓位置差不超过 `dist` 的一个人，每人最多被抓一次',
                 '求最多能抓多少人。本视频：`[1,1,0,0,0,1]`，`dist = 1` → `2`'],
        quote='对于当前遍历到的人，最优的配对方案必然是选择当前可以抓到这个人的鬼当中，位置最左侧的那一个，因为对于后续的人而言，其位置必然是更靠后的。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历把人、鬼的下标分别收进 `h`、`g`，天然有序',
              '`p` 记「最左侧还可能抓人」的鬼；太靠左的鬼对后面的人也没用，==直接丢掉==',
              '`p` 只增不减，所以均摊 `O(1)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`p == len(g)` 就可以 `break`：后面的人更靠右，只会更难配对',
                 '鬼配对成功后 `p += 1`；够不到时 `p` 不动，换下一个人再试',
                 '原文为 Python 2 风格，本题代码无需修改，可直接在 Python 3 运行'],
    ),
)
