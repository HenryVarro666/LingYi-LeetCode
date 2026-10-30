def _I(S):
    return S['_inner'].get('i')


def _txt(S):
    I = S['_inner']
    if 'i' not in I or 'j' not in I:
        return '数位 DP：枚举盒子编号 `j`，数 `[low, high]` 里数位和恰为 `j` 的数'
    return (f"`dfs(i={I['i']}, j={I['j']}, limit_low={I.get('limit_low')}, limit_high={I.get('limit_high')})`："
            f"第 {I['i']} 位及之后还要凑出数位和 =={I['j']}==")


CONFIG = dict(
    num=1742, title='盒子中小球的最大数量', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（枚举数位和）',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        high_s = str(highLimit)
        n = len(high_s)
        low_s = str(lowLimit).zfill(n)  # 补前导零，和 high_s 对齐

        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（一行代码实现记忆化）
        def dfs(i: int, j: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:  # 填完了
                return 0 if j else 1

            lo = int(low_s[i]) if limit_low else 0
            hi = int(high_s[i]) if limit_high else 9

            res = 0
            for d in range(lo, min(hi, j) + 1):  # 枚举当前数位填 d，但不能超过 j
                res += dfs(i + 1, j - d, limit_low and d == lo, limit_high and d == hi)
            return res

        mx = int(high_s[0]) + (n - 1) * 9  # 数位和的上界
        return max(dfs(0, j, True, True) for j in range(1, mx + 1))
''',
    call='Solution().countBalls(19, 28)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='low_s', label='low_s（补前导零）', cell=64, h=130, pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='string', var='high_s', label='high_s', cell=64, h=130, pointers={_I: 'pink'}, pointer_labels={_I: 'i'}),
        dict(type='calls', h=300),
    ],
    skip=['res = 0', 'for d in range'],
    max_steps=48,
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('j', lambda S: S['_inner'].get('j'), 'pink'),
           ('lo', lambda S: S['_inner'].get('lo'), 'cyan'), ('hi', lambda S: S['_inner'].get('hi'), 'orange'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'low_s = ': '`low_s = {low_s!r}`：给下界补前导零，两个数逐位对齐',
        'if i == n': lambda S, B, r: ('`i == n`：数位填完' if S.i == S.n else f'`i = {S.i} < n = {S.n}`：还没填完，继续枚举这一位'),
        'return 0 if j else 1': '填完时剩余数位和 `j = {B.j}`：为 0 才恰好凑成目标和 → 返回 ==1==，否则 0',
        'lo = ': '下界：`limit_low` 为真则这一位至少是 `low_s[{i}]`，否则从 0 起：`lo = {lo}`',
        'hi = ': '上界：`limit_high` 为真则这一位至多是 `high_s[{i}]`，否则到 9：`hi = {hi}`；`d` 从 `{lo}` 枚举到 `min({hi}, {j})`',
        'res += dfs': '这一位填 `d = {B.d}`：剩余和变 `{B.j - B.d}`；仅当 `d` 贴着边界，约束才继续往下传',
        'return res': '这个状态能凑出的数有 `{res}` 个',
        'mx = ': '`mx = {mx}`：数位和的上界，最高位至多 `high_s[0]`，其余每位至多 9',
        'return max': '逐个 `j` 调用 `dfs(0, j, True, True)`，取最大值 → ==装球最多的盒子==',
    },
    cards=dict(
        result='返回 `2`：盒子 10 装了 19 和 28',
        one_liner='枚举盒子编号 j，数位 DP 数「数位和恰为 j」的小球',
        complexity='时间 `O(D²·log²high)`，空间 `O(D·log²high)`',
        problem=['`[lowLimit, highLimit]` 的小球，按数位和放进对应编号的盒子',
                 '求装球最多的盒子里有多少球',
                 '示例：`19..28` → 盒子 10 有 19 和 28 → `2`'],
        quote='核心思路：枚举数位和 j=1,2,3,…,45，计算 [lowLimit, highLimit] 中的数位和为 j 的数字个数。',
        quote_src='—— 灵茶山艾府题解（方法三：数位 DP）',
        idea=['`dfs(i, j, limit_low, limit_high)`：从第 `i` 位起，剩余数位和恰为 `j` 的方案数',
              '`limit_low / limit_high` 表示是否仍贴着上下界，贴着时这一位才受限',
              '填完 `n` 位且 `j == 0` 就是一个合法数字，计 1'],
        summary=['时间 `O(D²·log²high)`，`D = 10`；每个状态只算一次',
                 '下界要补前导零和上界对齐；前导零不影响数位和',
                 '易错：`d` 的上限是 `min(hi, j)`，不能让剩余和变负',
                 '方法一暴力枚举、方法二前缀和适合本题数据范围；数位 DP 是 `10^18` 进阶解法'],
    ),
)
