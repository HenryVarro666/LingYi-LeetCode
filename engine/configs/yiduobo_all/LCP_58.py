SHAPES = [["000", "110", "000"], ["110", "011", "000"], ["110", "011", "110"],
          ["000", "010", "111"], ["011", "111", "011"], ["011", "010", "000"]]
N = 3
FACES = ['底面', '前面', '右面', '后面', '左面', '上面']
TARGET = [[0, 1, 2, 3], [0, 4, 5, 6], [1, 7, 8, 4], [2, 7, 9, 10], [3, 10, 11, 6], [5, 8, 9, 11]]


def _bits(v):
    return format(v, f'0{N}b')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    level = S.get('level')
    used = S.get('used') or [False] * 6
    choose = S.get('choose') or []
    cur_edge = S.get('edge') if 'tmp' in S else None
    cv.text((x0 + 18, y0 + 4), '6 块积木（蓝 = 已放，黄框 = 正在试）', 22, T['muted'], bold=True)
    cell = 24
    gap = (x1 - x0 - 40 - 6 * 3 * cell) / 5
    for k, sh in enumerate(SHAPES):
        X0 = x0 + 20 + k * (3 * cell + gap)
        Y0 = y0 + 50
        for r in range(N):
            for c in range(N):
                one = sh[r][c] == '1'
                fill = (T['blue'] if used[k] else (125, 133, 145)) if one else T['panel2']
                cv.rect((X0 + c * cell + 1, Y0 + r * cell + 1, X0 + (c + 1) * cell - 1, Y0 + (r + 1) * cell - 1), fill=fill, r=3)
        if cur_edge == k:
            cv.rect((X0 - 4, Y0 - 4, X0 + N * cell + 4, Y0 + N * cell + 4), outline=T['yellow'], width=4, r=6)
        cv.text((X0 + N * cell / 2, Y0 + N * cell + 6), f'积木 {k}', 18, T['text'] if used[k] else T['dim'], anchor='mt', bold=True)
    # 12 条棱
    yb = y0 + 190
    cv.text((x0 + 18, yb), '正方体 12 条棱的编码（高位 → 低位，每位 1 = 被占）', 22, T['muted'], bold=True)
    tgt = TARGET[level] if level is not None and 0 <= level < 6 else []
    tmp = S.get('tmp')
    bw = (x1 - x0 - 40) / 6
    for e in range(12):
        row, col = divmod(e, 6)
        X = x0 + 20 + col * bw
        Y = yb + 40 + row * 84
        filled = e < len(choose)
        hot = e in tgt
        cv.rect((X + 3, Y, X + bw - 3, Y + 70), fill=(52, 60, 72) if filled else T['panel2'], outline=T['yellow'] if hot else T['border'],
                width=3 if hot else 1, r=8)
        cv.text((X + 12, Y + 6), f'棱 {e}', 18, T['yellow'] if hot else T['dim'], bold=True)
        cv.text((X + bw / 2, Y + 44), _bits(choose[e]) if filled else '???', 28, T['green'] if filled else T['dim'], anchor='mm', mono=True, bold=True)
    # 当前尝试
    yt = yb + 40 + 2 * 84 + 8
    if level is not None and tmp is not None and 'edge' in S:
        cv.text((x0 + 18, yt), f'第 {level} 步 · {FACES[level]}：试放积木 {S["edge"]}（{"翻面" if S.get("d") else "原样"}，旋转方案 {S.get("candidate")}）', 22, T['yellow'], bold=True)
        parts = '  '.join(f'棱{TARGET[level][k]}={_bits(tmp[k])}' for k in range(4))
        cv.text((x0 + 18, yt + 34), '这个面的四条边：' + parts, 21, T['text'], mono=True)
        if 'flag' in S and S.get('_line') == 96:
            cv.text((x0 + 18, yt + 68), '与已摆好的棱：不重叠、中间能补满 → 可以放' if S['flag'] else '与已摆好的棱：重叠或中间有缺口 → 不行',
                    22, T['green'] if S['flag'] else T['red'], bold=True)


def _tmp(S, B, r):
    lv = S.level
    return (f'第 `{lv}` 面（{FACES[lv]}）试放积木 `{S.edge}`：`{"翻面" if S.d else "不翻面"}`，边的排列方案 `{S.candidate}`；'
            f'四条边编码 `{[_bits(v) for v in S.tmp]}`')


def _flag(S, B, r):
    if S.flag:
        return '四条边和已填好的棱都满足「按位与 = 0」且「按位或 ≥ 0111…10」→ ==这个摆法可行==，记下并去放下一个面'
    return '某条已填过的棱出现了==重叠==（按位与 ≠ 0）或==中间有缺口==（按位或太小）→ 换下一种摆法'


