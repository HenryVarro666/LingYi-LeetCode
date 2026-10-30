def _st(S):
    s = S['_inner']
    if 'wait1' not in s:
        return '`dfs(i, wait1, fuel0, fuel1)`：车 `i` 到来时，两台加油机的状态'
    i = s['i']
    d = S['demand']
    wait0 = d[i - 1] if i else 0
    return (f'车 `{i}`：加油机 0 再等 ==`{wait0}`== 秒空闲、剩余燃料 `{s["fuel0"]}`；'
            f'加油机 1 再等 ==`{s["wait1"]}`== 秒空闲、剩余燃料 `{s["fuel1"]}`')


def _I(S):
    return S['_inner'].get('i')


CONFIG = dict(
    num=4009, title='最小化最大可能等待时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多维 DP · 记忆化搜索 + 状态优化',
    tags=['其他线性 DP', '多维 DP', '难度分 2499'],
    code='''
class Solution:
    def minMaxWaitingTime(self, demand: list[int], fuel: list[int]) -> int:
        @cache
        def dfs(i: int, wait1: int, fuel0: int, fuel1: int) -> tuple[int, int]:
            if i == len(demand):
                return 0, 0

            res = (0, 0)  # (-最大服务车辆数, 最大等待时间的最小值)
            wait0 = demand[i - 1] if i else 0
            d = demand[i]

            # 跟在车 i-1 后面加油
            if d <= fuel0:
                num, wait = dfs(i + 1, max(wait1 - wait0, 0), fuel0 - d, fuel1)
                res = (num - 1, max(wait, wait0))

            # 不跟在车 i-1 后面加油
            if d <= fuel1:
                num, wait = dfs(i + 1, max(wait0 - wait1, 0), fuel1 - d, fuel0)  # 注意这里交换了 fuel0 和 fuel1
                res = min(res, (num - 1, max(wait, wait1)))

            return res

        max_num, best_wait = dfs(0, 0, fuel[0], fuel[1])
        return best_wait if max_num else -1
''',
    call='Solution().minMaxWaitingTime([3, 2, 4], [5, 6])',
    expect=2,
    views=[
        dict(type='array', var='demand', label='demand（蓝 = 当前要加油的车 i）', cell=84, h=200,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, k, v: 'blue' if k == _I(S) else None,
             dim=lambda S, k, v: _I(S) is not None and k < _I(S)),
        dict(type='text', fn=_st, size=24, h=110),
        dict(type='calls', h=300),
    ],
    watch=[('i', _I, 'blue'), ('wait1', lambda S: S['_inner'].get('wait1'), 'pink'),
           ('fuel0', lambda S: S['_inner'].get('fuel0'), 'cyan'), ('fuel1', lambda S: S['_inner'].get('fuel1'), 'orange'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=['d = demand[i]', 'res = (0, 0)', 'wait0 = demand', 'return 0, 0'],
    captions={
        'if i == len(demand)': lambda S, B, ret: ('`i == n`：车都处理完 → 返回 `(0, 0)`' if S.i == len(S.demand)
                                                   else f'安排车 `{S.i}`'),
        'res = (0, 0)': '`res` 记成 `(-服务车数, 最大等待)`：用元组比较，==先比车数（越多越小）再比等待时间==',
        'wait0 = demand': '车 `i-1` 刚开始加油，占着它的机器 `demand[i-1]` 秒 → ==`wait0 = {wait0}`==',
        'if d <= fuel0': '车 i-1 占着机器 `{wait0}` 秒；`d = {d}`，机器剩余 `{fuel0}`：`{d} <= {fuel0}` → {"够，可以跟在车 i-1 后面" if d <= fuel0 else "不够，这条路走不通"}',
        'dfs(i + 1, max(wait1 - wait0': '车 `i` 等 `{wait0}` 秒后上机；另一台的等待缩短 → `wait1 = max({wait1}-{wait0}, 0)`',
        'res = (num - 1': '子问题多服务 `{-num}` 辆，加上车 `i` 共 `{-res[0]}` 辆；最大等待 `max({wait}, {wait0}) = {res[1]}`',
        'if d <= fuel1': '`d = {d}`，另一台加油机剩余 `{fuel1}`：`{d} <= {fuel1}` → {"够，可以不跟在车 i-1 后面" if d <= fuel1 else "不够，不能走这边"}',
        'dfs(i + 1, max(wait0 - wait1': '车 `i` 等 `{wait1}` 秒后上机 1；下一层==交换两台机器的角色==，刚加油的那台当“机 0”',
        'res = min(res': '两种选择取元组最小：`res = {res}` → 服务 `{-res[0]}` 辆、最大等待 `{res[1]}`',
        'return res': lambda S, B, ret: f'`dfs` 返回 `{ret}`：最多服务 `{-ret[0]}` 辆，最大等待最小为 `{ret[1]}`',
        'max_num, best_wait': '入口 `dfs(0, 0, fuel[0], fuel[1])`：车 0 不用等，两台机器都空闲',
        'return best_wait if': '最多服务 `{-max_num}` 辆（非 0）→ 答案是 `best_wait = {best_wait}`；一辆都服务不了才返回 -1',
    },
    max_steps=120,
    cards=dict(
        one_liner='记忆化搜索：车 i 跟在 i-1 后面，还是去另一台机器',
        complexity='时间 `O(nUF)`，空间 `O(nUF)`',
        problem=['`demand[i]` 是第 `i` 辆车要的燃料，两台加油机各有初始燃料 `fuel[j]`，车按下标顺序被允许加油',
                 '先==最大化服务车辆数==，再让这些车里的==最大等待时间最小==；服务不了任何车返回 -1',
                 '示例：`demand=[6,8,4,6,5], fuel=[16,13]` → `6`',
                 '本视频：`demand=[3,2,4], fuel=[5,6]` → `2`'],
        quote='由于其中一个 wait_i 始终是 d，所以只需要保留另一个 wait_i。',
        quote_src='—— 灵茶山艾府题解（状态优化）',
        idea=['朴素状态 `dfs(i, wait0, wait1, fuel0, fuel1)`：车 i 选机 0 或机 1，选哪台就要等那台的 wait 秒',
              '车 `i-1` 刚上的那台机器要忙 `demand[i-1]` 秒，所以 `wait0` 不用存，只存 `wait1`',
              '返回 `(-服务车数, 最大等待)`，用元组 `min` 同时满足“先多服务、再少等待”'],
        summary=['时间 = 状态数 `O(nUF)` × `O(1)`：`fuel1` 可由 `i` 和 `fuel0` 推出，所以实际是三维',
                 '易错：选“不跟在 i-1 后面”时，递归要==交换 fuel0 和 fuel1==，让“机 0”永远是刚加油的那台',
                 '易错：最后 `max_num` 为 0 才返回 -1，而不是答案为 0',
                 '另一种写法：先求最多服务车数，再二分最大等待时间 + DFS 判定，本视频未演示'],
    ),
)
