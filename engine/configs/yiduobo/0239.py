NUMS = [5, 3, 4, 1, 2, 0]


def _win(S):
    return (max(0, S['index'] - S['k'] + 1), S['index']) if 'index' in S else (None, None)


def _dead(S, i, v):
    return 'l' in S and i < S['l']


def _q_color(S, i, v):
    if 'l' in S and i == S['l'] and i < S.get('r', 0):
        return 'pink'
    return None


def _while_cap(S, B, ret):
    if not B.r > B.l:
        return f'队列空了（`r = l = {B.l}`），`{B.nums[B.index]}` 直接入队'
    if B.q[B.r - 1] < B.nums[B.index]:
        return f'队尾 `q[{B.r - 1}] = {B.q[B.r - 1]}` < `nums[{B.index}] = {B.nums[B.index]}`：它更靠左还更小 → 弹出'
    return f'队尾 `q[{B.r - 1}] = {B.q[B.r - 1]}` ≥ `{B.nums[B.index]}`，停止弹出'


CONFIG = dict(
    num=239, title='滑动窗口最大值', difficulty='Hard', category='子串',
    author='yiduobo', technique='单调队列（数组 + 双指针模拟）',
    code='''
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        q = []
        pos = []
        l = 0
        r = 0

        for index in range(k):
            while r > l and q[r - 1] < nums[index]:
                pos.pop()
                q.pop()
                r -= 1

            q.append(nums[index])
            pos.append(index)
            r += 1

        res = [q[0]]

        for index in range(k, len(nums)):
            if pos[l] + k == index:
                l += 1
            while r > l and q[r - 1] < nums[index]:
                pos.pop()
                q.pop()
                r -= 1

            q.append(nums[index])
            pos.append(index)
            r += 1
            res.append(q[l])

        return res
''',
    call=f'Solution().maxSlidingWindow({NUMS}, 3)',
    expect=[5, 4, 4, 2],
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'},
             window=(lambda S: _win(S)[0], lambda S: _win(S)[1]),
             dim=lambda S, i, v: 'index' in S and not (_win(S)[0] <= i <= _win(S)[1]), cell=66, h=172),
        dict(type='array', var='q', label='q（值）：只有 q[l:r] 有效，灰色 = 已从队首出队', pointers={'l': 'pink', 'r': 'cyan'},
             dim=_dead, color=_q_color, min_slots=6, cell=66, h=200),
        dict(type='array', var='pos', label='pos（对应下标）', dim=_dead, min_slots=6, cell=66, h=134),
        dict(type='array', var='res', label='res（每个窗口的最大值）', color=lambda S, i, v: 'green', min_slots=4, cell=60, index=False, h=110),
    ],
    skip=['pos.pop()', 'pos.append', 'pos = []', 'r = 0'],
    watch=[('index', 'index', 'blue'), ('l', 'l', 'pink'), ('r', 'r', 'cyan'), ('q[l:r]', 'q[l:r]', 'purple')],
    captions={
        'q = []': '用==数组 + 左右指针==模拟双端队列：`q` 存值，`pos` 存下标',
        'l = 0': '`l`、`r` 是队列左右边界，有效部分是 `q[l:r]`（左闭右开）',
        'for index in range(k)': lambda S, B, ret: (f'先处理第一个窗口：`index = {S.index}`' if 'index' not in B or S.index != B.index
                                                    else '第一个窗口的 `k` 个数处理完了'),
        'while r > l and': _while_cap,
        'q.pop()': '`{B.q[-1]}` 在 `{nums[index]}` 左边又更小：直到它滑出窗口，`{nums[index]}` 都还在 → ==它不可能成为最大值==',
        'r -= 1': '`pos` 同步弹出，右边界 `r` 左移到 {r}',
        'q.append(nums[index])': '`{nums[index]}` 压入队尾（`pos` 同步记下标 `{index}`）',
        'r += 1': '`r = {r}`，有效队列 `q[{l}:{r}] = {q[l:r]}`，从左到右递减',
        'res = [q[0]]': '第一个窗口：最大的数一定在栈底 `q[0] = {q[0]}`',
        'for index in range(k, len': lambda S, B, ret: (f'窗口右移一格：新来的 `nums[{S.index}] = {S.nums[S.index]}`'
                                                        if S.index != B.index else '窗口滑到头了'),
        'if pos[l] + k == index': lambda S, B, ret: (
            f'队首下标 `pos[l] = {S.pos[S.l]}`，`{S.pos[S.l]} + k = {S.index}`：==它刚好滑出窗口=='
            if S.pos[S.l] + S.k == S.index else f'队首下标 `pos[l] = {S.pos[S.l]}` 还在窗口里'),
        'l += 1': '左边界 `l` 右移到 {l}：相当于弹出队首（数组里的值不用真删）',
        'res.append(q[l])': '`q[l:r]` 从左到右递减 → ==q[l] 就是窗口最大值==：记录 `{q[l]}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='左边更小的数永远当不了最大值：弹掉它，队首就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['大小为 `k` 的窗口从左滑到右，每次右移一位',
                 '返回==每个窗口里的最大值==',
                 '示例：`nums = [1,3,-1,-3,5,3,6,7], k = 3` → `[3,3,5,5,6,7]`',
                 '演示用 `nums = [5,3,4,1,2,0], k = 3` → `[5,4,4,2]`'],
        quote='若存在x，y，满足l <= x < y <= r，且nums[x] < nums[y]，那么在窗口在持续往右滑动的过程中，nums[x]是一定不可能成为某个窗口的最大值的。',
        quote_src='—— yiduobo 题解原文',
        idea=['所以每来一个新数，就把栈里比它小的全弹出 → 栈底到栈顶递减，==栈底就是最大值==',
              '但栈底会滑出窗口：要从底部删，栈做不到 → ==改用双端队列==',
              'yiduobo 用==数组 + 左右指针 l、r== 模拟双端队列：`l += 1` 就是出队'],
        summary=['一趟扫描，每个数最多进出队列一次：时间 `O(n)`',
                 '`pos[l] + k == index` 判断队首是否刚滑出窗口（窗口每次只滑一格）',
                 '弹队尾用的是严格 `<`：相等的数会保留，结果一样',
                 '数组模拟时出队只移动 `l`，旧元素留在数组里，所以空间是 `O(n)`',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
