def _grp(S):
    if 'mn' not in S:
        return ''
    m = S.get('mass')
    return f'行星质量 `mass` = =={m}==' + ('；每组的最小值 `mn`、元素和 `sum_` 见下' if 'm' not in S else '')


CONFIG = dict(
    num=2126, title='摧毁小行星', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='按二进制长度分组 · 贪心',
    tags=['灵神题单', '位运算', '难度分 1335'],
    code='''
class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        max_width = max(asteroids).bit_length()
        mn = [inf] * max_width
        sum_ = [0] * max_width

        for x in asteroids:
            i = x.bit_length() - 1
            mn[i] = min(mn[i], x)
            sum_[i] += x

        for m, s in zip(mn, sum_):
            if m == inf:
                continue
            if mass < m:  # 无法摧毁这组的任意小行星
                return False
            mass += s  # 获得这组小行星的质量
        return True
''',
    call='Solution().asteroidsDestroyed(5, [4, 9, 24, 5])',
    expect=False,
    views=[
        dict(type='text', fn=_grp, size=26),
        dict(type='array', var='asteroids', label='asteroids（蓝 = 当前处理的小行星）', cell=96, h=190,
             pointers={'asteroids.index(x) if _line < 12 else None': 'blue'}, pointer_labels={'asteroids.index(x) if _line < 12 else None': 'x'}),
        dict(type='array', var='mn', label='mn[i]：二进制长度为 i+1 的组里最小的数', cell=96, h=190,
             pointers={'i': 'pink'}),
        dict(type='array', var='sum_', label='sum_[i]：这一组的元素和', cell=96, h=190, pointers={'i': 'pink'}),
    ],
    watch=[('mass', 'mass', 'green'), ('x', 'x', 'blue'), ('i', 'i', 'pink'), ('m', 'm', 'yellow'), ('s', 's')],
    captions={
        'max_width =': '最大的数 `{max(asteroids)}` 的二进制长度是 `{max_width}`，所以只需 {max_width} 个组',
        'mn = [inf] *': '`mn[i]` 记第 `i` 组的最小值，先填 `inf`',
        'sum_ = [0] *': '`sum_[i]` 记第 `i` 组的元素和',
        'for x in asteroids': lambda S, B, r: (f'遍历 `x = {S.x}`（二进制 `{S.x:b}`）' if S.x != B.get('x') or 'x' not in B
                                               else '遍历完，每组的最小值和元素和都有了'),
        'i = x.bit_length': '`{x}` 的二进制长度是 {i + 1} → 属于第 `{i}` 组，区间 [`{1 << i}`, `{1 << (i + 1)}`)',
        'mn[i] = min': '第 {i} 组最小值：`min({B.mn[i]}, {x})` = =={mn[i]}==',
        'sum_[i] += x': '第 {i} 组的和累加 `{x}` → =={sum_[i]}==',
        'for m, s in zip': lambda S, B, r: (f'按组从小到大处理：这一组最小值 `m = {S.m}`，总和 `s = {S.s}`' if 'm' not in B or S.m != B.m or S.s != B.s or S.m != S.mn[-1]
                                            else '所有组都处理完了'),
        'if m == inf': lambda S, B, r: ('`m = inf`：这一组没有小行星 → 跳过' if S.m == inf else f'这组有小行星（最小 {S.m}），继续'),
        'continue': '空组，直接看下一组',
        'if mass < m': lambda S, B, r: (f'`mass = {S.mass} < m = {S.m}`：连这组最小的都撞不碎 → ==行星被摧毁=='
                                         if S.mass < S.m else f'`mass = {S.mass} ≥ m = {S.m}`：能摧毁最小的，吃掉后质量更大 → 组内所有都能摧毁'),
        'mass += s': '组内所有小行星都被摧毁：`mass += {s}` → =={mass}==',
        'return False': '`mass` 不够摧毁这一组 → `False`',
        'return True': '所有组都过了 → `True`',
    },
    cards=dict(
        one_liner='先吃小的再吃大的；按二进制长度分组，免去排序',
        complexity='时间 `O(n + log U)`，空间 `O(log U)`',
        problem=['行星质量 `mass`，可按任意顺序撞小行星；`mass ≥ 小行星` 才能摧毁并吸收它',
                 '问能否摧毁所有小行星',
                 '本视频：`mass = 5, [4,9,24,5]` → `false`'],
        quote='一个 ≥ 2^k 的数，加上另一个 ≥ 2^k 的数，和一定 ≥ 2^(k+1)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['贪心：从小到大摧毁最划算（交换论证：逆序相邻对可以换成顺序）',
              '同一组 `[2^k, 2^(k+1))`：吃掉组内最小值后质量 ≥ 2^(k+1)，组内其余都能吃',
              '所以每组只需记 ==最小值== 和 ==元素和==，不必排序'],
        result='`mass` 积累到 22，撞不碎 23 → False ✓',
        after=[dict(heading='优化前：直接排序', lines=[
            '`asteroids.sort()` 后依次检查：`mass < x` 就返回 False，否则 `mass += x`',
            '时间 `O(n log n)`；正确性可用“交换逆序相邻对”或逆否命题证明',
            '灵神还给了用 `mask & -mask` 枚举组的位运算写法，时间 `O(n)`'])],
        summary=['时间 `O(n + log U)`，空间 `O(log U)`，`U` 是最大值',
                 '==分组内无需排序==：吃掉组内最小值，质量就超过组内任何数',
                 '空组的 `mn` 是 `inf`，别忘了 `continue` 跳过',
                 '`mass` 可能很大，Python 不会溢出；其他语言要用 64 位'],
    ),
)
