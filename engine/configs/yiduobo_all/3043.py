CONFIG = dict(
    num=3043, title='最长公共前缀的长度', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀集合 · 取数值最大',
    tags=[],
    code='''
class Solution(object):
    def longestCommonPrefix(self, arr1, arr2):

        prefix = set()
        for v in arr1:
            while v:
                prefix.add(v)
                v //= 10
        
        ma = 0
        for v in arr2:
            while v:
                if v in prefix:
                    ma = max(ma, v)
                v //= 10
        
        if ma == 0:
            return 0
        return len(str(ma))
''',
    call='Solution().longestCommonPrefix([123, 45, 678], [1290, 6789, 9])',
    expect=3,
    views=[
        dict(type='array', var='arr1', label='arr1', h=130),
        dict(type='array', var='arr2', label='arr2', h=130),
        dict(type='set', var='prefix', label='prefix：arr1 的所有前缀', h=150),
        dict(type='text', h=60, fn=lambda S: (f"当前 v = =={S['v']}==　　目前最大公共前缀 ma = =={S['ma']}==" if 'ma' in S else f"当前 v = =={S['v']}==") if 'v' in S else ''),
    ],
    skip=['prefix = set()'],
    watch=[('v', 'v', 'orange'), ('ma', 'ma', 'green')],
    captions={
        'for v in arr1': lambda S, B, r: 'arr1 遍历完了，prefix 里有它所有的前缀' if S.v == 0 and B.get('v') == 0 else f'取 arr1 的数 `v = {S.v}`，把它的所有前缀都放进 prefix',
        'while v': lambda S, B, r: f'`v = {S.v}`' + ('：已变成 0，前缀处理完了' if not S.v else '：还有数位 → 继续'),
        'prefix.add(v)': '`{v}` 是 arr1 某个数的前缀，加入集合',
        'v //= 10': lambda S, B, r: f'去掉最后一位：`{B.v}` → `{S.v}`，得到更短的前缀',
        'for v in arr2': lambda S, B, r: 'arr2 也遍历完了' if S.v == 0 and B.get('v') == 0 else f'取 arr2 的数 `v = {S.v}`，枚举它的每个前缀',
        'if v in prefix': lambda S, B, r: f'`{S.v}` 在 prefix 里吗？' + ('==在==：公共前缀' if S.v in S.prefix else '不在，这个前缀不是公共的'),
        'ma = max': '`ma = max({B.ma}, {v}) = {ma}`：数值大的前缀位数必然更多',
        'ma == 0': lambda S, B, r: '`ma == 0`：没有任何公共前缀 → 返回 0' if S.ma == 0 else '`ma != 0`：有公共前缀，要算它的位数',
        'return len': '最大公共前缀 `{ma}`，位数 = =={ret}==',
    },
    max_steps=100,
    cards=dict(
        one_liner='先把 arr1 的前缀全算出来放集合，再拿 arr2 的前缀去查',
        complexity='时间 `O((n+m) log U)`，空间 `O(n log U)`',
        problem=['两个正整数数组，各取一个数，求它们的最长公共前缀的长度',
                 '没有公共前缀返回 0',
                 '本视频：`[123,45,678]` 和 `[1290,6789,9]` → 最长公共前缀 `678`，长度 ==3=='],
        quote='数值最大的前缀必然是最长的前缀，因此在寻找位数最多的前缀时可以直接选数值最大的前缀，最后再计算其位数作为结果返回。',
        quote_src='—— yiduobo 题解原文',
        idea=['数值不超过 `10^8`，每个数最多 9 个前缀，全部算出来也只有几十万种，不怕多',
              '不断 `v //= 10` 就能得到所有前缀',
              'arr2 的每个前缀去集合里查，命中就更新最大值 `ma`；不用比位数，比数值即可'],
        summary=['时间 `O((n+m) log U)`，空间 `O(n log U)`',
                 '原文为 Python 2 写法，整数除法 `v /= 10` 已改为 `v //= 10`',
                 '易错：`ma == 0` 要单独返回 0，因为 `len(str(0))` 是 1',
                 '与灵神的差别：灵神遇到已在集合的前缀就提前停止；这里每个前缀都老老实实加/查'],
    ),
)
