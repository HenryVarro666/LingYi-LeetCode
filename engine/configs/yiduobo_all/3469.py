NUMS = [6, 2, 8, 4, 5, 3]


def _cell(S, r, c, v):
    I = S.get('_inner') or {}
    if 'r' in I and 'pre' in I and (r, c) == (I['r'], I['pre']):
        return 'yellow'
    return None


def _txt(S):
    I = S.get('_inner') or {}
    if 'r' not in I:
        return '`f[r][pre]`：已做 `r` 轮、只剩下标 `pre` 的数时，清空数组还要的最小代价'
    r, pre = I['r'], I['pre']
    return f'`r = {r}`、`pre = {pre}`：参与本轮的另外两个数是 `nums[{2 * r + 1}]`、`nums[{2 * r + 2}]`（下标 `x`、`y`）'


def _cap_none(S, B, ret):
    I = S._inner
    if S.f[I['r']][I['pre']] is not None:
        return f'`f[{I["r"]}][{I["pre"]}] = {S.f[I["r"]][I["pre"]]}` 已经算过 → ==记忆化命中==，直接返回'
    return f'`f[{I["r"]}][{I["pre"]}]` 还是 `None` → 没算过，进入计算'


def _cap_x(S, B, ret):
    I = S._inner
    return f'`x = {I["r"]} * 2 + 1 = {I["x"]}`：除了留下的 `nums[pre]`，第二个参与的数'


CONFIG = dict(
    num=3469, title='移除所有数组元素的最小代价', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='记忆化搜索：轮次 r + 留下的下标 pre',
    tags=['难度分 2112'],
    code='''
class Solution(object):
    def minCost(self, nums):
        
        n = len(nums)
        rnd = (n - 1) // 2 + 1
        if (n - 1) % 2 == 0:
            rnd += 1

        f = [[None] * n for _ in range(rnd)]

        def calc(r, pre, f):
            if f[r][pre] is None:
                x = r * 2 + 1
                y = r * 2 + 2
                if x >= n:
                    f[r][pre] = nums[pre]
                elif y >= n:
                    f[r][pre] = max(nums[pre], nums[x])
                else:
                    f[r][pre] = min(calc(r + 1, pre, f) + max(nums[x], nums[y]), \\
                                    calc(r + 1, y, f) + max(nums[x], nums[pre]), \\
                                    calc(r + 1, x, f) + max(nums[y], nums[pre]))
            
            return f[r][pre]
        
        return calc(0, 0, f)
''',
    call=f'Solution().minCost({NUMS})',
    expect=16,
    max_steps=50,
    views=[
        dict(type='text', size=26, h=80, fn=_txt),
        dict(type='array', var='nums', label='nums', h=195, cell=90, index=True),
        dict(type='table', var='f', label='f[r][pre]（黄 = 当前这次调用的格子）', h=300, cell=80,
             rows=lambda S: [f'r={k}' for k in range(len(S['f']))], cols=lambda S: [str(k) for k in range(len(S['nums']))], color=_cell),
        dict(type='calls', h=250),
    ],
    watch=[('r', 'r', 'pink'), ('pre', 'pre', 'blue'), ('x', 'x', 'cyan'), ('y', 'y', 'purple')],
    captions={
        'n = len': '`n = {n}`',
        'rnd = (n - 1)': '总轮数：每轮拿走 2 个数，先算 `(n-1)//2 + 1 = {rnd}`',
        'rnd += 1': '`n - 1` 是偶数 → 最后还会剩一个数要单独删，轮数 `+1`',
        'f = [[None]': '`f[r][pre]`：已经操作 `r` 轮、留下 `nums[pre]` 时，还需要的代价；`None` = 还没算',
        'if f[r][pre] is None': _cap_none,
        'x = r * 2 + 1': _cap_x,
        'y = r * 2 + 2': '`y = r * 2 + 2 = {y}`：第三个参与的数',
        'if x >= n': lambda S, B, r: (f'`x = {S._inner["x"]} ≥ n`：只剩 `nums[pre]` 一个数 → 直接删，代价 `nums[{S._inner["pre"]}]`' if S._inner['x'] >= S.n
                                      else f'`x = {S._inner["x"]} < n`：至少还有两个数，继续看 `y`'),
        'elif y >= n': lambda S, B, r: (f'`y = {S._inner["y"]} ≥ n`：只剩 `nums[pre]` 和 `nums[x]` 两个 → 一次性删，代价 `max`' if S._inner['y'] >= S.n
                                        else f'`y = {S._inner["y"]} < n`：三个数都在，三选二'),
        'f[r][pre] = nums[pre]': '`f[{r}][{pre}] = nums[{pre}]` = =={nums[pre]}==',
        'f[r][pre] = max': '`f[{r}][{pre}] = max(nums[{pre}], nums[{x}])` = =={f[r][pre]}==',
        'f[r][pre] = min': lambda S, B, ret: (f'`f[{B._inner["r"]}][{B._inner["pre"]}]` = 三者最小 ==`{S.f[B._inner["r"]][B._inner["pre"]]}`==，记进表里'
                                              if S._inner.get('r') == B._inner['r'] and S.f[B._inner['r']][B._inner['pre']] is not None
                                              else f'先递归第一项：==留下 pre==（`pre = {B._inner["pre"]}`），`calc({B._inner["r"] + 1}, {B._inner["pre"]}, f)`，本轮删 `x, y`，代价 `max(nums[x], nums[y])`'),
        'calc(r + 1, y, f)': '再递归第二项：删 `x` 和 `pre`，==留下 y==，进入 `calc(r + 1, y, f)`，代价 `max(nums[x], nums[pre])`',
        'calc(r + 1, x, f)': '最后第三项：删 `y` 和 `pre`，==留下 x==，进入 `calc(r + 1, x, f)`，代价 `max(nums[y], nums[pre])`',
        'return f[r][pre]': '返回 `f[{r}][{pre}]` = =={ret}==',
        'return calc(0, 0, f)': '入口 `calc(0, 0, f)`：做了 0 轮、留下 `nums[0]`',
    },
    cards=dict(
        one_liner='做了 r 轮后，只要知道留下哪个下标，就知道下一轮是哪三个数',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['每步从 `nums` 前三个里选两个移除，花费 ==较大值==',
                 '不足三个时一次移除全部，花费剩余最大值',
                 '求移除所有元素的最小总成本；本视频 `[6,2,8,4,5,3]` → `16`'],
        quote='只需要保留操作的轮次rnd以及剩余元素的下标pre，就可以唯一确定下一轮操作时参与操作的三个元素是什么',
        quote_src='—— yiduobo 题解原文',
        idea=['`r` 轮后前 `2r+1` 个数里只剩 1 个（下标 `pre`），第二、第三个就是 `nums[2r+1]`、`nums[2r+2]`',
              '三选二：删 `x,y` 留 `pre`；删 `x,pre` 留 `y`；删 `y,pre` 留 `x`',
              '`x >= n` 只剩一个；`y >= n` 剩两个，直接删光；其余递归 + 记忆化'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`（`f` 有 `rnd × n` 个格子）',
                 '易错：轮数 `rnd` 要考虑 `n` 的奇偶，奇偶不同末尾剩的个数不同',
                 '记忆化用 `None` 表示未计算，所以要区分 0 与未算',
                 '对比灵神：灵神状态是后缀起点 `i` 和落单下标 `j`；这里用轮次 `r` 代替 `i`（`i = 2r + 1`）'],
    ),
)
