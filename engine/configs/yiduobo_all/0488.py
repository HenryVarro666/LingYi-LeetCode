CONFIG = dict(
    num=488, title='祖玛游戏', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='DFS 暴力插球 + 剪枝',
    tags=['图论算法', '链表树与回溯'],
    code='''
class Solution(object):
    def findMinStep(self, board, hand):

        hold_dict = {}
        for ball in hand:
            hold_dict[ball] = hold_dict.get(ball, 0) + 1

        board_dict = {}
        for ball in board:
            board_dict[ball] = board_dict.get(ball, 0) + 1
        
        for ball in board_dict:
            if board_dict[ball] + hold_dict.get(ball, 0) < 3:
                return -1

        self.res = len(hand) + 1
        self.dfs(board, hold_dict, 1)
        if self.res == len(hand) + 1:
            return -1
        return self.res

    def dfs(self, board, hold_dict, depth):
        if depth >= self.res:
            return

        if not hold_dict:
            return

        board_dict = {}
        for ball in board:
            board_dict[ball] = board_dict.get(ball, 0) + 1
        for ball in board_dict:
            if board_dict[ball] + hold_dict.get(ball, 0) < 3:
                return

        for ball in hold_dict:
            if hold_dict[ball] > 0:
                for index in range(0, len(board) + 1):
                    new_board = board[:index] + ball + board[index:]
                    new_board = self.clear_same(new_board)
                    if not new_board:
                        if depth < self.res:
                            self.res = depth
                            return
                    hold_dict[ball] -= 1
                    self.dfs(new_board, hold_dict, depth + 1)
                    hold_dict[ball] += 1

    def clear_same(self, board):
        now = None
        cnt = 0
        for index, ball in enumerate(board):
            if ball == now:
                cnt += 1
            elif cnt >= 3:
                return self.clear_same(board[:index - cnt] + board[index:])
            else:
                now = ball
                cnt = 1
        if cnt >= 3:
            return self.clear_same(board[:len(board) - cnt])
        return board
''',
    call='Solution().findMinStep("BBRR", "BR")',
    expect=2,
    views=[
        dict(type='string', var='board', label='board（当前层的桌面；clear_same 里是插入后、消除前）', cell=64, h=150,
             pointers={'index': 'blue'}),
        dict(type='map', var='hold_dict', label='hold_dict（手上剩余的球）', h=120),
        dict(type='text', h=70, fn=lambda S: (f"插球并消除后的桌面：`{S['new_board'] or '（空）'}`" if 'new_board' in S else '')),
        dict(type='calls', h=190, hide=('board',)),
    ],
    watch=['depth', ('res', 'self.res', 'green'), 'ball', 'index', 'new_board'],
    captions={
        'if board_dict[ball] + hold_dict.get(ball, 0) < 3': lambda S, B, r: (
            f'`{S.board_dict[S.ball]} + {S.hold_dict.get(S.ball, 0)} < 3`：球 `{S.ball}` 桌上加手上凑不够 3 个 → ==永远消不掉==，没解'
            if S.board_dict[S.ball] + S.hold_dict.get(S.ball, 0) < 3
            else f'`{S.ball}`：桌上 {S.board_dict[S.ball]} + 手上 {S.hold_dict.get(S.ball, 0)} ≥ 3，还有希望'),
        'self.res = len(hand) + 1': '`res` 先设成「比手球总数多 1」，表示还没找到解；后面用它剪枝',
        'self.dfs(board, hold_dict, 1)': '开始 DFS：`depth` 表示这是第几次放球',
        'if depth >= self.res': lambda S, B, r: (
            f'`depth = {S.depth} >= res = {S.self.res}`：已经不比最优解更好 → ==剪枝==' if S.depth >= S.self.res
            else f'`depth = {S.depth} < res = {S.self.res}`：还有可能更优，继续'),
        'if not hold_dict': lambda S, B, r: ('手上没球了，却还没清空 → 回溯' if not S.hold_dict else '手上还有球，继续'),
        'new_board = board[:index]': '把 `{ball}` 插到位置 `{index}`：新桌面 `{new_board}`（还没消除）',
        'new_board = self.clear_same': '调用 `clear_same`：检查 `{new_board}` 里有没有连续 ≥ 3 个的同色段',
        'if not new_board': lambda S, B, r: (f'消除后桌面 `{S.new_board}`：==清空了==！' if not S.new_board else f'消除后桌面 `{S.new_board}`，还有球 → 继续递归往下放'),
        'self.res = depth': '更新最优：`res = {depth}`，这层不用再试别的位置',
        'hold_dict[ball] -= 1': '用掉一个 `{ball}`，`hold_dict[{ball!r}]` = {hold_dict[ball]}',
        'self.dfs(new_board, hold_dict, depth + 1)': '进入下一层：再放第 `{depth + 1}` 个球',
        'hold_dict[ball] += 1': '回溯：把 `{ball}` 还回手里（恢复现场）',
        'return self.clear_same(board[:index - cnt]': lambda S, B, r: (
            f'发现连续 `{B.cnt}` 个 `{B.now}` ≥ 3 → ==消除==，剩 `{B.board[:B.index - B.cnt] + B.board[B.index:]}`，再递归检查连锁'),
        'return self.clear_same(board[:len(board) - cnt])': lambda S, B, r: (
            f'末尾连续 `{B.cnt}` 个 `{B.now}` ≥ 3 → ==消除==，剩 `{B.board[:len(B.board) - B.cnt]}`，再递归检查'),
        'return board': '没有可消除的了，返回桌面 `{ret}`',
        'return self.res': '返回最少插入数 `{self.res}`',
    },
    skip=['now = None', 'cnt = 0', 'cnt += 1', 'cnt = 1', 'board_dict[ball] = board_dict', 'hold_dict[ball] = hold_dict', 'for ball in hand:', 'for ball in board:', 'for ball in board_dict:',
          'board_dict = {}', 'hold_dict = {}', 'for index, ball in enumerate', 'now = ball', 'if ball == now', 'elif cnt >= 3', 'if cnt >= 3'],
    max_steps=62,
    cards=dict(
        one_liner='状压 DP、区间 DP 都不行，只能老老实实 DFS 插球',
        complexity='时间指数级（桌面 ≤ 20、手球 ≤ 5，靠剪枝），空间 `O(n)`',
        problem=['桌上一排彩球，手里几个球；每次可把手里一个球插到任意位置',
                 '连续 ≥ 3 个同色球会消除，消除后可能连锁；求清空桌面的最少插球数，不行返回 `-1`',
                 '本视频：`board="BBRR"`，`hand="BR"` → `2`'],
        quote='于是最后就只能老老实实使用dfs来做了。具体来说就是枚举手上的各类不同的球，尝试将其插入到每一个位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['为什么不用状压 / 区间 DP：==插入新球会改变状态==，`1 << index` 编码和 `f[l][r]` 都表示不了',
              '枚举手里每种球、每个插入位置，插入后用 `clear_same` 反复消除',
              '剪枝：某种颜色桌上加手上不足 3 个就必输；`depth >= res` 直接返回'],
        summary=['时间指数级，靠两个剪枝才能过；空间 `O(n)` 递归深度 ≤ 手球数',
                 '易错点：插入后要==反复==消除（连锁反应），所以 `clear_same` 递归调用自己',
                 '回溯要还原 `hold_dict[ball]`，每次递归前减 1、回来后加 1',
                 '作者提示：消除可以从插入位置向两侧检测，比每次从头扫更快',
                 '原文本身是 Python 2 风格但无需改动，代码逐字照搬'],
    ),
)
