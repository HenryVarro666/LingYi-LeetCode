def _bits(S):
    i = S.get('i')
    if i is None:
        return ''
    n = len(S['aliceArrows'])
    s = format(i, f'0{n}b')[::-1]
    chosen = [j for j in range(n) if s[j] == '1']
    return f"`i = {i}` 的二进制（低位在左）：`{s}`　→ Bob 想赢的区域 =={chosen}=="


CONFIG = dict(
    num=2212, title='射箭比赛中的最大得分', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='二进制枚举赢哪些区域（Go 原文转写）',
    tags=['灵神题单·链表树与回溯', '难度分 1869'],
    code='''
class Solution:
    def maximumBobPoints(self, numArrows: int, aliceArrows: List[int]) -> List[int]:
        ans = []
        max_score = -1
        for i in range(1 << len(aliceArrows)):  # 二进制枚举
            score = arrow = 0
            bob_arrows = [0] * 12
            for j, v in enumerate(aliceArrows):
                if i >> j & 1 == 1:
                    score += j
                    arrow += v + 1
                    bob_arrows[j] = v + 1  # Bob 多射一支箭
            if arrow > numArrows:  # 超出限制，区域集合不合法
                continue
            if score > max_score:
                max_score = score
                bob_arrows[0] += numArrows - arrow  # 随便找个位置补满至 numArrows
                ans = bob_arrows[:]
        return ans
''',
    call='Solution().maximumBobPoints(3, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2])',
    expect=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    trace_limit=296,
    skip=['ans = []', 'bob_arrows = [0] * 12', 'for j, v in enumerate', 'if i >> j', 'score = arrow = 0', 'score += j', 'bob_arrows[j] =', 'max_score = score', 'bob_arrows[0] +='],
    snap_maxlen=16,
    truncated_caption='后面同理：把 `4096` 个区域集合全部枚举完，留下得分最高的那个方案',
    views=[
        dict(type='text', fn=_bits, size=26),
        dict(type='array', cell=78, var='aliceArrows', label='aliceArrows（各区域 Alice 的箭数）', pointers={'j': 'blue'}, h=190,
             color=lambda S, i, v: 'green' if 'i' in S and (S['i'] >> i) & 1 else None),
        dict(type='array', cell=78, var='bob_arrows', label='bob_arrows（Bob 的方案，每个选中区域 = Alice + 1）', pointers={'j': 'blue'}, h=190),
        dict(type='array', cell=78, var='ans', label='ans（目前最好的方案）', h=170),
    ],
    watch=[('i', 'i', 'blue'), ('score', 'score', 'yellow'), ('arrow', 'arrow', 'pink'), ('numArrows', 'numArrows'), ('max_score', 'max_score', 'orange')],
    captions={
        'for i in range': lambda S, B, ret: f'第 `i = {S.i}` 种选法（共 `2^12` 种）：第 `j` 位是 1 = Bob ==赢==区域 `j`',
        'max_score = -1': '最高分先设成 `-1`：这样第一个合法方案一定能把它刷新',
        'arrow += v + 1': '赢区域 `{j}`：`score` +{j} → {score}；Alice 射 `{v}` 支，Bob 多射一支 = `{v + 1}`，`arrow` → {arrow}',
        'if arrow > numArrows': lambda S, B, ret: (f'`arrow = {S.arrow}` > `numArrows = {S.numArrows}` → ==箭不够==，这种选法不合法' if S.arrow > S.numArrows else f'`arrow = {S.arrow}` ≤ `numArrows = {S.numArrows}` → 箭够，合法'),
        'continue': '不合法，直接看下一个 `i`',
        'if score > max_score': lambda S, B, ret: (f'`score = {S.score}` > `max_score = {S.max_score}` → 比目前最好的更好' if S.score > S.max_score else f'`score = {S.score}` 没超过 `max_score = {S.max_score}` → 不更新'),
        'ans = bob_arrows': '刷新 `max_score = {max_score}`；没用完的箭补进区域 0（它得 0 分，不影响得分）；保存方案 `ans = {ans}`',
    },
    cards=dict(
        one_liner='只有 12 个区域，直接枚举 Bob 在哪些区域获胜',
        complexity='时间 `O(2^12 × 12)`，空间 `O(12)`',
        problem=['Alice 先射 `numArrows` 支箭，Bob 再射同样多；区域 `k` 谁箭多谁得 `k` 分（相等归 Alice）',
                 '已知 Alice 在 12 个区域的箭数，求 Bob 得分最高的射法',
                 '示例：`3, [0,0,1,0,0,0,0,0,0,0,0,2]` → 任意一种最优射法'],
        quote='由于只有 12 个区域，我们可以枚举 Bob 在哪些区域上获胜，这一共有 2^12 种不同的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['为了省箭，Bob 在要赢的区域只需比 Alice ==多射 1 支==，输的区域一支都不射',
              '用 `i` 的二进制位表示「赢哪些区域」，算出总得分 `score` 和总箭数 `arrow`',
              '`arrow > numArrows` 就不合法；否则比较 `score`，多出的箭补到区域 0'],
        result='运行结束：`ans` 是得分最高的合法射法（题目允许返回任意一种最优解）',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`[12]int{}` → `[0] * 12`，`ans = bobArrows[:]` → `bob_arrows[:]`）',
                 '时间 `O(2^12 × 12)`，空间 `O(12)`；视频只演示前几种选法，其余同理快进',
                 '易错：赢的区域只需 `v + 1` 支，不是 `v`（相等 Alice 得分）',
                 '易错：多余的箭要补满到恰好 `numArrows`，放区域 0 不影响得分'],
    ),
)
