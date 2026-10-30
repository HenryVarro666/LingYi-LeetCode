import math

CODE = '''
class Solution(object):
    def slidingPuzzle(self, board):

        factor = [1, 1, 2, 6, 24, 120, 720]
        now = self.cantor(board, factor)
        target = self.cantor([[1, 2, 3], [4, 5, 0]], factor)
        if now == target:
            return 0

        used = [False] * factor[-1]
        q = [now]
        used[now] = True
        l, r = 0, 1
        step = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        while l < r:
            step += 1
            for now in q[l: r]:
                now_board = self.cantor_reverse(now, factor)
                for nowx in range(2):
                    for nowy in range(3):
                        if now_board[nowx][nowy] == 0:
                            break
                    if now_board[nowx][nowy] == 0:
                        break
            
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < 2 and y >= 0 and y < 3:
                        now_board[nowx][nowy], now_board[x][y] = now_board[x][y], now_board[nowx][nowy]
                        tmp = self.cantor(now_board, factor)
                        if not used[tmp]:
                            used[tmp] = True
                            q.append(tmp)
                        now_board[nowx][nowy], now_board[x][y] = now_board[x][y], now_board[nowx][nowy]
            
            if used[target]:
                return step

            l, r = r, len(q)
        
        return -1

    def cantor(self, board, factor):
        tmp = board[0] + board[1]
        res = 0
        for i in range(6):
            cnt = 0
            for j in range(i + 1, 6):
                if tmp[i] > tmp[j]:
                    cnt += 1
            res += cnt * factor[6 - i - 1]

        return res

    def cantor_reverse(self, num, factor):
        res = []
        used = [False] * 6
        for i in range(6):
            cnt = num // factor[6 - i - 1]
            num -= cnt * factor[6 - i - 1]
            for j in range(6):
                if not used[j]:
                    if cnt == 0:
                        res.append(j)
                        used[j] = True
                        break
                    cnt -= 1
        
        return [res[:3], res[3:6]]
'''

_LINES = CODE.strip('\n').split('\n')
_HELPER = next(i for i, s in enumerate(_LINES, 1) if 'def cantor(self' in s)
_ZERO = [i for i, s in enumerate(_LINES, 1)
         if any(k in s for k in ('for nowx in range', 'for nowy in range', 'if now_board[nowx][nowy] == 0', 'break'))]
BOARD = [[1, 2, 3], [0, 4, 5]]


