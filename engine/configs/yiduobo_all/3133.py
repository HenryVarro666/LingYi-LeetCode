def _b(v, w=6):
    return format(v & ((1 << w) - 1), '0%db' % w)


def _res(S):
    if 'res' not in S:
        return ''
    return f"`res` = ==`{_b(S['res'])}`==（x 的 1 保持不动）"


def _n(S):
    if 'n' not in S:
        return ''
    return f"剩余要插入的 `n-1` = `{_b(S['n'], 3)}`"


def _p(S):
    if 'p' not in S or 'res' not in S:
        return ''
    p = S['p']
    return f"当前考察第 `{p}` 位：`res` 这一位是 `{S['res'] >> p & 1}`"


CONFIG = dict(
    num=3133, title='数组最后一个元素的最小值', difficulty='Medium', category='位运算',
    author='yiduobo', technique='把 n-1 的二进制穿插到 x 的 0 位',
    tags=['灵神题单·位运算', '难度分 1935'],
    code='''
class Solution(object):
    def minEnd(self, n, x):

        res = x
        p = 0
        n -= 1
        while n:
            while res & (1 << p) == (1 << p):
                p += 1
            
            if n & 1:
                res |= (1 << p)
            
            n >>= 1
            p += 1
        
        return res
''',
    call='Solution().minEnd(6, 5)',
    expect=23,
    views=[
        dict(type='text', fn=_res, size=30, h=70),
        dict(type='text', fn=_n, size=30, h=70),
        dict(type='text', fn=_p, size=30, h=70),
    ],
    watch=[('n', 'n', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = x': '先把 `x` 作为底：每个元素在 x 为 1 的位上必须也是 1',
        'n -= 1': '数组从 0 到 n-1 排布，最后一个对应 `n-1` = {n}',
        'while n:': lambda S, B, r: (f'`n` = {S.n} 非零：还有比特要插入' if S.n else '`n-1` 的比特插完了 → 结束'),
        'while res & (1 << p)': lambda S, B, r: (f'第 `{S.p}` 位已经是 1（属于 x）→ 不能占用，跳过' if S.res >> S.p & 1
                                                   else f'第 `{S.p}` 位是 0，是可以放 `n-1` 比特的位置'),
        'p += 1': lambda S, B, r: f'`p` → {S.p}',
        'if n & 1': lambda S, B, r: (f'`n` 的最低位是 1：把第 `{S.p}` 位置 1' if S.n & 1
                                     else f'`n` 的最低位是 0：这一位保持 0'),
        'res |= (1 << p)': '第 `{p}` 位填 1 → res = `{res:06b}`',
        'n >>= 1': '`n-1` 处理完最低位，右移丢掉：`n` → {n}',
        'return res': '`n-1` 的二进制穿插进 x 的 0 位后，结果 = =={res}==',
    },
    cards=dict(
        one_liner='无视 x 的 1，其余位上就是 0 到 n-1 的排布',
        complexity='时间 `O(log n + log x)`，空间 `O(1)`',
        problem=['构造长度 `n` 的递增正整数数组，所有元素按位与等于 `x`',
                 '求最后一个元素的最小值',
                 '示例：`n=3, x=4` → `6`；本视频：`n=6, x=5` → `23`'],
        quote='可以发现，在无视x中对应的数位时，其他位上对应的数值实际上就是n - 1的二进制表示，那么只需要将n - 1的二进制表示穿插到x二进制中非1的位置上即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['按位与等于 `x`：每个元素在 `x` 的 1 位上必须是 1',
              '要让数组尽量小：其余位按 `0,1,…,n-1` 依次排布',
              '例 `n=6, x=5`：`00101, 00111, 01101, 01111, 10101, 10111`',
              '所以只要把 `n-1 = 101` 依次放进 x 的空位'],
        summary=['时间 `O(log n)` 级，空间 `O(1)`',
                 '内层 `while` 负责跳过 x 里为 1 的位，别漏掉',
                 '先 `n -= 1`：最后一个元素对应编号 n-1',
                 '对比灵神：灵神用 `~x` + lowbit 找空位，这里逐位扫描跳过'],
    ),
)
