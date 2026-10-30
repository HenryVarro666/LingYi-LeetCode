NUMS = [3, 1, 5]
P = [1] + NUMS + [1]
N = len(P)


def _in_frame_prev(S, B):
    """for 行：上一轮 cut_pos 是否属于当前这一层（而不是外层残留的变量）"""
    return 'cut_pos' in B and isinstance(B.get('cut_pos'), int) and B['left'] < B['cut_pos'] < B['right']


def _cap_for(S, B, ret):
    l, r = S.left, S.right
    head = ''
    if _in_frame_prev(S, B):
        k = B.cut_pos
        head = f'`cut_pos = {k}` 试完 → `f[{l}][{r}] = {B.f[l][r]}`；'
    if 'cut_pos' in S and S.cut_pos != B.get('cut_pos') or not _in_frame_prev(S, B):
        k = S.cut_pos
        return head + f'试==最后戳== `nums[{k}] = {P[k]}`'
    return head + '分割点都试完了'


def _cap_long(S, B, ret):
    l, r, k = B.left, B.right, B.cut_pos
    if (l, r) == (0, N - 1) and k == 1:
        return (f'`f[{l}][{k}] + f[{k}][{r}] + {P[l]}×{P[r]}×{P[k]}`：先递归戳光两段；最后戳 `{P[k]}` 时'
                f'两边邻居是 `{P[l]}`、`{P[r]}`')
    return f'`f[{l}][{k}] + f[{k}][{r}] + {P[l]}×{P[r]}×{P[k]}`：递归求两段'


def _cap_memo(S, B, ret):
    l, r = S.left, S.right
    v = S.f[l][r]
    if v is not None:
        return f'`f[{l}][{r}] = {v}` ==已经算过==，直接返回（记忆化）'
    return f'`f[{l}][{r}]` 还没算过 → 计算'


def _cap_base(S, B, ret):
    l, r = S.left, S.right
    if l >= r - 1:
        return f'`({l},{r})` 之间==没有气球== → `f[{l}][{r}] = 0`'
    return f'`({l},{r})` 中间还有气球 `{P[l + 1:r]}` → `f` 先置 0，枚举最后戳哪个'


def _text(S, B):
    if 'left' not in S:
        return '两端补 1：`nums = [1] + nums + [1]`，`f[i][j]` = 戳光 i、j 之间（不含 i、j）的最大硬币'
    l, r = S['left'], S['right']
    k = S.get('cut_pos')
    if isinstance(k, int) and l < k < r and S.get('_line') == 18:
        a, b = S['f'][l][k], S['f'][k][r]
        sa = '?' if a is None else a
        sb = '?' if b is None else b
        return f'`f[{l}][{r}]` 候选：`f[{l}][{k}] + f[{k}][{r}] + {P[l]}×{P[r]}×{P[k]}` = `{sa} + {sb} + {P[l] * P[r] * P[k]}`'
    cur = S['f'][l][r]
    return f'当前区间 `({l},{r})`：中间的气球 `{P[l + 1:r]}`，`f[{l}][{r}] = {"未知" if cur is None else cur}`'


def _cell_color(S, i, j, v):
    if 'left' not in S:
        return None
    l, r, k = S['left'], S['right'], S.get('cut_pos')
    if (i, j) == (l, r):
        return 'yellow'
    if isinstance(k, int) and l < k < r and ((i, j) == (l, k) or (i, j) == (k, r)):
        return 'cyan'
    if v is not None and j > i:
        return 'green' if v else None
    return None


def _nums_color(S, i, v):
    if 'left' not in S:
        return 'purple' if i in (0, N - 1) else None
    l, r, k = S['left'], S['right'], S.get('cut_pos')
    if isinstance(k, int) and l < k < r and i == k:
        return 'orange'
    if i in (l, r):
        return 'blue'
    return None


