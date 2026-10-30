def _inf():
    parts = []
    for b in range(0, 4):
        r = list(range(max(10 * b, 1), 10 * b + 10))
        parts += r if b % 2 == 0 else r[::-1]
    return ''.join(map(str, parts))


INF = _inf()
K = 15


def _s(S):
    return INF[:K + 8]


def _col(S, i, v):
    return 'yellow' if i == K - 1 else None


def _text(S):
    if 'cnt' not in S:
        return f'无限字符串开头：`{INF[:30]}……`，要找第 `k = {K}` 位（黄色格）'
    k, cnt, ln = S['k'], S['cnt'], S['length']
    if 'x' not in S:
        return f'`cnt={cnt}`、`length={ln}`：这一段占 `cnt×length = {cnt * ln}` 位；当前偏移 `k={k}`'
    x = S['x']
    if 'tail' not in S:
        return f'答案在整数 `x={x}`（长 {ln}）里，位置偏移 `k % length = {k % ln}`'
    return f'`x={x}` 的第 `{k % ln}` 位（从 0、从高到低）= =={x // S["tail"] % 10}=='


CONFIG = dict(
    num=4022, title='无限字符串里第 K 个数字', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='按位数分段 + 块内翻转',
    tags=['灵神题单', '难度分 1915'],
    code='''
class Solution:
    def kthDigit(self, k: int) -> int:
        k -= 1  # k 改成从 0 开始，方便计算

        # 十进制长为 length 的正整数有 cnt = 9 * 10**(length-1) 个
        cnt, length = 9, 1
        while cnt * length <= k:
            k -= cnt * length  # 这里减小了 k
            cnt *= 10
            length += 1

        # 答案在正整数 x 中
        x = cnt // 9 + k // length
        if x // 10 % 2:
            # 改成递减顺序，例如 10 变成 19，11 变成 18 ……
            x += 9 - x % 10 * 2

        # 计算 x 从高到低第 k%length（从 0 开始）个数字
        tail = 10 ** (length - k % length - 1)
        return x // tail % 10
''',
    call='Solution().kthDigit(15)',
    expect=7,
    views=[
        dict(type='text', fn=_text, h=120, size=28),
        dict(type='string', var=_s, color=_col, h=200, cell=36, label='无限字符串的前缀（黄 = 第 k 位）'),
    ],
    watch=['k', ('cnt', 'cnt'), ('length', 'length', 'blue'), ('x', 'x', 'green')],
    captions={
        'k -= 1  #': '`k` 改成从 0 开始：`k = {k}`',
        'cnt, length = 9': '先看 1 位数：有 `cnt = 9` 个，每个长 `length = 1`',
        'while cnt * length': '这一段共 `{cnt}×{length} = {cnt * length}` 位，`k = {k}`：{"k 超出这一段，答案还在后面" if cnt * length <= k else "k 落在这一段里，停"}',
        'k -= cnt * length': '整段都不含答案，丢掉：`k` → {k}（相对下一段开头的偏移）',
        'cnt *= 10': '下一段的数多 10 倍：`cnt = {cnt}`',
        'length += 1': '长度加一：`length = {length}`',
        'x = cnt': '`x = 10^{length-1} + k // length = {cnt // 9} + {k // length}` = =={x}==（还没处理块内顺序）',
        'if x // 10': '`x // 10 = {x // 10}`：{"奇数块，数字是递减排列" if x // 10 % 2 else "偶数块，递增排列，x 不用改"}',
        'x += 9': '奇数块里 `x` 的个位 d 要换成 `9-d`：`x += 9 - 2d` → =={x}==',
        'tail =': '取 x 的第 `k % length = {k % length}` 位（从高到低）：`tail = 10^{length - k % length - 1} = {tail}`',
        'return': '`{x} // {tail} % 10` = =={ret}==',
    },
    cards=dict(
        one_liner='先按位数缩小范围，再算整数，最后处理奇数块翻转',
        complexity='时间 `O(log k)`，空间 `O(1)`',
        problem=['把所有正整数拼成无限字符串，但每 10 个数一块：偶数块递增、奇数块 ==递减==',
                 '开头是 `1..9`、`19..10`、`20..29`、`39..30`……',
                 '求第 `k` 位（`k ≤ 10^15`），示例 `k = 15` → `7`'],
        quote='十进制长为 length 的正整数，最高位不能填 0，有 9 种填法，其余 length-1 位有 10 种填法。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`length` 位数共 `9·10^(length-1)` 个，占 `cnt·length` 位：一段段减掉',
              '定位到第 `k // length` 个 `length` 位数 `x`',
              '若 `x // 10` 是奇数，所在块递减：个位 `d` 换成 `9-d`',
              '最后取 `x` 的第 `k % length` 位数字'],
        after=[dict(heading='验算 k = 15', lines=['`k = 14`：1 位数占 9 位，剩 `k = 5`',
                                                  '2 位数占 180 位，够了：`x = 10 + 5//2 = 12`',
                                                  '`12 // 10 = 1` 为奇数 → `x = 12 + 9 - 4 = 17`',
                                                  '取第 `5 % 2 = 1` 位 → `7`'])],
        summary=['时间 `O(log k)`，空间 `O(1)`',
                 '易错：先 `k -= 1` 改成从 0 开始，否则偏移错一位',
                 '易错：判断奇偶块用 `x // 10`，要在翻转 `x` 之前判断',
                 '同类题：400. 第 N 位数字（没有翻转）'],
    ),
)
