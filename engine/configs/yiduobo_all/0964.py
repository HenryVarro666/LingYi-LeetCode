def _t1(S, B, r):
    pw = S.power[S.p]
    return (f'最大的 `x^p ≤ {S.now}` 是 `{pw[0]}`（p={S.p}）：全用它凑，`t1 = {S.now} // {pw[0]}` = =={S.t1}== 个；'
            f'每个代价 `{pw[1] + 1}`，余下 `{S.now} % {pw[0]}` = {S.now % pw[0]}')


def _t2(S, B, r):
    pw, up = S.power[S.p], S.power[S.p + 1]
    return (f'或者多凑到更大的 `{up[0]}` 再往回减：`t2 = ({up[0]} − {S.now}) // {pw[0]}` = =={S.t2}== 个 `{pw[0]}`，'
            f'再加一个 `{up[0]}`，余下 `({up[0]} − {S.now}) % {pw[0]}` = {(up[0] - S.now) % pw[0]}')


CONFIG = dict(
    num=964, title='表示数字的最少运算符', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='x 进制拆位 · 字典记忆化 DP',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def leastOpsExpressTarget(self, x, target):

        if target == 1:
            return 1

        power = [[1, 1], [x, 0]]
        while power[-1][0] < target:
            power.append([power[-1][0] * x, power[-1][1] + 1])
        
        f = {0 : 0}
        for x, cnt in power:
            f[x] = cnt + 1
            
        return self.dfs(target, power, f) - 1
    
    def dfs(self, now, power, f):
        if now not in f:
            p = len(power) - 1
            while power[p][0] > now:
                p -= 1
            
            t1 = now // power[p][0]
            f[now] = t1 * (power[p][1] + 1) + self.dfs(now % power[p][0], power, f)

            t2 = (power[p + 1][0] - now) // power[p][0]
            f[now] = min(f[now], t2 * (power[p][1] + 1) + power[p + 1][1] + 1 + self.dfs((power[p + 1][0] - now) % power[p][0], power, f))
        
        return f[now]
''',
    call='Solution().leastOpsExpressTarget(3, 19)',
    expect=5,
    views=[
        dict(type='grid', var='power', label='power：[x^k, w]（w = 乘号数，凑一个的代价 = w+1）', cell=62, h=230,
             cols=['x^k', 'w']),
        dict(type='map', var='f', label='f：凑出某个数的最小代价（含第一个符号，最后 −1）', h=190, font=24),
        dict(type='calls', h=190, hide=('power', 'f')),
    ],
    watch=['now', 'p', 't1', 't2'],
    captions={
        'if target == 1': '`target = 1` 只能写 `x / x`，两个运算符，特判返回 1',
        'power = [[1, 1]': '`power` 存 `[x^k, 运算符数]`：`x^0 = x/x` 要 2 个符号（记 1+1），`x^1 = x` 要 1 个（记 0+1），`x^k` 要 `k` 个乘号',
        'while power[-1][0] < target': lambda S, B, r: f'`{S.power[-1][0]} < {S.target}`：继续造更大的幂' if S.power[-1][0] < S.target else f'`{S.power[-1][0]} ≥ {S.target}`：够大了，停',
        'power.append': '追加 `x^{len(power)-1} = {power[-1][0]}`，乘号数 `{power[-1][1]}`',
        'f = {0': '`f[v]`：凑出 `v` 的最小代价。`f[0] = 0`',
        'f[x] = cnt + 1': '`f[{x}] = {cnt} + 1` = {f[x]}：一个幂的代价 = 乘号数 + 前面的 `+`/`−` 一个',
        'return self.dfs(target': '`dfs(target)` 的结果包含了第一个符号，真正的表达式开头不需要，所以 ==最后减 1==',
        'if now not in f': lambda S, B, r: (f'`{S.now}` 没算过 → 往下分情况算' if S.now not in S.f else f'`{S.now}` 已有结果 `f = {S.f[S.now]}` → 直接用（记忆化）'),
        'p = len(power) - 1': '从最大的幂开始找，p 要满足 `x^p ≤ now`',
        'while power[p][0] > now': lambda S, B, r: (f'`{S.power[S.p][0]} > {S.now}` → 太大，`p` 往小退' if S.power[S.p][0] > S.now else f'`{S.power[S.p][0]} ≤ {S.now}`：找到 `p = {S.p}`'),
        'p -= 1': '`p` → {p}',
        't1 = now': _t1,
        'f[now] = t1': lambda S, B, r: f'方案一：`{B.t1} × {B.power[B.p][1] + 1}` = {B.t1 * (B.power[B.p][1] + 1)}，再加上余数 `{B.now % B.power[B.p][0]}` 的最小代价（递归求）',
        't2 = (power': _t2,
        'f[now] = min': lambda S, B, r: f'方案二：`{B.t2} × {B.power[B.p][1] + 1} + {B.power[B.p + 1][1] + 1}` = {B.t2 * (B.power[B.p][1] + 1) + B.power[B.p + 1][1] + 1}，再加余数 `{(B.power[B.p + 1][0] - B.now) % B.power[B.p][0]}` 的最小代价，和方案一取小',
        'return f[now]': '`{now}` 的最小代价 `f[{now}]` = =={f[now]}==',
    },
    skip=['p -= 1'],
    max_steps=70,
    cards=dict(
        one_liner='除号只用来造 1，其余全是 +/−，按 x 进制逐位凑',
        complexity='时间 `O(log^2 target)`，空间 `O(log target)`',
        problem=['只用 `+ − × ÷` 和数字 `x` 写一个表达式，值为 `target`，不能加括号',
                 '乘除先于加减，求最少用多少个运算符',
                 '示例：`x=3, target=19` → `5`（`3*3 + 3*3 + 3/3`）'],
        quote='注意到target为整数，那么这里除法的唯一作用就是通过x / x来得到1，那么此时问题就转化成了使用加法和减法，通过1、x、x^2、...、x^p来组成target的最小代价是什么。',
        quote_src='—— yiduobo 题解',
        idea=['`1` 代价 2（`x/x` 加一个符号），`x^k` 代价 `k`（`k−1` 个乘号加一个符号）',
              '设 `x^p ≤ target`：要么用 `t1` 个 `x^p` 逼近再补余数，要么冲到 `x^(p+1)` 再减回来',
              '每一轮 `target` 少一位 x 进制数，状态很少，用字典记忆化即可'],
        summary=['时间约 `O(log^2 target)`，状态数随 x 进制位数递减',
                 '最后要 `−1`：第一项前面不需要 `+`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（共 2 处）',
                 '易错：`for x, cnt in power` 把参数 x 覆盖了，但此后只用幂值，不影响结果'],
    ),
)
