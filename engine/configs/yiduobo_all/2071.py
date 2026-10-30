def _inchk(S):
    return 'q' in S['_inner']


CONFIG = dict(
    num=2071, title='你可以安排的最多任务数目', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 从难到易 + 双端队列',
    tags=['二分算法', '常用数据结构', '难度分 2648'],
    code='''
class Solution(object):
    def maxTaskAssign(self, tasks, workers, pills, strength):
        sorted_tasks = sorted(tasks)
        sorted_workers = sorted(workers, reverse=True)
        def check():
            if mid > len(sorted_workers):
                return False
            q = []
            l = 0
            r = 0
            p = 0
            cnt = 0
            for index in range(mid - 1, -1, -1):
                now_task = sorted_tasks[index]
                while p < len(sorted_workers) and sorted_workers[p] + strength >= now_task:
                    q.append(sorted_workers[p])
                    r += 1
                    p += 1
                if l == r:
                    return False
                if q[l] >= now_task:
                    l += 1
                elif cnt == pills:
                    return False
                else:
                    cnt += 1
                    q.pop()
                    r -= 1
            return True
        l = 0
        r = len(sorted_tasks)
        while l < r:
            mid = (l + r + 1) >> 1
            if check():
                l = mid
            else:
                r = mid - 1
        return l
''',
    call='Solution().maxTaskAssign([5,9,8,5,9], [1,6,4,2,6], 1, 5)',
    expect=3,
    skip=['r += 1', 'p += 1', 'r -= 1', 'l = 0', 'r = 0', 'p = 0', 'cnt = 0', 'q = []'],
    views=[
        dict(type='text', h=70, fn=lambda S: (
            (f"验证前 `{S['mid']}` 个任务，从最难的开始分配；药用了 `{S['cnt']}` / `{S['pills']}`" if 'cnt' in S and 'index' in S
             else f"二分 `l = {S['l']}` 能 / `r = {S['r']}` 不一定，试 `mid = {S['mid']}`" if 'mid' in S and not _inchk(S)
             else '') if 'mid' in S else '')),
        dict(type='array', var='sorted_tasks', label='sorted_tasks（升序；绿 = 前 mid 个，蓝箭头 = 当前任务）', cell=84, h=210,
             pointers={'index': 'blue'},
             dim=lambda S, i, v: 'mid' in S and i >= S['mid'],
             color=lambda S, i, v: 'green' if 'mid' in S and i < S['mid'] else None),
        dict(type='array', var='sorted_workers', label='sorted_workers（降序；p = 下一个待检查的工人）', cell=84, h=210,
             pointers={'p': 'pink'}),
        dict(type='array', var=lambda S: S['q'] if 'q' in S['_inner'] else None,
             label='q（能借药完成当前任务的工人；l = 队首）', cell=84, h=160, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid'), ('now_task', 'now_task', 'green'), ('cnt', 'cnt', 'orange')],
    captions={
        'sorted_tasks = sorted': '任务从小到大：只做最简单的 `k` 个，所以验证时看前 `mid` 个',
        'sorted_workers = sorted': '工人==从大到小==：队首就是剩余工人里力量最大的',
        'if mid > len': lambda S, B, r: ('`mid` 超过工人数，肯定不行' if S.mid > len(S.sorted_workers) else f'`mid = {S.mid}` ≤ 工人数 {len(S.sorted_workers)}，继续验证'),
        'for index in range': lambda S, B, r: ('`mid` 个任务全部分配完毕 → 循环结束' if B.get('index') == S.index and B.get('index') is not None and 'now_task' in B and S.index == 0 else f'从最难的任务往最简单的分配，当前 `index = {S.index}`'),
        'now_task = ': '当前要分配的任务需要力量 `{now_task}`',
        'while p < len': lambda S, B, r: (
            f'工人 `{S.sorted_workers[S.p]}` + 药 `{S.strength}` ≥ `{S.now_task}`：借药能做 → ==入队尾=='
            if S.p < len(S.sorted_workers) and S.sorted_workers[S.p] + S.strength >= S.now_task
            else ('工人都看完了' if S.p >= len(S.sorted_workers) else f'工人 `{S.sorted_workers[S.p]}` + 药也不到 `{S.now_task}`，后面更弱，停止入队')),
        'q.append': '工人 `{q[-1]}` 入队：队列里是借药能做这个任务的人，队首最强、队尾最弱',
        'if l == r': lambda S, B, r: ('队列空：没人能做当前任务 → ==check 失败==' if S.l == S.r else '队列非空，有人能做'),
        'if q[l] >= now_task': lambda S, B, r: (
            f'队首最强的 `{S.q[S.l]} ≥ {S.now_task}`：不吃药就能做 → 让他做，省药'
            if S.q[S.l] >= S.now_task else f'队首 `{S.q[S.l]} < {S.now_task}`：连最强的都得吃药'),
        'l += 1': '最强的工人直接完成任务，出队',
        'elif cnt == pills': lambda S, B, r: ('药用完了，只能失败 → ==check 失败==' if S.cnt == S.pills else f'药还有（已用 {S.cnt} / {S.pills}）'),
        'cnt += 1': '吃药：用掉 `{cnt}` 颗',
        'q.pop()': '吃药的人选==队尾最弱==的：他刚好够得着，强的留给后面不吃药',
        'mid = (l + r + 1) >> 1': '上取整 `mid = {mid}`：能完成 {mid} 个任务吗？',
        'l = mid': '能 → 答案 ≥ {mid}，`l = {l}`',
        'r = mid - 1': '不能 → 答案 < {mid}，`r = {r}`',
        'return l': '二分结束，最多 `{l}` 个任务',
    },
    cards=dict(
        one_liner='二分任务数；验证时从最难的任务往回分配',
        complexity='时间 `O(n log n + m log m)`，空间 `O(m)`',
        problem=['`tasks[i]` 是任务所需力量，`workers[j]` 是工人力量，一人一任务',
                 '`pills` 颗药，每人最多一颗，吃药力量 `+strength`',
                 '示例：`[5,9,8,5,9]`，`[1,6,4,2,6]`，1 颗药，`+5` → `3`'],
        quote='若有若干工人都可以完成最困难的任务，那么就让力量最大的工人去完成；需要药丸才能完成时，就选择力量最小的工人借助药丸去完成。',
        quote_src='—— yiduobo 题解（概括原文）',
        idea=['完成 `k` 个，就选最简单的 `k` 个任务；`k` 越小越容易 → 二分',
              '最难的任务先分：队首最强不吃药能做就==省药==，否则队尾最弱的吃药',
              '任务变简单，能借药的工人只增不减 → 用数组当双端队列'],
        summary=['时间瓶颈是排序，二分每次验证线性',
                 '易错：不能简单「最难任务给最强的人」，药丸会让这种分配出错',
                 '`mid = (l + r + 1) >> 1` 上取整，配合 `l = mid`、`r = mid - 1` 才不会死循环',
                 '`check` 里用的 `mid` 来自外层闭包',
                 '对比灵神：灵神从弱到强枚举工人，yiduobo 从难到易枚举任务，队列方向相反'],
    ),
)
