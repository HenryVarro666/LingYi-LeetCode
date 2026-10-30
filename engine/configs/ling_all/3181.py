VALS = [5, 2, 7, 2]
M = max(VALS)
NB = 2 * M          # 画 0 .. 2m-1 位


def _bits(n):
    return [i for i in range(n.bit_length()) if n >> i & 1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'f' not in S:
        cv.text((x0 + 18, y0 + 4), '二进制数 f：第 j 位为 1 = 能凑出总奖励 j（还没开始）', 22, T['muted'], bold=True)
        return
    f = S['f']
    old = B.get('f', f) if isinstance(B.get('f', f), int) else f
    v = S.get('v')
    line = S.get('_line')
    on_upd = line == 14 and isinstance(v, int)
    cv.text((x0 + 18, y0 + 4), '二进制数 f：第 j 位为 1 = 能凑出总奖励 j', 22, T['muted'], bold=True)
    cell = min(66, (x1 - x0 - 40) / NB)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * NB) / 2
    ys = y0 + 150
    ch = cell * 0.95
    low = (old & ((1 << v) - 1)) if on_upd else 0
    for j in range(NB):
        X = sx + j * cell
        is_on = bool(f >> j & 1)
        is_new = on_upd and is_on and not (old >> j & 1)
        is_low = on_upd and j < v and (old >> j & 1)
        fill = T['yellow'] if is_new else (T['blue'] if is_low else (T['green'] if is_on else T['panel2']))
        cv.rect((X + 3, ys, X + cell - 3, ys + ch), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), 1 if is_on else 0, 26, T['bg'] if fill != T['panel2'] else T['dim'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 8), j, 18, T['dim'], anchor='mt', mono=True)
    if on_upd:
        # 低 v 位（蓝）→ 左移 v 位 → 新增（黄）
        cv.rect((sx, ys - 10, sx + v * cell, ys + ch + 40), outline=T['blue'], width=3, r=10)
        cv.text((sx + v * cell / 2, ys - 18), f'低 {v} 位', 22, T['blue'], anchor='mb', bold=True)
        if low:
            hi = max(_bits(low))
            cv.arc_arrow((sx + (hi + 0.5) * cell, ys - 8), (sx + (hi + v + 0.5) * cell, ys - 8), 60, T['yellow'], 3)
            cv.text((sx + (hi + v / 2 + 0.5) * cell, ys - 96), f'左移 {v} 位', 22, T['yellow'], anchor='mb', bold=True)
    ans = f.bit_length() - 1
    cv.text((x0 + 18, ys + ch + 70), f'当前最大可达奖励：f.bit_length() - 1 = {ans}', 24, T['green'], bold=True)
    cv.text((x0 + 18, ys + ch + 108), f'上界 2m-1 = {2 * M - 1}（m = {M}），所以只画前 {NB} 位', 20, T['dim'])


def _cap_or(S, B, ret):
    v, old = S.v, B.f
    low = old & ((1 << v) - 1)
    lb = _bits(low)
    return (f'`v = {v}`：取 f 的低 {v} 位，可达 `{lb}`；整体左移 {v} 位 → `{[b + v for b in lb]}`；OR 回 f。'
            f'必须 `j < v` 才能再选 {v}（要求 {v} > 当前总奖励）')


CONFIG = dict(
    num=3181, title='执行操作可获得的最大总奖励 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='01 背包 · bitset 优化',
    tags=['难度分 2688'],
    code='''
class Solution:
    def maxTotalReward(self, rewardValues: List[int]) -> int:
        m = max(rewardValues)
        s = set()
        for v in rewardValues:
            if v in s:
                continue
            if v == m - 1 or m - 1 - v in s:
                return m * 2 - 1
            s.add(v)

        f = 1
        for v in sorted(s):
            f |= (f & ((1 << v) - 1)) << v
        return f.bit_length() - 1
''',
    call=f'Solution().maxTotalReward({VALS})',
    expect=12,
    skip=['for v in rewardValues'],
    views=[
        dict(type='array', var='rewardValues', label='rewardValues', h=130, cell=70,
             color=lambda S, i, v: 'blue' if S.get('v') == v and S.get('_line') in (5, 6, 7, 8, 10) else None),
        dict(type='set', var='s', label='s（去重后的奖励）', h=110, fmt=lambda x: str(x)),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('m', 'm', 'cyan'), ('v', 'v', 'blue'), ('f', 'bin(f)', 'green')],
    captions={
        'm = max': '`m = {m}`：最后一步选的一定是最大值 m，答案上界 `2m-1 = {2 * m - 1}`',
        's = set()': '重复的数不可能选两次（选了之后总奖励 ≥ 它自己），先去重',
        'if v in s': '看 `v = {v}`：已在 `s` 里？{"是，重复，跳过" if v in s else "否"}',
        'continue': '重复元素，直接跳过',
        'if v == m - 1': '优化三：若 `m-1` 能被凑出，答案就是 `2m-1`。检查 `v == {m - 1}` 或 `{m - 1 - v}` 在 `s` 中 → {"成立" if (v == m - 1 or m - 1 - v in s) else "不成立"}',
        's.add(v)': '`{v}` 加入 `s`：`s = {sorted(s)}`',
        'f = 1': '`f = 1`（二进制第 0 位为 1）：不选任何数，总奖励 0 可达',
        'for v in sorted(s)': lambda S, B, r: ('DP 结束' if S.v == max(S.s) and B.get('v') == S.v else f'从小到大考虑 `v = {S.v}`（先选大的就没法再选小的）'),
        'f |= ': _cap_or,
        'return f.bit_length()': '最高位是 `{f.bit_length() - 1}`：最大总奖励 =={ret}==，没有取到 `2m-1`',
    },
    max_steps=60,
    cards=dict(
        one_liner='从小到大选，用一个大整数的二进制位记录能凑出的奖励',
        complexity='时间 `O(nm/w)`，空间 `O(n + m/w)`',
        problem=['总奖励 `x` 从 0 开始，每次选未标记的 `rewardValues[i]`',
                 '只有它==严格大于当前 x== 才能加上去，求最大总奖励',
                 '示例：`[1,1,3,3]` → `4`；本视频：`[5,2,7,2]` → `12`'],
        quote='对于 rewardValues 中的数，如果先选大的，就没法再选小的，所以按照从小到大的顺序思考每个 rewardValues[i] 选或不选，这种做法是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序去重后做 0-1 背包：`f[j] = f[j] ∨ f[j-v]`，且 `v ≤ j < 2v`',
              '压成二进制数：取低 `v` 位、左移 `v` 位、OR 回去：`f |= (f & ((1<<v)-1)) << v`',
              '答案 = 最高位 = `f.bit_length() - 1`；优化三：`m-1` 可凑出就直接 `2m-1`'],
        summary=['时间 `O(nm/w)`，空间 `O(n + m/w)`',
                 '易错：只能用 `j < v` 的低位转移，否则会选到不比总奖励大的数',
                 '易错：先去重，再 sorted',
                 '优化二/三：包含 `m-1` 或有两数之和 `m-1`，答案必为 `2m-1`',
                 '相似题：1981. 最小化目标值与所选元素的差（bitset）'],
    ),
)
