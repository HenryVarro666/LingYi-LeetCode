N0 = 39


def _tern(v):
    s = ''
    while v:
        s = str(v % 3) + s
        v //= 3
    return s or '0'


def _text(S):
    n = S.get('n')
    t = _tern(N0)
    if n is None:
        return f'`n = {N0}`，模 3 取余法转三进制：`{t}`'
    return f'`{N0}` → 余数从低位到高位依次取出，当前剩下 `n = {n}`'


def _arr(S):
    return list(_tern(N0))


def _col(S, i, v):
    n = S.get('n')
    if n is None:
        return None
    t = _tern(N0)
    done = len(t) - len(_tern(n)) if n else len(t)
    if len(t) - 1 - i < done:
        return 'red' if v == '2' else 'green'
    return None


CONFIG = dict(
    num=1780, title='判断一个数字是否可以表示成三的幂的和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='模 3 取余转三进制',
    tags=['灵神题单', '难度分 1506'],
    code='''
class Solution(object):
    def checkPowersOfThree(self, n):

        while n:
            if n % 3 == 2:
                return False
            n //= 3
        
        return True
''',
    call='Solution().checkPowersOfThree(39)',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=80, lines=2),
        dict(type='array', var=_arr, label='39 的三进制（绿 = 已确认是 0 或 1）', color=_col, h=170),
    ],
    watch=[('n', 'n', 'blue'), ('余数', 'n % 3 if n else None', 'orange')],
    captions={
        'while n': lambda S, B, r: (f'`n = {S.n}`，还没转换完' if S.n else '`n = 0`：三进制转换完毕，没有遇到 2'),
        'n % 3 == 2': lambda S, B, r: (f'这一轮余数 `{S.n % 3}` ==等于 2== → 这一位不是 0 或 1，直接 false'
                                       if S.n % 3 == 2 else f'这一轮余数 `{S.n % 3}`，不等于 2 → 这一位合格'),
        'n //= 3': '`n` 整除 3 → =={n}==，进入下一位',
        'return False': '余数为 2，返回 `False`',
        'return True': '没有任何一位是 2，返回 `True`',
    },
    cards=dict(
        one_liner='问题等价于：三进制表示里有没有数字 2',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['能否把 `n` 写成若干个==不同==的 3 的幂之和',
                 '示例：`12 = 3 + 9` → `true`',
                 '本视频：`n = 39 = 3 + 9 + 27`，三进制 `1110`'],
        quote='题目实际上就是问n的三进制表示下是否有某一位的值不等于0或者1，那么这一位肯定就是等于2。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个 3 的幂只能选或不选 → 对应三进制这一位是 1 或 0',
              '用经典的模 3 取余法逐位转三进制',
              '某一轮余数为 2 就返回 false，全程没有就返回 true'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`n /= 3` 已改为 `n //= 3`（整数除法）',
                 '不需要真的把三进制字符串拼出来，边除边判断即可',
                 '对比灵神：灵神从「必须先分出最大的幂」推出三进制，这里直接转化为进制问题'],
    ),
)
