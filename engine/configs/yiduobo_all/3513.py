def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S['nums']
    n = len(nums)
    res = S.get('res')
    cv.text((x0 + 18, y0 + 4), '找最小的 2 的幂 p > n：0 ~ p−1 都能达成', 24, T['muted'], bold=True)
    if res is None:
        return
    cap = 8
    cell = 76
    sx = x0 + 24
    y = y0 + 80
    for v in range(1, cap + 1):
        X = sx + (v - 1) * (cell + 8)
        if v <= n:
            fill = T['blue']
        else:
            fill = (70, 76, 86)
        cv.rect((X, y, X + cell, y + cell - 10), fill=fill, r=6)
        cv.text((X + cell / 2, y + cell / 2 - 5), v, 24, T['bg'] if v <= n else T['muted'], anchor='mm', bold=True)
    cv.text((sx, y + cell + 6), f'蓝色 = 不超过 n={n} 的数；res 每次翻倍，直到超过 n', 20, T['muted'])
    X = sx + (min(res, cap) - 1) * (cell + 8) + cell / 2
    cv.tri_up(X, y + cell + 50, 12, T['orange'])
    cv.text((X, y + cell + 66), f'res={res}', 22, T['orange'], anchor='mt', bold=True)


CONFIG = dict(
    num=3513, title='不同 XOR 三元组的数目 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='构造 · 最小的 2 的幂 p > n',
    tags=['贪心算法', '构造题', '难度分 1663'],
    code='''
class Solution(object):
    def uniqueXorTriplets(self, nums):
        
        if len(nums) <= 2:
            return len(nums)
        
        res = 1
        while res <= len(nums):
            res += res
        return res
''',
    call='Solution().uniqueXorTriplets([3,1,5,2,4])',
    expect=8,
    views=[
        dict(type='array', var='nums', h=170, label='nums（1 到 n 的排列）'),
        dict(type='custom', draw=_draw, h=300),
    ],
    watch=['res'],
    captions={
        'if len(nums) <= 2': '`n = len(nums) = {len(nums)}`：{"n ≤ 2，数位不足，凑不出 0，答案就是 n" if len(nums) <= 2 else "n > 2，0 到 p−1 全部都能达成，往下求 p"}',
        'return len(nums)': '`n ≤ 2` → 直接返回 `{len(nums)}`',
        'res = 1': '`res` 从 1 开始，一路翻倍，找最小的比 n 大的 2 的幂 p',
        'while res <= len(nums)': lambda S, B, r: (f'`res = {S.res} ≤ n = {len(S.nums)}`：还不比 n 大 → 继续翻倍' if S.res <= len(S.nums)
                                                  else f'`res = {S.res} > n = {len(S.nums)}`：这就是 p，停止'),
        'res += res': '`res` 翻倍 → =={res}==',
        'return res': '答案就是 p = `{res}`：0 到 {res - 1} 的每个值都能凑出来',
    },
    cards=dict(
        one_liner='异或结果落在 0 ~ p−1，n≥3 时全部能达成，答案就是 p',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`nums` 是 `1~n` 的排列，选 `i ≤ j ≤ k`，求 `nums[i]^nums[j]^nums[k]` 有多少种不同值',
                 '示例：`[3,1,2]` → `4`',
                 '本视频：`[3,1,5,2,4]` → `8`'],
        quote='不管怎样异或，且结果都不可能出现最高位之外的1。令p表示最小的大于n的2的幂，那么最终异或的结果必然落在0到p - 1之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['按二进制 1 的个数分类：只有一个 1、至少三个 1、恰好两个 1、没有 1（结果 0）',
              '`n ≤ 2` 数位不够，凑不出 0；`n ≥ 3` 时 0 ~ p−1 全部可达',
              '所以 `n ≤ 2` 答案是 n，否则是 ==p==，用循环翻倍求 p'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`n ≤ 2` 要先特判，p 不适用',
                 '`while res <= len(nums)`：`n` 本身是 2 的幂时，p 要比 n 大一倍',
                 '对比灵神：灵神用 `1 << n.bit_length()` 一步得到 p；yiduobo 用循环翻倍求同一个数',
                 '代码原文已是 Python 3 可运行写法，未作修改'],
    ),
)
