CONFIG = dict(
    num='LCP 20', title='快速公交', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='记忆化搜索 · 只考虑最近的两个上车点',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def busRapidTransit(self, target, inc, dec, jump, cost):

        f = {}
        f[1] = inc
        mod = 10 ** 9 + 7

        def dfs(f, now):
            if now in f:
                return f[now]
            
            f[now] = inc * now
            for index in range(len(jump)):
                if now % jump[index] == 0:
                    f[now] = min(f[now], dfs(f, now // jump[index]) + cost[index])
                else:
                    left_pos = now // jump[index] * jump[index]
                    f[now] = min(f[now], dfs(f, now // jump[index]) + cost[index] + inc * (now - left_pos))
                    right_pos = (now // jump[index] + 1) * jump[index]
                    f[now] = min(f[now], dfs(f, now // jump[index] + 1) + cost[index] + dec * (right_pos - now))
            
            return f[now]

        return dfs(f, target) % mod
''',
    call='Solution().busRapidTransit(31, 5, 3, [6], [10])',
    expect=33,
    views=[
        dict(type='text', h=70, fn=lambda S: (
            f"目标 `{S['now']}`：全程走路 = `{S['now']} × {S['inc']}` = =={S['now'] * S['inc']}==" if 'now' in S and 'jump' in S else
            '`f[x]` = 到达位置 x 的最小花销')),
        dict(type='map', var='f', label='f（记忆化：位置 → 最小花销）', h=330),
        dict(type='calls', h=330, hide=('f',)),
    ],
    watch=[('now', 'now', 'blue'), ('inc', 'inc'), ('dec', 'dec'), ('f[now]', "f.get(now)", 'green')],
    captions={
        'f[1] = inc': '位置 1 只能走路过去：`f[1] = inc = {inc}`，当作递归边界',
        'if now in f': lambda S, B, r: (f'`{S.now}` 已经在 `f` 里了 → 直接返回，==记忆化省掉重复状态==' if S.now in S.f
                                        else f'`f` 里还没有 `{S.now}` → 要算'),
        'f[now] = inc * now': '先假设==头铁全程走路==：`f[{now}] = {inc} × {now}` = =={f[now]}==',
        'if now % jump[index] == 0': lambda S, B, r: (
            f'`{S.now} % {S.jump[S.index]} == 0` → 刚好能坐车到 `{S.now}`，起点只有 `{S.now // S.jump[S.index]}`' if S.now % S.jump[S.index] == 0
            else f'`{S.now} % {S.jump[S.index]} != 0` → 起点只可能是 `{S.now // S.jump[S.index]}`（走过来）或 `{S.now // S.jump[S.index] + 1}`（走回来）'),
        'for index in range': '枚举每一班车（`jump = {jump}`），看它能不能帮 `f[now]` 变小',
        'left_pos =': '坐车落在 `{left_pos}`（不超过 `{now}` 的最近落点），还要往前走 `{now - left_pos}` 步',
        'right_pos =': '起点加 1 坐车落在 `{right_pos}`（越过 `{now}`），要往回走 `{right_pos - now}` 步',
        'return f[now]': lambda S, B, r: (f'命中缓存：`f[{S.now}] = {S.f[S.now]}` 直接返回' if S['_line'] == 10 else
                                         f'`f[{S.now}]` 算完 = =={S.f[S.now]}==：全程走路与每班车两个起点方案中最小的，返回上一层'),
    },
    cards=dict(
        one_liner='坐车前后最多各走几步：只看最近的两个起点',
        complexity='时间约 `O(m log target)`（m 为班次数），空间同量级',
        problem=['从位置 0 出发去 `target`：走路前进 1 花 `inc`，后退 1 花 `dec`',
                 '第 `i` 班车从 `x` 直达 `x × jump[i]`，花 `cost[i]`，最后结果对 `10^9+7` 取模',
                 '示例：`target=31, inc=5, dec=3, jump=[6], cost=[10]` → `33`'],
        quote='坐车后紧挨着的走路次数不会大于等于 jump[i]，因为完全可以在坐车前走路，利用坐车乘以 jump[i] 来放大这次走路',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[x]` = 到 x 的最小花销，状态太大不能全存，只能从转移里找优化',
              '坐车前先走比坐车后走划算 → 每班车只需考虑 `x // jump` 和 `x // jump + 1`',
              'x 每次除以 jump 指数级变小，状态很少 → 字典 + 记忆化搜索'],
        summary=['时间约 `O(m log target)`，空间同量级',
                 '每班车两个起点：向下取整（再走过去）、向上取整（坐过站再退回）',
                 '`f[now] = inc * now` 作为初值，保证全程走路的方案不丢',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '取模只在最后做：中间取模会影响比较大小'],
    ),
)
