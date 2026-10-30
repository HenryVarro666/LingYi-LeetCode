NUMS = [2, 3, 4, 2, 5]


def _txt(S):
    x = S.get('x')
    if x is None:
        return '`f[x][j]`：末尾奇偶性为 `x`、末尾恰好连续 `j+1` 个同奇偶的稳定子序列个数'
    p = '偶' if x == 0 else '奇'
    return f'当前数奇偶性 `x = {x}`（=={p}数==）：只有第 `{x}` 行会变，另一行原样保留'


def _cell(S, r, c, v):
    x = S.get('x')
    if x is None or S.get('_line', 0) < 8:
        return None
    return 'yellow' if r == x else None


CONFIG = dict(
    num=3686, title='稳定子序列的数量', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='奇偶性 + 末尾连续个数 DP',
    tags=['灵神题单', '动态规划', '难度分 1969'],
    code='''
class Solution:
    def countStableSubsequences(self, nums: list[int]) -> int:
        MOD = 1_000_000_007
        f = [[0, 0], [0, 0]]
        for x in nums:
            x %= 2
            f[x][1] = (f[x][1] + f[x][0]) % MOD
            f[x][0] = (f[x][0] + f[x ^ 1][0] + f[x ^ 1][1] + 1) % MOD
        return (f[0][0] + f[0][1] + f[1][0] + f[1][1]) % MOD
''',
    call=f'Solution().countStableSubsequences({NUMS})',
    expect=29,
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=80),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='table', var='f', label='f[x][j]：j=0 末尾连续 1 个，j=1 连续 2 个（黄行 = 本次更新的奇偶性）', h=240, cell=110,
             rows=['x=0 偶', 'x=1 奇'], cols=['j=0', 'j=1'],
             color=_cell),
    ],
    watch=[('x', 'x', 'pink'), ('f[0]', 'f[0]', 'blue'), ('f[1]', 'f[1]', 'orange')],
    captions={
        'MOD = ': '答案很大，每步取模 `10^9 + 7`',
        'f = [[0, 0]': '`f[x][j]`：末尾奇偶性 `x`，末尾==恰好==连续 `j+1` 个同奇偶数；初始全 0',
        'for x in nums': '按顺序处理每个数：选或不选',
        'x %= 2': '只关心奇偶性：`x = {x}`（{"偶" if x == 0 else "奇"}数）',
        'f[x][1] =': '末尾已有 1 个同奇偶的子序列，再接一个 → 连续 2 个：`f[{x}][1]` = =={f[x][1]}==（==先更新 j=1，因为它要用旧的 f[x][0]==）',
        'f[x][0] =': '不选保留原来的，加上接在==异奇偶==子序列后面的 `f[{x^1}][0] + f[{x^1}][1]`，再 +1（自己单独成序列）：`f[{x}][0]` = =={f[x][0]}==',
        'return': '四个状态加起来，就是所有稳定子序列个数 = =={ret}==',
    },
    cards=dict(
        one_liner='末尾的奇偶性 + 连续个数，决定能不能接新数',
        complexity='时间 `O(nk)`（`k = 2`），空间 `O(k)`',
        problem=['子序列中不存在连续三个奇偶性相同的元素，称为稳定子序列',
                 '求非空稳定子序列的个数，答案对 `10^9 + 7` 取模',
                 '示例：`[2,3,4,2]` → `14`；本视频：`[2,3,4,2,5]` → `29`'],
        quote='定义 f[i+1][x][j] 表示……子序列末尾元素的奇偶性为 x……子序列末尾恰好有连续 j+1 个奇偶性都为 x 的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['考虑 `nums[i]` 选或不选：不选，状态不变',
              '选：接在异奇偶子序列后面（连续数回到 1），或接在末尾只有 1 个同奇偶的后面（变成 2）',
              '接在已有 2 个同奇偶的后面会凑成三个，不允许；再 +1 是它自己单独成序列'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：压缩第一维后，要==先更新 `f[x][1]` 再更新 `f[x][0]`==，因为前者用旧的后者',
                 '奇偶性不同的那一行，`nums[i]` 一定不能选，保持不变',
                 '灵神还给了「写法二」：用四个变量替代 list，常数更小'],
    ),
)
