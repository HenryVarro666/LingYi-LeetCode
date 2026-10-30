def _digits(S):
    return list(str(S['num']))


def _cur(S):
    n = len(str(S['num']))
    x = S['tmp']
    consumed = n if x == 0 else n - len(str(x))
    return n - 1 - consumed if x else None


def _best(S):
    m = S.get('delta', 0)
    return len(str(S['num'])) - len(str(m)) if m else None


class _P:
    def __call__(self, S):
        return _cur(S)

    def __str__(self):
        return '位'


def _txt(S):
    if 'p' not in S:
        return '每次模 10 取最低位，记下==最后一次出现的 6==（也就是最高位的 6）'
    if S.get('_line') == 13:
        return f"答案 = `{S['num']} + {S['delta']} × 3` = =={S['num'] + S['delta'] * 3}=="
    return f"`p = {S['p']}`（当前位权值），`delta = {S['delta']}`（最高位 6 的权值）"


CONFIG = dict(
    num=1323, title='6 和 9 组成的最大数字', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='模 10 取位 · 记最高位的 6',
    tags=['灵神题单', '贪心与思维', '难度分 1194'],
    code='''
class Solution(object):
    def maximum69Number (self, num):

        delta = 0
        tmp = num
        p = 1
        while tmp:
            if tmp % 10 == 6:
                delta = p
            p *= 10
            tmp//= 10
        
        return num + delta * 3
''',
    call='Solution().maximum69Number(9669)',
    expect=9969,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var=_digits, label='num 的各位数字（黄 = 当前位，绿 = 最高位的 6）',
             pointers={_P(): 'yellow'}, color=lambda S, i, v: 'green' if i == _best(S) else None, h=220),
    ],
    watch=[('tmp', 'tmp', 'blue'), ('p', 'p', 'cyan'), ('delta', 'delta', 'green')],
    captions={
        'delta = 0': '`delta` 是改最高位 6 后的权值，没有 6 就是 `0`',
        'tmp = num': '`tmp` 是 `num` 的副本，每次去掉最低位',
        'p = 1': '`p` 是当前位的权值',
        'while tmp': lambda S, B, r: (f'`tmp = {S["tmp"]}` 还没取完，继续' if S['tmp'] else '`tmp = 0`：数位取完，结束'),
        'if tmp % 10 == 6': lambda S, B, r: (f'`{S["tmp"]} % 10 = 6`：这一位是 6' if S['tmp'] % 10 == 6 else f'`{S["tmp"]} % 10 = {S["tmp"] % 10}`：是 9，跳过'),
        'delta = p': '从低位往高位，后出现的 6 更高，覆盖：`delta = {delta}`',
        'p *= 10': '`p` → {p}',
        'tmp//= 10': '去掉最低位：`tmp` → {tmp}',
        'return': '6 变 9 增加 `3 × delta`：`{num} + {delta} × 3` = =={num + delta * 3}==',
    },
    cards=dict(
        one_liner='把最高位的 6 变成 9',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['正整数 `num` 只含 6 和 9，最多翻转一位',
                 '返回能得到的最大数字',
                 '示例：`9669` → `9969`'],
        quote='比较基础的题目，将最高位的6变成9即可。……也可以对num每次模10取出最低位，找到过程中最后一个出现的6。',
        quote_src='—— yiduobo 题解原文',
        idea=['字符串做法：从头扫描找第一个 6',
              '本代码用数字做法：模 10 取最低位，从低到高，最后一个 6 就是最高位的 6',
              '6 变 9 增加 `3 × 权值`'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '没有 6 时 `delta = 0`，答案不变',
                 '原文为 Python 2 写法，`tmp/= 10` 已改为 `tmp//= 10`（整数除法）',
                 '对比灵神：灵神用 `divmod` 同时取商和余数，yiduobo 用 `%` 和 `//` 两步'],
    ),
)