CONFIG = dict(
    num='LCP 58', title='积木拼接', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='位运算编码边 + 枚举 8 种放法回溯',
    tags=['灵神题单·常用数据结构', '灵神题单·链表树与回溯'],
    code=r"""
class Solution(object):
    def composeCube(self, shapes):

        '''
                       ___________9____________
                      /|                      /|
                     / |                     / |
                   11  |                    8  |
                   /   |                   /   |  
                  /   10                  /    7
                 /_____|______5__________/     |
                 |     |                 |     |
                 |     |                 |     |
                 |     |___________2_____|_____|
                 |     /                 |     / 
                 6    /                  4    /
                 |   3                   |   1
                 |  /                    |  /
                 | /                     | /
                 |/___________0__________|/

                ori:                rev:
                   <----               <----
                     2                   0
               |            ^      |            ^
               | 3        1 |      | 3'       1'|
               v            |      v            |
                     0                   2
                   ---->               ----> 
        '''

        #6个面的枚举顺序，以及影响到的棱
        target_list = [[0, 1, 2, 3], [0, 4, 5, 6], [1, 7, 8, 4], [2, 7, 9, 10], [3, 10, 11, 6], [5, 8, 9, 11]]

        #编码顺序冲突的棱，检验时需要一方反向编码
        reverst_list = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]]
        
        n = len(shapes[0])
        state_without_corner = (1 << (n - 1)) - 2
        edge_list = []
        one_cnt = 0
        for s in shapes:
            edge_list.append([[0, 0, 0, 0], [0, 0, 0, 0]])
            for index in range(n):
                #按下、右、上、左的顺序逆时针编码
                edge_list[-1][0][0] += edge_list[-1][0][0] + int(s[n - 1][index])
                edge_list[-1][0][1] += edge_list[-1][0][1] + int(s[n - 1 - index][n - 1])
                edge_list[-1][0][2] += edge_list[-1][0][2] + int(s[0][n - 1 - index])
                edge_list[-1][0][3] += edge_list[-1][0][3] + int(s[index][0])

                #顺时针编码
                edge_list[-1][1][0] += edge_list[-1][1][0] + int(s[n - 1][n - 1 - index])
                edge_list[-1][1][1] += edge_list[-1][1][1] + int(s[index][n - 1])
                edge_list[-1][1][2] += edge_list[-1][1][2] + int(s[0][index])
                edge_list[-1][1][3] += edge_list[-1][1][3] + int(s[n - 1 - index][0])
        
                #统计1的数量
                one_cnt += int(s[0][index]) + int(s[n - 1][index]) + int(s[index][0]) + int(s[index][n - 1])
            
            #减去四个角重复计算的1
            one_cnt -= int(s[0][0]) + int(s[0][n - 1]) + int(s[n - 1][n - 1]) + int(s[n - 1][0])

        #判断1的数量是否合法
        if one_cnt != n * 12 - 16:
            return False

        #8种板子的放置方式
        candidate_list = [[[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]], 
                     [[0, 3, 2, 1], [1, 0, 3, 2], [2, 1, 0, 3], [3, 2, 1, 0]]]

        def dfs(level, choose, used):
            if level == 6:
                return True
            
            for edge in range(6):
                if not used[edge]:
                    #对于没有用过的板子，枚举所有可能的放置方法
                    for d in range(2):
                        for candidate in candidate_list[d]:
                            #放置后4条边对应的编码
                            #当前编码方式d与reverst_list异或，表示对于冲突棱的校验需要按当前编码方式进行反向编码
                            tmp = [edge_list[edge][d ^ reverst_list[level][index]][candidate[index]] for index in range(4)]
                            flag = True
                            fill_cnt = 0
                            for index in range(4):
                                #对于已经填充过的棱，需要检验重叠以及中间部分填充
                                if target_list[level][index] < len(choose):
                                    now = tmp[index]
                                    filled = choose[target_list[level][index]]
                                    if (now & filled) != 0 or (now | filled) < state_without_corner:
                                        flag = False
                                        break
                                else:
                                    fill_cnt += 1
                            
                            if flag:
                                #检验通过，按当前枚举的方式放置板子，然后继续处理下一个面
                                for index in range(4):
                                    if target_list[level][index] < len(choose):
                                        continue
                                    choose.append(tmp[index])
                                used[edge] = True
                                if dfs(level + 1, choose, used):
                                    return True
                                used[edge] = False
                                for index in range(fill_cnt):
                                    choose.pop()
            
            return False

        #板子0作为底面
        choose = [edge_list[0][0][0], edge_list[0][0][1], edge_list[0][0][2], edge_list[0][0][3]]
        used = [False] * 6
        used[0] = True
        if dfs(1, choose, used):
            return True

        #板子0翻转后作为底面
        choose = [edge_list[0][1][0], edge_list[0][1][3], edge_list[0][1][2], edge_list[0][1][1]]
        if dfs(1, choose, used):
            return True
        
        return False
""",
    call=f'Solution().composeCube({SHAPES!r})',
    expect=True,
    max_events=800000,
    max_steps=38,
    skip=['edge_list.append', 'for index in range(n)', 'edge_list[-1]', 'one_cnt +=', 'one_cnt -=', 'for s in shapes', 'state_without_corner',
          'for edge in range(6)', 'if not used[edge]', 'for d in range(2)', 'for candidate in', 'flag = True', 'fill_cnt = 0',
          'for index in range(4):', 'if target_list', 'now = tmp', 'filled = choose', 'if (now & filled)', 'flag = False', 'break',
          'else:', 'fill_cnt += 1', 'continue', 'choose.append(tmp[index])', 'for index in range(fill_cnt)', 'choose.pop()',
          'used[edge] = False', 'used[edge] = True', 'if level == 6', 'candidate_list =', '[[0, 3, 2, 1]', 'edge_list = []', 'one_cnt = 0'],
    views=[
        dict(type='custom', draw=_draw, h=600),
        dict(type='calls', h=100, hide=('choose', 'used')),
    ],
    watch=['level'],
    captions={
        'target_list =': '6 个面的枚举顺序：底、前、右、后、左、上；每个面各自影响正方体的 4 条棱（棱编号见代码里的示意图）',
        'reverst_list =': '有些棱在相邻两个面里的编码方向相反，校验时要让其中一方反向编码',
        'n = len(shapes[0])': '`n = {n}`：每块积木是 `n × n`',
        'if one_cnt != n * 12 - 16': '六块积木==四条边==上的 1 共 `{one_cnt}` 个（四个角不重复算）；正方体 12 条棱需要 `12n − 16 = {n * 12 - 16}` 个 → 数量不对就直接 False',
        'choose = [edge_list[0][0][0]': '积木 0 直接当底面：选哪个面只是换朝向，所以==不用旋转，只考虑翻不翻面==。它的四条边编码填进棱 0、1、2、3',
        'used[0] = True': '积木 0 已用',
        'if dfs(1, choose, used)': lambda S, B, r: ('从第 1 个面（前面）开始，枚举剩下积木的 8 种放法' if S._line < 120 else '底面不翻面凑不出，把积木 0 ==翻面==再试一次'),
        'tmp = [': _tmp,
        'if flag': _flag,
        'if dfs(level + 1': lambda S, B, r: f'这个面放好，棱 {TARGET[B.level]} 都定了 → 去放第 `{B.level + 1}` 个面',
        'return True': lambda S, B, r: ('6 个面都放好了，没有重叠 → ==能拼成正方体==，一路返回 True' if S._line < 90 else '这一层也返回 True，继续往上传'),
        'choose = [edge_list[0][1][0]': '积木 0 翻面作底面：四条边取顺时针编码，棱的顺序是 0,3,2,1',
        'return False': '两种底面都试完了 → False',
    },
    cards=dict(
        one_liner='把积木的四条边编码成二进制数，按位与判重叠、按位或判补满',
        complexity='时间 `O(6!·8^5·n)`（强剪枝后很小），空间 `O(n)`',
        problem=['6 块 `n×n` 积木（`1` 有格子，`0` 空缺，中间保证实心），可旋转、翻面',
                 '问能否各当正方体的一个面，==边缘严丝合缝==拼成正方体',
                 '本视频用示例 1（`n = 3`）→ `true`'],
        quote='对于棱长为n的正方体而言，这12条棱上一共有12 * n - 16个位置……底面的下侧边和前面的下侧边按位与必须等于0，否则就有位置重叠了。按位或必须大于等于(1 << (n - 1)) - 2，也就是二进制表示中的0111...1110。',
        quote_src='—— yiduobo 题解原文',
        idea=['六块板四条边 = 12 条棱，先数 1 的个数是否恰好 `12n − 16`',
              '每条边编码成 `n` 位二进制数，原样用逆时针编码，翻面用顺时针编码',
              '积木 0 固定当底面，其余面按 前、右、后、左、上 的顺序枚举积木、翻面、4 种旋转',
              '新放的面和已填的棱：按位与 ≠ 0 就重叠，按位或不够 `0111…10` 就有缺口，剪掉'],
        summary=['时间：最坏 `5!·8^5` 量级，但每步用位运算判断，剪枝很强；空间 `O(n)`',
                 '易错：棱 2、5、8、10、11、4 的编码方向相邻两面相反，要用 `reverst_list` 异或翻转编码',
                 '易错：积木 0 作底面只需考虑==翻不翻面==，不用考虑旋转',
                 '原文本身可直接在 Python 3 运行，未做修改（保留了开头那段棱编号示意图的字符串）',
                 '视频里数 1 与编码预处理没有逐行展示，只展示放面的回溯过程'],
    ),
)
