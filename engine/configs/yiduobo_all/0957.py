def _txt(S):
    if 'q' not in S:
        return ''
    q = S['q']
    return f"已经历 `{S.get('rnd', 1)}` 天，状态序列 `q` 共 {len(q)} 个；只有中间 6 间会变，状态数至多 ==64== 种"


CONFIG = dict(
    num=957, title='N天后的牢房', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='状态压缩 + 找环取模',
    code='''
class Solution(object):
    def prisonAfterNDays(self, cells, n):

        pow2 = [1, 2, 4, 8, 16, 32]

        now = 0
        for i in range(1, 7):
            if cells[i - 1] == cells[i + 1]:
                now += pow2[i - 1]
        
        q = [now]
        step = {now : 1}
        rnd = 1
        while rnd < n:
            now = q[-1]
            rnd += 1
            now_cell = [0] * 6
            for i in range(6):
                if now & pow2[i]:
                    now_cell[i] = 1

            next_cell = []
            for i in range(6):
                if i == 0:
                    next_cell.append(1 - now_cell[1])
                elif i == 5:
                    next_cell.append(1 - now_cell[4])
                elif now_cell[i - 1] == now_cell[i + 1]:
                    next_cell.append(1)
                else:
                    next_cell.append(0)
            
            next = 0
            for i in range(6):
                next += next_cell[i] * pow2[i]

            if next in step:
                start_rnd = step[next]
                loop_len = rnd - start_rnd
                final_state = q[start_rnd - 1 + (n - start_rnd) % loop_len]
                final_cell = [0] * 6
                for i in range(6):
                    if final_state & pow2[i]:
                        final_cell[i] = 1
                return [0] + final_cell + [0]
        
            q.append(next)
            step[next] = rnd

        final_state = q[-1]
        final_cell = [0] * 6
        for i in range(6):
            if final_state & pow2[i]:
                final_cell[i] = 1
        return [0] + final_cell + [0]
''',
    call='Solution().prisonAfterNDays([1, 0, 0, 1, 0, 1, 1, 0], 1000000000)',
    expect=[0, 1, 1, 1, 1, 1, 1, 0],
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='cells', label='cells（初始牢房）', cell=60, h=130),
        dict(type='array', var='now_cell', label='now_cell（今天的中间 6 间）', cell=60, h=130),
        dict(type='array', var='next_cell', label='next_cell（明天的中间 6 间）', cell=60, h=130,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='array', var='q', label='q：每一天的状态（6 位二进制编码）', cell=60, h=130),
        dict(type='map', var='step', label='step：状态 → 第一次出现的天数', h=120, font=22),
    ],
    watch=['rnd', 'now', 'next', ('n', 'n', 'blue')],
    skip=['for i in range(1, 7)', 'if cells[i - 1] == cells[i + 1]', 'now += pow2[i - 1]', 'pow2 = ',
          'for i in range(6)', 'if now & pow2[i]', 'now_cell[i] = 1', 'if i == 0', 'next_cell.append',
          'elif i == 5', 'elif now_cell', 'else:', 'next += next_cell', 'if final_state & pow2[i]', 'final_cell[i] = 1',
          'now = 0', 'rnd = 1', 'now_cell = [0] * 6'],
    captions={
        'q = [now]': lambda S, B, r: f'第 1 天的状态编码成整数 `now = {S.now}`（第 i 间对应 `2^i`）；==两侧牢房第 1 天起恒为 0==，只需记录中间 6 间',
        'step = {now': '`step` 记录“某状态第一次出现在第几天”，`rnd` 是已推到第几天',
        'while rnd < n': lambda S, B, r: (f'`rnd = {S.rnd} < n`：还没推到第 n 天，继续' if S.rnd < S.n else '推完了'),
        'now = q[-1]': '取出最近一天的状态 `now = {now}`',
        'rnd += 1': '推演第 `{rnd}` 天',
        'next_cell = []': lambda S, B, r: f'解码得 `now_cell = {S.now_cell}`；下面按规则算明天：两边邻居相同则 ==1==，否则 0（最左/最右的邻居是墙，视为 0）',
        'next = 0': lambda S, B, r: f'明天的状态 `next_cell = {S.next_cell}`，再编码回整数',
        'if next in step': lambda S, B, r: (f'`next = {S.next}` ==已经出现过==（第 {S.step[S.next]} 天）→ 找到环' if S.next in S.step else f'`next = {S.next}` 是新状态，继续往下推'),
        'start_rnd = step[next]': '环从第 `{start_rnd}` 天开始',
        'loop_len = rnd - start_rnd': '环长 = `{rnd} - {start_rnd}` = =={loop_len}==',
        'final_state = q[start_rnd - 1': lambda S, B, r: f'第 n 天落在环里：`(n - start_rnd) % loop_len = {(S.n - S.start_rnd) % S.loop_len}`，所以答案是 `q[{S.start_rnd - 1 + (S.n - S.start_rnd) % S.loop_len}]` = =={S.final_state}==，不用真的推 10^9 天',
        'final_cell = [0] * 6': lambda S, B, r: f'把答案状态 `{S.final_state}` 解码回 6 位',
        'return [0] + final_cell': lambda S, B, r: f'两侧补 0，得到 `{r}`',
        'q.append(next)': '把新状态记到队列 `q`（第 `{rnd}` 天）',
        'step[next] = rnd': '`step[{next}] = {rnd}`：记下它第一次出现的天数，之后碰到就是环',
        'final_state = q[-1]': '没有找到环就推到了第 n 天，直接取最后一个状态',
    },
    max_steps=110,
    cards=dict(
        one_liner='状态只有 2^6 种，一定有环：找到环再对 N 取模',
        complexity='时间 `O(2^6)`（与 N 无关），空间 `O(2^6)`',
        problem=['8 间牢房一排，每天：相邻两间 ==同占用或同空置== 则今天为 1，否则为 0',
                 '两端的牢房没有两个邻居，所以第 1 天起总是 0',
                 '求 `N` 天后的状态，`N` 最大 `10^9`',
                 '本视频：`[1,0,0,1,0,1,1,0]`，`N = 10^9` → `[0,1,1,1,1,1,1,0]`'],
        quote='乍一看这个N最多到10^9很吓人，但是仔细观察可以发现，从第1天开始，两侧的两间牢房就必然为0了，而剩下的6间牢房要么为0要么为1，也就是说之后任意一天牢房的状态撑死了也就2^6 = 32种。',
        quote_src='—— yiduobo 题解原文',
        idea=['把中间 6 间编码成二进制整数；每个状态只有一个“明天”，相当于每点一条出边的有向图，一定有环',
              '用字典 `step` 记状态第一次出现的天数，用列表 `q` 按天记状态',
              '再次遇到旧状态 `next`：环长 `rnd - step[next]`，答案在 `q` 里按余数取'],
        summary=['时间 `O(2^6)`，空间 `O(2^6)`，和 `N` 的大小无关',
                 '易错：状态按“第 1 天”起记录，所以 `q` 的下标要 `start_rnd - 1`',
                 '`n` 很小、没走到环时，直接取 `q[-1]` 即可',
                 '原文在 Python 3 下无需修改，逐字照搬；变量 `next` 覆盖了内置函数名但不影响结果'],
    ),
)
