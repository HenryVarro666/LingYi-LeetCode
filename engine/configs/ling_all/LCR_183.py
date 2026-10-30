H = [5, 3, 4, 1, 2, 0, 3]


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
        t = f'{idx}:{H[idx]}'
        w = max(84, cv.tlen(t, 28, mono=True) + 32)
        cv.rect((x, y, x + w, y + h), fill=T['pink'] if k == 0 else T['purple'], r=10,
                outline=T['green'] if idx not in bq else T['border'], width=5 if idx not in bq else 1)
        cv.text((x + w / 2, y + h / 2), t, 28, T['bg'], anchor='mm', mono=True, bold=True)
        x += w + 12
    if not q:
        cv.text((x, y + h / 2), '空', 26, T['dim'], anchor='lm')
    gone = [i for i in bq if i not in q]
    if gone:
        cv.text((x + 16, y + h / 2), '移出：' + '，'.join(f'{i}:{H[i]}' for i in gone), 24, T['red'], anchor='lm', bold=True)


def _while_cap(S, B, ret):
    if not B.q:
        return f'队列为空，`{B.x}` 直接入队'
    t = B.q[-1]
    if B.heights[t] <= B.x:
        return f'队尾 `heights[{t}] = {B.heights[t]}` ≤ `x = {B.x}`：又早又矮，==不可能再当最大值== → 弹出'
    return f'队尾 `heights[{t}] = {B.heights[t]}` > `x = {B.x}`：队尾更高，停止弹出，保持单调递减'


CONFIG = dict(
    num='LCR 183', title='望远镜中最高的海拔', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调队列',
    tags=[],
    code='''
class Solution:
    def maxAltitude(self, heights: List[int], limit: int) -> List[int]:
        ans = []
        q = deque()  # 双端队列
        for i, x in enumerate(heights):
            # 1. 入
            while q and heights[q[-1]] <= x:
                q.pop()  # 维护 q 的单调性
            q.append(i)  # 入队
            # 2. 出
            if i - q[0] >= limit:  # 队首已经离开窗口了
                q.popleft()
            # 3. 记录答案
            if i >= limit - 1:
                # 由于队首到队尾单调递减，所以窗口最大值就是队首
                ans.append(heights[q[0]])
        return ans
''',
    call=f'Solution().maxAltitude({H}, 3)',
    expect=[5, 4, 4, 2, 3],
    views=[
        dict(type='array', var='heights', label='heights（蓝框 = 当前窗口，粉 = 队首）',
             pointers={'i': 'blue'}, window=(lambda S: max(0, S['i'] - S['limit'] + 1) if 'i' in S else None, 'i'), color=_color,
             dim=lambda S, i, v: 'i' in S and not (S['i'] - S['limit'] + 1 <= i <= S['i']), cell=90),
        dict(type='custom', draw=_draw_q, h=130),
        dict(type='array', var='ans', label='ans（每个窗口的最大值）', color=lambda S, i, v: 'green', cell=80),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('q', 'list(q)', 'purple')],
    captions={
        'ans = []': '`ans` 收集每个窗口的最大值',
        'q = deque()': '双端队列 `q` 存==下标==：队首到队尾，对应的高度单调递减',
        'for i, x in enumerate': lambda S, B, ret: (f'枚举右端点：`i = {S.i}`，`x = {S.x}`' if 'i' not in B or S.i != B.i
                                                    else '数组遍历完毕'),
        'while q and': _while_cap,
        'q.pop()': '弹出队尾 `{B.q[-1]}`（高度 {heights[B.q[-1]]}）：新元素又新又不矮，它再也成不了最大值',
        'q.append(i)': '下标 `{i}` 入队尾，队列仍单调递减',
        'if i - q[0] >= limit': lambda S, B, ret: (f'`i - q[0] = {B.i} - {B.q[0]} = {B.i - B.q[0]}` ≥ `limit = {B.limit}`：队首已离开窗口' if B.i - B.q[0] >= B.limit
                                                  else f'`i - q[0] = {B.i} - {B.q[0]} = {B.i - B.q[0]}` < `limit = {B.limit}`：队首还在窗口里'),
        'q.popleft()': '队首 `{B.q[0]}` 离开窗口，从队首弹出（窗口一次只滑一格，所以用 `if`）',
        'if i >= limit - 1': lambda S, B, ret: (f'`i = {B.i}` ≥ `limit - 1 = {B.limit - 1}`：窗口已满，可以记录答案' if B.i >= B.limit - 1
                                               else f'`i = {B.i}` < `limit - 1 = {B.limit - 1}`：窗口还没凑满 `limit` 个'),
        'ans.append(heights[q[0]])': '队首到队尾单调递减 → ==最大值就是队首==：追加 `heights[{q[0]}] = {heights[q[0]]}`',
        'return ans': '返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='入队尾时维护单调，队首离窗就出，答案永远看队首',
        complexity='时间 `O(n)`，空间 `O(min(k, U))`',
        problem=['`heights[i]` 是各位置海拔，窗口大小为 `limit`，从左滑到右',
                 '返回==每个窗口内的最高海拔==',
                 '示例：`[14,2,27,-5,28,13,39], limit = 3` → `[27,27,28,28,39]`',
                 '演示用 `[5,3,4,1,2,0,3], limit = 3` → `[5,4,4,2,3]`（能看到队首离窗）'],
        quote='单调队列套路：1. 入（元素进入队尾，同时维护队列单调性）2. 出（元素离开队首）3. 记录/维护答案（根据队首）',
        quote_src='—— 灵茶山艾府题解',
        idea=['==入==：新元素进队尾前，弹掉队尾所有 `≤ 它` 的下标',
              '==出==：`i - q[0] >= limit` 说明队首滑出了窗口，弹队首',
              '==记录==：窗口凑满后，队首对应的值就是窗口最大值'],
        summary=['时间 `O(n)`：每个下标至多入队、出队各一次，二重循环总次数是 `O(n)`',
                 '队列存==下标==而不是值，才能判断队首是否离开窗口',
                 '弹队尾用 `<=`：相等的老元素也没用了',
                 '同 239 题；课后作业 1438、2398、862、1499 都是单调队列'],
    ),
)
