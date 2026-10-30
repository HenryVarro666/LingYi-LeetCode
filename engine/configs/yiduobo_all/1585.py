def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pl = S.get('pos_list')
    if pl is None:
        return
    digs = sorted(set(S['s']) | set(S['t']))
    np_ = S.get('now_pos')
    cur = int(S['char']) if 'char' in S else None
    cv.text((x0 + 18, y0 + 4), 'pos_list：每个数字在 s 中的位置（黄 = 队首，还没被用的最靠前位置）', 22, T['muted'], bold=True)
    cell, rowh = 56, 60
    top = y0 + 46
    for r, dch in enumerate(digs):
        d = int(dch)
        y = top + r * rowh
        hot = cur == d
        cv.text((x0 + 30, y + 23), f'数字 {d}', 24, T['cyan'] if hot else T['text'], anchor='lm', bold=True)
        if hot:
            cv.rect((x0 + 10, y - 4, x1 - 10, y + rowh - 10), outline=T['cyan'], width=2, r=10)
        for j, p in enumerate(pl[d]):
            X = x0 + 170 + j * (cell + 10)
            used = np_ is not None and j < np_[d]
            head = np_ is not None and j == np_[d]
            blocked = False
            if 'num' in S and cur is not None and hot and head and np_ is not None:
                pass
            fill = (60, 66, 76) if used else T['yellow'] if head else (110, 118, 130)
            cv.rect((X, y, X + cell, y + 46), fill=fill, r=8)
            cv.text((X + cell / 2, y + 26), p, 28, T['bg'] if head else T['text'], anchor='mm', bold=True)
    n = S.get('num')
    if cur is not None and n is not None and np_ is not None and n < cur and n < 10:
        pass


def _blk(S, B, ret):
    n, now = S['num'], S['now']
    a = S['pos_list'][n]
    if S['now_pos'][n] < len(a) and a[S['now_pos'][n]] < S['pos_list'][now][S['now_pos'][now]]:
        return f'数字 `{n}` 还没用的最靠前位置是 `{a[S["now_pos"][n]]}`，在 `{S["pos_list"][now][S["now_pos"][now]]}` 前面 → ==小数挡在前面，{now} 过不去 → False=='
    return f'数字 `{n}` {"已经用完了" if S["now_pos"][n] >= len(a) else "最靠前的位置 " + str(a[S["now_pos"][n]]) + " 在后面"}：不会挡住 `{now}`，继续检查下一个更小的数字'


CONFIG = dict(
    num=1585, title='检查字符串是否可以通过排序子字符串得到另一个字符串', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='逐位匹配 · 小数不能被大数越过',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def isTransformable(self, s, t):

        pos_list = [[] for _ in range(10)]
        for index, char in enumerate(s):
            now = int(char)
            pos_list[now].append(index)
        
        now_pos = [0] * 10
        for char in t:
            now = int(char)
            if now_pos[now] == len(pos_list[now]):
                return False
            for num in range(now):
                if now_pos[num] < len(pos_list[num]) and pos_list[num][now_pos[num]] < pos_list[now][now_pos[now]]:
                    return False
            
            now_pos[now] += 1
        
        return True
''',
    call='Solution().isTransformable("2301", "0231")',
    expect=True,
    views=[
        dict(type='string', var='s', h=130, cell=56, label='s'),
        dict(type='string', var='t', pointers={'sum(now_pos)': 'blue'}, h=190, cell=56, label='t（蓝 = 当前要匹配的字符）'),
        dict(type='custom', draw=_draw, h=380),
    ],
    watch=['char', 'now', 'num', ('now_pos', 'now_pos[:5]', 'cyan')],
    skip=['for _ in range(10)'],
    captions={
        'pos_list = [': '`pos_list[d]`：数字 `d` 在 `s` 里出现的下标，从前往后',
        'for index, char in enumerate(s)': '{"`s` 扫描完了" if B.get("index") == index and B.get("char") == char and index == len(s) - 1 and len(pos_list[int(char)]) and pos_list[int(char)][-1] == index else f"扫描 `s`，第 `{index}` 位是 `{char}`"}',
        'now = int(char)': None,
        'pos_list[now].append': '记下：数字 `{now}` 出现在下标 `{index}`，`pos_list[{now}] = {pos_list[now]}`',
        'now_pos = [0] * 10': '`now_pos[d]`：数字 `d` 已经用掉了几个（指向它还没用的最靠前位置）',
        'for char in t': lambda S, B, ret: ('`t` 处理完了' if B.get('char') == S.get('char') and S.get('now') == int(S.get('char')) and sum(S.now_pos) == len(S.t) else '处理 `t` 的下一个字符 `%s`：要把 `s` 里对应的数字“搬”到这个位置' % S.char),
        'if now_pos[now] == len': '`now_pos[{now}] = {now_pos[now]}`，`s` 里一共有 `{len(pos_list[now])}` 个 `{now}`：{"用完了，凑不出 → False" if now_pos[now] == len(pos_list[now]) else "还有，可以用"}',
        'for num in range(now)': lambda S, B, ret: ('比 `%d` 小的数字都检查完，没有被挡住' % S.now if (S.now == 0 or B.get('num') == S.get('num') and S.get('num') == S.now - 1) else '检查比 `%d` ==更小==的数字 `%d`：大数只能往后挪、不能越过小数' % (S.now, S.num)),
        'if now_pos[num] < len': _blk,
        'now_pos[now] += 1': '数字 `{now}` 的这个位置匹配完毕 → `now_pos[{now}] = {now_pos[now]}`',
        'return True': '`t` 的每一位都能匹配 → ==True==',
        'return False': '被挡住或不够用 → ==False==',
    },
    cards=dict(
        one_liner='排序只能让小数往前走：前面有更小的数，大数就过不去',
        complexity='时间 `O(10·n)`，空间 `O(n)`',
        problem=['给两个数字串 `s`、`t`，每次可以==把 s 的某个子串升序排序==',
                 '问能否经过任意多次操作把 `s` 变成 `t`',
                 '本视频：`s = "2301"`，`t = "0231"` → `True`'],
        quote='对于原字符串中的两个字符s[i]和s[j]而言，若i < j且s[i] < s[j]，那么无论怎么排s[j]都是不可能被排到s[i]前面去的。',
        quote_src='—— yiduobo 题解原文',
        idea=['要把 `s[k]` 放到前面，它前面所有字符都必须 `>= s[k]`',
              '于是按 `t` 的顺序逐位匹配：`t[i]` 在 `s` 里取未用的最靠前位置 `p`',
              '只要有==更小的数字==在更靠前的未用位置，`s[p]` 就越不过它 → False',
              '按相对顺序两两交换（像冒泡），不会打乱其余未用字符的相对位置'],
        summary=['时间 `O(10n)`，空间 `O(n)`；每个数字一个队列（下标列表 + 指针）',
                 '只需检查比当前数字==更小==的数字，相等或更大的不会阻挡',
                 '先判断该数字是否还有剩余，没有就直接 False',
                 '原文在 Python 3 下可直接运行，没有改动'],
    ),
)
