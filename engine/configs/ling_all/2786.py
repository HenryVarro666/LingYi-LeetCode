def _ix(S):
    return S['nums'].index(S['v']) if 'v' in S else -1


def _fv(S):
    if 'f' not in S:
        return '`f[j]`：从当前位置往后选，第一个数奇偶性为 `j` 时的最大得分'
    if 'v' not in S:
        return '`f[0]` = 偶数开头最大得分，`f[1]` = 奇数开头最大得分，初始都是 0'
    v, r = S['v'], S['v'] % 2
    return f"`f[{r}] = max(f[{r}], f[{r ^ 1}] − x) + {v}`（{'偶' if r == 0 else '奇'}数）"


CONFIG = dict(
    num=2786, title='访问数组中的位置使分数最大', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='倒着递推 · 奇偶状态机',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1733'],
    code='''
class Solution:
    def maxScore(self, nums: List[int], x: int) -> int:
        f = [0, 0]
        for v in reversed(nums):
            r = v % 2
            f[r] = max(f[r], f[r ^ 1] - x) + v
        return f[nums[0] % 2]
''',
    call='Solution().maxScore([2,3,6,1,9,4], 5)',
    expect=13,
    views=[
        dict(type='array', var='nums', label='nums（从右往左处理）', h=200, cell=90,
             color=lambda S, i, v: ('blue' if i == _ix(S) else None) if 'v' in S else None,
             dim=lambda S, i, v: 'v' in S and i < _ix(S)),
        dict(type='array', var='f', label='f[0]（偶数开头）  f[1]（奇数开头）', h=190, cell=120,
             color=lambda S, i, v: 'green' if 'r' in S and i == S['r'] and S.get('_line') == 6 else None),
        dict(type='text', fn=_fv, size=26, h=80),
    ],
    watch=[('v', 'v', 'blue'), ('r', 'r', 'cyan'), ('x', 'x', 'orange'), ('f', 'f', 'green')],
    captions={
        'f = [0, 0]': '`f[j]`：在已处理的后缀里选子序列、第一个数奇偶性为 `j` 的最大得分，初始 0',
        'for v in reversed': lambda S, B, r: ('`nums` 倒着看完了，`nums[0]` 必选，答案在 `f` 里取' if B.get('v') == S.nums[0] and S.v == S.nums[0] else f'倒着看 `v = {S.v}`：因为 `nums[0]` 必选，倒着递推初值和答案都更简单'),
        'r = v % 2': '`{v}` 是{"奇" if r else "偶"}数，`r = {r}`',
        'f[r] = max': ('`v = {v}` 一定要选（全是正数，选了不亏）：接同奇偶 `f[{r}] = {B.f[r]}`，或接不同奇偶 `f[{r ^ 1}] − x = {B.f[r ^ 1]} − {x}`；'
                       '取大再加 `v` → `f[{r}] = =={f[r]}==`'),
        'return f[': '答案取 `nums[0]` 的奇偶性：`f[{nums[0] % 2}] = {f[nums[0] % 2]}`',
    },
    cards=dict(
        one_liner='倒着递推：同奇偶白拿，换奇偶扣 x，只需维护两个状态',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从位置 0 出发只能往右跳，得分 `nums[i]`；相邻两次所跳位置奇偶性不同，扣 `x`',
                 '求最大总得分，`nums[0]` 一开始就算',
                 '示例：`[2,3,6,1,9,4], x=5` → `13`'],
        quote='因为 nums 中的元素都是正数，假如不选更优，那么在最终子序列的任意奇数前插入 nums[1]=3，不会减去 x，而又增加了得分，矛盾，所以一定要选。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `dfs(i, j)`：下标 `[i, n-1]` 中选子序列，首个数奇偶为 `j`',
              '`nums[i]` 奇偶符合 `j` 就==一定选==：`max(dfs(i+1,j), dfs(i+1,j^1)-x) + v`',
              '记忆化 → 1:1 翻译成递推 → 去掉第一维，只剩 `f[0]`、`f[1]`'],
        after=[dict(heading='其他写法', lines=['题解主推：`@cache` 记忆化搜索 → 二维 `f[i][j]` 递推 → 本视频的一维滚动数组',
                                              '写法 2 手写 `max` 更快，逻辑相同'])],
        summary=['时间 `O(n)`，空间 `O(1)`（记忆化 / 二维递推是 `O(n)`）',
                 '`nums[0]` 必选：倒着递推，答案取 `f[nums[0] % 2]`',
                 '`r ^ 1` 表示相反的奇偶性；换奇偶才减 `x`',
                 '易错：不匹配奇偶的状态无需更新（化简后 `f[j] = f[j]`）'],
    ),
)
