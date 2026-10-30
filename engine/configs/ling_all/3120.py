def _set(m):
    s = ''.join(chr(96 + i) for i in range(1, 27) if m >> i & 1)
    return '{' + ','.join(s) + '}'


def _cur(S):
    if 'c' not in S or 'mask' not in S:
        return ''
    c = S['c']
    return f"当前字符 `{chr(c)}`：第 5 位 `c>>5&1` = =={c >> 5 & 1}== → {'小写' if c >> 5 & 1 else '大写'}，字母编号 `c&31` = {c & 31}"


def _mk(S):
    if 'mask' not in S:
        return ''
    return f"大写集合 `mask[0]` = =={_set(S['mask'][0])}==　小写集合 `mask[1]` = =={_set(S['mask'][1])}=="


CONFIG = dict(
    num=3120, title='统计特殊字母的数量 I', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='位运算 · 集合交集', tags=[],
    code='''
class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        mask = [0] * 2  # 大写字母集合、小写字母集合
        for c in map(ord, word):
            # 用 c>>5&1 区分大小写，c&31 获取 c 是第几个字母
            mask[c >> 5 & 1] |= 1 << (c & 31)
        return (mask[0] & mask[1]).bit_count()  # 计算交集大小
''',
    call='Solution().numberOfSpecialChars("aAbaBcC")',
    expect=3,
    views=[
        dict(type='string', var='word', h=300, cell=110),
        dict(type='text', fn=_cur, h=70),
        dict(type='text', fn=_mk, h=70),
    ],
    watch=[('c', 'c', 'blue'), ('mask', 'mask', 'cyan')],
    captions={
        'mask = [0]': '两个空集合：`mask[0]` 存大写，`mask[1]` 存小写，==用二进制位当集合==',
        'for c in': lambda S, B, r: (f'取出下一个字符 `{chr(S.c)}`（ASCII {S.c}）' if S.c != B.get('c') else '字符串遍历完，去算交集'),
        'mask[c >> 5': '`c>>5&1` = {c >> 5 & 1}（{"小写" if c >> 5 & 1 else "大写"}），把第 `{c & 31}` 位置 1 → 字母 `{chr(c)}` 加入对应集合',
        'return': '两个集合 AND 得到交集，`bit_count()` 数 1 的个数 → 特殊字母 ==`{ret}`== 个',
    },
    skip=[],
    cards=dict(
        one_liner='大小写各记一个集合，交集大小就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`word` 里某个字母的小写、大写都出现过，就是特殊字母', '数一共有多少个特殊字母',
                 '示例：`"aAbaBcC"` → `3`（a、b、c）'],
        quote='集合可以用二进制数表示，两个二进制数的 AND 即为交集，AND 结果中的 1 的个数即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['小写字母第 6 位是 1，大写是 0 → `c>>5&1` 区分大小写',
              '大小写字母低 5 位相同 → `c&31` 就是字母编号，大小写落在同一位',
              '两集合按位与：两边都有的字母才留下'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`mask[0]` 是大写、`mask[1]` 是小写，别搞反（对结果无影响，但读代码要对应）',
                 '`bit_count()` 需要 Python 3.10+',
                 '题解还给了 set 写法：小写入 lower，大写转小写入 upper，取 `len(lower & upper)`'],
    ),
)
