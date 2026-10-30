NUMS = [1, 1, 4, 2, 3]
X = 5


def _info(S):
    if 'now' not in S:
        return '找和为 `target = sum(nums) − x` 的==最短删除==：保留区间 `[l, r)` 越长越好' if 'target' in S else ''
    l, r = S['l'], S['r']
    rel = '<' if S['now'] < S['target'] else ('=' if S['now'] == S['target'] else '>')
    return f"区间 `[{l}, {r})` 和 `now = {S['now']}` {rel} `target = {S['target']}`" + (
        f"，删去 `n − (r − l) = {S['n'] - (r - l)}` 个" if rel == '=' else '')


def _expand(S, B, ret):
    if S.now < S.target and S.r < S.n:
        return f'`now = {S.now} < target = {S.target}` 且 `r < n` → ==向右扩展=='
    if S.now >= S.target:
        return f'`now = {S.now} ≥ target = {S.target}`：停止扩展'
    return f'`r = {S.r}` 已到 `n`：无法再扩展'


def _shrink(S, B, ret):
    if S.l < S.r and S.now > S.target:
        return f'`now = {S.now} > target = {S.target}` → ==移除左边界=='
    return f'`now = {S.now} ≤ target = {S.target}`：不用移除左边界'


def _eq(S, B, ret):
    if S.now == S.target:
        return f'`now == target = {S.target}`：保留 `[{S.l}, {S.r})`，删掉其余 `{S.n - (S.r - S.l)}` 个'
    return f'`now = {S.now} ≠ {S.target}`'


CONFIG = dict(
    num=1658, title='将 x 减到 0 的最小操作数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='转化为区间和 + 双指针',
    tags=['labuladong', '灵神题单·滑动窗口与双指针', '难度分 1817'],
    code='''
class Solution(object):
    def minOperations(self, nums, x):

        n = len(nums)
        target = sum(nums) - x
        if target == 0:
            return n
        elif target < 0:
            return -1

        res = -1
        l = 0
        r = 1
        now = nums[0]

        while l < n:
            while now < target and r < n:
                now += nums[r]
                r += 1

            if now < target and r == n:
                break

            while l < r and now > target:
                now -= nums[l]
                l += 1

            if now == target:
                if res == -1 or res > n - (r - l):
                    res = n - (r - l)
                now -= nums[l]
                l += 1

        return res
''',
    call=f'Solution().minOperations({NUMS}, {X})',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（框 = 保留区间 [l, r)，灰 = 要删去的前缀和后缀）', cell=110,
             pointers={'l': 'blue', 'r': 'pink'}, pointer_labels={'l': 'l 左闭', 'r': 'r 右开'}, window=('l', lambda S: S['r'] - 1),
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i < S['r'])),
        dict(type='text', fn=_info, size=28, h=90),
        dict(type='text', fn=lambda S: (f"目前最少删去 `res = {S['res']}` 个" if S.get('res', -1) >= 0
                                        else '还没找到合法区间（`res = -1`）') if 'res' in S else '', size=26, h=90),
    ],
    watch=[('n', 'n'), ('target', 'target', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'),
           ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'target = sum(nums) - x': '前缀 + 后缀的和 = `x` ⇔ 中间一段的和 = `{sum(nums)} − {x}` = =={target}==',
        'if target == 0': '`target = {target}`：不是 0，不必删光整个数组',
        'elif target < 0': '`target = {target}` 也不小于 0，删光整个数组也能凑够',
        'res = -1': '`res = -1` 表示还没有答案',
        'r = 1': '区间是左闭右开 `[l, r)`：`l = 0`，`r = 1`',
        'now = nums[0]': '此时区间和 `now = nums[0] = {now}`',
        'while l < n': lambda S, B, r: f'`l = {S.l} < n`，继续' if S.l < S.n else '`l` 到达 `n`，结束',
        'while now < target and r < n': _expand,
        'now += nums[r]': '加入 `nums[{r}] = {nums[r]}`，`now = {now}`',
        '                r += 1': '`r` → {r}',
        'if now < target and r == n': lambda S, B, r: (
            f'`now = {S.now} < target` 且 `r == n`：==后面的区间和不可能达到 target 了==' if S.now < S.target and S.r == S.n
            else '还有希望，继续'),
        'break': '退出循环',
        'while l < r and now > target': _shrink,
        25: '移出 `nums[{l}] = {nums[l]}`，`now = {now}`',
        'if now == target': _eq,
        'if res == -1 or res > n - (r - l)': lambda S, B, r: (
            f'`res = {S.res}`，`n − (r − l) = {S.n - (S.r - S.l)}` → ' + ('==更新答案==' if S.res == -1 or S.res > S.n - (S.r - S.l) else '不更好，不更新')),
        'res = n - (r - l)': '`res = {res}`',
        26: '左边界右移 → `l = {l}`',
        31: '以 `l` 为左边界再往右扩，和必然 > target → ==没有意义==，移出 `nums[{l}] = {nums[l]}`，`now = {now}`',
        32: '`l` → {l}，继续找下一个区间',
        'return res': '最少操作数 =={res}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='删去前缀 + 后缀 ⇔ 保留中间一段：找和为 sum − x 的最长区间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次从 `nums` 的最左或最右移除一个数，并从 `x` 中减去它',
                 '求把 `x` ==恰好==减到 0 的最小操作数，做不到返回 `-1`',
                 '示例：`nums = [1,1,4,2,3], x = 5` → `2`（删掉后两个）'],
        quote='将前缀和与后缀和视为从整个数组中去掉中间的连续一段……注意到这里nums中的数都非负，所以也可以使用双指针来做。往常都是用前缀和来实现的，这一次我选择了用双指针。',
        quote_src='—— yiduobo 题解原文',
        idea=['边界：`target = 0` 要删光，返回 `n`；`target < 0` 返回 `-1`',
              '区间 `[l, r)`：和不够就扩 `r`，和超了就缩 `l`',
              '和恰好为 `target` 时用 `n − (r − l)` 更新答案，再把 `l` 右移一位继续找'],
        summary=['时间 `O(n)`：`l`、`r` 都只往右走；空间 `O(1)`',
                 '区间是==左闭右开==，长度是 `r − l`',
                 '扩到 `r == n` 仍不够时可以直接 `break`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '作者另一思路：前缀和 + 哈希表记录每个前缀和首次出现的位置'],
    ),
)
