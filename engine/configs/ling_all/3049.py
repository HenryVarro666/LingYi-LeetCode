def _txt(S):
    if 'cnt' in S and 'slow' in S:
        return f"二分的答案 `mx={S['mx']}`：可用天数 `cnt=`==`{S['cnt']}`==，慢速复习+考试还需 `slow=`==`{S['slow']}`==；最后要 `cnt ≥ slow`"
    return '二分答案 `mx`：倒着扫前 `mx` 天，尽量把快速复习放在靠左的天'


CONFIG = dict(
    num=3049, title='标记所有下标的最早秒数 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='二分答案 + 反悔堆',
    tags=['堆（优先队列）', '反悔贪心', '难度分 3125'],
    code='''
class Solution:
    def earliestSecondToMarkIndices(self, nums: List[int], changeIndices: List[int]) -> int:
        n, m = len(nums), len(changeIndices)
        total = n + sum(nums)

        first_t = [-1] * n
        for t in range(m - 1, -1, -1):
            first_t[changeIndices[t] - 1] = t

        def check(mx: int) -> bool:
            cnt = 0
            slow = total  # 慢速复习+考试所需天数
            h = []
            for t in range(mx - 1, -1, -1):
                i = changeIndices[t] - 1
                v = nums[i]
                if v <= 1 or t != first_t[i]:
                    cnt += 1  # 留给左边，用来快速复习/考试
                    continue
                if cnt == 0:
                    if not h or v <= h[0]:
                        cnt += 1  # 留给左边，用来快速复习/考试
                        continue
                    slow += heappop(h) + 1
                    cnt += 2  # 反悔：一天快速复习，一天考试
                slow -= v + 1
                cnt -= 1  # 快速复习，然后消耗一天来考试
                heappush(h, v)
            return cnt >= slow  # 剩余天数搞定慢速复习+考试

        ans = n + bisect_left(range(n, m + 1), True, key=check)
        return -1 if ans > m else ans
''',
    call='Solution().earliestSecondToMarkIndices([2,3], [2,1,1,1])',
    expect=4,
    skip=['i = changeIndices[t]', 'v = nums[i]', 'continue', 'for t in range(m - 1, -1, -1):'],
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='array', var='nums', label='nums（每门课慢速复习需要的天数）', h=170, cell=96),
        dict(type='array', var='changeIndices', label='changeIndices（第 t 天可以快速复习哪门课，t 从 0 开始）', h=220, cell=96,
             pointers={'t': 'blue'},
             dim=lambda S, i, v: 'mx' in S and i >= S['mx']),
        dict(type='heap', var='h', label='小根堆 h：已选快速复习的 nums', h=220),
    ],
    watch=[('mx', 'mx', 'pink'), ('t', 't', 'blue'), ('cnt', 'cnt', 'yellow'), ('slow', 'slow', 'orange')],
    captions={
        'total = n + sum': '全部慢速复习+考试需要 `n + sum(nums)` = =={total}== 天',
        'first_t[changeIndices[t] - 1] = t': '倒着记录每门课在 `changeIndices` 里==首次出现==的下标：`first_t` = {first_t}',
        'cnt = 0': '开始检查 `mx = {mx}`：倒着遍历前 `mx` 天，`cnt` 是留给左边的空闲天数',
        'slow = total': '先假设所有课都慢速复习：`slow` = =={slow}==',
        'h = []': '小根堆存已选择快速复习的课程的复习时间',
        'for t in range(mx - 1': lambda S, B, r: (f'看第 `{S.t}` 天：能快速复习第 `{S.changeIndices[S.t]-1}` 门课（慢速要 `{S.nums[S.changeIndices[S.t]-1]}` 天）' if 't' in S and S.t >= 0 else '前 `mx` 天都看完了'),
        'if v <= 1 or t != first_t[i]': lambda S, B, r: (f'`v = {S.v} ≤ 1`：快速复习省不了什么 → 这天留给左边' if S.v <= 1 else (f'`t = {S.t}` 不是这门课首次出现的位置 → 这天留给左边' if S.t != S.first_t[S.i] else f'`v = {S.v} > 1` 且是首次出现 → 值得快速复习')),
        18: '留给左边：`cnt` → {cnt}',
        22: '留给左边（反悔也不划算）：`cnt` → {cnt}',
        'if cnt == 0': lambda S, B, r: (f'`cnt = 0`：没有空闲天可以考试 → 只能考虑反悔' if S.cnt == 0 else f'`cnt = {S.cnt} > 0`：右边有空闲天留给考试 → 直接快速复习'),
        'if not h or v <= h[0]': lambda S, B, r: ('堆为空，没得反悔' if not S.h else (f'`v = {S.v} ≤ 堆顶 {S.h[0]}`：不比已选的更值 → 不反悔' if S.v <= S.h[0] else f'`v = {S.v} > 堆顶 {S.h[0]}`：它比已选的最小的更值 → ==反悔==')),
        'slow += heappop(h) + 1': '反悔堆顶那门课：改回慢速复习+考试，`slow` += 它的 `nums+1` → =={slow}=='  ,
        'cnt += 2': '反悔后多出两天（一天快速复习、一天考试）：`cnt` → =={cnt}==',
        'slow -= v + 1': '这门课改成快速复习：慢速需求 `slow` 少 `{v}+1` → =={slow}==',
        'cnt -= 1': '快速复习占这一天，还要消耗一天考试：`cnt` → =={cnt}==',
        'heappush(h, v)': '`{v}` 入堆：{h}',
        'return cnt >= slow': '`cnt = {cnt}` 与 `slow = {slow}` 比：{"天数够，mx 可行" if cnt >= slow else "天数不够，mx 不可行"} → {cnt >= slow}',
        'ans = n + bisect_left': lambda S, B, r: ('二分答案：对 `mx = n..m` 二分，用 `check(mx)` 判断 `mx` 秒内能否搞定' if 'ans' not in S else f'二分得到最小可行的 `mx`：`ans` = =={S.ans}=='),
        'return -1 if': '`ans = {ans}`（超过 `m = {m}` 则返回 -1）',
    },
    max_steps=110,
    cards=dict(
        one_liner='二分天数，倒着扫：快速复习尽量靠左，不够就反悔',
        complexity='时间 `O(m log m log n)`，空间 `O(n)`',
        problem=['`nums[i]`：把下标 `i` 减到 0 要几次操作；`changeIndices[s]`：第 `s` 秒可把它直接设为 0',
                 '每秒只能做一件事：减 1、清零、标记或什么也不做；标记要求值为 0',
                 '求最早在第几秒标记完所有下标，不行返回 `-1`',
                 '本视频：`nums=[2,3]`，`changeIndices=[2,1,1,1]` → `4`'],
        quote='设二分的答案为 mx。我们从下标 mx-1 开始，倒着遍历 changeIndices 的前 mx 个数……否则如果 cnt=0，那么尝试在小根堆中「反悔」一个复习时间比 nums[i] 小的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换成「复习+考试」的故事：慢速复习一天减 1，快速复习一天搞定一门课',
              '答案越大越容易 → ==二分答案== `mx`',
              '倒着扫前 `mx` 天：首次出现且 `nums>1` 的课才值得快速复习',
              '空闲天 `cnt` 不够时，把堆里更小的那门反悔成慢速，换更大的快速复习'],
        summary=['时间 `O(m log m log n)`，空间 `O(n)`',
                 '易错：`t != first_t[i]` 的天不能用来快速复习，只能留给左边',
                 '反悔时 `cnt += 2`，再执行常规流程的 `cnt -= 1`，净增 1',
                 '最后 `cnt >= slow` 判断剩余天数能否搞定所有慢速复习+考试',
                 '本题演示的输入很小；真实数据下二分约 `log m` 轮，每轮都跑一遍倒序扫描'],
    ),
)
