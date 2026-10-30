NUMS = [5, 3, 4, 1, 2, 0]


def _win_l(S):
    return max(0, S['i'] - S['k'] + 1) if 'i' in S else None


def _color(S, i, v):
    q = S.get('q')
    if not q or i not in q:
        return None
    return 'pink' if i == q[0] else 'purple'


def _draw_q(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'q（下标:值，队首 → 队尾单调递减；粉 = 队首 = 窗口最大值）', 24, T['muted'], bold=True)
    q = S.get('q')
    if q is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    bq = list(B.get('q') or [])
    x, y, h = x0 + 18, y0 + 46, 58
    for k, idx in enumerate(q):
        t = f'{idx}:{NUMS[idx]}'
        w = max(84, cv.tlen(t, 28, mono=True) + 32)
        cv.rect((x, y, x + w, y + h), fill=T['pink'] if k == 0 else T['purple'], r=10,
                outline=T['green'] if idx not in bq else T['border'], width=5 if idx not in bq else 1)
        cv.text((x + w / 2, y + h / 2), t, 28, T['bg'], anchor='mm', mono=True, bold=True)
        x += w + 12
    if not q:
        cv.text((x, y + h / 2), '空', 26, T['dim'], anchor='lm')
    gone = [i for i in bq if i not in q]
    if gone:
        cv.text((x + 16, y + h / 2), '移出：' + '，'.join(f'{i}:{NUMS[i]}' for i in gone), 24, T['red'], anchor='lm', bold=True)


def _while_cap(S, B, ret):
    if not B.q:
        return f'队列为空，新员工 `x = {B.x}` 直接入队'
    t = B.q[-1]
    if B.nums[t] <= B.x:
        return f'队尾 `nums[{t}] = {B.nums[t]}` ≤ `x = {B.x}`：新员工==不比老员工弱== → 裁掉老员工'
    return f'队尾 `nums[{t}] = {B.nums[t]}` > `x = {B.x}`：老员工更强，停止裁员'


CONFIG = dict(
    num=239, title='滑动窗口最大值', difficulty='Hard', category='子串',
    author='灵茶山艾府', technique='单调队列（降本增笑）',
    code='''
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ans = [0] * (len(nums) - k + 1)  # 窗口个数
        q = deque()  # 双端队列

        for i, x in enumerate(nums):
            # 1. 右边入
            while q and nums[q[-1]] <= x:
                q.pop()  # 维护 q 的单调性
            q.append(i)  # 注意保存的是下标，这样下面可以判断队首是否离开窗口

            # 2. 左边出
            left = i - k + 1  # 窗口左端点
            if q[0] < left:  # 队首离开窗口
                q.popleft()

            # 3. 在窗口左端点处记录答案
            if left >= 0:
                # 由于队首到队尾单调递减，所以窗口最大值就在队首
                ans[left] = nums[q[0]]

        return ans
''',
    call=f'Solution().maxSlidingWindow({NUMS}, 3)',
    expect=[5, 4, 4, 2],
    views=[
        dict(type='array', var='nums', label='nums',
             pointers={'i': 'blue'}, window=(_win_l, 'i'), color=_color,
             dim=lambda S, i, v: 'i' in S and not (S['i'] - S['k'] + 1 <= i <= S['i']), cell=90),
        dict(type='custom', draw=_draw_q, h=130),
        dict(type='array', var='ans', label='ans（每个窗口的最大值）',
             color=lambda S, i, v: 'green' if 'left' in S and (i < S['left'] or i == S['left'] and v == S['nums'][S['q'][0]]) else None, cell=80),
    ],
    watch=[('i', 'i', 'blue'), 'x', 'left', ('q', 'list(q)', 'purple')],
    captions={
        'ans = [0]': '一共 `n − k + 1 = {len(ans)}` 个窗口，先开好答案数组',
        'q = deque()': '双端队列 `q` 存==下标==：从队首到队尾，对应的值单调递减',
        'for i, x in enumerate': lambda S, B, ret: (f'新员工入职：`i = {S.i}`，`x = {S.x}`' if 'i' not in B or S.i != B.i
                                                    else '数组遍历完毕'),
        'while q and': _while_cap,
        'q.pop()': '`nums[{B.q[-1]}] = {nums[B.q[-1]]}` 比新人老、还不比新人强，==永远当不了最大值==，弹出队尾',
        'q.append(i)': '下标 `{i}` 入队尾（存下标，才能判断队首是否离开窗口）',
        'left = i - k + 1': lambda S, B, ret: (f'窗口是 `[{S.left}, {S.i}]`，左端点 `left = {S.i} − {S.k} + 1 = {S.left}`' if S.left >= 0
                                               else f'左端点 `left = {S.i} − {S.k} + 1 = {S.left}`，还是负数：窗口没满'),
        'if q[0] < left': lambda S, B, ret: (f'队首下标 `{B.q[0]}` < `left = {B.left}`：老员工 35 岁了，离开窗口' if B.q[0] < B.left
                                             else f'队首下标 `{B.q[0]}` ≥ `left = {B.left}`，还在窗口里'),
        'q.popleft()': '弹出队首 `{B.q[0]}`：窗口一步一步滑，==每轮最多出一个==，所以用 `if` 不用 `while`',
        'if left >= 0': lambda S, B, ret: ('`left ≥ 0`：窗口凑满 `k` 个了，记录答案' if B.left >= 0
                                           else f'`left = {B.left} < 0`：窗口还没凑满 `k` 个'),
        'ans[left] = nums[q[0]]': '队首到队尾单调递减 → ==最大值就在队首==：`ans[{left}] = nums[{q[0]}] = {ans[left]}`',
        'return ans': '返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='新人更强就裁老人，老人超龄也裁：队首永远是窗口最大值',
        complexity='时间 `O(n)`，空间 `O(min(k, U))`',
        problem=['大小为 `k` 的窗口从左滑到右，每次右移一位',
                 '返回==每个窗口里的最大值==',
                 '示例：`nums = [1,3,-1,-3,5,3,6,7], k = 3` → `[3,3,5,5,6,7]`',
                 '演示用 `nums = [5,3,4,1,2,0], k = 3` → `[5,4,4,2]`（能看到队首离开窗口）'],
        quote='如果新员工比老员工强（或者一样强），把老员工裁掉。如果老员工 35 岁了，也裁掉。裁员后，资历最老（最左边）的人就是最强的员工了。',
        quote_src='—— 灵茶山艾府题解「降本增笑」的比喻',
        idea=['==右边入==：新元素入队尾前，弹出所有 ≤ 它的（维护单调递减）',
              '==左边出==：队首下标 < 窗口左端点，就弹出',
              '==记录答案==：队首就是当前窗口的最大值'],
        summary=['时间 `O(n)`：每个下标最多入队一次、出队一次，`while` 总共只跑 `O(n)` 次',
                 '队列存==下标==而不是值，才能判断队首是否离开窗口',
                 '弹队尾用 `<=`：一样强的老员工也没用了',
                 '队首离开窗口用 `if` 即可：窗口每次只滑一格',
                 '单调队列三步套路：右边入 → 左边出 → 记录答案'],
    ),
)
