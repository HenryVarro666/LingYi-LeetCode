def _fold(dl):
    v = 0
    for d in dl:
        v = v * 10 + d
    return v


def _forcap(S, B, r):
    dl = S.digit_list
    if _fold(dl) == S.now:
        return f'`digit_list` 已全部用完 → 反转结束，`now = {S.now}`'
    return f'依次取出 `digit = {S.digit}`'


def _eq(S):
    if 'k' not in S:
        return ''
    k = S['k']
    line = S.get('_line', 0)
    if 'digit_list' in S and line <= 9:
        return f"拆数位：`k = {k}`，从低位到高位取出 `digit_list = {S['digit_list']}`"
    if line >= 14:
        return f"`k + now = {k} + {S['now']}` = =={k + S['now']}==　目标 `num = {S['num']}`"
    return f"用 `digit_list = {S.get('digit_list', [])}` 从头拼回：`now = {S.get('now', 0)}`"


CONFIG = dict(
    num=2443, title='反转之后的数字和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举 · 数位列表反转',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def sumOfNumberAndReverse(self, num):

        for k in range(num + 1):
            now = k
            digit_list = []
            while now:
                digit_list.append(now % 10)
                now //= 10
            
            now = 0
            for digit in digit_list:
                now = now * 10 + digit
            
            if k + now == num:
                return True

        return False
''',
    call='Solution().sumOfNumberAndReverse(33)',
    expect=True,
    views=[
        dict(type='text', fn=_eq, size=28),
        dict(type='array', var=lambda S: list(S.get('digit_list', [])), label='digit_list（低位在前）', h=180, cell=90,
             color=lambda S, i, v: 'green' if S.get('_line', 0) >= 12 and 'digit' in S and False else None),
    ],
    watch=['num', ('k', 'k', 'blue'), ('now', 'now', 'pink'), ('digit', 'digit', 'cyan')],
    captions={
        'for k in range': '`num ≤ 100000`，从 `0` 到 `num` 枚举每个 `k`：现在是 `k = {k}`',
        'now = k': '`now` 先等于 `k`，用来一位位拆开：`now = {now}`',
        'digit_list = []': '准备一个空列表，按顺序存 `k` 的各位数字',
        'while now': lambda S, B, r: (f'`now = {S.now}` 还没拆完 → 继续取最低位' if S.now else '`now = 0`：数位全部取出'),
        'digit_list.append': '最低位 `{B.now % 10}` 放进列表，列表是 `{digit_list}`（低位在前）',
        'now //= 10': '`now` 去掉最低位 → {now}',
        'now = 0': '把 `now` 清零，准备用 `digit_list` 重新拼出反转后的数',
        'for digit in digit_list': _forcap,
        'now = now * 10 + digit': '`now = {B.now} * 10 + {digit}` = =={now}==：低位先进来，所以变成了高位',
        'if k + now == num': lambda S, B, r: (f'`{S.k} + {S.now} = {S.k + S.now}` ==等于== `num = {S.num}` → 找到了' if S.k + S.now == S.num else f'`{S.k} + {S.now} = {S.k + S.now}` 不等于 `{S.num}` → 换下一个 k'),
        'return True': '`k = {k}` 满足 `k + reverse(k) = num` → ==True==',
    },
    skip=[],
    max_steps=60,
    cards=dict(
        one_liner='num 不超过 10 万，从 0 枚举到 num，逐个检查',
        complexity='时间 `O(n log n)`，空间 `O(log n)`',
        problem=['非负整数 `num`，是否存在非负整数 `k` 使 `k + reverse(k) = num`',
                 '`reverse(k)` 把 `k` 的数位反转，允许前导零',
                 '示例：`443 → true`（172+271），`63 → false`；本视频用 `33`（12+21）'],
        quote='由于num不会超过100000，那么只需从0开始到100000进行枚举，检测当前枚举到的数以及其反转之后的数之和是否等于num。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 的最大值就是 `num`，枚举量最多 10 万',
              '先把 `k` 的每一位从低到高放进 `digit_list`',
              '再从头遍历 `digit_list` 拼数：最低位先进，最后成了最高位，就是反转'],
        summary=['时间 `O(n log n)`，空间 `O(log n)`（`digit_list`）',
                 '`range(num + 1)` 要包含 `num`',
                 '`k = 0` 时 `digit_list` 为空，`now = 0`，`0 + 0 = 0`，所以 `num = 0` 也是 true',
                 '原文为 Python 2 写法，整数除法 `now /= 10` 已改为 `now //= 10`',
                 '对比灵神：灵神一边取低位一边拼 `rev`，省掉了 `digit_list`'],
    ),
)
