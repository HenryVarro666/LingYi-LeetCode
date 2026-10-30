CONFIG = dict(
    num=3851, title='不违反限制的最大请求数', difficulty='Medium', category='设计',
    author='yiduobo', technique='按时间排序 + 每个用户一个队列',
    tags=['队列', '哈希表'],
    code='''
class Solution(object):
    def maxRequests(self, requests, k, window):
        
        timestamp = {}
        res = 0
        for u, t in sorted(requests, key=lambda d:d[1]):
            if u not in timestamp:
                timestamp[u] = deque()
            
            while timestamp[u] and t - timestamp[u][0] > window:
                timestamp[u].popleft()
            
            if len(timestamp[u]) < k:
                timestamp[u].append(t)
                res += 1
        
        return res
''',
    call='Solution().maxRequests([[1,5],[1,1],[2,2],[1,2],[1,3],[2,9]], 2, 3)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"当前请求：用户 `{S['u']}` 在时间 `{S['t']}`　窗口 `[{S['t'] - S['window']}, {S['t']}]`" if 'u' in S else '先按时间从小到大排序'), size=28, h=60),
        dict(type='map', var='timestamp', label='timestamp（用户 → 窗口内已接受的请求时间队列）', fmt=lambda k, v: f'用户 {k}：{list(v)}', h=230),
    ],
    watch=['k', 'window', ('u', 'u', 'blue'), ('t', 't', 'pink'), ('res', 'res', 'green')],
    captions={
        'timestamp = {}': '哈希表：每个用户一个队列，只存窗口内已接受的请求时间',
        'res = 0': '`res` 统计接受的请求数',
        'for u, t in sorted': '按时间从小到大处理请求：现在是用户 `{u}` 在时间 `{t}`',
        'if u not in timestamp': lambda S, B, r: (f'用户 `{S.u}` 第一次出现 → 建一个空队列' if S.u not in B['timestamp'] else f'用户 `{S.u}` 已有队列'),
        'timestamp[u] = deque()': '为用户 `{u}` 建空队列',
        'while timestamp[u] and t': lambda S, B, r: (f'队首 `{S.timestamp[S.u][0]}`：`{S.t} − {S.timestamp[S.u][0]} = {S.t - S.timestamp[S.u][0]}` > `window={S.window}` → ==滑出窗口==，弹掉' if S.timestamp[S.u] and S.t - S.timestamp[S.u][0] > S.window else (f'队首 `{S.timestamp[S.u][0]}` 仍在窗口 `[{S.t - S.window}, {S.t}]` 内 → 不用再弹' if S.timestamp[S.u] else '队列空了 → 停止')),
        'timestamp[u].popleft()': '弹出队首，现在队列 `{list(timestamp[u])}`',
        'if len(timestamp[u]) < k': lambda S, B, r: (f'窗口内已有 `{len(S.timestamp[S.u])}` 个 < `k={S.k}` → ==还能接受==' if len(S.timestamp[S.u]) < S.k else f'窗口内已有 `{len(S.timestamp[S.u])}` 个，已满 `k={S.k}` → ==丢弃当前请求==（丢本次比丢前面更省后续压力）'),
        'timestamp[u].append(t)': '接受：时间 `{t}` 入队尾，队列 `{list(timestamp[u])}`',
        'res += 1': '`res` → {res}',
        'return res': '最多保留 =={res}== 个请求',
    },
    cards=dict(
        one_liner='按时间处理请求，窗口满了就丢掉当前这个',
        complexity='排序 `O(n log n)`，其余均摊 `O(n)`，空间 `O(n)`',
        problem=['`requests[i] = [user, time]`；某用户在任意 `[t, t+window]` 内请求数 `> k` 就违规',
                 '可以丢弃任意请求，求最多能保留多少个',
                 '本视频：`k=2`，`window=3`，6 个请求，答案 `5`'],
        quote='丢弃本次请求而不是丢弃前面的请求，能更有效的减轻后续窗口内的请求压力。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按时间排序，逐个处理；当前请求是它所在窗口里最晚的',
              '每个用户一个队列，先弹掉 `t − window` 之前的旧请求',
              '队列长度 `< k` 就接受并入队，否则丢掉当前这个，什么也不做'],
        summary=['窗口是闭区间：时间差 `== window` 的请求仍在窗口内（弹出条件是 `> window`）',
                 '必须先排序，输入顺序不一定按时间',
                 '时间 `O(n log n)`（排序），空间 `O(n)`',
                 '原文为 Python 2 风格写法，本题代码在 Python 3 下无需修改'],
    ),
)
