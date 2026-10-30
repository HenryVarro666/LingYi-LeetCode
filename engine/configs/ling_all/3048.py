NUMS = [2, 2, 0]
CI = [2, 2, 2, 2, 3, 2, 2, 1]


def _exam_cells(mx):
    last = {}
    for t, v in enumerate(CI[:mx]):
        last[v] = t
    return set(last.values())


def _col(S, i, v):
    mx = S.get('mx')
    if mx is None or i >= mx:
        return None
    return 'blue' if i in _exam_cells(mx) else None


def _top(S):
    mx = S.get('mx')
    if mx is None:
        return f'把 `nums[i]` 当作第 `i` 门课要复习的天数，`changeIndices[t]` 是第 `t` 天可考的科目 → ==二分天数 mx=='
    if S.get('exam') is None:
        return f'试探 `mx = {mx}` 天：只看前 `{mx}` 天（蓝格 = 每门课最晚的考试日）'
    return f'倒着扫：还要考 `exam = {S["exam"]}` 门，已欠复习 `study = {S["study"]}` 天（考试前必须复习够）'


CONFIG = dict(
    num=3048, title='标记所有下标的最早秒数 I', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 逆向遍历',
    tags=['灵神题单·二分算法', '难度分 2263'],
    code='''
class Solution:
    def earliestSecondToMarkIndices(self, nums: List[int], changeIndices: List[int]) -> int:
        n, m = len(nums), len(changeIndices)
        if n > m:
            return -1

        done = [0] * n  # 避免反复创建和初始化数组
        def check(mx: int) -> bool:
            exam, study = n, 0
            for i in range(mx - 1, -1, -1):
                idx = changeIndices[i] - 1
                if done[idx] != mx:
                    done[idx] = mx
                    exam -= 1  # 考试
                    study += nums[idx]  # 需要复习的天数
                elif study:
                    study -= 1  # 复习
            return exam == 0 and study == 0  # 考完了并且复习完了

        left = n + sum(nums)
        ans = left + bisect_left(range(left, m + 1), True, key=check)
        return -1 if ans > m else ans
''',
    call=f'Solution().earliestSecondToMarkIndices({NUMS}, {CI})',
    expect=8,
    views=[
        dict(type='text', fn=_top, size=24, h=100),
        dict(type='array', var='changeIndices', label='changeIndices（蓝 = 前 mx 天里每门课最晚的考试日；灰 = 超出 mx）', cell=84, h=250,
             pointers={'i': 'yellow'}, dim=lambda S, i, v: S.get('mx') is not None and i >= S['mx'], color=_col),
        dict(type='array', var='nums', label='nums（第 i+1 门课需要复习的天数）', cell=100, h=170),
        dict(type='text', fn=lambda S: f"考试日记录 `done = {S['done']}`（等于 mx 表示这门课已经遇到过）" if 'done' in S and S.get('mx') else '', size=22, h=70),
    ],
    watch=[('mx', 'mx', 'yellow'), ('i', 'i', 'blue'), ('exam', 'exam', 'orange'), ('study', 'study', 'cyan'), ('left', 'left', 'green')],
    captions={
        'n, m = len': '`n = {n}` 门课，`m = {m}` 天',
        'if n > m': '`n = {n} > m = {m}`？{"每门课至少要一天考试，天数不够 → -1" if n > m else "天数够，继续"}',
        'done = [0]': '`done[idx]` 记“这门课在本次 check 里是否已经安排过考试”，用 mx 当标记，避免每次重新初始化',
        'exam, study = n, 0': '`check({mx})`：`exam` = 还没安排考试的课程数，`study` = 欠着的复习天数',
        'for i in range': lambda S, B, r: (f'倒着扫第 `{S.i + 1}` 天' if B.get('i') is None or B.get('i') != S.i else '扫描完毕'),
        'idx = changeIndices': '第 `{i + 1}` 天可考科目 `{idx + 1}`，这门课需要复习 `nums[{idx}] = {nums[idx]}` 天',
        'if done[idx] != mx': '`done[{idx}] = {done[idx]}` {"!=" if done[idx] != mx else "=="} `mx = {mx}`：{"倒着数第一次遇到，这天就是它==最晚的考试日==" if done[idx] != mx else "之前已遇到，这天不是最晚考试日，只能用来复习"}',
        'done[idx] = mx': '标记科目 `{idx + 1}` 已安排考试',
        'exam -= 1': '安排考试：还剩 `exam = {exam}` 门没考',
        'study += nums[idx]': '考试之前要先复习 `{nums[idx]}` 天：`study = {study}`（这些复习要在更早的日子里完成）',
        'elif study': '`study = {study}`：{"还欠复习，这天用来复习" if study else "没有欠账，这天空着"}',
        'study -= 1': '这天用来复习一天：`study = {study}`',
        'return exam == 0': '`exam = {exam}`，`study = {study}`：{"全部考完且复习够 → True" if exam == 0 and study == 0 else "有课没安排或复习不够 → False"}',
        'left = n + sum': '至少需要 `n + sum(nums) = {left}` 天（每门课 1 天考试 + 复习），答案不会小于它',
        'ans = left + bisect': '`check(mx)` 随 mx 增大由 False 变 True：在 `[{left}, {m}]` 里二分找第一个 True → 答案 =={ans}==',
        'return -1 if ans': '`ans = {ans}` {"> m → -1" if ans > m else "<= m，有解"} → 返回 =={ret}==',
    },
    max_steps=58,
    cards=dict(
        one_liner='把题意换成复习考试：二分天数，倒着扫安排最晚考试日',
        complexity='时间 `O(m log m)`，空间 `O(n)`',
        problem=['下标从 1 开始。第 `s` 秒可以：把某个 `nums[i]` 减 1；或在 `nums[changeIndices[s]] == 0` 时标记它；或什么都不做',
                 '求把所有下标都标记完的==最早秒数==，做不到返回 `-1`',
                 f'本视频：`nums = {NUMS}`，`changeIndices = {CI}` → `8`'],
        quote='你有 n 门课程需要考试，第 i 门课程需要用 nums[i] 天复习。同一天只能复习一门课程。……考试的时间越晚越好，这样我们能有更充足的时间复习。',
        quote_src='—— 灵茶山艾府题解',
        idea=['二分天数 `mx`：天数越多越能搞定所有课程 → 单调',
              '倒着扫前 `mx` 天：某科第一次出现（= 最晚的一天）就考试，并记下它要欠的复习天数',
              '其余的日子用来还账：`study` 大于 0 就减 1。最后 `exam` 和 `study` 都为 0 才算成功'],
        summary=['时间 `O(m log m)`，空间 `O(n)`；先判 `n > m` 直接 `-1`',
                 '二分下界 `n + sum(nums)`：每门课至少 1 天考试，加上全部复习天数',
                 '用 `done[idx] = mx` 当标记，省掉每次 check 重新建数组',
                 '题解另有“正向遍历”写法一：正着扫，用 `cnt` 累积可用复习天数',
                 '倒着扫是关键：先定考试日，再往前分配复习天数'],
    ),
)
