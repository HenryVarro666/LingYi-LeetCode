def _fvals(S):
    s = S['customers']
    if 'index' not in S:
        return [0]
    upto = S['index'] + 1 if S['_line'] >= 11 else S['index']
    return [2 * s[:p].count('N') - p for p in range(upto + 1)]


def _txt(S):
    if 'index' not in S:
        return '代价 = `k + cnt[p] + cnt[p] − p`，`k` 是常量 → 只看 `2×cnt − p`'
    p, cnt = S['index'] + 1, S['cnt']
    if S['_line'] >= 11:
        return f"分割点 `p = {p}`：`cnt + cnt − p = {cnt} + {cnt} − {p}` = =={2 * cnt - p}==　（目前最小 `min_cnt = {S['min_cnt']}`）"
    return f"前 `{S['index']}` 个字符里 `N` 的个数 `cnt = {cnt}`"


CONFIG = dict(
    num=2483, title='商店的最少代价', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='推导代价 = k + 2cnt − p · 一趟遍历',
    tags=['灵神题单', '动态规划', '难度分 1495'],
    code='''
class Solution(object):
    def bestClosingTime(self, customers):

        min_cnt = 0
        res = 0

        cnt = 0
        for index, c in enumerate(customers):
            if c == 'N':
                cnt += 1
            if cnt + cnt - (index + 1) < min_cnt:
                res = index + 1
                min_cnt = cnt + cnt - (index + 1)
        
        return res
''',
    call='Solution().bestClosingTime("YYNYNNYY")',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='customers', label='customers（粉 = N，绿 = Y；蓝框 = 刚越过分割线的字符）', h=200, pointers={'index': 'blue'},
             color=lambda S, i, v: ('pink' if v == 'N' else 'green') if 'index' in S and i <= S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='array', var=_fvals, label='2×cnt − p，p = 0, 1, 2, …（分割点 p 的相对代价，越小越好）', h=200,
             color=lambda S, i, v: 'orange' if 'res' in S and i == S['res'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'cyan'), ('min_cnt', 'min_cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'min_cnt = 0': '`min_cnt`：目前最小的 `2×cnt − p`，初始 0 对应 `p = 0`（全不开门）',
        'res = 0': '`res = 0`：先假设 0 点关门',
        'cnt = 0': '`cnt` 统计前缀里 `N` 的个数',
        'for index, c': lambda S, B, r: ('每个分割点都看完了' if S.index == B.get('index', -1) else f"往右看一个字符：`customers[{S.index}] = '{S.c}'`，分割点 `p = {S.index + 1}`"),
        "if c == 'N'": lambda S, B, r: ("是 `N`：它在左边（关门前的开门期）白开了一小时" if S.c == 'N' else "是 `Y`：`cnt` 不变（左边多一个 Y，右边就少一个 Y）"),
        'cnt += 1': '`cnt` → =={cnt}==',
        'if cnt + cnt': '`cnt + cnt − p = {cnt} + {cnt} − {index+1}` = {cnt+cnt-(index+1)}，和 `min_cnt = {min_cnt}` 比 → {"==更小=="  if cnt+cnt-(index+1) < min_cnt else "不更小，不动" + ("（==相等也不动==，保证最早）" if cnt+cnt-(index+1) == min_cnt else "")}',
        'res = index + 1': '`res = {res}`：在第 {res} 小时关门',
        'min_cnt = cnt': '`min_cnt` 更新为 =={min_cnt}==',
        'return res': '`2×cnt − p` 最小的分割点：关门时间 =={res}==',
    },
    cards=dict(
        one_liner='代价 = k + 2·cnt − p，k 是常数，只比较后两项',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`customers` 的 `Y` 表示该小时有顾客，`N` 表示没有',
                 '开门时无人到达 +1，关门时有人到达 +1；求代价最小的最早关门时间',
                 '本视频：`"YYNYNNYY"` → `2`'],
        quote='总的代价就是cnt[p] + k - (p - cnt[p]) = k + cnt[p] + cnt[p] - p，由于k是常量，实际上就是要找出使得cnt[p] + cnt[p] - p最小的p。',
        quote_src='—— yiduobo 题解原文',
        idea=['常规做法：正反两趟预处理前缀 `N`、后缀 `Y` 的个数，再枚举分割点',
              '设 `Y` 共 `k` 个，前缀 `N` 有 `cnt` 个 → 前缀 `Y` 有 `p − cnt` 个，后缀 `Y` 有 `k − (p − cnt)` 个',
              '代价化简成 `k + 2cnt − p`，边遍历边维护 `cnt`，不需要额外空间'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`min_cnt` 初始 0 对应 `p = 0`；更新用严格 `<`，相等保留更早的时间',
                 '`res = index + 1`：分割点 `p` 是字符 `index` 右边那条线',
                 '对比灵神：灵神把 `N` 记 +1、`Y` 记 −1，等价于这里的 `2cnt − p`',
                 '原文代码无需改动，已是 Python 3 可运行'],
    ),
)
