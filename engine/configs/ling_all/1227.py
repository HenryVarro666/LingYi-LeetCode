def _seat_color(S, i, v):
    n = S['n']
    if v == 1:
        return 'blue'
    if v == n:
        return 'pink'
    return None


def _seat_dim(S, i, v):
    return 1 < v < S['n']


def _txt1(S):
    n = S['n']
    if n == 1:
        return '只有 1 个座位，他只能坐在自己的座位上 → ==1=='
    return f'中间的乘客 2 ~ {n - 1} 等价于「都坐在自己的座位上」'


def _txt2(S):
    n = S['n']
    if n == 1:
        return ''
    return f'最后只剩座位 1 和座位 {n}，第 1 位乘客随机选 → 各 ==1/2=='


CONFIG = dict(
    num=1227, title='飞机座位分配概率', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='等价替换 · 只剩两个座位',
    tags=['灵神题单·数学算法'],
    code='''
class Solution:
    def nthPersonGetsNthSeat(self, n: int) -> float:
        return 1 if n == 1 else 0.5
''',
    call='Solution().nthPersonGetsNthSeat(5)',
    expect=0.5,
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='座位编号（蓝 = 1 号座位，粉 = n 号座位）',
             color=_seat_color, dim=_seat_dim, index=False, h=230),
        dict(type='text', fn=_txt1, size=28, h=90),
        dict(type='text', fn=_txt2, size=28, h=90),
    ],
    watch=['n'],
    captions={
        'return 1 if n == 1': lambda S, B, ret: (
            '只有 `n = 1`：第一位乘客只会坐在自己的位置上 → ==1==' if S.n == 1 else
            f'`n = {S.n} ≥ 2`：中间乘客可以视为都坐对了位置，只剩 1 号和 {S.n} 号座位，随机选 → ==0.5=='),
    },
    cards=dict(
        one_liner='后面的人分不清谁坐错了，等价于最后只剩两个座位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 位乘客登机，飞机有 `n` 个座位；第 1 位乘客把票弄丢，随便选一个座位',
                 '其他人：自己的座位空着就坐自己的，被占了就随机选一个空座',
                 '问第 `n` 位乘客坐到自己座位的概率。`n = 2` → `0.5`'],
        quote='对于后面的乘客，他们其实无法区分谁坐错了位置，他们会认为其中一位乘客只是正常地坐在座位 2 上，而另一位乘客随机选了一个座位 5。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设第 1 位坐到 2 号座位，则第 2 位被迫随机选；他的选择又可以看作「第 1 位坐在 2 号、他自己随机选」',
              '依此类推，等价于第 2 ~ n−1 位都正常坐在自己位置，最后剩 2 个座位给第 1 位随机选',
              '最后剩下的是 1 号座位和 n 号座位，概率各 `1/2`'],
        after=[dict(heading='用 n = 3 验证一下', lines=['第 1 位选 1 号（概率 `1/3`）→ 后面都坐对 → 第 3 位成功',
                                                 '第 1 位选 3 号（概率 `1/3`）→ 3 号被占 → 失败',
                                                 '第 1 位选 2 号（概率 `1/3`）→ 第 2 位在 1、3 号里随机 → 成功一半',
                                                 '合计 `1/3 + 0 + 1/3 × 1/2` = ==1/2==，和结论一致'])],
        summary=['时间、空间都是 `O(1)`',
                 '`n = 1` 要单独判断：只有一个座位，概率是 1，不是 0.5',
                 '作者还给了一张图解推导递推式 f(n)，结论相同；推导过程与 790 题（多米诺）类似',
                 '易错点：不要被「随机」吓到去写递归或模拟，结论与 n 无关'],
    ),
)
