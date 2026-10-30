def _tv(v):
    return {-1: '#', -2: '^', -3: '$'}.get(v, v)


def _top(S):
    if 'half_len' not in S:
        return '`t`：在 `s` 的每个数两侧插入 `-1`，首尾放哨兵 `-2`、`-3`，奇偶回文统一成奇回文'
    if 'pre' in S:
        return '`ans` = 各回文中心的 ==子数组和== 的最大值（前缀和差）'
    if 'i' not in S:
        return ''
    return f"当前中心 `t[{S['i']}]`；已知最右回文 `[{S['box_m']*2-S['box_r']+1}, {S['box_r']-1}]`，中心 `box_m = {S['box_m']}`，`box_r = {S['box_r']}`"


CONFIG = dict(
    num=3985, title='回文子数组求和', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='Manacher 算法 + 前缀和',
    tags=['灵神题单', '字符串', '难度分 2202'],
    code='''
class Solution:
    def getSum(self, s: List[int]) -> int:
        # Manacher 模板
        # 将 s 改造为 t，这样就不需要讨论 len(s) 的奇偶性，因为新串 t 的每个回文子串都是奇回文串（都有回文中心）
        # s 和 t 的下标转换关系：
        # (si+1)*2 = ti
        # ti/2-1 = si
        # ti 为偶数，对应奇回文串（从 2 开始）
        # ti 为奇数，对应偶回文串（从 3 开始）
        t = [-2]
        for x in s:
            t.append(-1)
            t.append(x)
        t.append(-1)
        t.append(-3)

        # 定义一个奇回文串的回文半径=(长度+1)/2，即保留回文中心，去掉一侧后的剩余字符串的长度
        # half_len[i] 表示在 t 上的以 t[i] 为回文中心的最长回文子串的回文半径
        # 即 [i-half_len[i]+1,i+half_len[i]-1] 是 t 上的一个回文子串
        half_len = [0] * (len(t) - 2)
        half_len[1] = 1
        # box_r 表示当前右边界下标最大的回文子串的右边界下标+1
        # box_m 为该回文子串的中心位置，二者的关系为 r=mid+half_len[mid]
        box_m = box_r = max_i = 0
        for i in range(2, len(half_len)):
            hl = 1
            if i < box_r:
                # 记 i 关于 box_m 的对称位置 i'=box_m*2-i
                # 若以 i' 为中心的最长回文子串范围超出了以 box_m 为中心的回文串的范围（即 i+half_len[i'] >= box_r）
                # 则 half_len[i] 应先初始化为已知的回文半径 box_r-i，然后再继续暴力匹配
                # 否则 half_len[i] 与 half_len[i'] 相等
                hl = min(half_len[box_m * 2 - i], box_r - i)

            # 暴力扩展
            # 算法的复杂度取决于这部分执行的次数
            # 由于扩展之后 box_r 必然会更新（右移），且扩展的的次数就是 box_r 右移的次数
            # 因此算法的复杂度 = O(len(t)) = O(n)
            while t[i - hl] == t[i + hl]:
                hl += 1
                box_m, box_r = i, i + hl

            half_len[i] = hl
            if hl > half_len[max_i]:
                max_i = i

        pre = list(accumulate(s, initial=0))
        ans = 0

        for i in range(2, len(half_len)):
            hl = half_len[i]
            # 注意 t 上的最长回文子串的最左边和最右边都是 -1
            # 所以要对应到 s，最长回文子串的下标是从 i-hl+2 到 i+hl-2
            # 结合上文的下标转换关系，得到其在 s 上的下标范围是从 (i-hl)/2 到 (i+hl)/2-2
            ans = max(ans, pre[(i + hl) // 2 - 1] - pre[(i - hl) // 2])
        return ans
''',
    call='Solution().getSum([3,1,3,2])',
    expect=7,
    skip=['t.append', 'half_len[1] = 1', 'for x in s', 'for i in range(2', 'if hl > half_len', 'max_i = i', 'hl = half_len[i]', 'half_len[i] = hl'],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='array', var='t', label='t（-1 = 分隔，-2/-3 = 哨兵）', cell=60, pointers={'i': 'blue', 'box_m': 'pink'}, h=190,
             color=lambda S, k, v: ('green' if 'i' in S and 'hl' in S and S['i'] - S['hl'] < k < S['i'] + S['hl'] else None)),
        dict(type='array', var='half_len', label='half_len（回文半径）', cell=60, pointers={'i': 'blue'}, h=170),
        dict(type='array', var='pre', label='pre（s 的前缀和）', cell=60, h=150),
    ],
    watch=[('i', 'i', 'blue'), ('hl', 'hl', 'cyan'), ('box_m', 'box_m', 'pink'), ('box_r', 'box_r', 'orange'), ('ans', 'ans', 'green')],
    captions={
        't.append(x)': '放入 `x = {x}`',
        'hl = 1': '`i = {i}`：回文半径至少是 1（自己）',
        'if i < box_r': lambda S, B, r: (f'`i = {S.i} < box_r = {S.box_r}`：`i` 落在已知回文 ==里面== → 能借对称点的结果' if S.i < S.box_r
                                         else f'`i = {S.i} >= box_r = {S.box_r}`：在已知回文 ==外面==，没有信息可借，只能暴力扩展'),
        'hl = min(': '对称点 `i\' = {box_m*2-i}`，半径 `{half_len[box_m*2-i]}`，但不能超出 `box_r - i = {box_r-i}` → 取小，`hl = {hl}`',
        'while t[i - hl]': lambda S, B, r: (f'`t[{S.i-S.hl}] = {S.t[S.i-S.hl]}` == `t[{S.i+S.hl}] = {S.t[S.i+S.hl]}` → ==能继续扩展=='
                                            if S.t[S.i-S.hl] == S.t[S.i+S.hl]
                                            else f'`t[{S.i-S.hl}] = {S.t[S.i-S.hl]}` ≠ `t[{S.i+S.hl}] = {S.t[S.i+S.hl]}` → 到边界了，停'),
        'hl += 1': '半径扩大：`hl = {hl}`',
        'box_m, box_r': '右边界超过了旧的 `box_r` → 更新 `box_m = {box_m}`，`box_r = {box_r}`（`box_r` 只会右移，所以总共 O(n)）',
        'pre = list': '前缀和：`pre[k]` = `s` 前 `k` 个数之和 = {pre}',
        'ans = 0': '`ans` 记录最大的回文子数组和',
        'ans = max': lambda S, B, r: (f'中心 `i = {S.i}`：`s` 下标 `{(S.i-S.hl)//2}` 到 `{(S.i+S.hl)//2-2}`，和 = `pre[{(S.i+S.hl)//2-1}] - pre[{(S.i-S.hl)//2}]` = `{S.pre[(S.i+S.hl)//2-1] - S.pre[(S.i-S.hl)//2]}`；`ans` = =={S.ans}=='),
        'return ans': '元素都为正，越长越好 → 每个中心取最长回文，答案 `{ans}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='元素都是正数：枚举回文中心，取最长回文，前缀和求和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，找一个==回文子数组==，使元素和最大',
                 '`nums[i] >= 1`，所以子数组越长和越大',
                 '本视频：`[3,1,3,2]` → `7`'],
        quote='本题 nums 中的数都是非负数，所以子数组越长越好。用 Manacher 算法，可以求出以 nums[i] 为回文中心（或者以 nums[i] 和 nums[i+1] 为回文中心）的最长回文子数组的范围。枚举回文中心，用前缀和计算子数组和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把 `s` 改造成 `t`（每个数两侧插 `-1`），奇偶长度的回文都变成奇回文',
              'Manacher：维护最右回文 `[box_m, box_r)`，新中心落在里面就借对称点的半径，再暴力扩展',
              '求出每个中心的 `half_len`，换算回 `s` 的下标范围，用前缀和相减'],
        summary=['时间 `O(n)`：`box_r` 只右移，暴力扩展总次数不超过 `len(t)`',
                 '易错：`t` 与 `s` 的下标换算，范围是 `(i-hl)/2` 到 `(i+hl)/2-2`',
                 '哨兵 `-2`、`-3` 互不相等又不等于任何数，扩展会自动停下',
                 '若有负数：只看右半边，在回文半径内找最大前缀和（ST 表 / 线段树，`O(n log n)`）'],
    ),
)
