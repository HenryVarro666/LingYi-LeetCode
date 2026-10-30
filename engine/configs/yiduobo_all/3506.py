def _bs(S):
    if 'mid' in S:
        return f"二分答案：`left = {S.get('left')}`，`right = {S.get('right')}`，试 `mid = ` =={S['mid']}=="
    if 'right' in S:
        return f"二分范围：`left = {S['left']}`（最长的一个）～ `right = {S['right']}`（先分裂到够多再各打一个）"
    return '先算上界：分裂到白细胞数 ≥ n 需要多久'


def _plan(S):
    if 'mid' not in S or 'index' not in S:
        return ''
    n = len(S['timeReq'])
    return (f"限时 `{S['mid']}`：已分裂 `{S.get('split_cnt', 0)}` 次，白细胞 `now = {S['now']}`，"
            f"还剩 `{n - S['index']}` 个细菌要处理")


CONFIG = dict(
    num=3506, title='查找消除细菌菌株所需时间', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二分答案 + 贪心（先分裂后打最长）',
    tags=['二分答案'],
    code='''
class Solution(object):
    def minEliminationTime(self, timeReq, splitTime):
        
        n = len(timeReq)
        now = 1
        t = 0
        while now < n:
            now += now
            t += splitTime

        timeReq.sort(reverse=True)
        left = timeReq[0]
        right = t + left
        while left < right:
            mid = (left + right) // 2
            now = 1
            flag = True
            split_cnt = 0
            for index, t in enumerate(timeReq):
                r = mid - t - split_cnt * splitTime
                while r >= splitTime and now < n - index:
                    now += now
                    r -= splitTime
                    split_cnt += 1

                if now >= n - index:
                    break
                
                if now == 0:
                    flag = False
                    break
                
                now -= 1
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().minEliminationTime([3,1,2,4], 2)',
    expect=8,
    views=[
        dict(type='text', fn=_bs, size=26, h=70),
        dict(type='array', var='timeReq', label='timeReq（从大到小：先处理最耗时的）', cell=90,
             pointers={'index': 'pink'}, h=200,
             color=lambda S, i, v: ('pink' if i == S.get('index') else None)),
        dict(type='text', fn=_plan, size=26, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('now', 'now', 'cyan'), ('split_cnt', 'split_cnt', 'orange'), ('r', 'r', 'purple')],
    captions={
        5: '最开始只有 `now = 1` 个白细胞',
        'while now < n': '白细胞 `now = {now}` < 细菌数 `{n}`，还不够一人一个 → 继续分裂',
        8: '全体分裂一次，数量翻倍：`now = {now}`',
        't += splitTime': '分裂要花 `splitTime`，累计 `{t}`',
        'timeReq.sort': '从大到小排序：==耗时最长的细菌最先交给细胞==',
        'left = timeReq[0]': '下界 `left = {left}`：至少要等最长的那个打完',
        'right = t + left': '上界 `right = {right}`：先分裂到够多（`{t}`），再各打一个，最慢是最长那个',
        'while left < right': lambda S, B, r: ('`left < right`，还没收敛，继续二分' if S.left < S.right else '`left == right`：答案就是 `{}`'.format(S.left)),
        'mid = ': '试时限 `mid = ({B.left} + {B.right}) // 2 = {mid}`：时间越充足越容易成功，所以能二分',
        16: '每次尝试都从 1 个白细胞开始：`now = 1`',
        'r = mid - t': '处理 `{t}` 要预留 `{t}`，分裂已花 `{split_cnt} × {splitTime}`，机动时间 `r = {mid} - {t} - {split_cnt * splitTime} = {r}`',
        'while r >= splitTime': lambda S, B, r: ('`r = {}` ≥ `splitTime`，且细胞还不够多 → ==趁早分裂==，数量翻倍'.format(S.r)
                                                if S.r >= S.splitTime and S.now < len(S.timeReq) - S.index
                                                else '`r = {}`：不能再分裂（时间不够或已经够多）'.format(S.r)),
        22: '分裂：白细胞数量翻倍，`now = {now}`',
        'r -= splitTime': '分裂花掉 `splitTime`：`r = {r}`',
        'split_cnt += 1': '累计分裂 `split_cnt = {split_cnt}`',
        'if now >= n - index': lambda S, B, r: ('`now = {}` ≥ 剩余细菌 `{}`：每个细菌都有细胞 → ==这个时限够用=='.format(S.now, len(S.timeReq) - S.index)
                                               if S.now >= len(S.timeReq) - S.index else '`now = {}` < 剩余 `{}`，继续'.format(S.now, len(S.timeReq) - S.index)),
        'if now == 0': lambda S, B, r: ('`now = 0`：细胞都派出去了，还有细菌没人管 → ==时限不够==' if S.now == 0 else '`now = {}`，还有细胞可用'.format(S.now)),
        'now -= 1': '派出一个白细胞去打 `{t}`：`now = {now}`（它不再分裂了）',
        'flag = False': '失败：`mid` 太小',
        'right = mid': '`mid` 够用 → 答案 ≤ mid，`right = {right}`',
        'left = mid + 1': '`mid` 不够 → 答案 > mid，`left = {left}`',
        'return left': '最少需要 `{left}` 单位时间',
    },
    cards=dict(
        one_liner='二分时限：先尽早分裂，再让单个细胞去打最耗时的',
        complexity='时间 `O(n log n)`（排序 + 二分每次 `O(n)`），空间 `O(1)`',
        problem=['`timeReq[i]` 是消灭第 `i` 种细菌所需时间，白细胞分裂要 `splitTime`',
                 '初始 1 个白细胞，每个细胞只能打一种细菌，可以并行，求最少总时间',
                 '本视频：`timeReq = [3,1,2,4]`，`splitTime = 2`'],
        quote='时间越充足，消除所有细菌的成功率就越高，因此在这里可以二分答案。……分裂应该趁早执行，而为了保证在特定的时间内处理掉所有细菌，到了特定的时间就必须开始攻击当前所需时间最长的细菌。',
        quote_src='—— yiduobo 题解原文',
        idea=['时限 `mid` 越大越容易成功 → 二分；下界是最长的细菌，上界是分裂够数再各打一个',
              '顺序：分裂 → 派一个细胞打最长的 → 分裂 → 再派一个……',
              '机动时间 `r = mid - t - 已分裂次数 × splitTime`，够一次分裂就分，直到细胞数 ≥ 剩余细菌数'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：`now` 是还没派出去的细胞数，派出一个就 `now -= 1`；`now == 0` 说明时限不够',
                 '分裂条件还要加 `now < n - index`，够多了就不用再分裂',
                 '原文为 Python 2 风格，除 `class Solution(object)` 外无需修改（已是 `//`）'],
    ),
)
