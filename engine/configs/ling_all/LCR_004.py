def _bin(v):
    return format(v & 0b111, '03b')


def _state(S):
    if 'a' not in S:
        return ''
    x = S.get('x')
    xs = f"当前数 `x` = `{_bin(x)}`（{x}）" if x is not None else ''
    return xs


def _ab(S):
    if 'a' not in S:
        return ''
    return f"`a` = =={_bin(S['a'])}==　　`b` = =={_bin(S['b'])}==　　（每一列的 `(a,b)` = 该位 1 的个数 mod 3）"


def _cols(S):
    if 'a' not in S:
        return ''
    out = []
    for k in (2, 1, 0):
        a, b = S['a'] >> k & 1, S['b'] >> k & 1
        out.append(f"第{k}位 `({a},{b})` = {a * 2 + b}")
    return '　'.join(out)


CONFIG = dict(
    num='LCR 004', title='只出现一次的数字 II', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='位运算 · 模 3 加法', tags=[],
    code='''
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        a = b = 0
        for x in nums:
            b = (b ^ x) & ~a
            a = (a ^ x) & ~b
        return b
''',
    call='Solution().singleNumber([2, 2, 3, 2])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=190, label='nums（高亮 = 与当前 x 相同）',
             color=lambda S, i, v: ('yellow' if 'x' in S and v == S['x'] else None)),
        dict(type='text', fn=_state, h=60),
        dict(type='text', fn=_ab, h=70),
        dict(type='text', fn=_cols, h=70),
    ],
    watch=[('x', 'x', 'yellow'), ('a', 'a', 'orange'), ('b', 'b', 'green')],
    captions={
        'a = b = 0': '`a`、`b` 两个数用来表示「每个比特位上 1 的个数 mod 3」：`(a,b)` = `00 → 01 → 10 → 00`',
        'for x in nums': lambda S, B, r: ('4 个数都处理完了，结束循环' if S.b == 3 and B.get('x') == S.x else f'取下一个数 `x = {S.x}`（二进制 `{S.x:03b}`）'),
        'b = (b ^ x)': '先更新 `b`：`b ^ x` 做模 2 翻转，`& ~a` 保证 `a=1` 时 `b` 保持 0 → `b = {b:03b}`',
        'a = (a ^ x)': '再用新的 `b` 更新 `a`：`b=1` 的位上 `a` 必须保持 0 → `a = {a:03b}`',
        'return b': '出现 3 次的数，各位都转回了 `(0,0)`；只出现一次的数留在 `b` 里 → =={b}==（`{b:03b}`）',
    },
    cards=dict(
        one_liner='用两个变量 a、b 并行做每一位的「模 3 加法」',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组里一个数只出现 `1` 次，其余都恰好出现 `3` 次',
                 '找出这个数，要求线性时间、不用额外空间',
                 '示例：`[2,2,3,2]` → `3`'],
        quote='模 3 加法就是在 0,1,2 之间不断转换……由于 0,1,2 需要两个比特才能表示，设这两个比特分别为 a 和 b。',
        quote_src='—— 灵茶山艾府题解',
        idea=['某一位上 1 的个数 mod 3：出现 3 次的数贡献 0，只出现一次的数贡献 1',
              '转换 `(0,0)→(0,1)→(1,0)→(0,0)`：异或翻转，再加「约束」`& ~a`、`& ~b`',
              '位运算天然并行，一个 `x` 同时更新所有比特，最后 `b` 就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`b` 要先于 `a` 更新，`a` 的更新用的是==更新后的 `b`==',
                 '最终每一位的计数只会是 0 或 1，所以答案就是 `b`',
                 '另一种写法：逐位统计 1 的个数 mod 3，最高位（符号位）要单独处理',
                 '思考题：改成出现 5 次时，需要 3 个比特表示 0~4'],
    ),
)
