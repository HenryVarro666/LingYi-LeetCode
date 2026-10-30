PEOPLE = [5, 1, 4, 2, 3, 2]
LIMIT = 5
SORTED = sorted(PEOPLE)


def _all_boats():
    """贪心的完整船序列（每条船是排序后下标的元组）"""
    l, r = 0, len(SORTED) - 1
    out = []
    while l <= r:
        if l == r:
            out.append((r,))
            break
        if SORTED[l] + SORTED[r] <= LIMIT:
            out.append((l, r))
            l += 1
        else:
            out.append((r,))
        r -= 1
    return out


BOATS = _all_boats()


def _boats(S):
    """已经安排好的船 = 前 res 条（return res + 1 那一步再加上最后一条）"""
    if S.get('people') != SORTED or not isinstance(S.get('res'), int):
        return None
    k = S['res'] + (1 if S.get('_line') == 9 else 0)
    return BOATS[:k]


def _boat_strs(S):
    b = _boats(S)
    if b is None:
        return None
    return ['+'.join(str(SORTED[i]) for i in t) for t in b]


def _color(S, i, v):
    b = _boats(S)
    if b is None:
        return None
    if any(i in t for t in b):
        return 'green'
    if i in (S['l'], S['r']) and S['l'] <= S['r']:
        return 'orange'
    return None


def _dim(S, i, v):
    b = _boats(S)
    return b is not None and any(i in t for t in b)


def _text(S):
    if S.get('people') != SORTED or not isinstance(S.get('l'), int):
        return f'一艘船==最多坐两人==，载重 `limit = {LIMIT}`'
    l, r = S['l'], S['r']
    if l > r:
        return '所有人都上船了'
    if l == r:
        return f'只剩 `people[{l}] = {SORTED[l]}` 一个人'
    a, b = SORTED[l], SORTED[r]
    rel = '≤' if a + b <= LIMIT else '>'
    return f'最轻 `{a}` + 最重 `{b}` = `{a + b}` {rel} `limit = {LIMIT}`'


def _cap_pair(S, B, ret):
    l, r, p = S.l, S.r, S.people
    a, b = p[l], p[r]
    if a + b <= LIMIT:
        return f'`{a} + {b} = {a + b} ≤ {LIMIT}`：最重的人和最轻的人==可以同船=='
    return f'`{a} + {b} = {a + b} > {LIMIT}`：最重的人和最轻的都坐不下 → 只能==单独坐一艘=='


CONFIG = dict(
    num=881, title='救生艇', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 双指针：最重的配最轻的',
    tags=['字节30天'],
    code='''
class Solution(object):
    def numRescueBoats(self, people, limit):
        l = 0
        r = len(people) - 1
        people = sorted(people)
        res = 0
        while l <= r:
            if l == r:
                return res + 1
            if people[l] + people[r] <= limit:
                l += 1
                r -= 1
                res += 1
            else:
                r -= 1
                res += 1

        return res
''',
    call=f'Solution().numRescueBoats({PEOPLE}, {LIMIT})',
    expect=4,
    views=[
        dict(type='text', fn=_text, h=64),
        dict(type='bars', var='people', label='people（排序后；橙 = 当前最轻/最重，绿 = 已上船）', h=380,
             pointers={'l': 'blue', 'r': 'pink'}, color=_color, dim=_dim, vmax=5),
        dict(type='array', var=_boat_strs, label='已经安排的船', cell=110, h=150),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('limit', 'limit'), ('res', 'res', 'green')],
    skip=['l = 0', 'res = 0'],
    captions={
        'r = len(people) - 1': '`l`、`r` 指向当前最轻和最重的人（排序后）：`r = {r}`',
        'people = sorted(people)': '先按体重排序：`{people}`',
        'while l <= r': lambda S, B, ret: (f'`l = {B.l} ≤ r = {B.r}`：还有人没上船' if B.l <= B.r
                                           else f'`l = {B.l} > r = {B.r}`：所有人都安排好了'),
        'if l == r': lambda S, B, ret: (f'`l == r = {B.l}`：==就剩最后一个人==' if B.l == B.r
                                        else f'`l = {B.l} ≠ r = {B.r}`：至少还有两个人'),
        'return res + 1': '最后一个人再安排一艘船，返回 `{res} + 1` = =={ret}==',
        'if people[l] + people[r] <= limit': _cap_pair,
        'l += 1': '最轻的人上船：`l` → {l}',
        12: '最重的人也上这艘船：`r` → {r}',
        13: '两人同船，船数 `res` → =={res}==',
        15: '最重的人单独上船：`r` → {r}',
        16: '单独一艘，船数 `res` → =={res}==',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='考虑当前最重的人：能和最轻的同船就同船，否则单独一艘',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 新建列表）',
        problem=['第 `i` 人体重 `people[i]`，每艘船载重 `limit`，==最多坐两人==',
                 '求载走所有人的最少船数（保证每人体重 ≤ limit）',
                 '示例：`people = [3,2,2,1], limit = 3` → `3`',
                 '本视频：`people = [5,1,4,2,3,2], limit = 5` → `4`'],
        quote='如果我们考虑当前最重的人，那么若其与当前最轻的人体重之和超过了limit，==最重的人就只能单独坐一艘船==，否则就应当安排其与最轻的人坐一艘船。',
        quote_src='—— yiduobo 题解原文',
        idea=['最重的人连最轻的都带不了 → 跟谁都坐不下，只能单独坐',
              '带得了最轻的 → 一起走（最轻的人和谁坐都行，配给最重的不亏）',
              '排序后用 `l`、`r` 指向当前最轻、最重，每轮至少送走一个人'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`l == r` 时只剩一个人：要再加一艘船（`return res + 1`）',
                 '两个分支都要 `res += 1`、`r -= 1`：每轮最重的人一定上船',
                 '注意 `r = len(people) - 1` 写在排序前，长度不变所以没问题',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
