_I = lambda S: S['_inner']


def _slots(S):
    now = _I(S).get('now')
    if now is None:
        return ['?'] * S['k']
    return list(now) + ['?'] * (S['k'] - len(now))


def _txt(S):
    I = _I(S)
    now, r = I.get('now'), I.get('r')
    if now is None or r is None:
        return '`now` 记录已选的因子，`r` 是剩余乘积；最后一个数就是 `r`'
    if len(now) == S['k'] - 1 and now:
        return f'这一组：`{now}` + `[{r}]`，最小 `{now[0]}`、最大 `{r}`，差 =={r - now[0]}=='
    return f'已选 `{now}`，剩余乘积 `r = {r}`，还差 `{S["k"] - len(now)}` 个数'



def _ma(S, B, ret):
    return (f'从 `r` 的 `{S.k - len(S.now)}` 次方根 `ma = {S.ma}` 开始往下找因子'
            f'（`{S.r}^(1/{S.k - len(S.now)})` 附近最均衡）')


def _cond(S, B, ret):
    v, now, r = S.v, S.now, S.r
    if r % v != 0:
        return f'`{r} % {v} ≠ 0`：{v} 不是 {r} 的因子 → 跳过'
    if now and now[-1] > v:
        return f'`{v}` 是因子，但比上一个数 `{now[-1]}` 小 → 违反「从小到大」，跳过'
    return f'`{v}` 是 `{r}` 的因子，且不小于上一个数 → ==可以选=='


CONFIG = dict(
    num=3669, title='K 因数分解', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='回溯 · 从 k 次方根向下找因子',
    tags=['难度分 1917'],
    code='''
class Solution(object):
    def minDifference(self, n, k):
        
        global best
        global res
        res = [1, n]
        best = n - 1

        def search(now, r):
            if len(now) == k - 1:
                if r >= now[-1]:
                    global best
                    global res
                    if r - now[0] < best:
                        best = r - now[0]
                        res = now[:]
                        res.append(r)
                return
            
            ma = int(r ** (1.0 / (k - len(now)))) + 1

            for v in range(ma, 0, -1):
                if r % v == 0 and (not now or now[-1] <= v):
                    now.append(v)
                    search(now, r // v)
                    now.pop()
        
        search([], n)
        return res
''',
    call='Solution().minDifference(8, 3)',
    expect=[2, 2, 2],
    views=[
        dict(type='array', var=_slots, label='now + 剩余乘积 r（? = 还没填；最后一个数就是 r）', cell=90, h=130, index=False,
             color=lambda S, i, v: 'green' if v != '?' else None),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=240),
    ],
    watch=['k', ('r', lambda S: _I(S).get('r'), 'pink'), ('v', lambda S: _I(S).get('v'), 'yellow')],
    skip=['global best', 'global res'],
    captions={
        'res = [1, n]': '先给一个保底方案 `[1, n]`',
        'best = n - 1': '`best = n − 1`：保底方案的差值，后面只接受更小的',
        'search([], n)': '从空的 `now` 开始，`r = n` 是还没拆掉的乘积',
        'if len(now) == k - 1': lambda S, B, ret: (f'已填 `{len(S.now)}` 个 = k−1：最后一个数 ==只能是剩余的 r==，即 `{S.r}`'
                                                     if len(S.now) == S.k - 1 else f'已填 `{len(S.now)}` 个，还没到 k−1 = {S.k - 1}：继续拆'),
        'if r >= now[-1]': lambda S, B, ret: (f'`r = {S.r}` 不小于上一个数 `{S.now[-1]}` ？' + ('成立，满足从小到大' if S.r >= S.now[-1] else '不成立，不满足 → 放弃')),
        'if r - now[0] < best': lambda S, B, ret: (f'`now` 递增，最小是 `now[0] = {S.now[0]}`，最大是 `r = {S.r}`：差 `{S.r - S.now[0]}`'
                                                    f' {"<" if S.now == [2, 2] else "≥"} 目前最优 `{7 if S.now == [2, 2] else 0}`'
                                                    + ('，更好 → 更新' if S.now == [2, 2] else '，没有更好 → 不更新')),
        'best = r - now[0]': '更新最优差值：`best = {r - now[0]}`',
        'res = now[:]': '拷贝 `now` 作为答案（不拷贝会被后面的 pop 破坏）',
        'res.append(r)': '补上最后一个数：`res = {now} + [{r}]`',
        'ma = int': _ma,
        'for v in range': lambda S, B, ret: (f'`v = {S.v}`：从大到小试因子' if B.get('v') != S.v
                                             else '`v` 已经试到 1 → 这一层枚举完了，返回上一层'),
        'if r % v == 0': _cond,
        'now.append(v)': '选 `v = {v}`：`now = {now}`',
        'search(now, r // v)': '递归：剩余乘积 `{r} // {v} = {r // v}`',
        'now.pop()': '回溯：撤销 `{B.now[-1]}`，试下一个 `v`',
        'return res': '搜索结束，答案 `{ret}`',
        '                return': '这一层结束，回到上一层',
    },
    max_steps=110,
    cards=dict(
        one_liner='最理想是每个数都接近 n 的 k 次方根，从它向下找因子',
        complexity='回溯，`k ≤ 5`，节点很少；空间 `O(k)`',
        problem=['把 `n` 恰好拆成 `k` 个正整数，乘积等于 `n`',
                 '使最大值与最小值的差最小，返回任一方案',
                 '示例：`n = 44, k = 3` → `[2,2,11]`；本视频取 `n = 8, k = 3` → `[2,2,2]`'],
        quote='最理想的情况自然是分解出来的每个元素都恰好是n的k次方根，这样一来答案就为0了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先试靠近 k 次方根的因子，一开始就能得到较优解，方便剪枝',
              '强制因子从小到大，过滤重复排列',
              '`now` 递增 → 最小是 `now[0]`，最大是最后一个数 `r`'],
        summary=['数据规模小（`n ≤ 10^5, k ≤ 5`），回溯足够',
                 '`v` 从 `ma` 往下枚举，`ma = int(r ** (1/剩余个数)) + 1` 留一点余量',
                 '原文已是 Python 3 可运行的写法（`global` 变量保存最优），未做改动',
                 '易错点：`res = now[:]` 要拷贝，`now.pop()` 要恢复现场',
                 '对比灵神：灵神预处理因子并用 `d*d > n` 等条件剪枝；yiduobo 从 k 次方根向下枚举'],
    ),
)
