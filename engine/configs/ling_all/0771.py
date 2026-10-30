CONFIG = dict(
    num=771, title='宝石与石头', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='位运算压缩集合',
    code='''
class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        # 把 jewels 转换成字符集合 mask
        mask = 0
        for c in jewels:
            mask |= 1 << (ord(c) & 63)
        # 统计有多少 stones[i] 在集合 mask 中
        return sum(mask >> (ord(c) & 63) & 1 for c in stones)
''',
    call='Solution().numJewelsInStones("aA", "aAAbbb")',
    expect=3,
    views=[
        dict(type='string', var='jewels', label='jewels', h=150),
        dict(type='text', fn=lambda S: (f"`mask` = ==`{S['mask']:b}`==（二进制，第 `ord(c)&63` 位为 1 表示是宝石）" if 'mask' in S else ''), size=30),
        dict(type='text', fn=lambda S: (f"`c = '{S['c']}'`，`ord(c) & 63 = {ord(S['c']) & 63}`" if 'c' in S else ''), size=34),
        dict(type='string', var='stones', label='stones', h=200),
    ],
    watch=['c', ('mask', 'mask', 'cyan')],
    captions={
        'mask = 0': '`mask` 是一个整数，用二进制位当集合，代替哈希表',
        'for c in jewels': '取宝石 `{c}`，`ord(c) & 63 = {ord(c) & 63}`（大小写映射到不同的位）',
        'mask |= 1 <<': '把第 `{ord(c) & 63}` 位置 1：`mask` = `{mask:b}`',
        'return sum': lambda S, B, r: f'逐个检查 stones：`mask >> (ord(c)&63) & 1` 为 1 就是宝石，共 =={r}== 块',
    },
    cards=dict(
        one_liner='字符低 6 位互不相同，一个整数就能当集合',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['`jewels` 的每个字符是一种宝石，`stones` 是拥有的石头',
                 '数 `stones` 里有多少块是宝石，区分大小写',
                 '示例：`jewels="aA"`，`stones="aAAbbbb"` → `3`'],
        quote='取字符的的低 6 位，就可以把不同的大小写字母映射到不同的数字上。所以，可以用一个 64 位整数 mask 来代替哈希表/布尔数组，压缩存储 jewels 中的字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['大写 `A~Z` 低 6 位是 1~26，小写 `a~z` 是 33~58，互不冲突',
              '`mask |= 1 << (ord(c) & 63)` 把宝石放进集合',
              '`mask >> (ord(c) & 63) & 1` 判断石头是否在集合里，然后求和'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '`ord(c) & 63` 取低 6 位，位置范围 1~58，64 位整数装得下',
                 '`jewels` 字符唯一，重复置位也不影响结果',
                 '对比 yiduobo：用哈希集合，思路相同但空间 `O(n)`'],
    ),
)
