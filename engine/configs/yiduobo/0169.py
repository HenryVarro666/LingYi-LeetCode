NUMS = [3, 3, 4, 2, 4, 4, 2, 4, 4]

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _votes(cv, S, B, box, T):
    """候选者 + 票数（只用于画图）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '候选者与票数', 24, T['muted'], bold=True)
    res, cnt = S.get('res'), S.get('cnt')
    if cnt is None:
        return
    X, Y = x0 + 60, y0 + 46
    cv.rect((X, Y, X + 220, Y + 80), fill=T['cyan'] if res is not None else T['panel2'], r=14)
    cv.text((X + 110, Y + 40), f'候选者 {res}' if res is not None else '无候选者', 32,
            T['bg'] if res is not None else T['dim'], anchor='mm', bold=True)
    cv.text((X + 260, Y + 40), '票数', 26, T['muted'], anchor='lm')
    for j in range(cnt):
        cv.rect((X + 330 + j * 52, Y + 18, X + 374 + j * 52, Y + 62), fill=T['green'], r=8)
    if cnt == 0:
        cv.text((X + 330, Y + 40), '0', 30, T['dim'], anchor='lm', bold=True)


def _sim(m):
    """模拟前 m 个数的投票：返回 (res, cnt, 存活的票, 已抵消的数)"""
    res, cnt, alive, gone = None, 0, [], set()
    for i, num in enumerate(NUMS[:m]):
        if cnt == 0:
            res, cnt, alive = num, 1, [i]
        elif res == num:
            cnt += 1
            alive.append(i)
        else:
            cnt -= 1
            gone |= {alive.pop(), i}
    return res, cnt, alive, gone


def _done(S):
    k = getattr(S.get('nums'), 'k', -1)
    if k is None:
        return len(NUMS)
    if k < 0 or 'cnt' not in S:
        return 0
    a = _sim(k + 1)[:2]
    return k + 1 if a == (S['res'], S['cnt']) and _sim(k)[:2] != a else k


def _color(S, i, v):
    _, _, alive, _ = _sim(_done(S))
    return 'cyan' if i in alive else None


def _dim(S, i, v):
    return i in _sim(_done(S))[3]


CONFIG = dict(
    num=169, title='多数元素', difficulty='Easy', category='技巧',
    author='yiduobo', technique='投票法',
    code='''
class Solution(object):
    def majorityElement(self, nums):
        res = None
        cnt = 0

        for num in nums:
            if cnt == 0:
                res = num
                cnt = 1
            elif res == num:
                cnt += 1
            else:
                cnt -= 1

        return res
''',
    setup=TRACK,
    call=f'Solution().majorityElement(TList({NUMS}))',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（青色 = 候选者手里的票，灰色 = 已一换一抵消）', h=200,
             pointers={_k: 'yellow'}, pointer_labels={_k: 'num'}, color=_color, dim=_dim),
        dict(type='custom', draw=_votes, h=160),
        dict(type='text', fn=lambda S: '相同 → 票数 ==+1==；不同 → 票数 ==−1==（一换一抵消）；票数为 0 → 下一个数当候选者', size=26, h=90, lines=2),
    ],
    watch=[('num', 'num', 'yellow'), ('res', 'res', 'cyan'), ('cnt', 'cnt', 'green')],
    captions={
        'res = None': '候选者 `res` 先为空',
        'cnt = 0': '票数 `cnt = 0`',
        'for num in nums': lambda S, B, ret: (f'下一个数 `num = {S.num}`' if _k(S) is not None else '扫描结束'),
        'if cnt == 0': lambda S, B, ret: ('票数为 0 → 取这个数作为==新的候选者==' if S.cnt == 0
                                          else f'候选者 `{S.res}` 还有 `{S.cnt}` 票'),
        'res = num': '候选者换成 `{num}`',
        'cnt = 1': '它自己先投 `1` 票',
        'elif res == num': lambda S, B, ret: (f'`{S.num}` 与候选者相同' if S.res == S.num
                                              else f'`{S.num}` 与候选者 `{S.res}` 不同'),
        'cnt += 1': '票数加一：`cnt = {cnt}`',
        'cnt -= 1': lambda S, B, ret: (f'和候选者==互相抵消==一票：`cnt = {S.cnt}`' + ('，候选者被抵消光了' if S.cnt == 0 else '')),
        'return res': '最终候选者 `{ret}` 就是多数元素',
    },
    cards=dict(
        one_liner='投票：相同加一、不同减一，票数归零就换候选者',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回数组中出现次数 ==大于 n/2== 的多数元素（保证存在）',
                 '进阶：`O(n)` 时间、`O(1)` 空间',
                 '示例：`[2,2,1,1,1,2,2]` → `2`'],
        before=[dict(heading='yiduobo 先想到的：随机法', chapter='② 思路', lines=[
            '多数元素超过一半 → 随机拿一个数，拿到它的概率 ==超过 1/2==',
            '随机取一个数，扫描一遍数它出现了几次；不是就再随机一个',
            '重复次数的期望值为 2 次，性能有保证'])],
        quote='维护一个当前候选者与票数……若下一个数与当前候选者相同，则票数加一，否则票数减一。当票数为0时，取下一个数作为新的候选者。',
        quote_src='—— yiduobo 题解（另一种做法：投票法）',
        idea=['每次“不同”就是一个其他数和候选者==一换一抵消==',
              '极端情况下，多数元素与其他数字各自抵消了票数',
              '多数元素出现次数大于 n/2，抵消完必有剩余 → 最终候选者一定是它'],
        result='最终候选者 `4` 就是多数元素 ✓（4 出现 5 次 > 9/2）',
        summary=['时间 `O(n)`，空间 `O(1)`；也可排序或用 dict 计数',
                 '中途候选者可能不是答案（本例开头是 3），只有最终的才保证',
                 '前提是多数元素==一定存在==；否则需再扫一遍验证',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
