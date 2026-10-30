A, B = '1100011000', '0101001010'


def _col(S, k, v):
    if A[k] == B[k]:
        return None
    if 'i' in S and 'j' in S and S.get('_line', 0) >= 9 and k in (S['i'], S['j']):
        return 'blue' if k == S['i'] else 'pink'
    return 'orange'


def _fx(S):
    ln = S.get('_line', 0)
    if 'f0' not in S or ln < 8 or 'p' not in S:
        return '`f` 记录的是「把差异位置配好的最小花费 × 2」，这样 `x/2` 不用小数'
    f0, f1 = S['f0'], S['f1']
    if ln == 10 and 'i' in S:
        return f'配对 `p` 里相邻两个位置 `{S["i"]}` 和 `{S["j"]}`：花费翻倍 `f0 = {f0}`，`f1 = {f1}`（实际代价 = f ÷ 2）'
    return f'`f0 = {f0}`，`f1 = {f1}`；最后答案 = `f1 // 2`'


CONFIG = dict(
    num=2896, title='执行操作使两个字符串相等', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='差异位置序列 · O(n) 线性 DP',
    tags=['其他线性 DP', '多维 DP', '难度分 2172'],
    code='''
class Solution:
    def minOperations(self, s1: str, s2: str, x: int) -> int:
        if s1 == s2:
            return 0
        p = [i for i, (x, y) in enumerate(zip(s1, s2)) if x != y]
        if len(p) % 2:
            return -1
        f0, f1 = 0, x
        for i, j in pairwise(p):
            f0, f1 = f1, min(f1 + x, f0 + (j - i) * 2)
        return f1 // 2
''',
    call=f'Solution().minOperations({A!r}, {B!r}, 2)',
    expect=4,
    views=[
        dict(type='string', var=lambda S: A, label='s1（橙 = 与 s2 不同的位置，蓝/粉 = 正在配对的两个）', h=130, cell=70, color=_col),
        dict(type='string', var=lambda S: B, label='s2', h=130, cell=70, color=_col),
        dict(type='array', var=lambda S: S['p'] if 'p' in S and S.get('_line', 0) >= 6 else [], label='p：不同位置的下标', h=170, cell=90,
             color=lambda S, k, v: ('blue' if 'i' in S and v == S['i'] else 'pink' if 'j' in S and v == S['j'] else None) if S.get('_line', 0) >= 9 else None),
        dict(type='text', fn=_fx, size=26, h=80),
    ],
    watch=[('f0', 'f0', 'blue'), ('f1', 'f1', 'pink'), ('x', 'x', 'orange')],
    captions={
        'if s1 == s2': '先看两串是否已经相等：相等就不用操作，返回 0',
        'p = [i for': lambda S, B, r: f'把 `s1[i] ≠ s2[i]` 的下标收集到 `p` = `{S.p}`：只有这些位置要翻转',
        'if len(p) % 2': lambda S, B, r: (f'`len(p) = {len(S.p)}` 是奇数 → 每次操作都翻转两个位，1 的个数奇偶不变 → ==无解 -1==' if len(S.p) % 2
                                          else f'`len(p) = {len(S.p)}` 是偶数 → 一定有解，只需决定怎么配对'),
        'f0, f1 = 0, x': '`f0 = 0` 是空前缀；`f1 = x`：第一个位置先按「花 x 的任意操作」算，==整体放大 2 倍==，所以 `x/2` 记成 `x`',
        'for i, j in pairwise(p)': '看相邻两个差异位置 `{i}` 和 `{j}`（下标）',
        'f0, f1 = f1, min': lambda S, B, r: f'`f1 = min({B.f1} + {S.x}, {B.f0} + ({S.j} − {S.i}) × 2)` = =={S.f1}==：==任选两位花 x（每位 x/2）==，还是==相邻翻转 {S.j - S.i} 次（每次 1）==，取小',
        'return f1 // 2': '`f1 = {f1}`，放大了 2 倍 → 答案 `{f1} // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='只看不同的位置，相邻配对用 1 一步一步翻，远的用 x 一次翻',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s1`、`s2` 是等长二进制串，目标把 `s1` 变成 `s2`',
                 '操作一：任选两个下标翻转，代价 `x`；操作二：翻转相邻两位，代价 `1`',
                 '示例：`"1100011000"` → `"0101001010"`，`x = 2`，答案 `4`'],
        quote='把 s1[i] ≠ s2[i] 的下标统计到数组 p 中。如果 p 的长度是奇数，那么……无法操作，返回 -1。',
        quote_src='—— 灵茶山艾府题解（方法二：O(n) DP）',
        idea=['每次操作都会翻转两个字符，`1` 的个数奇偶不变，所以差异位置个数必须是偶数',
              '`f[i]` = 修好 `p` 前 `i` 个位置的最小花费：单独用操作一每个算 `x/2`，或和前一个配成相邻翻转 `p[i]−p[i−1]`',
              '为避开 `x/2`，把所有代价乘 2，最后 `// 2`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判断奇偶：`len(p)` 为奇数直接 `-1`',
                 '易错：`f` 里整体放大了 2 倍，返回时要 `// 2`',
                 '灵神还给了 `O(n²)` 的记忆化搜索写法（状态含免费翻转次数和是否被上一位翻转）',
                 '题解里「相邻位置逐步翻」的贪心是错的，如 `10000011000001`，反转首尾更优'],
    ),
)
