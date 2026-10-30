def _rep(S):
    if 'x' not in S:
        return ''
    i = S.get('i')
    if i is None:
        return f"从 `1` 开始，余数 `x = 1 % k = {S['x']}`"
    return f"全 1 数共 =={i}== 位：`{'1' * i}`，它模 {S['k']} 的余数 `x` = =={S['x']}=="


CONFIG = dict(
    num=1015, title='可被 K 整除的最小整数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='迭代模运算 + 先排除 2、5 的倍数',
    tags=['数学算法', '链表、二叉树与回溯'],
    code='''
class Solution:
    def smallestRepunitDivByK(self, k: int) -> int:
        if k % 2 == 0 or k % 5 == 0:
            return -1
        x = 1 % k
        for i in count(1):  # 一定有解
            if x == 0:
                return i
            x = (x * 10 + 1) % k
''',
    setup='from itertools import count',
    call='Solution().smallestRepunitDivByK(7)',
    expect=6,
    views=[
        dict(type='text', fn=_rep, size=34, h=110),
        dict(type='text', fn=lambda S: (f"下一步：`x = ({S['x']} * 10 + 1) % {S['k']}`" if 'x' in S else ''), h=80),
    ],
    watch=['k', ('i', 'i', 'blue'), ('x', 'x', 'yellow')],
    captions={
        'k % 2 == 0': lambda S, B, r: (f'`k = {S.k}` 是 2 或 5 的倍数 → 全 1 数个位是 1，永远整除不了 → 返回 -1' if S.k % 2 == 0 or S.k % 5 == 0
                                       else f'`{S.k}` 不是 2 或 5 的倍数 → ==一定有解==（余数序列必会回到 0），继续'),
        'x = 1 % k': '第 1 个全 1 数是 `1`，余数 `x = 1 % {k} = {x}`（`k=1` 时就是 0，所以要写 `1 % k`）',
        'for i in count': '`i = {i}`：当前全 1 数有 `{i}` 位',
        'if x == 0': lambda S, B, r: (f'`x = 0` → {S.i} 位的全 1 数能被 {S.k} 整除 → 找到答案' if S.x == 0
                                      else f'`x = {S.x} != 0` → {S.i} 位的全 1 数还不行，加一位'),
        'x = (x * 10 + 1)': '末尾添一个 1：`n * 10 + 1`；只保留余数：`({B.x} * 10 + 1) % {k}` = =={x}==',
        'return i': '`x == 0`：返回位数 =={i}==',
    },
    cards=dict(
        one_liner='全 1 数一位位往后长，只记它模 k 的余数',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['找最小的、只含数字 `1` 的正整数 `n`，使它能被 `k` 整除，返回 `n` 的位数',
                 '不存在就返回 `-1`；`n` 可能超过 64 位',
                 '示例：`k=3` → `3`（`111`）；`k=2` → `-1`；本视频用 `k=7` → `6`'],
        quote='(a·b) mod m = ((a mod m)·(b mod m)) mod m ……每次循环计算出新的 x 后，把 x 替换成 x mod k。',
        quote_src='—— 灵茶山艾府题解（模运算前置知识）',
        idea=['`n` 后面添一个 1 得到 `n*10+1`，余数同样按 `(x*10+1) % k` 递推',
              '`k` 是 2 或 5 的倍数时，全 1 数个位是 1 不可能整除 → 直接 -1',
              '否则余数序列不会进入不含 0 的环，一定有解，不用 set 判重，空间 `O(1)`'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '易错点：初值写 `1 % k`，而不是 `1`（`k = 1` 时答案是 1）',
                 '算法一用 set 记录出现过的余数，出现重复就说明无解；算法二先排除 2、5 的倍数，免去 set',
                 '算法三用欧拉函数枚举 `phi(9k)` 的因子，时间 `O(sqrt(k) log k)`',
                 '`count` 是 itertools.count（已注入）'],
    ),
)
