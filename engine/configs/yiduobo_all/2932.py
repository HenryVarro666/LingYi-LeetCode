CONFIG = dict(
    num=2932, title='找出强数对的最大异或值 I', difficulty='Easy', category='位运算',
    author='yiduobo', technique='暴力枚举', tags=[],
    code='''
class Solution(object):
    def maximumStrongPairXor(self, nums):

        res = 0
        for x in nums:
            for y in nums:
                if abs(x - y) <= min(x, y):
                    res = max(res, x ^ y)
        
        return res
''',
    call='Solution().maximumStrongPairXor([5,6,25,30])',
    expect=7,
    views=[
        dict(type='array', var='nums', color=lambda S, k, v: 'blue' if 'x' in S and S['x'] == v else ('pink' if 'y' in S and S['y'] == v else None), h=220),
        dict(type='text', size=40, h=110, fn=lambda S: (
            f"`x={S['x']}, y={S['y']}`：`|x−y| = {abs(S['x']-S['y'])}`，`min = {min(S['x'], S['y'])}`，异或 `{S['x']^S['y']}`" if 'y' in S else '')),
        dict(type='text', size=40, h=110, fn=lambda S: f"当前最大异或 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录最大异或值，初始 0',
        'if abs(x - y)': lambda S, B, r: (f'`|{S.x}−{S.y}| = {abs(S.x-S.y)} <= min = {min(S.x,S.y)}` → ==强数对=='
                                          if abs(S.x - S.y) <= min(S.x, S.y)
                                          else f'`|{S.x}−{S.y}| = {abs(S.x-S.y)} > min = {min(S.x,S.y)}` → 不是强数对，跳过'),
        'res = max': '`{x} ^ {y} = {x^y}`，`res = max({B.res}, {x^y}) = {res}`',
        'return res': '数据只有 50 个数，枚举完所有数对 → `{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='数据很小，直接枚举每一对 x、y',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['强数对：`|x − y| <= min(x, y)`，可选同一个数两次',
                 '在所有强数对里求最大的 `x XOR y`',
                 '本视频：`[5,6,25,30]` → `7`（`25 XOR 30`）'],
        quote='题目的数据规模非常小，因此可以直接枚举每一组x和y，对于所有符合条件的x和y，计算二者的异或值并更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['两层循环枚举所有 `(x, y)`，包含 `x = y`（异或为 0）',
              '满足强数对条件才计算 `x ^ y`，并更新 `res`'],
        summary=['时间 `O(n²)`，`n <= 50` 足够',
                 '`x` 和 `y` 都遍历整个数组，所以同一个数选两次也被覆盖',
                 '原文无需修改，Python 3 直接可运行',
                 '加强版（2935）数据变大，需要 0-1 trie'],
    ),
)
