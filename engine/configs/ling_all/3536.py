CONFIG = dict(
    num=3536, title='两个数字的最大乘积', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='维护最大与次大数位',
    code='''
class Solution:
    def maxProduct(self, n: int) -> int:
        mx = mx2 = 0
        while n > 0:
            n, d = divmod(n, 10)
            if d > mx:
                mx2 = mx
                mx = d
            elif d > mx2:
                mx2 = d
        return mx * mx2
''',
    call='Solution().maxProduct(41927)',
    expect=63,
    views=[
        dict(type='text', h=120, size=34, fn=lambda S: f"剩余 `n = {S['n']}`，当前数位 `d = {S['d']}`" if 'd' in S else f"剩余 `n = {S['n']}`"),
        dict(type='text', h=120, size=34, fn=lambda S: f"最大 `mx` = =={S['mx']}==　次大 `mx2` = =={S['mx2']}==" if 'mx' in S else ''),
        dict(type='text', h=120, size=34, fn=lambda S: f"乘积 `{S['mx']} × {S['mx2']} = {S['mx'] * S['mx2']}`" if 'mx' in S else ''),
    ],
    watch=['n', 'd', ('mx', 'mx', 'green'), ('mx2', 'mx2', 'cyan')],
    captions={
        'mx = mx2 = 0': '最大值 `mx` 和次大值 `mx2` 都从 0 开始',
        'while n > 0': lambda S, B, r: (f'`n = {S.n} > 0`，还有数位没处理' if S.n > 0 else '`n = 0`，所有数位处理完了'),
        'divmod': '拆出最低位 `d = {d}`，剩下 `n = {n}`',
        'if d > mx:': lambda S, B, r: (f'`d = {S.d} > mx = {S.mx}`：比最大值还大 → 成为新的最大值' if S.d > S.mx
                                       else f'`d = {S.d}` 不超过 `mx = {S.mx}`，再看是否超过次大'),
        'mx2 = mx': '原来的最大值降级为次大：`mx2 = {mx2}`',
        'mx = d': '`mx` 更新为 `{mx}`',
        'elif d > mx2': lambda S, B, r: (f'`d = {S.d} > mx2 = {S.mx2}`：夹在最大和次大之间 → 更新次大' if S.d > S.mx2
                                          else f'`d = {S.d}` 不超过 `mx2 = {S.mx2}`，忽略'),
        'mx2 = d': '`mx2` 更新为 `{mx2}`',
        'return mx * mx2': '最大 `{mx}` × 次大 `{mx2}` = =={mx * mx2}==',
    },
    cards=dict(
        one_liner='乘积越大越好，取最大和次大的两个数位相乘',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给定正整数 `n`，从它的各位数字里选==两个不同位置==的数相乘',
                 '求最大乘积；同一个数字出现多次可以重复使用',
                 '示例：`n = 124` → `2 × 4 = 8`；本视频：`41927` → `63`'],
        quote='贪心地，相乘的数越大越好，所以答案为 s 最大值与次大值的乘积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数位都是非负数，乘积随两个因子变大而变大',
              '所以只需要最大和次大的数位',
              '写法二不用字符串也不排序：`divmod` 拆位，同时维护 `mx`、`mx2`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：新的最大值出现时，旧最大值要先降级给 `mx2`',
                 '数位重复时，`d == mx` 走 `elif`，会更新次大，所以 `22` 得 4',
                 '写法一是排序：`sorted(str(n))` 取最后两个，视频选写法二'],
    ),
)
