def _x(S):
    l = S.get('left')
    return S['nums'][l] if l is not None and 'x' in S else None


def _col(S, i, v):
    l = S.get('left')
    if l is None or 'x' not in S:
        return None
    if i == l:
        return 'yellow'
    return 'green' if v == S['x'] else None


def _txt(S):
    if 'cp' not in S:
        return '总方案 `C(n,5)` 减去「x 不是唯一众数」的方案，按 x 的个数和另一个数 y 分类'
    if 'px' not in S:
        return '先准备 6 个和式：内层「枚举 y」的循环被压成 `O(1)`'
    px, sx, left = S['px'], S['sx'], S['left']
    right = len(S['nums']) - 1 - left
    return (f'x = {S["x"]}：左边 `{left}` 个（x 占 `{px}`），右边 `{right}` 个（x 占 `{sx}`）；'
            f'当前 `ans = {S["ans"]}`')


CONFIG = dict(
    num=3395, title='唯一中间众数子序列 I', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='枚举中间数 + 式子变形 O(n)',
    tags=['灵神题单', '组合计数', '难度分 2800'],
    code='''
class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        suf = Counter(nums)
        pre = defaultdict(int)
        ans = comb(n, 5)  # 所有方案数

        cp = ps = p2s = ps2 = 0
        cs = sum(comb(c, 2) for c in suf.values())

        # 枚举 x，作为子序列正中间的数
        for left, x in enumerate(nums[:-2]):
            suf[x] -= 1

            px = pre[x]
            sx = suf[x]

            cs -= sx
            ps -= px
            p2s -= px * px
            ps2 -= (sx * 2 + 1) * px

            right = n - 1 - left
            ans -= comb(left - px, 2) * comb(right - sx, 2)
            ans -= (cp - comb(px, 2)) * sx * (right - sx)
            ans -= (cs - comb(sx, 2)) * px * (left - px)
            ans -= ((ps - px * sx) * (right - sx) - (ps2 - px * sx * sx)) * px
            ans -= ((ps - px * sx) * (left - px)  - (p2s - px * px * sx)) * sx

            cp += px
            ps += sx
            ps2 += sx * sx
            p2s += (px * 2 + 1) * sx

            pre[x] += 1

        return ans % 1_000_000_007
''',
    setup='from math import comb',
    call='Solution().subsequencesWithMiddleMode([1, 2, 2, 2, 1, 3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前中间数 x，绿 = 其他的 x）', color=_col, cell=84, h=170,
             pointers={'left': 'yellow'}),
        dict(type='map', var='pre', label='pre：x 左边各数的个数', h=150, font=26),
        dict(type='map', var='suf', label='suf：x 右边各数的个数', h=150, font=26),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=['px', 'sx', 'cp', 'cs', 'ps', 'p2s', 'ps2', ('ans', 'ans', 'green')],
    skip=['px = pre[x]', 'ps -= px', 'p2s -= px * px', 'ps2 -= (sx', 'right = n - 1', 'ps += sx', 'ps2 += sx * sx', 'p2s += (px'],
    max_steps=110,
    captions={
        'ans = comb(n, 5)': '先假设全部合法：`C({n}, 5) = {ans}`，后面把「不合法」的减掉',
        'cp = ps = p2s': '四个和式从 0 开始：开始时左边什么都没有，`pre` 全是 0',
        'cs = sum': '`cs` = 对每个数 y 的 `C(suf_y, 2)` 求和 = `{cs}`',
        'for left, x': '枚举 `nums[{left}] = {x}` 作为正中间的数 x（最后两位右边不够，不枚举）',
        'suf[x] -= 1': '`x` 自己是中间那个，不能算进右边：`suf[{x}]` 减 1 → {suf[x]}',
        'sx = suf[x]': '`px` = x 左边的 x 个数 = {px}，`sx` = x 右边的 x 个数 = {sx}（先把 x 自己从右边扣掉）',
        'cs -= sx': '`suf_x` 少 1，四个和式 `cs/ps/p2s/ps2` 跟着扣掉 x 的那一项',
        'ans -= comb(left - px': '只有一个 x：左右各从「非 x」里选 2 个 → 减去 `C({left-px},2)·C({right-sx},2)`，`ans = {ans}`',
        'ans -= (cp': '两个 x，左边两个 y：对所有 y≠x 一次算完 → `ans = {ans}`',
        'ans -= (cs': '两个 x，右边两个 y：`cs` 去掉 y=x 那项 → `ans = {ans}`',
        'ans -= ((ps - px * sx) * (right': '左右各一个 y，另一个 x 在左边：用 `ps`、`ps2` → `ans = {ans}`',
        'ans -= ((ps - px * sx) * (left': '左右各一个 y，另一个 x 在右边：用 `ps`、`p2s` → `ans = {ans}`',
        'cp += px': '`pre_x` 要加 1，`cp/ps/ps2/p2s` 同步加上增量；`cp={cp}`',
        'pre[x] += 1': 'x 走到左边：`pre[{x}]` → {pre[x]}',
        'return ans': '答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='总数减不合法：枚举中间数 x，把内层枚举 y 变成 O(1) 的和式',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['长度为 5 的子序列，若中间元素是==唯一众数==（出现次数严格最多）就合法',
                 '求 `nums` 中合法子序列的个数，模 `10^9+7`',
                 '示例：`[1,1,1,1,1,1]` → `6`；本视频：`[1,2,2,2,1,3]` → `3`'],
        quote='总方案数为组合数 C(n,5)，减去不合法的方案数，即为答案。枚举不合法子序列正中间的数 x，分类讨论。',
        quote_src='—— 灵茶山艾府题解',
        idea=['正难则反：不合法 = 只有 1 个 x，或只有 2 个 x 且另有 y 出现 ≥ 2 次',
              '2 个 x 的情况按 y 在左右的分布分 4 种，每种都是「对 y 求和」',
              '把和式拆成 `Σ_y − (y=x 的项)`，用 6 个变量 O(1) 维护 `Σ`'],
        summary=['时间 `O(n)`：方法一枚举 y 是 `O(n²)`，本视频用方法二的式子变形',
                 '`suf[x] -= 1` 必须先做：中间的 x 不属于左右任何一边',
                 '`pre`、`suf` 变化时，和式的增量要按 `(s+1)² − s²` 这类差分算准',
                 '思考题：众数位置或子序列长度改变时，分类讨论同理'],
    ),
)
