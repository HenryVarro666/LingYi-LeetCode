def _f(S):
    if S.get('num') is None:
        return ''
    n = S['num']
    return f"n = {n} 笔订单：插入新的 P、D 共 `s = {n}×(2×{n}−1) = {n*(2*n-1)}` 种，`f[{n}] = f[{n-1}] × {n*(2*n-1)}`"


def _chk(S):
    if S.get('num') is None or S.get('s') is None:
        return ''
    n = S['num']
    return f"检查：`s` 递推得到 {S['s']}，公式 `2n²−n` = {2*n*n-n}"


CONFIG = dict(
    num=1359, title='有效的快递序列数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='逐单插入 · 递推 s[n]',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def countOrders(self, n):

        mod = 10 ** 9 + 7
        res = 1
        s = 1
        for num in range(2, n + 1):
            s += num * 4 - 3
            res = res * s % mod
        
        return res
''',
    call='Solution().countOrders(4)',
    expect=2520,
    views=[
        dict(type='text', fn=lambda S: '每一笔订单有取件 P 和配送 D，D 必须在 P 之后', h=70),
        dict(type='text', fn=_f, h=90),
        dict(type='text', fn=_chk, h=90),
        dict(type='text', fn=lambda S: (f"当前：`s = {S['s']}`，`res = {S['res']}`" if S.get('res') is not None else ''), size=40, h=120),
    ],
    watch=['num', ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'mod = 10': '结果可能很大，对 `10^9 + 7` 取模',
        'res = 1': '1 笔订单只有 `P1 D1` 一种：`res = 1`',
        's = 1': '`s` 表示新增一笔订单时 P、D 的插入方案数，n = 1 时为 1',
        'for num in range': '从第 2 笔订单开始，依次在已有序列里插入新的 P 和 D',
        's += num * 4 - 3': '`s[n] = s[n−1] + 4n − 3`：`s` 增加 `{num}×4−3` → =={s}==（即 `2n²−n`）',
        'res = res * s % mod': '前 `{num-1}` 笔排法 `{B.res}` × 新订单插入方案 `{s}` = =={res}==',
        'return res': lambda S, B, r: f'每一笔订单互相独立，连乘得到 {r} 种有效序列',
    },
    cards=dict(
        one_liner='在 n−1 笔的基础上，数新订单的 P、D 有几种插法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有 `n` 笔订单，每笔有取件 `P_i` 和配送 `D_i`，要求 `D_i` 在 `P_i` 之后',
                 '求所有有效的取件/配送序列数量，对 `10^9 + 7` 取模',
                 '示例：`n = 2` → `6`；本视频：`n = 4` → `2520`'],
        quote='不妨使用X代替D和P，对于n - 1笔订单，一个可行的排布为 X X X X ... X，一共有(n - 1) * 2个X，此时我们需要将一个新的P和D插入到这个串中。',
        quote_src='—— yiduobo 题解原文',
        idea=['P 先选位置，D 再插到它后面：方案数 `(2n−1)+…+1 = n(2n−1)`',
              '所以 `f[n] = f[n−1] × s[n]`',
              '为了少算乘法，用 `s[n] = s[n−1] + 4n − 3` 随 n 更新'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`s[n] = 2n² − n`，`s` 每轮加 `4n − 3`',
                 '`res` 和 `s` 只依赖上一轮，两个变量就够，不用数组',
                 '易错：别忘了每一步对 `mod` 取模'],
    ),
)
