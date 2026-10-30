def _txt(S):
    if 'same_freq' not in S:
        return '好子序列：非空，且每个出现的字符次数都相同；枚举这个共同次数 `same_freq`'
    cnt = S['cnt']
    f = S['same_freq']
    parts = [f'`{ch}`:{c}' for ch, c in cnt.items()]
    return f'每个字符 {" ".join(parts)}；选 `{f}` 个同字符，各字符方案数相乘再减 1（空）'


CONFIG = dict(
    num=2539, title='好子序列的个数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举相同频次 + 组合数乘法原理',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countGoodSubsequences(self, s):

        mod = 10 ** 9 + 7

        def quickPow(base, p):
            if p == 1:
                return base

            x = quickPow(base, p // 2)
            x *= x
            x %= mod
            if p & 1:
                x *= base
                x %= mod
            return x

        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        ma_freq = max(cnt.values())

        frac = [1]
        inv_frac = [1]
        for index in range(1, ma_freq + 1):
            frac.append(frac[-1] * index % mod)
            inv_frac.append(quickPow(frac[-1], mod - 2))
        
        res = 0
        for same_freq in range(1, ma_freq + 1):
            now = 1
            for freq in cnt.values():
                if freq >= same_freq:
                    now *= (frac[freq] * inv_frac[freq - same_freq] * inv_frac[same_freq] % mod + 1)
                    now %= mod
            
            res += now - 1
            if res < 0:
                res += mod
            if res >= mod:
                res -= mod
        
        return res
''',
    call="Solution().countGoodSubsequences('aabbc')",
    expect=20,
    views=[
        dict(type='map', var='cnt', label='cnt：各字符出现次数', h=150, font=28),
        dict(type='array', var=lambda S: S.get('frac', []), label='frac：阶乘 0!, 1!, 2!, …', cell=84, h=150),
        dict(type='array', var=lambda S: S.get('inv_frac', []), label='inv_frac：阶乘的逆元', cell=84, h=150),
        dict(type='text', fn=_txt, size=28, h=100),
    ],
    watch=[('same_freq', 'same_freq', 'blue'), 'now', ('res', 'res', 'green')],
    skip=['if p == 1', 'return base', 'x = quickPow', 'x *= x', 'x %= mod', 'if p & 1', 'x *= base', 'return x',
          'mod = 10', 'now %= mod', 'if res < 0', 'res += mod', 'if res >= mod', 'res -= mod', 'cnt = {}', 'frac = [1]', 'inv_frac = [1]'],
    captions={
        'for char in s': '遍历字符串，统计每种字符出现的次数',
        'cnt[char] = ': '`cnt[{char}] = {cnt[char]}`',
        'ma_freq = max': '好子序列里每个字符的次数只能在 `1..ma_freq` 之间：`ma_freq = {ma_freq}`',
        'frac.append(frac': '`frac[{index}] = {index}! = {frac[-1]}`',
        'inv_frac.append(quickPow': '`inv_frac[{index}]` = `{index}!` 的乘法逆元（费马小定理 `x^(mod-2)`）；没有除法，用它代替 `/{index}!`',
        'for same_freq': lambda S, B, r: ('每个次数都枚举完了' if B.get('same_freq') == S.same_freq else f'枚举好子序列中每个字符出现的次数 `same_freq = {S.same_freq}`'),
        'now = 1': '`now` 累乘各字符的方案数，从 1 开始',
        'for freq in cnt.values': '依次看每种字符；全看完就退出内层循环',
        'if freq >= same_freq': lambda S, B, r: (f'`{S.freq} ≥ {S.same_freq}`：这个字符可以选 {S.same_freq} 个' if S.freq >= S.same_freq
                                                  else f'`{S.freq} < {S.same_freq}`：不够 {S.same_freq} 个，只能不选，方案数 1，跳过'),
        'now *= (': '方案数 = `C({freq}, {same_freq}) + 1`（+1 表示不选它）= {frac[freq] * inv_frac[freq - same_freq] * inv_frac[same_freq] % mod + 1}，`now = {now}`',
        'res += now - 1': '各字符方案相乘包含「什么都不选」那 1 种，要减掉：`res += {now} - 1` → {res}',
        'return res': '答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='枚举每个字符出现的次数，各字符方案数相乘',
        complexity='时间 `O(26·maxfreq)`，空间 `O(maxfreq)`',
        problem=['字符串 `s` 的子序列里，==每个出现的字符次数都相同==的叫「好子序列」（非空）',
                 '求好子序列的个数，模 `10^9+7`',
                 '示例：`aabb` → `11`；本视频：`aabbc`'],
        quote='可以枚举每种字符出现的频率freq，然后对于每种字符分别统计选择freq个该字符的方案数，然后使用乘法原理计算频率为freq的好子序列数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用哈希表 `cnt` 数每种字符的次数，`ma_freq` 是最大次数',
              '固定共同次数 `freq`：次数 ≥ freq 的字符各有 `C(cnt, freq) + 1` 种（+1 = 不选）',
              '各字符相乘，再减 1 去掉「全都不选」；对所有 freq 求和'],
        summary=['时间 `O(26·ma_freq)`，空间 `O(ma_freq)`',
                 '组合数要取模，除法用乘法逆元：`inv_frac = (n!)^(mod-2)`',
                 '别忘了减 1：乘积里含有空子序列',
                 '原文为 Python 2 写法，`quickPow` 里的整数除法 `p / 2` 已改为 `p // 2`'],
    ),
)
