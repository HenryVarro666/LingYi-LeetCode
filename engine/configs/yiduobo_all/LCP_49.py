def _b(x, w=3):
    return format(x, f'0{w}b')


def _cl(S):
    return list(S['check_list']) if 'check_list' in S else list(S['challenge'])


def _lr(S, name):
    v = S.get(name)
    if v is None:
        return ['?'] * len(S['challenge'])
    return ['?' if x is None else x for x in v]


def _text(S):
    if 'res' not in S:
        return '先求最高位，再从高位到低位逐位尝试把 `res` 的这一位置 0'
    w = max(3, len(bin(max(S['challenge']))) - 2)
    s = f"`res` = =={_b(S['res'], w)}=={f'（{S['res']}）'}"
    if 'now' in S and 'p' in S and 'left' in S:
        s += f"　当前能力 `now` = =={_b(S['now'], w)}=="
    if S.get('pow2'):
        s += f"　试探位 `pow2` = {S['pow2']}"
    return s


CONFIG = dict(
    num='LCP 49', title='环形闯关游戏', difficulty='Hard', category='位运算',
    author='yiduobo', technique='高位向低位贪心 · 环形展开 + 单调扩展',
    tags=[],
    code='''
class Solution(object):
    def ringGame(self, challenge):

        n = len(challenge)
        ma = max(challenge)
        max_l = 0
        while ma:
            max_l += 1
            ma //= 2
        
        pow2 = 1
        for index in range(max_l - 1):
            pow2 += pow2
        
        check_list = challenge[:] + challenge[:] + challenge[:]

        def check():
            left = [None] * n
            right = [None] * n

            stack = []
            now = res
            p = n
            while p < n + n:
                while p < n + n + n and now >= check_list[p]:
                    now |= check_list[p]
                    if p < n + n:
                        stack.append(p)
                    p += 1
            
                while stack:
                    right[stack[-1] - n] = p
                    stack.pop()
                
                if p < n + n:
                    right[p - n] = p
                now = res
                p += 1
            
            stack = []
            now = res
            p = n + n - 1
            while p >= n:
                while p >= 0 and now >= check_list[p]:
                    now |= check_list[p]
                    if p >= n:
                        stack.append(p)
                    p -= 1
                
                while stack:
                    left[stack[-1] - n] = p
                    stack.pop()
                
                if p >= n:
                    left[p - n] = p
                now = res
                p -= 1

            for index in range(n):
                if right[index] - 1 - left[index] >= n:
                    return True

            return False

        res = pow2 + pow2 - 1
        pow2 //= 2
        while pow2:
            res -= pow2
            if not check():
                res += pow2
            pow2 //= 2

        return res
''',
    call='Solution().ringGame([2, 4, 7])',
    expect=5,
    max_steps=90,
    skip=['ma = max', 'pow2 = 1', 'for index in range(n)', 'max_l = 0', 'while ma', 'max_l += 1', 'ma //= 2', 'for index in range(max_l', 'pow2 += pow2',
          'left = [None]', 'right = [None]', 'stack = []', 'now = res', 'stack.pop()', 'while stack', 'def check',
          'right[stack[-1]', 'left[stack[-1]', 'now |= ', 'stack.append', 'if p < n + n:', 'if p >= n:', 'right[p - n] = p', 'left[p - n] = p',
          'p += 1', 'p -= 1', 'p = n', 'p = n + n - 1', 'while p < n + n:', 'while p >= n:'],
    views=[
        dict(type='text', fn=_text, size=26, h=100),
        dict(type='array', var=_cl, label='check_list（复制三份，中间一份下标 n..2n-1 是真正的起点）', cell=64, h=230,
             pointers={'p': 'blue'},
             dim=lambda S, i, v: 'challenge' in S and not (len(S['challenge']) <= i < 2 * len(S['challenge'])),
             color=lambda S, i, v: 'blue' if S.get('p') == i else None),
        dict(type='array', var=lambda S: _lr(S, 'left'), label='left[i]：从 i 向左最远能扩展到的位置', cell=64, h=200),
        dict(type='array', var=lambda S: _lr(S, 'right'), label='right[i]：从 i 向右最远（不含）扩展到的位置', cell=64, h=200),
    ],
    watch=[('pow2', 'pow2', 'yellow'), ('res', 'res', 'green'), ('now', 'now', 'cyan'), ('p', 'p', 'blue')],
    captions={
        'n = len': '`n = {n}` 个关卡，成环',
        'check_list = ': '环形化成线性：把数组复制三份，只枚举中间一份作起点，两边留给扩展',
        'res = pow2 + pow2 - 1': '`res` 先设成所有位都是 1 的最大值 `{res}`（二进制 `{res:b}`），从高位往下尝试置 0',
        'pow2 //= 2': lambda S, B, r: ('`pow2` 减半，试探下一位' if S.pow2 else '所有位都试过了'),
        'while pow2': lambda S, B, r: (f'`pow2 = {S.pow2}`：试着把 `res` 的这一位变成 0' if S.pow2 else '`pow2 = 0`，所有位都处理完，结束'),
        'res -= pow2': '假设这一位为 0：`res` → =={res}==（二进制 `{res:b}`），能否仍然通关？',
        'while p < n + n + n and': lambda S, B, r: (
            f'向右扩展：`now = {S.now}` `>=` `check_list[{S.p}] = {S.check_list[S.p]}` → ==能过==，`now |=` 它，继续右移'
            if S.p < 3 * S.n and S.now >= S.check_list[S.p] else
            (f'向右扩展停止：已到右边尽头（`p = {S.p}`）' if S.p >= 3 * S.n else f'向右扩展停止：`now = {S.now}` 小于 `check_list[{S.p}] = {S.check_list[S.p]}`，这批起点最远扩展到 `{S.p}`（不含）')),
        'while p >= 0 and': lambda S, B, r: (
            f'向左扩展：`now = {S.now}` `>=` `check_list[{S.p}] = {S.check_list[S.p]}` → ==能过==，`now |=` 它，继续左移'
            if S.p >= 0 and S.now >= S.check_list[S.p] else
            (f'向左扩展停止：已到左边尽头（`p = {S.p}`）' if S.p < 0 else f'向左扩展停止：`now = {S.now}` 小于 `check_list[{S.p}] = {S.check_list[S.p]}`，这批起点最远扩展到 `{S.p}`')),
        'for index in range(n)': lambda S, B, r: f'逐个起点查看：左右能扩展的总长度是否覆盖整圈 `n = {S.n}`',
        'if right[index] - 1 - left[index] >= n': '起点 `{index}`：`right − 1 − left` = `{right[index]} − 1 − ({left[index]})` = {right[index] - 1 - left[index]}，' + '{"`>= n` ==能通关==" if right[index] - 1 - left[index] >= n else "`< n`，这个起点走不完一圈"}',
        'return True': '存在能扩展整圈的起点：这个 `res` ==可行==',
        'return False': '没有起点能通关：这个 `res` ==不可行==',
        'if not check()': '调用 `check()`：用 `res = {res}` 作初始能力值，能通关整圈吗？',
        'res += pow2': '这一位必须是 1：把 `pow2` 加回去，`res` → =={res}==',
        'return res': '每一位都定下来了：最小初始能力值 ==`{res}`==',
    },
    cards=dict(
        one_liner='从高位到低位逐位试：这一位能置 0 就置 0',
        complexity='时间 `O(n log C)`，空间 `O(n)`',
        problem=['环形的 `n` 个关卡，`challenge[i]` 是第 `i` 关的挑战值',
                 '选初始能力值 `res`，可从任一关开始，向左右相邻关卡闯',
                 '能力 `>=` 关卡值才能过，过关后 `能力 |= 关卡值`',
                 '求能通关整圈的最小初始能力值。本视频：`[2,4,7]` → `5`'],
        quote='一个自然的想法就是从高位开始逐位向下确定当前位为0时能否完成闯关。若可以，那么该位就是0，否则该位是1。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案的最高位必须是 1（或运算只增不减）：先令 `res` 全 1',
              '从高位往下逐位试 0，用 `check()` 判断当前 `res` 能否通关整圈',
              '环形问题复制三份成线性；从每个起点用单调栈思路求向左、向右最远能扩展到哪',
              '`right - 1 - left >= n` 说明该起点能走完一整圈'],
        summary=['时间 `O(n log C)`，空间 `O(n)`（`C` 为最大值）',
                 '易错：扩展指的是 `now >= 关卡值` 后 `now |= 关卡值`，不是加法',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`',
                 '视频只展示 `check()` 的关键判断，栈内的逐行操作已折叠'],
    ),
)
