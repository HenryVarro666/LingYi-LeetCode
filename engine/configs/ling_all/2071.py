CONFIG = dict(
    num=2071, title='你可以安排的最多任务数目', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 双端队列贪心',
    tags=['二分算法', '常用数据结构', '难度分 2648'],
    code='''
class Solution:
    def maxTaskAssign(self, tasks: List[int], workers: List[int], pills: int, strength: int) -> int:
        tasks.sort()
        workers.sort()
        def check(k: int) -> bool:
            # 贪心：用最强的 k 名工人，完成最简单的 k 个任务
            i, p = 0, pills
            valid_tasks = deque()
            for w in workers[-k:]:  # 枚举工人
                # 在吃药的情况下，把能完成的任务记录到 valid_tasks 中
                while i < k and tasks[i] <= w + strength:
                    valid_tasks.append(tasks[i])
                    i += 1
                # 即使吃药也无法完成任务
                if not valid_tasks:
                    return False
                # 无需吃药就能完成（最简单的）任务
                if w >= valid_tasks[0]:
                    valid_tasks.popleft()
                    continue
                # 必须吃药
                if p == 0:  # 没药了
                    return False
                p -= 1
                # 完成（能完成的）最难的任务
                valid_tasks.pop()
            return True
        left, right = 0, min(len(tasks), len(workers)) + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call='Solution().maxTaskAssign([5,9,8,5,9], [1,6,4,2,6], 1, 5)',
    expect=3,
    views=[
        dict(type='text', h=70, fn=lambda S: (
            f"二分 `left={S['left']}` 能 / `right={S['right']}` 不能" +
            (f"；验证 `k = {S['k']}`，药 `p = {S['p']}`" if 'k' in S and 'p' in S else '')
        ) if 'left' in S else ''),
        dict(type='array', var='tasks', label='tasks（升序；绿 = 最简单的 k 个，i = 下一个待入队）', cell=84, h=200,
             pointers={'i': 'blue'},
             dim=lambda S, i, v: 'k' in S and i >= S['k'],
             color=lambda S, i, v: 'green' if 'k' in S and i < S['k'] else None),
        dict(type='array', var='workers', label='workers（升序；只用最强的后 k 名，粉 = 当前 w）', cell=84, h=200,
             dim=lambda S, i, v: 'k' in S and i < len(S['workers']) - S['k'],
             color=lambda S, i, v: 'pink' if 'k' in S and 'w' in S and v == S['w'] and i >= len(S['workers']) - S['k'] else None),
        dict(type='queue', var='valid_tasks', label='valid_tasks（吃药后能做的任务；左 = 最简单，右 = 最难）', h=160, font=30),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid'), ('k', 'k'), ('w', 'w', 'pink'), ('p', 'p', 'orange')],
    captions={
        'tasks.sort()': '任务从小到大排序：后面要「取最简单的 k 个」',
        'workers.sort()': '工人从小到大排序：后面要「取最强的 k 个」',
        'i, p = 0, pills': '`i` 指向下一个待加入的任务，`p = {p}` 是剩余药丸',
        'valid_tasks = deque()': '双端队列：队首 = 最简单的任务，队尾 = 最难的任务',
        'for w in workers[-k:]': '最强的 {k} 名工人，从弱到强逐个看：当前 `w = {w}`',
        'while i < k and tasks[i] <= w': lambda S, B, r: (
            f'`tasks[{S.i}] = {S.tasks[S.i]} ≤ w + strength = {S.w + S.strength}`：吃药能做 → ==入队尾=='
            if S.i < S.k and S.tasks[S.i] <= S.w + S.strength
            else (f'没有更多任务了（`i = {S.i} = k`）' if S.i >= S.k
                  else f'`tasks[{S.i}] = {S.tasks[S.i]} > {S.w + S.strength}`：吃药也做不了，先不入队')),
        'valid_tasks.append': '任务 `{tasks[i]}` 进队尾（越往后越难）',
        'if not valid_tasks': lambda S, B, r: ('队列空：吃药也没有任务可做 → `k` 太大，==check 失败=='
                                               if not S.valid_tasks else '队列非空：至少有一个任务能做'),
        'if w >= valid_tasks[0]': lambda S, B, r: (
            f'`w = {S.w} ≥ 最简单的 {S.valid_tasks[0]}`：不吃药就能做'
            if S.w >= S.valid_tasks[0] else f'`w = {S.w} < 最简单的 {S.valid_tasks[0]}`：不吃药做不了，必须吃药'),
        'valid_tasks.popleft()': '不吃药 → 做最简单的任务，省药；更强的工人也能做更难的，不用担心',
        'if p == 0': lambda S, B, r: ('药用完了，`w` 又必须吃药 → ==check 失败==' if S.p == 0 else f'还剩 `{S.p}` 颗药，可以吃'),
        'p -= 1': '吃一颗药，剩 `{p}` 颗',
        'valid_tasks.pop()': '既然吃了药，就做能做的==最难==的任务，别浪费药效',
        'mid = (left + right) // 2': '试 `mid = {mid}`：能完成 {mid} 个任务吗？',
        'left = mid': '能完成 → 答案 ≥ {mid}，`left = {left}`',
        'right = mid': '不能完成 → 答案 < {mid}，`right = {right}`',
        'return left': '二分结束，最多完成 `{left}` 个任务',
    },
    cards=dict(
        one_liner='二分能完成几个任务，用双端队列贪心验证',
        complexity='时间 `O(n log n + m log m)`，空间 `O(min(n,m))`',
        problem=['`tasks[i]` 是任务所需力量，`workers[j]` 是工人力量，一人一任务',
                 '有 `pills` 颗药，每人最多一颗，吃药力量 `+strength`',
                 '示例：`tasks=[5,9,8,5,9]`，`workers=[1,6,4,2,6]`，1 颗药，`+5` → `3`'],
        quote='如果可以完成 $k$ 个任务，那么也可以完成小于 $k$ 个任务。如果无法完成 $k$ 个任务，那么也无法完成大于 $k$ 个任务。据此，可以二分答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['选最强的 `k` 名工人，去做最简单的 `k` 个任务',
              '枚举工人：不吃药能做最简单的就做它；==必须吃药才做最难的能做的==',
              '「能做的任务」只在队尾加、队首和队尾删 → ==双端队列=='],
        summary=['时间瓶颈是排序；二分 `O(log)` 次，每次 check 线性',
                 '易错：不吃药能做时不要硬吃药去做更难的，后面更强的工人能做，还能省药',
                 '右端点取 `min(n, m) + 1`，开区间二分',
                 '题解另附库函数写法：`bisect_left(range(...), True, key=check)`',
                 '`tasks.sort()` 会改动入参，本视频里看到的是排序后的数组'],
    ),
)

