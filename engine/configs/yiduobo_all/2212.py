def _bits(S):
    i = S.get('state')
    if i is None:
        return '12 个区域，每个区域「赢」或「不赢」：共 `2^12 = 4096` 种选法'
    s = format(i, '012b')[::-1]
    chosen = [j for j in range(12) if s[j] == '1']
    return f"`state = {i}` 的二进制（低位在左）：`{s}`　→ 要赢的区域 =={chosen}=="


CONFIG = dict(
    num=2212, title='射箭比赛中的最大得分', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='01 背包 · 枚举 4096 种选择',
    tags=['灵神题单·链表树与回溯', '难度分 1869'],
    code='''
class Solution(object):
    def maximumBobPoints(self, numArrows, aliceArrows):
        res = [0] * 12
        max_score = 0

        for state in range(4096):
            score = 0
            cnt = 0
            now = [0] * 12
            for index in range(12):
                if state & (1 << index):
                    now[index] = aliceArrows[index] + 1
                    cnt += now[index]
                    score += index
            
            if cnt <= numArrows and score > max_score:
                max_score = score
                res = now[:]
                res[0] += numArrows - cnt
        
        return res
''',
    call='Solution().maximumBobPoints(3, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2])',
    expect=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    trace_limit=306,
    snap_maxlen=16,
    truncated_caption='后面同理：`4096` 种选法都试一遍，得分最高的方案留在 `res` 里',
    skip=['res = [0] * 12', 'max_score = 0', 'score = 0', 'cnt = 0', 'now = [0] * 12', 'for index in range', 'if state & (1 << index)', 'now[index] =', 'cnt += now[index]'],
    views=[
        dict(type='text', fn=_bits, size=26),
        dict(type='array', cell=78, var='aliceArrows', label='aliceArrows（Alice 每个区域的箭数）', pointers={'index': 'blue'}, h=190,
             color=lambda S, i, v: 'green' if 'state' in S and (S['state'] >> i) & 1 else None),
        dict(type='array', cell=78, var='now', label='now（这一种选法下 Bob 的箭）', pointers={'index': 'blue'}, h=190),
        dict(type='array', cell=78, var='res', label='res（目前最好的方案）', h=170),
    ],
    watch=[('state', 'state', 'blue'), ('score', 'score', 'yellow'), ('cnt', 'cnt', 'pink'), ('numArrows', 'numArrows'), ('max_score', 'max_score', 'orange')],
    captions={
        'for state in range': lambda S, B, ret: f'试第 `state = {S.state}` 种选法：二进制第 `index` 位是 1，就让 Bob 去赢区域 `index`',
        'score += index': '选中区域 `{index}`：Bob 要射 `aliceArrows[{index}] + 1 = {now[index]}` 支才能赢 → `cnt = {cnt}`；得 `{index}` 分 → `score = {score}`',
        'if cnt <= numArrows': lambda S, B, ret: (f'`cnt = {S.cnt}` ≤ `numArrows = {S.numArrows}` 且 `score = {S.score}` > `max_score = {S.max_score}` → ==更优的合法方案==' if S.cnt <= S.numArrows and S.score > S.max_score
                                                   else (f'`cnt = {S.cnt}` > `numArrows = {S.numArrows}` → ==箭不够==，这种选法不行' if S.cnt > S.numArrows
                                                         else f'箭够，但 `score = {S.score}` 没超过 `max_score = {S.max_score}` → 不更新')),
        'max_score = score': '最高分更新为 `{max_score}`',
        'res = now[:]': '把这一种选法复制进 `res`（用 `[:]` 复制，别和 `now` 共用同一个列表）',
        'res[0] +=': '没射完的 `{numArrows - cnt}` 支箭随便放进区域 0：它得 0 分，不影响得分 → `res = {res}`',
    },
    cards=dict(
        one_liner='输了一分不得：每个区域要么不射，要么比 Alice 多射一支',
        complexity='时间 `O(2^12 × 12)`，空间 `O(12)`',
        problem=['Alice 先射、Bob 后射，各 `numArrows` 支；区域 `k` 谁箭多谁得 `k` 分（相等归 Alice）',
                 '已知 Alice 每个区域的箭数，求 Bob 得分最高的射法',
                 '示例：`3, [0,0,1,0,0,0,0,0,0,0,0,2]` → 得 27 分的一种射法'],
        quote='对于某个积分区域，bob要么一支箭都不射，要么就要比alice刚好多出一支箭。',
        quote_src='—— yiduobo 题解',
        idea=['区域 `i` 的代价是 `aliceArrows[i] + 1`，得分是 `i`，所以是一道 01 背包',
              '但箭数和单个代价都很大，背包数组开不起来；注意到区域只有 12 个',
              '直接枚举「赢哪些区域」共 `4096` 种，箭够就用得分更新答案，多余的箭放哪都行'],
        result='运行结束，返回 `res`：Bob 在区域 8、9、10 各射一支，共 27 分',
        summary=['时间 `O(2^12 × 12)`，空间 `O(12)`；视频只演示前几种选法，其余快进',
                 '易错：`res = now[:]` 要复制，否则后面的选法会改掉已保存的答案',
                 '易错：多出的箭要补满到 `numArrows`，放到区域 0 不影响得分',
                 '对照灵神：同样是二进制枚举，他用 `max_score = -1` 起步，这里从 0 起步（得分 0 的方案不必保存）'],
    ),
)
