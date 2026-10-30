def _wl(S):
    i = S.get('index')
    if i is None:
        return 0
    return i + 1


def _wr(S):
    i = S.get('index')
    if i is None:
        return S['k'] - 1
    return i + S['k']


def _txt(S):
    if 'now' not in S:
        return ''
    return f"当前频率分数 `now = {S['now']}`（每种数 x 贡献 x^出现次数）"


CONFIG = dict(
    num=2524, title='子数组的最大频率分数', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='定长窗口 · 哈希表计数 + 快速幂增量更新',
    tags=['滑动窗口与双指针', '常用数据结构'],
    code='''
class Solution(object):
    def maxFrequencyScore(self, nums, k):            

        mod = 10 ** 9 + 7
        cnt = {}
        for num in nums[:k]:
            cnt[num] = cnt.get(num, 0) + 1

        def quickPow(base, x):
            if x == 1:
                return base
            
            p = quickPow(base, x // 2)
            p *= p
            if x & 1:
                p *= base
            
            return p % mod

        now = 0
        for num in cnt:
            now += quickPow(num, cnt[num])
            if now >= mod:
                now -= mod
        
        res = now
        for index, num in enumerate(nums[k:]):
            if num == nums[index]:
                continue
            
            if num not in cnt:
                now += num
                if now >= mod:
                    now -= mod
                cnt[num] = 1
            else:               
                now -= quickPow(num, cnt[num])
                if now < 0:
                    now += mod
                cnt[num] += 1
                now += quickPow(num, cnt[num])
                if now >= mod:
                    now -= mod
            
            now -= quickPow(nums[index], cnt[nums[index]])
            if now < 0:
                now += mod
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                cnt.pop(nums[index])
            else:
                now += quickPow(nums[index], cnt[nums[index]])
                if now >= mod:
                    now -= mod

            res = max(res, now)
        
        return res
''',
    call='Solution().maxFrequencyScore([2,3,2,3,3,2], 3)',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前窗口）', pointers={'index': 'pink'}, window=(_wl, _wr), h=170, cell=96),
        dict(type='map', var='cnt', label='cnt：窗口内每种数的出现次数', fmt=lambda k, v: f"{k}: {v}次", h=130, font=30),
        dict(type='text', h=80, size=30, fn=_txt),
        dict(type='calls', h=130),
    ],
    watch=[('index', 'index', 'pink'), 'num', ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'cnt[num] = cnt.get': '`cnt[{num}]` = {cnt[num]}',
        21: '遍历 `cnt` 里的每一种数，累加它的贡献',
        'p = quickPow': '先算一半次数的幂，再平方：这是快速幂的递归写法',
        'if x == 1': '`x = {x}`：{"次数为 1，幂就是 base 本身" if x == 1 else "继续折半"}',
        22: '初始分数累加这一种数的贡献：`{num}^{cnt[num]}`（快速幂算）',
        41: '再加上新贡献 `{num}^{cnt[num]}`（快速幂）',
        52: '还剩 `{cnt[nums[index]]}` 个 `{nums[index]}`：补上新贡献 `{nums[index]}^{cnt[nums[index]]}`',
        'if now >= mod': '`now = {now}`：{"超过 mod，减掉一次 mod" if now >= mod else "没超过 mod，不用处理"}',
        'if now < 0': '`now = {now}`：{"减成负数了，加回 mod" if now < 0 else "还没减成负数，不用处理"}',
        'res = now': '初始窗口的分数就是第一个候选答案 `res = {res}`',
        'if num == nums[index]': '滑入 `{num}`，滑出 `{nums[index]}`：{"两者相同 → 分数不变，直接下一轮" if num == nums[index] else "不同，分数需要更新"}',
        'continue': '同一个数进出，什么都不用改',
        'if num not in cnt': '`{num}` 之前{"不在窗口里：贡献从 0 变成 num^1" if B.num not in B.cnt else "出现过：贡献要从 num^c 变成 num^(c+1)"}',
        'now += num': '新数第一次出现：贡献只是 `{num}^1`，直接 `now += {num}`',
        'cnt[num] = 1': '记下 `{num}` 出现了 1 次',
        'now -= quickPow(num': '先减去旧贡献 `{num}^{cnt[num]}`（快速幂）',
        'cnt[num] += 1': '`{num}` 的次数加 1：`{B.cnt[num]}` → `{cnt[num]}`',
        'now -= quickPow(nums[index]': '滑出的数 `{nums[index]}`：先减去它原来的贡献 `{nums[index]}^{cnt[nums[index]]}`',
        'cnt[nums[index]] -= 1': '窗口里少一个 `{nums[index]}`：次数变成 {cnt.get(nums[index], 0)}',
        'cnt.pop': '次数变 0：`{nums[index]}` 不再有贡献，从哈希表删除',
        'res = max': '窗口分数 `{now}`，`res = max({B.res}, {now}) = {res}`',
        'return res': '最大频率分数 `{res}`',
    },
    skip=['now -= mod', 'now += mod', 'p *= p', 'p *= base'],
    max_steps=100,
    cards=dict(
        one_liner='窗口滑一格只改两个数的贡献，用快速幂做增量更新',
        complexity='时间 `O(n log k)`，空间 `O(k)`',
        problem=['长为 `k` 的子数组：出现 `c` 次的数 `x` 贡献 `x^c`，频率分数是所有不同数贡献之和（对 `10^9+7` 取模）',
                 '求所有长为 `k` 的子数组里分数的最大值',
                 '本视频：`[2,3,2,3,3,2]`，`k=3`'],
        quote='若窗口滑动时新进入的数字与被滑出的数字相同，那么频率分数就不会发生变化，此时无需进行任何处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算前 `k` 个数的初始分数，哈希表 `cnt` 记次数',
              '新进 `x`：减去 `x^cnt`，次数加 1，再加 `x^(cnt+1)`；没出现过就直接加 `x`',
              '滑出 `y`：减去 `y^cnt`，次数减 1，还剩就补回 `y^(cnt-1)`',
              '`cnt` 可能很大，所以乘方用快速幂'],
        summary=['时间 `O(n log k)`，空间 `O(k)`',
                 '进出同一个数时直接 `continue`，不需要更新',
                 '每次加减后都要把 `now` 拉回 [0, mod)；减到负数要加回 `mod`',
                 '原文为 Python 2 写法，快速幂里的 `x / 2` 已改为 `x // 2`',
                 '对比灵神：灵神用每个数一个乘积栈，免去快速幂'],
    ),
)
