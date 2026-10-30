PERSONS = [0, 1, 1, 0, 0]
TIMES = [0, 5, 10, 15, 20]
FINAL_CNT = {0: 3, 1: 2}


def _info(S):
    c = S.get('self.candidate_list')
    if c is None:
        return '只记录「领先者发生变化」的时间点：`[候选人, 时间]`'
    if 'p' in S and 'winner' in S and 't' in S and 'l' not in S:
        return f'`{S["p"]}` 在 `t = {S["t"]}` 投票后得 `{S["cnt_dict"][S["p"]]}` 票，当前最高 `max_cnt = {S["max_cnt"]}`，领先者 `winner = {S["winner"]}`'
    return f'`candidate_list = {c}`'


def _ct(S):
    c = S.get('self.candidate_list')
    return None if c is None else [x[1] for x in c]


CONFIG = dict(
    num=911, title='在线选举', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='记录领先者变化点 + 二分',
    tags=['灵神题单·二分算法'],
    code='''
class TopVotedCandidate(object):

    def __init__(self, persons, times):
        cnt_dict = {}
        max_cnt = 0
        winner = None
        self.candidate_list = []
        for p, t in zip(persons, times):
            cnt_dict[p] = cnt_dict.get(p, 0) + 1
            if cnt_dict[p] >= max_cnt:
                max_cnt = cnt_dict[p]
                if winner != p:
                    self.candidate_list.append([p, t])
                    winner = p

    def q(self, t):
        if t >= self.candidate_list[-1][1]:
            return self.candidate_list[-1][0]
        else:
            l = 0
            r = len(self.candidate_list) - 1
            while l < r:
                mid = (l + r) >> 1
                if t > self.candidate_list[mid][1]:
                    l = mid + 1
                else:
                    r = mid
            
            if self.candidate_list[l][1] == t:
                return self.candidate_list[l][0]
            else:
                return self.candidate_list[l - 1][0]
''',
    call='''v = TopVotedCandidate([0, 1, 1, 0, 0], [0, 5, 10, 15, 20])
[v.q(12), v.q(5)]''',
    expect=[1, 1],
    max_steps=90,
    views=[
        dict(type='array', var=lambda S: S.get('persons') or PERSONS, label='persons（第 i 票投给谁）', cell=80, h=150,
             color=lambda S, i, v: 'yellow' if S.get('p') is not None and 'times' in S and S.get('t') == S['times'][i] and 'l' not in S else None),
        dict(type='array', var=lambda S: S.get('times') or TIMES, label='times（投票时间）', cell=80, h=150,
             color=lambda S, i, v: 'yellow' if S.get('t') == v and 'l' not in S and S.get('p') is not None else None),
        dict(type='map', var=lambda S: S.get('cnt_dict') or FINAL_CNT, label='cnt_dict：每人的票数', fmt=lambda k, v: f'{k}: {v}', h=110),
        dict(type='array', var=_ct, label='candidate_list 的时间点（领先者每次换人的时刻）', cell=80, h=230,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, window=('l', 'r')),
        dict(type='text', h=100, size=28, fn=_info),
    ],
    watch=[('winner', 'winner', 'green'), 'max_cnt', 't', 'l', 'r', 'mid'],
    skip=['cnt_dict = {}', 'max_cnt = 0'],
    captions={
        'winner = None': '只关心每个时刻==谁领先==，不存票数：记 `winner`',
        'self.candidate_list = []': '`candidate_list`：每次领先者换人时，记一条 `[候选人, 时间]`',
        'for p, t in zip': lambda S, B, ret: (
            '所有投票处理完，开始回答查询' if 'p' in B and S.p == B.p and S.t == B.t else
            '按时间顺序处理：`t = {}` 时给 `{}` 号候选人的一票'.format(S.t, S.p)),
        'cnt_dict[p] = ': '`{p}` 的票数 → `{cnt_dict[p]}`',
        'if cnt_dict[p] >= max_cnt': lambda S, B, ret: (
            ('`{} >= {}`：追平或超过最高票 → 他是新领先者（平局取最近得票的）'.format(S.cnt_dict[S.p], S.max_cnt)) if S.cnt_dict[S.p] >= S.max_cnt
            else '`{} < {}`：没追上最高票，领先者不变'.format(S.cnt_dict[S.p], S.max_cnt)),
        'max_cnt = cnt_dict[p]': '最高票数更新为 `{max_cnt}`',
        'if winner != p': lambda S, B, ret: ('领先者从 `{}` 换成 `{}` → 要记录'.format(S.winner, S.p) if S.winner != S.p
                                             else '领先者还是 `{}`，不用记'.format(S.winner)),
        'self.candidate_list.append': '记录变化点：`t = {t}` 起领先者是 `{p}`；`candidate_list = {self.candidate_list}`',
        'winner = p': '`winner` → {winner}',
        'if t >= self.candidate_list[-1][1]': lambda S, B, ret: (
            '`t = {} >= 最后一个变化点 {}`：之后领先者不变 → 直接返回最后一个'.format(S.t, S['self.candidate_list'][-1][1])
            if S.t >= S['self.candidate_list'][-1][1] else
            '`t = {} < 最后一个变化点 {}`：在中间，要二分'.format(S.t, S['self.candidate_list'][-1][1])),
        'return self.candidate_list[-1][0]': '返回最后一个领先者 `{ret}`',
        'l = 0': '在变化点的时间里二分：找第一个 `>= t` 的位置',
        'r = len(self.candidate_list) - 1': '区间 `[0, {r}]`',
        'while l < r': lambda S, B, ret: '`l < r`，继续二分' if S.l < S.r else '`l == r`：定位完成',
        'mid = (l + r) >> 1': '取中点 `mid = {mid}`',
        'if t > self.candidate_list[mid][1]': lambda S, B, ret: (
            '`t = {} > {}`：这个变化点还没发生 → 答案在右边，`l = mid + 1`'.format(S.t, S['self.candidate_list'][S.mid][1])
            if S.t > S['self.candidate_list'][S.mid][1] else
            '`t = {} <= {}`：mid 可能就是第一个 `>= t` → `r = mid`'.format(S.t, S['self.candidate_list'][S.mid][1])),
        'l = mid + 1': '`l` → {l}',
        'r = mid': '`r` → {r}',
        'if self.candidate_list[l][1] == t': lambda S, B, ret: (
            '`l` 处的时间 `{}` 恰好等于 `t`：这一刻领先者刚好变了 → 就是它'.format(S['self.candidate_list'][S.l][1])
            if S['self.candidate_list'][S.l][1] == S.t else
            '`l` 处的时间 `{}` 大于 `t`：那次变化还没发生 → 取前一个'.format(S['self.candidate_list'][S.l][1])),
        'return self.candidate_list[l][0]': '正好在变化点：返回 `{ret}`',
        'return self.candidate_list[l - 1][0]': '`t` 落在两个变化点之间：取前一个变化点的领先者 `{ret}`',
    },
    cards=dict(
        one_liner='只记领先者换人的时间点，查询时二分找最近的一个',
        complexity='初始化 `O(n)`，每次查询 `O(log n)`；空间 `O(n)`',
        problem=['`persons[i]` 在 `times[i]` 时刻得到一票；`q(t)` 返回时刻 `t` 得票最多的人，平局取最近得票者',
                 '`times` 严格递增，`q` 的 `t` 不小于 `times[0]`',
                 '本视频：`[0,1,1,0,0]`、`[0,5,10,15,20]`，`q(12)=1`、`q(5)=1`'],
        quote='由于我们只关心最终的结果而不关心票数，因此我们可以按时间遍历整个投票过程，记录下每次投票结果产生改变的时间点，那么就可以得到一个单调递增的数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['初始化时顺序扫一遍：`cnt_dict` 数票，`>= max_cnt` 就产生新领先者，换人时才记 `[候选人, 时间]`',
              '记下的时间点单调递增，查询 `q(t)` 就是在其中二分',
              '找第一个 `>= t` 的位置 `l`：时间恰好等于 `t` 取它自己，否则取前一个'],
        summary=['`>=` 而不是 `>`：平局时最近投票的人领先',
                 '易错：`t` 恰好等于变化点时，该时刻的结果已经变了，要取变化点本身',
                 '`t >= 最后一个变化点` 要先单独判，否则二分会越界',
                 '原文本身是 Python 3 可运行的写法，未做修改；题面库里没有，题意按 LeetCode 原题补写'],
    ),
)
