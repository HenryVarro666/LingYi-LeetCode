def _rq(S):
    r = S.get('requests')
    return list(r) if r else None


def _fcell(S, i, j, v):
    if S.get('_line', 0) in (10, 11, 12, 13, 14, 15) and 'j' in S and i == S['j'] and 'i' in S:
        return 'yellow' if v is not None and v != float('inf') else 'blue'
    if v == float('inf'):
        return None
    return 'green' if v == 0 else None


def _formula(S):
    if 'i' not in S or 'j' not in S or 'remain' not in S or 'requests' not in S:
        return '`f[j][0/1]`：电梯在已处理区间 `[i, j]` 的左端/右端，剩余请求的最小惩罚增量'
    r = S['requests']
    return (f'`remain` = 剩余请求数 = `{S["remain"]}`；移动 1 层 → 惩罚增加 `remain` '
            f'（区间 [{r[S["i"]]}, {r[S["j"]]}]）')


CONFIG = dict(
    num=4023, title='电梯请求 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP · 惩罚增量',
    tags=['区间 DP'],
    code='''
class Solution:
    def elevatorRequests(self, n: int, start: int, requests: list[int]) -> int:
        requests += [start, -1, n]  # 插入 start 和两个哨兵
        requests.sort()
        m = len(requests)
        idx = bisect_left(requests, start)
        f = [[inf, inf] for _ in range(m)]
        for i in range(1, idx + 1):
            for j in range(m - 2, idx - 1, -1):
                if i == 1 and j == m - 2:
                    f[j][0] = f[j][1] = 0
                    continue
                remain = m - 3 - j + i
                f[j][1] = min(f[j][0] + (requests[j] - requests[i - 1]) * remain,  # 往左
                              f[j + 1][1] + (requests[j + 1] - requests[j]) * remain)  # 往右
                f[j][0] = min(f[j][0] + (requests[i] - requests[i - 1]) * remain,  # 往左
                              f[j + 1][1] + (requests[j + 1] - requests[i]) * remain)  # 往右
        return f[idx][0]
''',
    call='Solution().elevatorRequests(10, 5, [0, 2, 9])',
    expect=22,
    skip=['for _ in range', 'for j in range', 'f[j + 1][1] + (requests[j + 1]'],
    views=[
        dict(type='array', var=_rq, label='requests（排序后，含 start 与哨兵 -1 / n）', h=250, cell=80,
             pointers={'i': 'blue', 'j': 'pink', 'idx': 'green'},
             dim=lambda S, k, v: v in (-1, 10) and k in (0, len(S['requests']) - 1)),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[j] = [电梯在左端 i, 电梯在右端 j]（黄 = 当前 j 行）', h=300, cell=56,
             rows=lambda S: [f'j={k}' for k in range(len(S['f']))], cols=['左', '右'],
             color=_fcell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('idx', 'idx', 'green'), 'remain'],
    captions={
        'requests += ': '把起点 `start` 和哨兵 `-1`、`n` 塞进去：不用再判断越界',
        'requests.sort()': '排序后 `requests = {requests}`：电梯走过的楼层一定是一段连续区间',
        'm = len': '`m = {m}`（含 3 个额外元素）',
        'idx = bisect_left': '起点 `start` 在 `requests` 里的下标 `idx = {idx}`',
        'f = [[inf': '`f[j][0]`/`f[j][1]`：已处理 `[i, j]`，电梯在左端/右端。`i` 这一维被滚动掉了',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：算 `i` 要先有 `i-1` → ==i 从小到大==（左端往外扩）' if S.get('i') != B.get('i') else '所有 i 都枚举完了'),
        'if i == 1 and j == m - 2': lambda S, B, r: ('`i = 1` 且 `j = m-2`：==所有请求都处理完了==，剩余惩罚 0' if (S.i == 1 and S.j == S.m - 2) else f'`i = {S.i}, j = {S.j}` 不是终点，继续转移'),
        'f[j][0] = f[j][1] = 0': '终点：`f[{j}][0] = f[{j}][1] = 0`',
        'remain = ': '剩余未处理的请求数 `remain = {m} - 3 - {j} + {i}` = =={remain}==：每走 1 秒，每个都 +1 惩罚',
        'f[j][1] = min': lambda S, B, r: f'电梯在右端 `{S.requests[S.j]}`：往左 `{B.f[S.j][0]} + {(S.requests[S.j]-S.requests[S.i-1])}×{S.remain}` = {B.f[S.j][0] + (S.requests[S.j]-S.requests[S.i-1])*S.remain}，往右 `{B.f[S.j+1][1]} + {(S.requests[S.j+1]-S.requests[S.j])}×{S.remain}` = {B.f[S.j+1][1] + (S.requests[S.j+1]-S.requests[S.j])*S.remain}，==取小==',
        'f[j][0] = min': lambda S, B, r: f'电梯在左端 `{S.requests[S.i]}`：往左 `{B.f[S.j][0]} + {(S.requests[S.i]-S.requests[S.i-1])}×{S.remain}` = {B.f[S.j][0] + (S.requests[S.i]-S.requests[S.i-1])*S.remain}，往右 `{B.f[S.j+1][1]} + {(S.requests[S.j+1]-S.requests[S.i])}×{S.remain}` = {B.f[S.j+1][1] + (S.requests[S.j+1]-S.requests[S.i])*S.remain}，==取小==',
        'return f[idx][0]': '起点单独成区间 `[idx, idx]`，答案 `f[{idx}][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='不记时间，只算每一秒还剩几个请求',
        complexity='时间 `O(m^2)`，空间 `O(m)`',
        problem=['电梯从 `start` 出发，每秒走一层；请求 `requests` 的楼层同时发出，在时刻 `t` 到达某请求，惩罚 `t`',
                 '求处理完所有请求的==最小总惩罚==',
                 '示例：`n=10, start=5, requests=[0,2,9]` → `22`'],
        quote='考虑每过一秒，总惩罚增加了多少。……我们只需考虑==还剩下多少个未完成的请求==，即为每过一秒总惩罚的增量。',
        quote_src='—— 灵茶山艾府题解',
        idea=['电梯走过 `[p, q]`，里面的请求顺带处理 → 状态是排序后的连续区间 + 电梯在左端还是右端',
              '往外扩一格的代价 = 距离 × 剩余请求数 `remain`',
              '记忆化 `dfs(i, j, is_right)` → 1:1 递推 → 去掉 `i` 维，空间 `O(m)`'],
        summary=['时间 `O(m^2)`，空间 `O(m)`（`m` 是请求数，与楼层数 `n` 无关）',
                 '易错：`start` 和哨兵 `-1`、`n` 要一起插入再排序，`requests` 被原地修改',
                 '`remain = m - 3 - j + i`：减 3 是去掉 start 和两个哨兵',
                 '题解还给了 `@cache` 记忆化搜索与二维递推两种写法，这里演示最后的空间优化版',
                 '同类区间 DP：见灵神动态规划题单「区间 DP」'],
    ),
)
