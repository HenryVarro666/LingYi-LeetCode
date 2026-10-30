def _txt(S):
    if 'q_info' not in S or 't' not in S:
        return ''
    idx = S.get('index')
    if idx is None:
        q = S['q_info'][0][1]
    else:
        q = S['q_info'][idx][1]
    return f'当前询问时间 `{q}`，窗口 ==[{q - S["x"]}, {q}]==；正在处理时间点 `t = {S["t"]}`'


CONFIG = dict(
    num=2747, title='统计没有收到请求的服务器数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按时间点滑窗 · 哈希表记次数',
    tags=['离线算法', '难度分 2405'],
    code='''
class Solution(object):
    def countServers(self, n, logs, x, queries):

        log_info = {}
        for sid, t in logs:
            if t not in log_info:
                log_info[t] = set()
            log_info[t].add(sid)
        
        cnt = {}
        q_info = sorted(enumerate(queries), key=lambda d:d[1])

        res = [None] * len(q_info)
        for t in range(q_info[0][1] - x, q_info[0][1] + 1):
            if t in log_info:
                for sid in log_info[t]:
                    cnt[sid] = cnt.get(sid, 0) + 1
        res[q_info[0][0]] = n - len(cnt)

        for index in range(1, len(q_info)):
            for t in range(q_info[index - 1][1] + 1, q_info[index][1] + 1):
                if t in log_info:
                    for sid in log_info[t]:
                        cnt[sid] = cnt.get(sid, 0) + 1
            
                if t - x - 1 in log_info:
                    for sid in log_info[t - x - 1]:
                        cnt[sid] -= 1
                        if cnt[sid] == 0:
                            cnt.pop(sid)
            
            res[q_info[index][0]] = n - len(cnt)

        return res
''',
    call='Solution().countServers(3, [[1,3],[2,6],[1,5]], 5, [10, 11])',
    expect=[1, 2],
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='map', var='log_info', label='log_info：时间点 → 收到请求的服务器集合', h=200,
             fmt=lambda k, v: f'{k}: {sorted(v)}'),
        dict(type='map', var='cnt', label='cnt：窗口内有请求的服务器 → 次数（没出现的就是没收到请求）', h=200,
             fmt=lambda k, v: f'服务器{k}: {v}'),
        dict(type='array', var='res', label='res（按原询问顺序）', h=150),
    ],
    watch=['t', ('index', 'index', 'blue'), ('len(cnt)', 'len(cnt)', 'green')],
    captions={
        'log_info = {}': '先把日志按时间点归类：知道每个时间点有哪些服务器收到请求',
        'log_info[t].add(sid)': '时间 `{t}` 有服务器 `{sid}` 收到请求 → `log_info[{t}] = {sorted(log_info[t])}`',
        'cnt = {}': '`cnt` 只存窗口内收到过请求的服务器，`n - len(cnt)` 就是答案',
        'q_info = sorted': '询问从小到大排序，并带着原下标 → `{q_info}`',
        'res = [None]': '`res` 按原询问顺序放答案',
        'for t in range(q_info[0][1] - x': lambda S, B, r: (f'先用最小询问建窗口：从时间 `{S.q_info[0][1] - S.x}` 扫到 `{S.q_info[0][1]}`，现在是 `t = {S.t}`' if not (B.get('t') == S.t and S.t == S.q_info[0][1]) else '第一个窗口的时间点扫完了'),
        'res[q_info[0][0]]': '第一个窗口建好：`res[{q_info[0][0]}] = n - len(cnt) = {n} - {len(cnt)} = =={res[q_info[0][0]]}==`',
        'for index in range(1': lambda S, B, r: (f'开始处理第 `{S.index + 1}` 小的询问（时间 `{S.q_info[S.index][1]}`）' if S.index != B.get('index') else '所有询问都处理完了'),
        'for t in range(q_info[index - 1][1] + 1': lambda S, B, r: (f'窗口从上一个询问滑到本询问：只扫新增的时间点 `{S.q_info[S.index - 1][1] + 1}` 到 `{S.q_info[S.index][1]}`，现在是 `t = {S.t}`' if B.get('t') != S.t else '新增的时间点扫完了，窗口滑到位'),
        'if t in log_info': lambda S, B, r: (f'时间 `{S.t}` 有请求 → 右边界新进来这些服务器' if S.t in S.log_info else f'时间 `{S.t}` 没人收到请求，跳过'),
        'cnt[sid] = cnt.get': '服务器 `{sid}` 窗口内请求数 → `{cnt[sid]}`',
        'if t - x - 1 in log_info': lambda S, B, r: (f'老的左边界 `{S.t} - {S.x} - 1 = {S.t - S.x - 1}` 刚滑出窗口，它有请求 → 要减掉' if S.t - S.x - 1 in S.log_info else f'滑出窗口的时间点 `{S.t - S.x - 1}` 没有请求，不用减'),
        'cnt[sid] -= 1': '服务器 `{sid}` 的这次请求离开窗口 → `{cnt[sid]}`',
        'if cnt[sid] == 0': lambda S, B, r: (f'`cnt[{S.sid}] == 0`：窗口里已经没有它的请求 → 从 `cnt` 里删掉' if S.cnt[S.sid] == 0 else f'`cnt[{S.sid}] = {S.cnt[S.sid]}`，窗口里还有请求，保留'),
        'cnt.pop(sid)': '删除服务器 `{sid}`，`len(cnt) = {len(cnt)}`',
        'res[q_info[index][0]]': '窗口 `[{q_info[index][1] - x}, {q_info[index][1]}]` 就绪 → `res[{q_info[index][0]}] = {n} - {len(cnt)} = =={res[q_info[index][0]]}==`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='窗口长度固定为 x：让它沿时间轴一格一格滑，进出各加减一次',
        complexity='时间 `O(max(queries) + m)`，空间 `O(m)`',
        problem=['`n` 台服务器，`logs[i] = [id, time]`；对每个询问 `q`，求 `[q - x, q]` 内没收到请求的服务器数',
                 '示例：`n=3, logs=[[1,3],[2,6],[1,5]], x=5, queries=[10,11]` → `[1,2]`',
                 '本视频用的就是这个示例'],
        quote='题目中的询问区间长度固定，那么很自然想到使用滑动窗口来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先遍历 `logs`，用哈希表存==每个时间点有哪些服务器==收到请求',
              '询问排序后，用最小询问建第一个窗口；之后每次把窗口右端滑到下一个询问',
              '每滑一格：右端时间点的服务器次数 +1，左端滑出的时间点 -1，减到 0 就删掉'],
        summary=['时间 `O(max(queries) + m)`：每个时间点只进出窗口一次，不超过 `10^6`',
                 '易错：滑出窗口的是 `t - x - 1`，不是 `t - x`（闭区间）',
                 '易错：次数减到 0 要 `pop`，否则 `len(cnt)` 算多',
                 '对比灵神：灵神按 logs 双指针 + 数组计数；yiduobo 按时间点逐格滑动',
                 '原文本身可直接在 Python 3 运行，未做修改'],
    ),
)
