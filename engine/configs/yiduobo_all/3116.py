def _cycle(S):
    t = S.get('tot_l')
    return list(range(0, t + 1)) if t else []


def _f_view(S):
    f = S.get('f') or []
    return [f'{l}{"+" if d > 0 else "−"}' for l, d in f]


def _info(S):
    line = S.get('_line', 0)
    if 'mid' in S and S.get('cnt') is not None and line >= 41:
        return f"`mid = {S['mid']}`：1..mid 里能凑出的金额有 ==`{S['cnt']}`== 个，目标是第 `k = {S['k']}` 个 → " + ('==够了，往左找==' if S['cnt'] >= S['k'] else '==不够，往右找==')
    if 'tot' in S and 'tot_l' in S:
        return f"一轮 `1..{S['tot_l']}` 里有 `tot = {S['tot']}` 个金额（容斥累加中）"
    return '金额每隔 `lcm` 重复一轮：先算一轮里有几个，再在最后一轮里二分'


CONFIG = dict(
    num=3116, title='单面值组合的第 K 小金额', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='lcm 周期 + 容斥 + 二分',
    tags=['数学算法', '难度分 2387'],
    code='''
class Solution(object):
    def findKthSmallest(self, coins, k):

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x
        
        def get_l(arr):
            l = arr[0]
            for v in arr[1:]:
                l = l * v // gcd(l, v)

            return l

        tot_l = get_l(coins)

        f = []
        for state in range(1, (1 << len(coins))):
            tmp = []
            for index, v in enumerate(coins):
                if state & (1 << index) == (1 << index):
                    tmp.append(v)
            
            if len(tmp) % 2 == 0:
                f.append([get_l(tmp), -1])
            else:
                f.append([get_l(tmp), 1])

        tot = 0
        for l, delta in f:
            tot += tot_l // l * delta

        res = k // tot * tot_l
        k %= tot

        if k > 0:
            left = 1
            right = tot_l - 1
            while left < right:
                mid = (left + right) // 2
                cnt = 0
                for l, delta in f:
                    cnt += mid // l * delta
                
                if cnt < k:
                    left = mid + 1
                else:
                    right = mid
        
            res += left
        
        return res
''',
    call='Solution().findKthSmallest([2, 3], 7)',
    expect=10,
    views=[
        dict(type='array', var='coins', label='coins', h=110, cell=60),
        dict(type='array', var=_f_view, label='f：每个子集的 [lcm, 符号]（+ 奇数种，− 偶数种）', h=130, cell=70),
        dict(type='array', var=_cycle, label='一轮循环 1..tot_l（绿 = 能凑出的金额，格子数字 = 下标）', h=210, cell=64,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'},
             color=lambda S, i, v: 'green' if v > 0 and any(v % x == 0 for x in S['coins']) else None,
             dim=lambda S, i, v: v == 0),
        dict(type='text', fn=_info, size=26, h=90),
    ],
    watch=['tot_l', 'tot', 'k', 'res', ('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', ('cnt', 'cnt', 'green')],
    skip=['for index, v in enumerate(coins)', 'tmp = []', 'while y', 'for v in arr[1:]', 'for l, delta in f', 'cnt = 0', 'if state &', 'tmp.append(v)', 'l = arr[0]', 'x, y = y'],
    captions={
        'tot_l = get_l(coins)': '所有面额的最小公倍数 `tot_l = {tot_l}`：金额每过 {tot_l} 就重复一轮',
        'f.append([get_l(tmp), -1])': '选了 `{tmp}`：偶数种 → 这些数的公倍数被多算了 → 记 ==−1==，`lcm = {f[-1][0]}`',
        'f.append([get_l(tmp), 1])': '选了 `{tmp}`：奇数种 → 记 ==+1==，`lcm = {f[-1][0]}`',
        'tot += tot_l // l * delta': '一轮里 `{l}` 的倍数有 `{tot_l // l}` 个，符号 {delta} → `tot` = {tot}',
        'res = k // tot * tot_l': '整整 `{k} // {tot} = {k // tot}` 轮：先把这些轮的金额跨度 `{k // tot} × {tot_l}` 记进 `res = {res}`',
        'k %= tot': '剩下的 `k = {k}`：第 {k} 个落在最后一轮里',
        'if k > 0': lambda S, B, r: ('`k > 0`：还要在最后一轮里二分找位置' if S.k > 0 else '`k = 0`：恰好是一整轮的最后一个，不用二分'),
        'left = 1': '二分范围：最后一轮 `[1, {tot_l - 1}]`',
        'mid = (left + right) // 2': '取中点 `mid = {mid}`',
        'cnt += mid // l * delta': lambda S, B, r: f"1..{S.mid} 里 `{S.l}` 的倍数 `{S.mid // S.l}` 个，符号 {'+' if S.delta > 0 else '−'}：`cnt` = =={S.cnt}==（容斥累加）",
        'if cnt < k': lambda S, B, r: (f'`cnt = {S.cnt} < k = {S.k}`：{S.mid} 还不够 → ==`left = mid + 1`==' if S.cnt < S.k
                                       else f'`cnt = {S.cnt} ≥ k = {S.k}`：够了，答案 ≤ {S.mid} → ==`right = mid`=='),
        'left = mid + 1': '`left` → {left}',
        'right = mid': '`right` → {right}',
        'res += left': '二分结束，最后一轮里的位置是 `left = {left}` → `res = {res}`',
        'return res': '第 k 小金额 = `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='金额按 lcm 一轮一轮重复，先数整轮，再在最后一轮里二分',
        complexity='时间 `O(n·2^n + 2^n·log lcm)`，空间 `O(2^n)`',
        problem=['面额互不相同的硬币，每次只能用同一种，金额是它的倍数',
                 '所有硬币能凑的金额合起来，求第 `k` 小',
                 '本视频：`coins=[2,3], k=7` → `10`（2,3,4,6,8,9,10）'],
        quote='以coin的两种面值2和5的最小公倍数10为界，各种组合在不断循环。',
        quote_src='—— yiduobo 题解原文',
        idea=['`tot_l` = 全部面额的 lcm：金额每过 `tot_l` 就重复一轮，一轮里有 `tot` 个',
              '`k // tot` 整轮直接跳过，余下 `k % tot` 在 `[1, tot_l-1]` 里二分',
              '数个数用容斥：奇数种硬币 +，偶数种 −；原文用二项式定理证明了这个符号'],
        summary=['时间 `O(n·2^n)` 预处理 f，每次二分 `O(2^n)`；空间 `O(2^n)`',
                 '`k % tot = 0` 时恰好是整轮的最后一个，答案就是 `k // tot * tot_l`',
                 '`tot_l` 最大是 lcm(1..25)，Python 大整数没有溢出问题',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神对整个值域二分，不删倍数前 lcm 也不会溢出；yiduobo 先利用周期把 k 压小'],
    ),
)
