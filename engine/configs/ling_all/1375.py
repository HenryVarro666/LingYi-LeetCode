CONFIG = dict(
    num=1375, title='二进制字符串前缀一致的次数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='前缀最大值',
    code='''
class Solution:
    def numTimesAllBlue(self, flips: List[int]) -> int:
        ans = mx = 0
        for i, x in enumerate(flips, 1):  # i 从 1 开始
            mx = max(mx, x)
            ans += mx == i
        return ans
''',
    call='Solution().numTimesAllBlue([3,2,4,1,5])',
    expect=2,
    views=[
        dict(type='array', var='flips', pointers={'i-1': 'blue'}, h=220,
             dim=lambda S, i, v: 'i' in S and i + 1 > S['i'],
             color=lambda S, i, v: 'yellow' if 'mx' in S and v == S['mx'] and i + 1 <= S.get('i', 0) else None),
        dict(type='text', fn=lambda S: f"前 {S['i']} 个数最大值 `mx = {S['mx']}`，{'==等于== i → 恰好是 1 到 i' if S['mx'] == S['i'] else '大于 i → 还缺小的数'}" if 'mx' in S and 'i' in S else '', size=30, h=80),
    ],
    watch=['i', 'x', ('mx', 'mx', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'mx = max': '前 `{i}` 个数的最大值 `mx = {mx}`',
        'ans += mx == i': lambda S, B, r: (f'`mx = {S.mx}` == `i = {S.i}`：前 {S.i} 个互不相同的数最大才 {S.i} → ==恰好是 1 到 {S.i}==，答案 +1 → {S.ans}'
                                           if S.mx == S.i else f'`mx = {S.mx}` != `i = {S.i}`：mx 更大，说明 1 到 {S.i} 里有数还没出现，不计'),
        'return': '前缀一致 `{ret}` 次',
    },
    cards=dict(
        one_liner='前 i 个数的最大值恰好等于 i，就是一次前缀一致',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长度为 n 的二进制串初始全 0，第 i 步把 `flips[i]` 位翻成 1',
                 '第 i 步后 `[1,i]` 全是 1 且其余全 0，算一次前缀一致',
                 '本视频：`[3,2,4,1,5]` → `2`'],
        quote='如果前 i 个数的最大值等于 i，则说明找到了 [1,i] 内的所有整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前 i 步翻了 i 个不同的位置，要刚好是 1 到 i',
              'flips 是排列，前 i 个数互不相同 → 最大值 `== i` 就等价于恰好是 1 到 i',
              '一边遍历一边维护 `mx`，相等就加一'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`enumerate(flips, 1)` 让 i 从 1 开始，别写成 0 开始',
                 '`ans += mx == i` 利用布尔值当 0/1 加',
                 '对比 yiduobo：他用前缀和比对 1+…+k，这里只用最大值'],
    ),
)