CONFIG = dict(
    num=312, title='戳气球', difficulty='Hard', category='多维动态规划',
    author='yiduobo', technique='区间 DP · 枚举最后戳的气球（记忆化搜索）',
    tags=['热题173'],
    code='''
class Solution(object):
    def maxCoins(self, nums):
        nums = [1] + nums + [1]
        f = [[None] * len(nums) for _ in range(len(nums))]

        return self.dfs(0, len(nums) - 1, f, nums)

    def dfs(self, left, right, f, nums):
        if f[left][right] is not None:
            return f[left][right]

        if left >= right - 1:
            f[left][right] = 0
            return f[left][right]

        f[left][right] = 0
        for cut_pos in range(left + 1, right):
            f[left][right] = max(f[left][right], self.dfs(left, cut_pos, f, nums) + self.dfs(cut_pos, right, f, nums) + nums[left] * nums[right] * nums[cut_pos])

        return f[left][right]
''',
    call=f'Solution().maxCoins({NUMS})',
    expect=35,
    views=[
        dict(type='text', fn=_text, size=25, h=64),
        dict(type='array', var=lambda S: S['nums'] if isinstance(S.get('nums'), list) and len(S['nums']) == N else P,
             label='nums（两端补 1；蓝 = 区间端点 left/right，橙 = 最后戳的 cut_pos）', cell=86, h=200,
             pointers={'left': 'blue', 'right': 'pink'}, color=_nums_color),
        dict(type='table', var='f', label='f[left][right]（黄 = 正在算，青 = 两个子区间，· = 未算）', h=250, cell=52,
             rows=lambda S: list(range(N)), cols=lambda S: list(range(N)), color=_cell_color),
        dict(type='calls', h=130, hide=('f', 'nums')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cut_pos', 'cut_pos', 'orange')],
    skip=['f = [[None]', 10, 13, 14, 16],
    captions={
        'nums = [1] + nums': '两端补上虚拟的 `1`：`nums = {nums}`，戳到边上时邻居就是 1',
        'return self.dfs(0': f'答案是 `f[0][{N - 1}]`：戳光 0 和 {N - 1} 之间的所有气球',
        'if f[left][right] is not None': _cap_memo,
        'if left >= right - 1': _cap_base,
        13: '`f[{left}][{right}] = 0`',
        14: '返回 0',
        16: '`f[{left}][{right}]` 先设为 0，下面枚举最后戳哪个',
        'for cut_pos in range': _cap_for,
        'f[left][right] = max': _cap_long,
        'return f[left][right]': lambda S, B, ret: f'`f[{S.left}][{S.right}] = {ret}` 算好，返回',
    },
    max_steps=50,
    cards=dict(
        one_liner='f[i][j] = 戳光 i、j 之间的气球的最大硬币；枚举最后戳的那一个',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['`n` 个气球，戳破第 `i` 个得到 `nums[i-1] × nums[i] × nums[i+1]` 枚硬币',
                 '戳破后左右两个气球变成相邻；越界的位置当作数字 `1`',
                 '求戳破所有气球能获得的最多硬币',
                 f'示例：`[3,1,5,8]` → `167`；本视频：`{NUMS}` → `35`'],
        quote='这里表示的则是==从i到j这一段戳剩下i和j之后最大的硬币数==，那么直接枚举分割点cut_pos……==最后戳cut_pos==',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]`：只保留 i、j，把中间全戳光的最大收益',
              '枚举中间==最后一个==戳的 `cut_pos`：它两边早就被戳光，邻居恰好是 `nums[i]`、`nums[j]`',
              '`f[i][j] = max(f[i][cut] + f[cut][j] + nums[i]×nums[j]×nums[cut])`',
              '两侧补 1 正好适配；`j - i ≤ 1` 时中间没气球，`f = 0`'],
        result='`f[0][4] = 35`：先戳 1（3×1×5），再戳 3（1×3×5），最后戳 5（1×5×1）',
        summary=['时间 `O(n^3)`：`O(n^2)` 个区间，每个枚举 `O(n)` 个分割点',
                 '关键：枚举==最后==戳的，而不是第一个戳的，左右两段才互不影响',
                 '原文用记忆化搜索；也可以按区间长度从短到长递推',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改'],
    ),
)