def _dec(num):
    rest = list(range(6))
    out = []
    for i in range(6):
        f = math.factorial(5 - i)
        out.append(rest.pop(num // f))
        num %= f
    return out


def _bs(num):
    p = _dec(num)
    return ''.join(map(str, p[:3])) + '/' + ''.join(map(str, p[3:]))


def _board_view(S):
    nb = S.get('now_board')
    if isinstance(nb, list) and len(nb) == 2 and 'step' in S:
        return nb
    return None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (x >= 0 and x < 2 and y >= 0 and y < 3):
        return f'0 往 `({x},{y})` 移会出界 → 跳过'
    return f'`({x},{y})` 在界内 → 把它和 0 ==交换==，得到新状态'


def _tmp(S, B, r):
    t = S.tmp
    if B.used[t]:
        return f'交换后的棋盘编码为 `{t}`，已出现过 → 不入队'
    return f'交换后的棋盘编码为 =={t}==，第一次出现 → `used[{t}] = True` 并入队'


CONFIG = dict(
    num=773, title='滑动谜题', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='BFS + 康托展开编码状态',
    tags=['labuladong', '灵神题单·图论算法'],
    code=CODE,
    call=f'Solution().slidingPuzzle({BOARD})',
    expect=2,
    max_steps=75,
    skip=list(range(_HELPER, len(_LINES) + 1)) + _ZERO + ['dx = [', 'dy = [', 'x = nowx', 'y = nowy',
                                                          'q.append(tmp)', 'for index in range(4)',
                                                          'used[now] = True', 'l, r = 0, 1', 'step = 0', 'tmp = self.cantor(now_board', 'used[tmp] = True'],
    views=[
        dict(type='text', fn=lambda S: (f"目标 `123/450` 的编码 `target = {S['target']}`"
                                        + (f"　　当前状态 `now = {S['now']}` ↔ `{_bs(S['now'])}`" if isinstance(S.get('now'), int) else ''))
             if isinstance(S.get('target'), int) else '康托展开：把 0~5 的排列编成 0~719 的整数', size=26, h=60),
        dict(type='grid', var=_board_view, label='now_board（蓝框 = 0 所在格，粉框 = 要和它交换的格）', cell=96, h=290,
             color=lambda S, i, j, v: 'yellow' if v == 0 else None,
             cursors=[('nowx', 'nowy', 'blue'), ('x', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'{c}' for c in S['q']] if isinstance(S.get('q'), list) and 'step' in S else None,
             label='q：状态编码（暗 = 之前的轮次，[l, r) = 当前这一轮）', cell=86, h=170,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='text', fn=lambda S: ('q 对应的棋盘：' + '  '.join(f'`{c}={_bs(c)}`' for c in S['q'][:5])
                                        + (' …' if len(S['q']) > 5 else '')) if isinstance(S.get('q'), list) and 'step' in S else '',
             size=22, h=50),
    ],
    watch=[('step', 'step', 'green'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('tmp', 'tmp', 'yellow')],
    captions={
        'factor = [': '`factor[k] = k!`：康托展开要用到的阶乘表',
        'now = self.cantor(board': '把初始棋盘按行展开成排列，用==康托展开==编码成整数',
        'target = self.cantor': '目标 `[[1,2,3],[4,5,0]]` 也编码成整数',
        'if now == target': lambda S, B, r: (f'初始编码 `{S.now}` ≠ 目标 `{S.target}`，需要移动' if S.now != S.target else '已经是目标'),
        'used = [False] * factor[-1]': '6 个数一共 `6! = 720` 种排列 → 用长度 720 的数组去重',
        'q = [now]': lambda S, B, r: f'初始状态 `{S.now}`（`{_bs(S.now)}`）入队并标记',
        'used[now] = True': '标记初始状态已出现',
        'l, r = 0, 1': '`q[l:r]` 是当前这一轮的状态',
        'step = 0': '`step` = 已经走了几步',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：这一轮还有状态' if S.l < S.r else '没有新状态了'),
        'step += 1': '第 =={step}== 轮：扩展出的状态都要 {step} 步',
        'for now in q[l: r]': lambda S, B, r: ('这一轮的状态都扩展完了' if 'now_board' in B and B.now == S.now else f'取出编码 `{S.now}`'),
        'now_board = self.cantor_reverse': lambda S, B, r: f'==康托逆展开==：编码 `{B.now}` → 棋盘 `{_bs(B.now)}`，再找到 0 的位置',
        'if x >= 0 and x < 2': _nb,
        'now_board[nowx][nowy], now_board[x][y] = now_board[x][y], now_board[nowx][nowy]':
            lambda S, B, r: (f'交换后：`{S.now_board}`' if 'tmp' not in S or S.tmp is None or not isinstance(S.now_board, list)
                             or S.now_board[S.nowx][S.nowy] != 0 else f'换回来，恢复 `{S.now_board}`，试下一个方向'),
        'tmp = self.cantor(now_board': '把交换后的棋盘编码',
        'if not used[tmp]': _tmp,
        'used[tmp] = True': '`used[{tmp}] = True`，`{tmp}` 入队',
        'if used[target]': lambda S, B, r: (f'这一轮扩展完，==目标 `{S.target}` 已出现== → 答案就是 `step = {S.step}`'
                                            if S.used[S.target] else f'这一轮扩展完，目标还没出现'),
        'return step': '最少移动 =={step}== 次',
        'l, r = r, len(q)': '进入下一轮：`l, r = {l}, {r}`',
    },
    cards=dict(
        one_liner='BFS 搜索所有棋盘状态，用康托展开把状态编成 0~719 去重',
        complexity='时间 `O(6! × 4 × 6^2)`，空间 `O(6!)`',
        problem=['2×3 的板上有 1~5 五块砖和一个空位 0，0 每次可以和上下左右相邻的砖交换',
                 '求变成 `[[1,2,3],[4,5,0]]` 的最少步数，做不到返回 -1',
                 '本视频：`[[1,2,3],[0,4,5]]` → `2`'],
        quote='对于题目中的板子，如果从上往下从左往右排下来，那么就可以形成一个0到5的全排列。对于这个排列，==可以使用康拓展开来进行编码==。',
        quote_src='—— yiduobo 题解原文',
        before=[dict(heading='康托展开（原文的例子）', lines=[
            '排列 `4,1,2,5,0,3`：每一位看“后面比它小的有几个”',
            '`4×5! + 1×4! + 1×3! + 2×2! + 0×1! = 480+24+6+4+0 = 514`',
            '逆过来：`514 // 120 = 4` 余 `34`，`34 // 24 = 1` 余 `10` ……',
            '每次除以阶乘，商 `k` 表示取剩余数字里==第 k+1 小==的'])],
        idea=['720 种状态各有唯一编号，`used` 数组即可去重',
              'BFS 按轮扩展：解码 → 找到 0 → 四个方向交换 → 编码 → 没出现过就入队',
              '一轮结束后若 `used[target]` 为真，当前轮数就是答案'],
        summary=['状态只有 `6! = 720` 个，BFS 每个状态最多入队一次',
                 '交换后要==换回来==，再试下一个方向',
                 '原文在整轮扩展完才检查目标，结果仍是最短步数',
                 '原文为 Python 2 写法，`cantor_reverse` 中的整数除法 `num / factor[...]` 已改为 `//`'],
    ),
)
