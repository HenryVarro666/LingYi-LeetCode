ORIG = [1, 2, 3]


def _nums(S):
    return S['nums'] or ORIG


def _bins(S):
    return '  '.join(f'`{v}` = {bin(v)[2:]}' for v in _nums(S))


def _txt(S):
    if 'ans' in S and 'x' in S:
        return f'拼接结果：==`{bin(S["ans"])[2:]}`== = {S["ans"]}'
    if 'a' in S and 'b' in S and 'len_b' in S:
        a, b = S['a'], S['b']
        sa, sb = bin(a)[2:], bin(b)[2:]
        return f'比较 `{sa}+{sb}` = {sa + sb}  与  `{sb}+{sa}` = {sb + sa}'
    return '二进制看成字符串：`a+b > b+a` 则 a 排前面'


CONFIG = dict(
    num=3309, title='连接二进制表示可形成的最大数值', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='自定义比较排序 · a+b > b+a',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def maxGoodNumber(self, nums: List[int]) -> int:
        def cmp(a: int, b: int) -> int:
            len_a = a.bit_length()
            len_b = b.bit_length()
            return (b << len_a | a) - (a << len_b | b)
        nums.sort(key=cmp_to_key(cmp))

        ans = 0
        for x in nums:
            ans = ans << x.bit_length() | x
        return ans
''',
    setup='from functools import cmp_to_key',
    call='Solution().maxGoodNumber([1,2,3])',
    expect=30,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var=lambda S: _nums(S), cell=130, h=230, label='nums',
             color=lambda S, i, v: 'yellow' if 'x' in S and S['x'] == v and 'ans' in S else None),
        dict(type='text', fn=lambda S: '各数二进制：' + _bins(S), h=80),
    ],
    watch=[('ans', 'ans', 'green'), 'a', 'b'],
    captions={
        'len_a =': '`a = {a}` 的二进制长度 `len_a = {len_a}`',
        'len_b =': '`b = {b}` 的二进制长度 `len_b = {len_b}`',
        'return (b << len_a': lambda S, B, r: (f'`b` 放前面：`{bin(S.b)[2:]}{bin(S.a)[2:]}` = {(S.b << S.len_a) | S.a}；`a` 放前面：`{bin(S.a)[2:]}{bin(S.b)[2:]}` = {(S.a << S.len_b) | S.b}；差 =={r}=='
                                               + ('，>0 → ==b 排在 a 前面==' if r > 0 else '，<0 → ==a 排在 b 前面==' if r < 0 else '，相等')),
        'nums.sort': '按 `cmp` 排序：拼起来更大的数排在前面',
        'ans = 0': '`ans` 用来存拼接结果',
        'ans = ans << x.bit_length() | x': '`ans` 左移 `{x.bit_length()}` 位（腾出 x 的位置）再或上 `{x}` → `{bin(ans)[2:]}` = {ans}',
        'return ans': '最大数值：`{ans}`',
    },
    cards=dict(
        one_liner='把二进制当字符串，a+b 更大的数排在前面',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['长度为 3 的数组，把各元素的二进制表示按某种顺序连接',
                 '求能得到的最大数值（二进制无前导零）',
                 '示例：`[1,2,3]` → 按 `[3,1,2]` 得 `11110` = `30`'],
        quote='本题是 179. 最大数 的二进制版本，做法是一样的。对于相比较的两个元素 a 和 b，如果其二进制表示（字符串）满足 a+b>b+a，那么 a 排在 b 的左边，否则 b 排在 a 的左边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['比较 a、b：谁放前面拼出的数更大，就谁在前',
              '不用转字符串：`(b << len_a | a)` 就是把 a 接在 b 后面',
              '排好序后依次左移拼接：`ans << bit_length | x`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错点：左移的位数是==后接那个数==的二进制长度',
                 '`cmp` 返回正数表示 a 排在 b 后面，所以 b 在前的拼接值写在减号前面',
                 '原文用到 `cmp_to_key`，LeetCode 预置；这里在 setup 里补了 `from functools import cmp_to_key`',
                 '同类题：179 最大数'],
    ),
)
