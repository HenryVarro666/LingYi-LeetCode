def _t(S):
    if 'res' not in S:
        return '先反转 `n` 得到 `r`，再逐个检查区间里的数是不是质数'
    if 'flag' in S and 'v' in S and 'x' in S:
        return f"检查 `v = {S['v']}`：试除 `x = {S['x']}`，`x×x = {S['x'] * S['x']}` " + ('`≤ v`' if S['x'] * S['x'] <= S['v'] else '`> v`') + f"；已累计质数和 `res = {S['res']}`"
    return f"已累计质数和 `res = {S['res']}`"


CONFIG = dict(
    num=3918, title='数与其逆序数之间的质数和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='数位反转 + 区间试除判质数',
    tags=['灵神题单·数学算法', '数学算法', '难度分 1301'],
    code='''
class Solution(object):
    def sumOfPrimesInRange(self, n):
        
        r = 0
        x = n
        while x:
            r = r * 10 + x % 10
            x //= 10

        res = 0
        for v in range(min(r, n), max(r, n) + 1):
            if v == 1:
                continue
            
            x = 2
            flag = True
            while x * x <= v:
                if v % x == 0:
                    flag = False
                    break
                
                x += 1
            
            if flag:
                res += v
        
        return res
''',
    call='Solution().sumOfPrimesInRange(10)',
    expect=17,
    views=[
        dict(type='array', var=lambda S: list(range(min(S['r'], S['n']), max(S['r'], S['n']) + 1)) if 'res' in S else [],
             label='区间 [min(n, r), max(n, r)]', h=190, cell=80, pointers={},
             color=lambda S, i, v: 'green' if v == S.get('v') and S.get('flag') and S.get('x', 0) * S.get('x', 0) > v else ('pink' if v == S.get('v') else None),
             dim=lambda S, i, v: 'v' in S and v < S['v']),
        dict(type='text', size=28, h=120, fn=_t),
    ],
    watch=[('n', 'n', 'blue'), ('r', 'r', 'pink'), ('v', 'v', 'cyan'), ('x', 'x', 'orange'), ('flag', 'flag'), ('res', 'res', 'green')],
    max_steps=90,
    captions={
        'r = 0': '`r` 用来拼反转后的数',
        'x = n': '`x` 拆 `n` 的数位，不动 `n`',
        'while x:': lambda S, B, r: (f'`x = {S.x}`，非 0，还有数位' if S.x else '`x = 0`，数位拆完'),
        'r = r * 10': '取个位 `{x % 10}` 接到 `r` 末尾：`{B.r} × 10 + {x % 10}` = =={r}==',
        'x //= 10': '去掉个位：`x` → {x}',
        'res = 0': '`res` 累计区间内的质数和',
        'for v in range': '检查 `v = {v}`，区间是 `[{min(r, n)}, {max(r, n)}]`',
        'if v == 1': lambda S, B, r: ('`v == 1`：1 ==不是质数==，跳过' if S.v == 1 else f'`v = {S.v} ≠ 1`，继续判断'),
        'continue': '跳过，看下一个数',
        'x = 2': '从 `x = 2` 开始试除',
        'flag = True': '先假设 `{v}` 是质数',
        'while x * x <= v': lambda S, B, r: (f'`x×x = {S.x*S.x} ≤ {S.v}`：还要试' if S.x * S.x <= S.v else f'`x×x = {S.x*S.x} > {S.v}`：试完了，没有因数'),
        'if v % x == 0': lambda S, B, r: (f'`{S.v} % {S.x} == 0`：有因数 `{S.x}`，是合数' if S.v % S.x == 0 else f'`{S.v} % {S.x} = {S.v % S.x}`，不整除'),
        'flag = False': '`{v}` 是合数，`flag = False`',
        'break': '已经确定是合数，退出',
        'x += 1': '换下一个除数 `x = {x}`',
        'if flag': lambda S, B, r: (f'`{S.v}` 是质数 → 累加' if S.flag else f'`{S.v}` 是合数 → 不加'),
        'res += v': '`res` += `{v}` → =={res}==',
        'return res': '区间 `[{min(r, n)}, {max(r, n)}]` 的质数和为 =={res}==',
    },
    cards=dict(
        one_liner='先反转出 r，再对区间里每个数试除判质数',
        complexity='时间 `O(m√M)`（m 为区间长度），空间 `O(1)`',
        problem=['`r` 是把 `n` 的数字反转后的整数',
                 '求 `min(n, r)` 到 `max(n, r)` 之间所有==质数的和==',
                 '示例：`n = 13` → `132`；`n = 8` → `0`',
                 '本视频：`n = 10`，`r = 1`，区间 `[1, 10]` → `17`'],
        quote='通过模10除以10的方式将n的数位分离出来，在分离的过程中通过乘以10再加上当前位的方式计算得到r。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x % 10` 取个位，`x //= 10` 去掉个位，同时 `r = r*10 + 个位`',
              '区间不大（`n <= 1000`），不用筛，逐个 `v` 试除',
              '试除到 `x*x <= v`；`1` 要单独跳过'],
        summary=['时间 `O(m√M)`，`n <= 1000` 足够快',
                 '易错点：==`v == 1` 要跳过==，否则 1 会被当质数',
                 '易错点：`r` 可能小于 `n`，所以用 `min/max` 确定区间',
                 '对比灵神：灵神筛法 + 前缀和，一次查询 `O(1)`；yiduobo 每次现场试除'],
    ),
)
