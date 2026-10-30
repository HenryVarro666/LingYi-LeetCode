def _b(v, w=6):
    return format(v & ((1 << w) - 1), '0%db' % w)


def _x(S):
    if 'x' not in S:
        return ''
    return f"`x` = ==`{_b(S['x'])}`==（1 是固定位，0 是空位）"


def _n(S):
    if 'n' not in S or 'j' not in S:
        return ''
    n, j = S['n'], S['j']
    return f"`n-1` = `{_b(n)}`，已填 `{j}` 位，还剩 `{_b(n >> j, 3)}` 待填"


def _t(S):
    if 't' not in S:
        return ''
    t = S['t']
    lb = S.get('lb')
    s = f"`t = ~x` 的低位 = `{_b(t)}`（1 = 空位）"
    if lb:
        s += f"，最低的空位 `lb` = `{lb:06b}`"
    return s


CONFIG = dict(
    num=3133, title='数组最后一个元素的最小值', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='把 n-1 的比特填入 x 的空位',
    tags=['灵神题单·位运算', '难度分 1935'],
    code='''
class Solution:
    def minEnd(self, n: int, x: int) -> int:
        n -= 1
        j = 0
        t = ~x
        while n >> j:
            lb = t & -t
            x |= (n >> j & 1) * lb
            j += 1
            t ^= lb
        return x
''',
    call='Solution().minEnd(7, 4)',
    expect=14,
    views=[
        dict(type='text', fn=_x, size=30, h=70),
        dict(type='text', fn=_n, size=30, h=70),
        dict(type='text', fn=_t, size=30, h=70),
    ],
    watch=[('n', 'n', 'blue'), ('j', 'j', 'pink'), ('lb', "S.get('lb', '')", 'orange'), ('x', 'x', 'green')],
    captions={
        'n -= 1': '最小的 `n` 个超集是第 `0..n-1` 个，最大的那个对应 `n-1`：`n` → {n}',
        't = ~x': '`~x` 取反：原来 x 的 0（空位）变成 1，用 lowbit 就能逐个找到空位',
        'while n >> j': lambda S, B, r: (f'`n >> {S.j}` = {S.n >> S.j} 非零：`n-1` 还有比特没填完，继续' if S.n >> S.j
                                         else '`n-1` 的比特全部填完 → 结束'),
        'lb = t & -t': '`lb` = t 的最低位 1 = 当前最低的空位 `{lb:06b}`',
        'x |= ': '`n-1` 的第 `{j}` 位是 `{n >> j & 1}`：为 1 就把空位填 1，为 0 保持 0 → x = `{x:06b}`',
        'j += 1': '`n-1` 的下一个比特：`j` → {j}',
        't ^= lb': '这个空位用掉了，从 `t` 里去掉，下一轮找次低的空位',
        'return x': '空位里依次填满 `n-1` 的比特，最后一个元素最小值 = =={x}==',
    },
    cards=dict(
        one_liner='x 是每个数的子集；把 n-1 的比特依次塞进 x 的空位',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['构造严格递增、长度为 `n` 的正整数数组，所有元素 AND 起来恰好是 `x`',
                 '求最后一个元素 `nums[n-1]` 的最小值',
                 '示例：`n=3, x=4` → `6`；本视频：`n=7, x=4` → `14`'],
        quote='把 x 的二进制中的 0 视作「空位」，把 n-1 二进制的每个比特逐个填入空位，即为最小的 nums[n-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['集合视角：`x` 是每个 `nums[i]` 的子集，`nums[i]` 是 `x` 的超集',
              '只看空位上的比特，就是自然数序列 0,1,2,…',
              '所以第 `n` 小的超集 = 把 `n-1` 填进空位',
              '优化写法：对 `~x` 用 lowbit 枚举空位'],
        summary=['时间 `O(log n)`，循环次数只和 `n` 有关；空间 `O(1)`',
                 '先 `n -= 1`：第 n 个数对应的是自然数 n-1',
                 '空位不够时相当于在 x 前面补前导 0，循环不用特殊处理',
                 '题解先给了逐位找空位的写法（时间 `O(log x + log n)`），这里演示 lowbit 优化'],
    ),
)
