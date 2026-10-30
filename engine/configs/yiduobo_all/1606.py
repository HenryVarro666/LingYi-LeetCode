CONFIG = dict(
    num=1606, title='找到处理最多请求的服务器', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='两个堆：working 小根堆 + pending 轮次编号',
    tags=[],
    code='''
class Solution(object):
    def busiestServers(self, k, arrival, load):

        n = len(arrival)
        working = []
        pending = list(range(k))
        cnt = [0] * k

        for index, t in enumerate(arrival):
            target = index % k
            while working and working[0][0] <= t:
                num = working[0][1]
                if num < target:
                    num += (index // k + 1) * k
                else:
                    num += index // k * k 
                
                heapq.heappush(pending, num)
                heapq.heappop(working)

            if pending:
                choose = heapq.heappop(pending)
                cnt[choose % k] += 1
                heapq.heappush(working, [t + load[index], choose % k])

        res = [0]
        for index in range(1, k):
            if cnt[index] > cnt[res[0]]:
                res = [index]
            elif cnt[index] == cnt[res[0]]:
                res.append(index)
        
        return res
''',
    call='Solution().busiestServers(3, [1,4,5,6,7,8], [5,5,4,2,5,3])',
    expect=[0],
    views=[
        dict(type='text', h=70, size=24, fn=lambda S: (
            f"第 `{S['index']}` 个请求：到达时间 `t = {S['t']}`，目标服务器 `target = {S['index']} % {S['k']} = {S['target']}`"
            if 'target' in S and 'res' not in S else '')),
        dict(type='heap', var='working', label='working 小根堆 [结束时间, 服务器号]', fmt=lambda x: f'[{x[0]},S{x[1]}]', top_color='orange', h=105),
        dict(type='heap', var='pending', label='pending 小根堆：轮次编号（编号 % k = 服务器号）', fmt=lambda x: f'{x}→S{x % 3}', top_color='blue', h=105),
        dict(type='array', var='cnt', label='cnt[服务器号] = 处理的请求数', h=140,
             color=lambda S, i, v: 'green' if v == max(S['cnt']) and v > 0 else None),
    ],
    watch=[('index', lambda S: S.get('index', ''), 'yellow'), ('t', lambda S: S.get('t', ''), 'orange'),
           ('target', lambda S: S.get('target', ''), 'pink'), ('res', lambda S: S.get('res', ''), 'green')],
    captions={
        'working = []': '`working`：正在忙的服务器，按==结束时间==排的小根堆',
        'pending = list(range(k))': '`pending`：空闲服务器的「轮次编号」，开始是 `0..k-1`（第 0 轮）',
        'cnt = [0] * k': '`cnt` 记录每台服务器处理了多少请求',
        'target = index % k': '第 `{index}` 个请求优先给 `target = {index} % {k} = {target}` 号服务器',
        'while working and working[0][0] <= t': lambda S, B, r: (
            '没有忙的服务器' if not S.working else
            f'最早结束的服务器 S{S.working[0][1]} 在 `{S.working[0][0]}` 结束，`{S.working[0][0]} <= t = {S.t}` → ==已空闲==，要放回 pending' if S.working[0][0] <= S.t else
            f'堆顶结束时间 `{S.working[0][0]} > t = {S.t}`：没有更多服务器空闲了'),
        'num = working[0][1]': '取出刚空闲的服务器号 `num = {num}`',
        'if num < target': lambda S, B, r: (
            f'`num = {S.num} < target = {S.target}`：它在 target 左边，这一轮 target 到 k-1 都用完才轮到它 → ==排到下一轮=='
            if S.num < S.target else
            f'`num = {S.num} >= target = {S.target}`：它在 target 右边（含），==这一轮就能用=='),
        'num += (index // k + 1) * k': '下一轮：编号 `num += ({index} // {k} + 1) × {k}` = `{num}`',
        'num += index // k * k': '本轮：编号 `num += {index} // {k} × {k}` = `{num}`',
        'heapq.heappush(pending, num)': '编号 `{num}` 放进 pending（编号越小越先被选，对应「从 target 起顺时针找」）',
        'heapq.heappop(working)': '把它从 working 弹出',
        'if pending': lambda S, B, r: ('pending 里有空闲服务器 → 可以处理' if S.pending else '没有空闲服务器 → ==请求被丢弃=='),
        'choose = heapq.heappop(pending)': 'pending 最小编号 `choose = {choose}` → 服务器 `{choose} % {k}` = =={choose % k}==，正好是从 target 起顺时针第一台空闲的',
        'cnt[choose % k] += 1': '服务器 S{choose % k} 处理数 +1：`cnt = {cnt}`',
        'heapq.heappush(working, [t + load[index], choose % k])': 'S{choose % k} 变忙，结束时间 `t + load = {t} + {load[index]} = {t + load[index]}`',
        'res = [0]': '统计最大值：先假设服务器 0 最多',
        'for index in range(1, k)': '依次看服务器 `{index}`',
        'if cnt[index] > cnt[res[0]]': lambda S, B, r: (
            f'`cnt[{S.index}] = {S.cnt[S.index]}` 对比当前最大 `{S.cnt[S.res[0]]}` → ' + ('更大，换' if S.cnt[S.index] > S.cnt[S.res[0]] else '不更大')),
        'res = [index]': '`res = {res}`：重新开始记录',
        'elif cnt[index] == cnt[res[0]]': lambda S, B, r: ('相等 → 并列，追加' if S.cnt[S.index] == S.cnt[S.res[0]] else '更小，忽略'),
        'res.append(index)': '`res = {res}`',
        'return res': '最忙的服务器：`{ret}`',
    },
    skip=[4, 12, 19, 23, 26],
    max_steps=100,
    cards=dict(
        one_liner='忙的放小根堆等结束，空闲的存「轮次编号」，最小编号就是该用的服务器',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['`k` 台服务器，第 `i` 个请求到达时间 `arrival[i]`，耗时 `load[i]`',
                 '请求先给 `i % k` 号；它忙就依次往后（到 k-1 后回 0）找第一台空闲的；都忙则丢弃',
                 '求处理请求最多的服务器。本视频：`k=3`，`arrival=[1,4,5,6,7,8]`，`load=[5,5,4,2,5,3]` → `[0]`'],
        quote='若p < target，其将被排到下一轮。当前轮次为index / k，那么下一轮就是index / k + 1，因此p在下一轮的编号就是p + (index / k + 1) * k',
        quote_src='—— yiduobo 题解原文',
        idea=['一个小根堆 `working` 记结束时间：堆顶 `<= t` 的服务器已空闲，弹出',
              '空闲服务器不分左右两段，而给它一个「轮次编号」：在 target 右边（含）本轮编号，在左边就排下一轮',
              '`pending` 小根堆里最小的编号，正是从 target 开始顺时针的第一台空闲服务器'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '易错点：`num < target` 才加下一轮，`num >= target` 当轮；`pending` 为空要丢弃请求',
                 '服务器号由 `编号 % k` 还原；`cnt` 与结果下标都用服务器号',
                 '原文为 Python 2 写法，`index / k` 已改为 `index // k`；`pending = range(k)` 已改为 `list(range(k))`',
                 '另一种做法：用线段树/平衡树查「[target,k-1] 和 [0,target-1] 的最小空闲号」'],
    ),
)
