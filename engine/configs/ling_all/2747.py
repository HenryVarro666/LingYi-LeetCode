def _win(S):
    if 'right' not in S:
        return ''
    q = S.get('q')
    if q is None:
        return ''
    return f'询问 `{q}`：窗口时间 ==[{q - S["x"]}, {q}]==，没收到请求的服务器 `out_of_range = {S["out_of_range"]}`'


CONFIG = dict(
    num=2747, title='统计没有收到请求的服务器数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='离线询问 · 排序 + 滑动窗口',
    tags=['离线算法', '难度分 2405'],
    code='''
class Solution:
    def countServers(self, n: int, logs: List[List[int]], x: int, queries: List[int]) -> List[int]:
        logs.sort(key=lambda p: p[1])  # 按照 time 排序
        ans = [0] * len(queries)
        cnt = [0] * (n + 1)
        out_of_range = n
        left = right = 0
        for qi, q in sorted(enumerate(queries), key=lambda p: p[1]):
            while right < len(logs) and logs[right][1] <= q:  # 进入窗口
                i = logs[right][0]
                if cnt[i] == 0: out_of_range -= 1
                cnt[i] += 1
                right += 1
            while left < len(logs) and logs[left][1] < q - x:  # 离开窗口
                i = logs[left][0]
                cnt[i] -= 1
                if cnt[i] == 0: out_of_range += 1
                left += 1
            ans[qi] = out_of_range
        return ans
''',
    call='Solution().countServers(4, [[1,3],[2,6],[1,5],[3,9]], 5, [10, 7, 11])',
    expect=[1, 2, 2],
    views=[
        dict(type='text', fn=_win, size=26),
        dict(type='array', var=lambda S: [f'{a}@{t}' for a, t in S['logs']], label='logs（按时间排序，格内写 服务器@时间）',
             pointers={'left': 'blue', 'right': 'pink'}, h=230,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i < S['right'])),
        dict(type='array', var='cnt', label='cnt[服务器 id]：窗口内收到的请求数（下标 0 不用）', h=180,
             color=lambda S, i, v: ('green' if v > 0 else None) if i > 0 else None,
             dim=lambda S, i, v: i == 0),
        dict(type='array', var='ans', label='ans（按原询问顺序）', h=150),
    ],
    watch=['q', 'left', 'right', ('out_of_range', 'out_of_range', 'green')],
    captions={
        'logs.sort': '先按时间排序：窗口只会向右滑',
        'cnt = [0]': '`cnt[i]`：服务器 i 在窗口内收到的请求数',
        'out_of_range = n': '一开始窗口是空的，`n = {n}` 台服务器全都没收到请求',
        'for qi, q': lambda S, B, r: (f'所有询问都处理完了，退出循环' if B.get('q') is not None and S.q == B.get('q') else f'询问也按时间排序，用 `qi` 记住原下标 → 当前处理询问 `{S.q}`，窗口 `[{S.q - S.x}, {S.q}]`'),
        'while right': lambda S, B, r: (f'`logs[{S.right}]` 的时间 `{S.logs[S.right][1]} <= {S.q}`：这条请求在窗口右端以内 → 进入窗口'
                                        if S.right < len(S.logs) and S.logs[S.right][1] <= S.q else f'没有时间 `<= {S.q}` 的新请求了，右端停在 `right = {S.right}`'),
        'if cnt[i] == 0: out_of_range -= 1': lambda S, B, r: (f'`cnt[{S.i}]` 原来是 0：这台服务器第一次出现在窗口 → `out_of_range` 减 1 变成 =={S.out_of_range}=='
                                                         if S.out_of_range != B.out_of_range else f'`cnt[{S.i}]` 已经不是 0，服务器本来就有请求，`out_of_range` 不变'),
        'cnt[i] += 1': '`cnt[{i}]` → {cnt[i]}',
        'i = logs[right][0]': '取出这条请求的服务器 `i = {i}`',
        'i = logs[left][0]': '取出这条请求的服务器 `i = {i}`',
        'right += 1': '`right` → {right}',
        'while left': lambda S, B, r: (f'`logs[{S.left}]` 的时间 `{S.logs[S.left][1]} < {S.q - S.x}`：比窗口左端 `{S.q - S.x}` 还早 → 离开窗口'
                                       if S.left < len(S.logs) and S.logs[S.left][1] < S.q - S.x else f'`left` 处的请求已在窗口内，不再移除'),
        'cnt[i] -= 1': '`cnt[{i}]` → {cnt[i]}',
        'if cnt[i] == 0: out_of_range += 1': lambda S, B, r: (f'`cnt[{S.i}]` 减到 0：窗口里再也没有这台服务器的请求 → `out_of_range` 加 1 变成 =={S.out_of_range}=='
                                                         if S.out_of_range != B.out_of_range else f'`cnt[{S.i}]` 还剩 {S.cnt[S.i]} 次，仍收到过请求，`out_of_range` 不变'),
        'left += 1': '`left` → {left}',
        'ans[qi] = out_of_range': '窗口 `[{q - x}, {q}]` 已经调整好 → `ans[{qi}]` = =={out_of_range}==（按原询问下标存）',
        'return ans': '按原顺序返回 `{ans}`',
    },
    cards=dict(
        one_liner='询问窗口大小固定：排序后滑动窗口，用计数数组维护「没收到请求的服务器数」',
        complexity='时间 `O(n + m log m + q log q)`，空间 `O(n + q)`',
        problem=['`n` 台服务器，`logs[i] = [id, time]` 表示 id 在 time 收到请求',
                 '对每个询问 `q`，求闭区间 `[q - x, q]` 内没收到请求的服务器数',
                 '示例：`n=3, logs=[[1,3],[2,6],[1,5]], x=5, queries=[10,11]` → `[1,2]`',
                 '本视频：`n=4, x=5, queries=[10,7,11]`，4 条日志'],
        quote='由于询问的窗口大小是固定的，所以可以用滑动窗口（双指针）来算，维护窗口内的各个服务器收到了多少次请求 cnt，以及没有收到请求的服务器数目 outOfRange。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `logs` 按时间排序；询问也排序，但用下标数组记住原位置，答案才不会乱',
              '询问从小到大，窗口 `[q-x, q]` 的两端只会往右走 → 双指针',
              '`cnt` 记每台服务器的请求数：0→1 时 `out_of_range` 减 1，1→0 时加 1'],
        summary=['时间 `O(n + m log m + q log q)`：数组计数要加上 `n`',
                 '易错：窗口左端是 `logs[left][1] < q - x` 才离开（闭区间，等于 `q - x` 要保留）',
                 '易错：必须带着 `qi` 排序，最后写到 `ans[qi]`',
                 '灵神的思考题：询问区间长度不固定时，改为离线 + 其他做法'],
    ),
)
