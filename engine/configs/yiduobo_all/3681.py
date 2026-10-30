def _b(v, w=3):
    return format(v, f'0{w}b')


def _txt(S):
    if 'f' not in S or 'length' not in S:
        return ''
    w = S['length']
    inner = S.get('_inner', S)
    parts = []
    if S['_line'] <= 15 and 'x' in S:
        parts.append(f"x = `{_b(S['x'], w)}`")
    if 'best' in S or 'res' in S:
        pass
    if 'res' in S and S['_line'] >= 19:
        parts.append(f"res = ==`{_b(S['res'], w)}`==")
    basis = '　'.join(f"f[{i}]=`{_b(v, w)}`" for i, v in enumerate(S['f']) if v)
    parts.append('基：' + (basis or '（空）'))
    return '　'.join(parts)


CONFIG = dict(
    num=3681, title='子序列最大 XOR 值', difficulty='Hard', category='位运算',
    author='yiduobo', technique='异或线性基 · 逐位填充',
    tags=['灵神题单·位运算', '位运算 · 七、线性基'],
    code='''
class Solution(object):
    def maxXorSubsequences(self, nums):
        
        length = len(bin(max(nums))) - 2
        f = [None] * (length + 1)
        for x in nums:
            for index in range(length, -1, -1):
                if x & (1 << index) == (1 << index):
                    if f[index] is None:
                        f[index] = x
                        break
                    else:
                        x ^= f[index]

        res = 0
        for index in range(length, -1, -1):
            if f[index] and (res & (1 << index) == 0):
                res ^= f[index]
            
        return res
''',
    call='Solution().maxXorSubsequences([5, 2, 7, 3])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', h=180),
        dict(type='array', var='f', label='f[index]：最高位在 index 的基（空 = 还没有）', h=210,
             pointers={'index': 'pink'}, color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_txt, size=28, h=140),
    ],
    watch=[('length', 'length', 'cyan'), ('x', 'x', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'length = len': '`bin({max(nums)})` 带 `0b` 前缀，所以位数 = `len(bin(..)) - 2` = `{length}`',
        'f = [None]': '`f[index]` 存最高位在 `index` 的基，先全部为空',
        'if x & (1 << index)': lambda S, B, r: (f"x 的第 `{S.index}` 位是 1 → 看 `f[{S.index}]`" if S.x & (1 << S.index) else f"x 的第 `{S.index}` 位是 0 → 跳过这一位"),
        'if f[index] is None': lambda S, B, r: (f"`f[{S.index}]` 为空 → x 成为新的基" if S.f[S.index] is None
                                                else f"`f[{S.index}] = {S.f[S.index]}` 已有 → 用它消去 x 的这一位"),
        'f[index] = x': '`f[{index}] = {x}`：填进线性基，处理下一个数 → `break`',
        'x ^= f[index]': 'x 异或 `f[{index}]`，这一位变 0 → `x = {x}`',
        'res = 0': '基建好了，开始从高位到低位拼最大值：`res = 0`',
        'if f[index] and': lambda S, B, r: (f"`f[{S.index}]` 为空，这一位没法靠基变 1" if not S.f[S.index]
                                            else (f"`res` 第 `{S.index}` 位是 0，且 `f[{S.index}]` 存在 → 异或后这一位变 1" if S.res & (1 << S.index) == 0
                                                  else f"`res` 第 `{S.index}` 位已经是 1 → 不动")),
        'res ^= f[index]': '`res` 变成 =={res}==（低位的基不会影响更高位）',
        'return res': '最大异或和 = ==`{res}`==',
    },
    max_steps=70,
    cards=dict(
        one_liner='重叠部分互相抵消，转化为子集最大异或，用线性基解决',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['在数组里选两个可空、可重叠的子序列，各自异或得到 `x`、`y`',
                 '求 `x XOR y` 的最大值',
                 '本视频：`[5,2,7,3]` → `7`'],
        quote='这两个子序列中的元素不应该重叠，因为同一个元素异或两次等于0，也就是说不选取这两个子序列重叠的部分对结果并没有任何影响。',
        quote_src='—— yiduobo 题解原文',
        idea=['重叠的元素异或两次抵消，所以相当于只选一个子序列',
              '这就是子集最大异或：沿用 3630 里的异或线性基',
              '`f[index]` 记最高位在 `index` 的基；最后从高位到低位，缺 1 就异或'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`',
                 '`length = len(bin(max(nums))) - 2`，要去掉 `0b` 前缀',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '建基时每个数先消高位，所以每个 `f[index]` 的最高位互不相同',
                 '对比灵神：灵神把基封装成 `XorBasis` 类；yiduobo 直接写在函数里'],
    ),
)
