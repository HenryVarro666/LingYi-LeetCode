def _wk(p):
    return f'工人{-p[1]}→{p[0]}'


def _wt(p):
    return f'工人{-p[0]}'


CONFIG = dict(
    num=2532, title='过桥的时间', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='四个堆模拟',
    tags=['灵神题单', '难度分 2589'],
    code='''
class Solution:
    def findCrossingTime(self, n: int, k: int, time: List[List[int]]) -> int:
        time.sort(key=lambda t: t[0] + t[2])  # 稳定排序
        cur = 0
        workL, waitL, waitR, workR = [], [[-i, 0] for i in range(k - 1, -1, -1)], [], []  # 下标越大效率越低
        while n:
            while workL and workL[0][0] <= cur:
                p = heappop(workL)
                p[0], p[1] = p[1], p[0]
                heappush(waitL, p)  # 左边完成放箱
            while workR and workR[0][0] <= cur:
                p = heappop(workR)
                p[0], p[1] = p[1], p[0]
                heappush(waitR, p)  # 右边完成搬箱
            if waitR:  # 右边过桥，注意加到 waitR 中的都是 <= cur 的（下同）
                p = heappop(waitR)
                cur += time[-p[0]][2]
                p[1] = p[0]
                p[0] = cur + time[-p[0]][3]
                heappush(workL, p)  # 放箱
            elif waitL:  # 左边过桥
                p = heappop(waitL)
                cur += time[-p[0]][0]
                p[1] = p[0]
                p[0] = cur + time[-p[0]][1]
                heappush(workR, p)  # 搬箱
                n -= 1
            elif len(workL) == 0: cur = workR[0][0]  # cur 过小，找个最小的放箱/搬箱完成时间来更新 cur
            elif len(workR) == 0: cur = workL[0][0]
            else: cur = min(workL[0][0], workR[0][0])
        while workR:
            t, i = heappop(workR)  # 右边完成搬箱
            # 如果没有排队，直接过桥；否则由于无论谁先过桥，最终完成时间都一样，所以也可以直接计算
            cur = max(t, cur) + time[-i][2]
        return cur  # 最后一个过桥的时间
''',
    call='Solution().findCrossingTime(3, 2, [[1,5,1,8],[10,10,10,10]])',
    expect=37,
    views=[
        dict(type='heap', var='waitL', label='waitL 左等（堆顶最低效）', fmt=_wt, top_color='blue', h=105),
        dict(type='heap', var='workL', label='workL 左放箱（→完成时间）', fmt=_wk, h=105),
        dict(type='heap', var='waitR', label='waitR 右等（堆顶最低效）', fmt=_wt, top_color='pink', h=105),
        dict(type='heap', var='workR', label='workR 右搬箱（→完成时间）', fmt=_wk, h=105),
        dict(type='text', h=70, size=26, fn=lambda S: (f"时钟 `cur = {S['cur']}`，还要从左边派 =={S['n']}== 个工人" if 'cur' in S and 'n' in S else '')),
    ],
    watch=[('cur', 'cur', 'yellow'), ('n', 'n', 'orange'), ('p', 'p', 'cyan')],
    captions={
        'time.sort': '按 `left+right` 稳定排序：==下标越大效率越低==，之后只看下标就能比大小：`{time}`',
        'workL, waitL': '四个堆：workL / waitL / waitR / workR；开始所有人都在左边等：waitL 里存 `[-i, 0]`，下标大的在堆顶',
        'while n': lambda S, B, r: (f'还有 `{S.n}` 个箱子没从左边派人去搬 → 继续' if S.n else f'箱子都有人去搬了，剩下只要等右边的人过桥'),
        'while workL and workL[0][0] <= cur': lambda S, B, r: (f'放完箱的工人（完成时间 `{S.workL[0][0]}` ≤ cur `{S.cur}`）回到桥边' if S.workL and S.workL[0][0] <= S.cur
                                                              else '左边没有人在这个时刻完成放箱'),
        'p = heappop(workL)': '弹出最早放完箱的工人',
        'p[0], p[1] = p[1], p[0]': '交换：把关键字从「完成时间」换成「-下标」，排队时按效率排',
        'heappush(waitL, p)': '工人 `{-p[0]}` 回到左边等桥',
        'while workR and workR[0][0] <= cur': lambda S, B, r: (f'搬完箱的工人（完成时间 `{S.workR[0][0]}` ≤ cur `{S.cur}`）回到桥边' if S.workR and S.workR[0][0] <= S.cur
                                                              else '右边没有人在这个时刻搬完箱'),
        'p = heappop(workR)': '弹出最早搬完箱的工人',
        'heappush(waitR, p)': '工人 `{-p[0]}` 在右边等桥',
        'if waitR': lambda S, B, r: ('右边有人在等 → ==优先让右边（效率最低）的工人过桥==' if S.waitR else '右边没人等桥，看左边'),
        'p = heappop(waitR)': '右边效率最低的是工人 `{-p[0]}`',
        'cur += time[-p[0]][2]': '右→左过桥要 `{time[-p[0]][2]}`，桥被占用 → `cur = {B.cur} + {time[-p[0]][2]} = {cur}`',
        'p[0] = cur + time[-p[0]][3]': '过桥后去新仓库放箱，放完时刻 `{p[0]}`',
        'heappush(workL, p)': '工人进入 workL（放箱中）',
        'elif waitL': lambda S, B, r: ('右边没人，左边有人等且箱子还没派完 → 让左边效率最低的过桥' if S.waitL else '左边也没人排队'),
        'p = heappop(waitL)': '左边效率最低的是工人 `{-p[0]}`',
        'cur += time[-p[0]][0]': '左→右过桥要 `{time[-p[0]][0]}` → `cur = {B.cur} + {time[-p[0]][0]} = {cur}`',
        'p[0] = cur + time[-p[0]][1]': '过桥后去旧仓库搬箱，搬完时刻 `{p[0]}`',
        'heappush(workR, p)': '工人进入 workR（搬箱中）',
        'n -= 1': '又派走一个人去搬箱，剩 `n = {n}`',
        'elif len(workL) == 0': lambda S, B, r: (f'两边都没人排队，==cur 太小==；左边没人在放箱 → 桥空着，直接跳到最早搬完箱的时刻 `{S.workR[0][0]}`' if not S.workL
                                                 else '两边都没人排队，但左边还有人在放箱，往下看'),
        'elif len(workR) == 0': lambda S, B, r: (f'右边没人在搬箱 → 直接跳到最早放完箱的时刻 `{S.workL[0][0]}`' if not S.workR
                                                 else '右边也有人在搬箱，往下看'),
        'else: cur': '两边都有人在忙 → 跳到两个堆里最早的完成时刻 `cur = {cur}`',
        'while workR': lambda S, B, r: (f'箱子都派完了，workR 里还有 `{len(S.workR)}` 个工人没回到左边' if S.workR else '所有人都已经过桥回到左边'),
        't, i = heappop(workR)': '最早搬完箱的工人 `{-i}`，完成时间 `{t}`',
        'cur = max(t, cur)': '没排队就从 `t` 开始过桥，否则接着 `cur` 过；==谁先过最终时间一样==：`cur = max({t}, {B.cur}) + {time[-i][2]} = {cur}`',
        'return cur': '最后一个箱子到达左边的时间 =={ret}==',
    },
    cards=dict(
        one_liner='四个堆分别装「左等、左放箱、右等、右搬箱」的人，时钟一格格推进',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['`k` 个工人搬 `n` 个箱子，过桥同一时刻只能一人；右边等桥的工人优先，效率最低的先走',
                 '效率低：`left+right` 大，相同则下标大。求最后一个箱子到达左边的时间',
                 '示例：`n=3, k=2, time=[[1,5,1,8],[10,10,10,10]]` → `37`'],
        quote='建立 4 个堆，每个堆都记录工人下标 i 和完成时间 t……代码实现时，可以先把 time 从小到大稳定排序，这样下标越大的工人效率越低，只看下标就能比较工人的效率。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`workL/workR` 记「完成放/搬箱」的时间，`waitL/waitR` 记排队的工人',
              '每轮先把 `<= cur` 的工人从 work 堆挪到 wait 堆，再决定谁过桥：==右边优先==',
              '没人排队就把 `cur` 跳到最早的完成时间；箱子派完后，剩下的人只算过桥'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '排序后用 `-i` 当关键字，小顶堆的堆顶就是效率最低的工人',
                 '两个堆里的列表是 `[完成时间, -i]` 和 `[-i, 完成时间]` 来回交换，别弄混',
                 '最后只算「最后一个工人过桥」，不用算放箱时间',
                 '题目会改写 `time`（排序）；灵神的视频讲解思考过程见题解链接'],
    ),
)
