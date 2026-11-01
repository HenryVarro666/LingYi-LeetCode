def _txt(S):
    if 'f' not in S:
        return '`f[0]`、`f[1]`、`f[2]` 分别是：全 0 / 先 0 后 1 / 特殊子序列 的个数'
    f = S['f']
    v = S.get('v')
    if v is None:
        return f'`f = {f}`'
    if v == 0:
        return f'遇到 `0`：`f[0] = 2 × f[0] + 1`，当前 `f = {f}`'
    if v == 1:
        return f'遇到 `1`：`f[1] = 2 × f[1] + f[0]`，当前 `f = {f}`'
    return f'遇到 `2`：`f[2] = 2 × f[2] + f[1]`，当前 `f = {f}`'


CONFIG = dict(
    num=1955, title='统计特殊子序列的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 2125'],
    code='''
mod = 10 ** 9 + 7

class Solution:
    def countSpecialSubsequences(self, nums: List[int]) -> int:
        f = [0] * 3
        for v in nums:
            if v == 0:
                f[0] = (f[0] * 2 + 1) % mod
            elif v == 1:
                f[1] = (f[1] * 2 + f[0]) % mod
            else:
                f[2] = (f[2] * 2 + f[1]) % mod
        return f[2]
''',
    call='Solution().countSpecialSubsequences([0, 1, 2, 0, 1, 2])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（依次取出 v）', cell=84, h=170,
             color=lambda S, i, v: None),
        dict(type='array', var='f', label='f[0] 全0  /  f[1] 先0后1  /  f[2] 特殊子序列', cell=130, h=200,
             color=lambda S, i, v: 'yellow' if S.get('v') == i and S.get('_line', 0) in (7, 8, 9, 10, 11, 12) else ('green' if i == 2 and v else None)),
        dict(type='text', fn=_txt, size=26, h=100),
    ],
    watch=[('v', 'v', 'blue'), ('f', 'f', 'green')],
    captions={
        'f = [0] * 3': '`f` 是压缩掉第一维的 DP：三个状态都从 0 个开始',
        'for v in nums': '取下一个数（`v` 现在是 {v}）：它只会更新 `f[v]`，其余状态原样保留；取完就结束循环',
        'v == 0': '`v` 是 `0` 吗：{v == 0}',
        'v == 1': '`v` 是 `1` 吗：{v == 1}',
        'f[0] = (': '选或不选这个 0：不选 `f[0]`，选则可单独成序列或接在前面 → `f[0] = 2 × {B.f[0]} + 1` = =={f[0]}==',
        'f[1] = (': '选或不选这个 1：选的话接在已有的 1 后，或接在全 0 序列后 → `f[1] = 2 × {B.f[1]} + {f[0]}` = =={f[1]}==',
        'f[2] = (': '选或不选这个 2：选的话接在已有的 2 后，或接在“先0后1”后 → `f[2] = 2 × {B.f[2]} + {f[1]}` = =={f[2]}==',
        'return f[2]': '答案是 `f[2]`：以 2 结尾的特殊子序列个数 = =={ret}==',
    },
    cards=dict(
        one_liner='三个状态：全0、先0后1、特殊序列，遇到谁更新谁',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['特殊序列：正整数个 `0`，接着正整数个 `1`，最后正整数个 `2`',
                 '数组 `nums` 只含 `0`、`1`、`2`，求不同特殊子序列的数目（对 `10^9+7` 取余）',
                 '下标集合不同就算不同',
                 '示例：`nums = [0,1,2,0,1,2]` → `7`'],
        quote='若 j = nums[i] 则需要分类计算：……选 0 时，可以单独组成一个子序列，也可以与前面的 0 组合，因此有 f[i][0] = f[i-1][0] + 1，两者相加得 f[i][0] = 2·f[i-1][0] + 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` 表示前 `i` 项得到的三类子序列个数',
              '`j ≠ nums[i]`：直接继承 `f[i-1][j]`',
              '`j = nums[i]`：选或不选，相加得到 `2·f + 前一类`',
              '第一维只依赖上一项，压缩成长度 3 的数组'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`const mod` 对应顶层的 `mod`）',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：遇到 `0` 要 `+1`（单独成序列），`1`、`2` 则加上前一类的个数',
                 '每步都要对 `10^9+7` 取余',
                 '同类状态机 DP：按顺序拼出一个固定模式的子序列'],
    ),
)
