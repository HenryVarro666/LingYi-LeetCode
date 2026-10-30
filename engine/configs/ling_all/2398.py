_CT = [3, 6, 1, 3, 4]
_RC = [2, 1, 3, 4, 5]


def _cost(S):
    if 'right' not in S or not S.get('q'):
        return ''
    n = S['right'] - S['left'] + 1
    m = S['chargeTimes'][S['q'][0]]
    tot = m + n * S['s']
    ok = '≤' if tot <= S['budget'] else '>'
    return f"总开销 = max `{m}` + 长度 `{n}` × 运行和 `{S['s']}` = =={tot}== {ok} budget {S['budget']}"


CONFIG = dict(
    num=2398, title='预算内的最多机器人数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='不定长滑窗 + 单调队列',
    tags=['单调队列', '滑动窗口', '难度分 1917'],
    code='''
class Solution:
    def maximumRobots(self, chargeTimes: List[int], runningCosts: List[int], budget: int) -> int:
        ans = s = left = 0
        q = deque()
        for right, (t, c) in enumerate(zip(chargeTimes, runningCosts)):
            # 1. 入
            while q and t >= chargeTimes[q[-1]]:
                q.pop()
            q.append(right)
            s += c  # 维护 sum(runningCosts)

            # 2. 出
            while q and chargeTimes[q[0]] + (right - left + 1) * s > budget:
                if q[0] == left:
                    q.popleft()
                s -= runningCosts[left]  # 维护 sum(runningCosts)
                left += 1

            # 3. 更新答案
            ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().maximumRobots([3,6,1,3,4], [2,1,3,4,5], 25)',
    expect=3,
    views=[
        dict(type='text', fn=_cost, h=64),
        dict(type='array', var='chargeTimes', label='chargeTimes（充电时间）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), h=190),
        dict(type='array', var='runningCosts', label='runningCosts（运行开销）', pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), h=190),
        dict(type='queue', var='q', label='单调队列 q（下标:充电时间，队首最大）', fmt=lambda i: f'{i}:{_CT[i]}', h=130),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = s = left': '`ans`、`s`（窗口运行开销和）、`left` 都从 0 开始',
        'q = deque()': '队列里存==下标==，这样才能判断队首是否已经滑出窗口',
        'for right, (t, c)': '枚举右端点 `right = {right}`：充电 `{t}`，运行 `{c}`',
        'while q and t >=': lambda S, B, r: (
            f'新来的 `{S.t}` ≥ 队尾 `{S.chargeTimes[S.q[-1]]}`：队尾又老又弱，永远当不了最大值 → ==弹掉=='
            if S.q and S.t >= S.chargeTimes[S.q[-1]] else '队尾比新来的大（或队列空）→ 停止弹出'),
        'q.append(right)': '`{right}` 入队：队首到队尾的充电时间严格递减，==队首 = 窗口最大值==',
        's += c': '`s += {c}` → 窗口运行开销和 =={s}==',
        'while q and chargeTimes[q[0]]': lambda S, B, r: (
            f'总开销 `{S.chargeTimes[S.q[0]]} + {S.right - S.left + 1} × {S.s}` = {S.chargeTimes[S.q[0]] + (S.right - S.left + 1) * S.s}'
            + (f' > {S.budget}：超预算 → 缩窗口' if S.chargeTimes[S.q[0]] + (S.right - S.left + 1) * S.s > S.budget
               else f' ≤ {S.budget}：没超，窗口合法')),
        'if q[0] == left': lambda S, B, r: (
            f'队首下标 {S.q[0]} 正好是 `left`：这个最大值要离开窗口 → ==出队=='
            if S.q[0] == S.left else f'队首下标 {S.q[0]} ≠ `left = {S.left}`：最大值还在窗口里，不动'),
        'q.popleft()': '队首出队',
        's -= runningCosts[left]': '左端点移出窗口：`s -= {B.runningCosts[B.left]}` → {s}',
        'left += 1': '`left` 右移到 {left}',
        'ans = max': '窗口长度 `{right} − {left} + 1` = {right - left + 1}，`ans = max({B.ans}, {right - left + 1})` = =={ans}==',
        'return ans': '最多连续运行 =={ret}== 个机器人',
    },
    max_steps=110,
    cards=dict(
        one_liner='右端点往右扩，超预算就收左端点，单调队列随时给出窗口最大充电时间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个机器人，连续运行 `k` 个的总开销 = `max(chargeTimes) + k × sum(runningCosts)`',
                 '求不超过 `budget` 的==最长连续==机器人段',
                 '示例：`[3,6,1,3,4]`、`[2,1,3,4,5]`、`budget=25` → `3`'],
        quote='在 239 题的基础上，把定长滑窗改为不定长滑窗：入：弹出队尾的 ≤ chargeTimes[right] 的元素。出：如果总开销超过 budget，则不断移出左端点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右端点，`right` 越大，合法的 `left` 也越大，==有单调性==，所以能滑窗',
              '窗口最大充电时间用==单调队列==，队首永远是最大值',
              '队列存下标：左端点等于队首时，才需要弹出队首'],
        summary=['时间 `O(n)`：每个元素至多入队、出队各一次，`left` 最多加 n 次',
                 '`>` 判超预算；窗口空时 `q` 也空，循环自然结束',
                 '另一种做法是二分答案 + 定长滑窗（239 题），多一个 log',
                 '前置题：239 滑动窗口最大值'],
    ),
)
