def _txt(S):
    line = S.get('_line', 0)
    if 'res' in S and line >= 18:
        return f"累计最小公倍数 `res = {S['res']}`" + (f"　正在算 `gcd({S['x']}, {S['y']})`" if 'x' in S and line >= 20 else '')
    if 'num' in S:
        return f"从位置 `{S['num']}` 出发，每次翻倍落到新位置，数了 `step = {S.get('step', 0)}` 步"
    return ''


CONFIG = dict(
    num=1806, title='还原排列的最少操作步数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='置换环 · 步长取最小公倍数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def reinitializePermutation(self, n):

        step_list = []
        used = [False] * n
        for num in range(n):
            if not used[num]:
                step = 0
                now = num
                while not used[now]:
                    used[now] = True
                    step += 1
                    now += now
                    if now >= n:
                        now = now - n + 1
                    

                step_list.append(step)
                
        res = 1
        for step in step_list:
            x, y = res, step
            while x:
                x, y = y % x, x
            
            res = res * step // y
        
        return res
''',
    call='Solution().reinitializePermutation(6)',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var=lambda S: list(range(S['n'])), label='位置 0 ~ n-1（绿 = 已属于某个环）', pointers={'now': 'blue'}, h=230, cell=80,
             color=lambda S, i, v: 'green' if 'used' in S and S['used'][i] and i != S.get('now') else None),
        dict(type='array', var=lambda S: list(S.get('step_list', [])), label='step_list：每个环走回原位的步数', h=190, cell=80),
    ],
    watch=['n', ('num', 'num', 'blue'), ('now', 'now', 'pink'), 'step', ('res', 'res', 'green')],
    captions={
        'step_list = []': '`step_list` 收集每个环的长度（走回原位要几步）',
        'used = [False]': '`used[i]` 标记位置 `i` 是否已经算进某个环',
        'for num in range': lambda S, B, r: ('所有位置都检查完了 → 得到 `step_list`' if all(S.used) else f'检查位置 `num = {S.num}`'),
        'if not used[num]': lambda S, B, r: (f'`used[{S.num}]` 还是 False → 这个位置没在已知的环里，新开一个环' if not S.used[S.num] else f'`used[{S.num}]` 已是 True → 它在前面某个环里，跳过'),
        'step = 0': '新环从 `{num}` 出发，步数清零',
        'now = num': '`now` 记当前走到的位置：`now = {now}`',
        'while not used[now]': lambda S, B, r: (f'`now = {S.now}` 还没走过 → 继续走' if not S.used[S.now] else f'`now = {S.now}` 已走过 → 回到起点，环走完了，长度 `step = {S.step}`'),
        'now += now': '位置 `{B.now}` 标记为已走过，走了 `{step}` 步；下一位置翻倍：`{now}`',
        'now = now - n + 1': '超出范围 `>= n`，按 `2*now mod (n-1)` 绕回 → `now = {now}`',
        'step_list.append': '记下这个环的长度 `{step}` → `step_list = {step_list}`',
        'res = 1': '所有位置都回原位，需要步数的最小公倍数：`res` 从 1 开始',
        'for step in step_list': '依次处理 `step_list` 里的环长：`step = {step}`，当前 `res = {res}`',
        'x, y = res, step': '求 `gcd({x}, {y})`：`x = {x}`，`y = {y}`',
        'while x': lambda S, B, r: (f'`x = {S.x}` 不为 0 → 继续辗转相除' if S.x else f'`x = 0` → `y = {S.y}` 就是最大公约数'),
        'x, y = y % x, x': '辗转相除：`x = {x}`，`y = {y}`',
        'res = res * step': '`lcm = res * step // gcd = {B.res} * {step} // {y}` = =={res}==',
        'return res': '所有环同时回到原位要 =={res}== 步',
    },
    skip=['used[now] = True', 'step += 1'],
    max_steps=100,
    cards=dict(
        one_liner='每个数的下一个位置固定，拆成环，答案是各环长度的最小公倍数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['偶数 `n`，初始排列 `perm[i] = i`；每次操作按固定规则重排，每个位置的数去哪由位置决定',
                 '求最少操作几次才能变回初始排列',
                 '示例：`n=2 → 1`，`n=4 → 2`，`n=6 → 4`；本视频用 `n=6`（答案 4）'],
        quote='由于题目中每个位置的下一个目标位置都是恒定的，那么对于排列中任意位置上的数而言，其在变换若干步之后必然会走回原来的位置',
        quote_src='—— yiduobo 题解原文',
        idea=['位置 `now` 一步后到 `2*now`，超过 `n-1` 就绕回：把位置连成若干个环',
              '同一个环里的数同时走回原位，用 `used` 保证每个位置只走一次，总共 `O(n)`',
              '所有环都回到原位的最少步数 = 各环长度的最小公倍数，用 gcd 求'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`now >= n` 时 `now - n + 1`，而不是 `now - n`：位置 `n-1` 固定不动',
                 '求 lcm 要先除后乘或用 `//`：`res * step // gcd`',
                 '原文为 Python 2 写法，最后的整数除法 `/` 已改为 `//`',
                 '位置 0 和 `n-1` 各自成环，长度为 1，不影响 lcm'],
    ),
)
