def _dsum(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


def _color(S, i, v):
    if 'index' not in S or v < 2:
        return None
    if v == S['index']:
        return 'blue'
    if v < S['index'] and _dsum(v) % 2 == 0:
        return 'green'
    return None


def _dim(S, i, v):
    return v < 2 or ('index' in S and v < S['index'] and _dsum(v) % 2 == 1)


def _txt(S):
    if 'index' not in S:
        return ''
    done = ('now' in S and S['tmp'] == 0 and S['_line'] >= 9) 
    return f"枚举 `{S['index']}`：剩下 `tmp = {S['tmp']}`，各位数字之和 `now = {S['now']}`" if 'now' in S else f"枚举 `{S['index']}`"


CONFIG = dict(
    num=2180, title='统计各位数字之和为偶数的整数个数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='暴力枚举 + 拆数位', tags=[],
    code='''
class Solution(object):
    def countEven(self, num):

        res = 0
        for index in range(2, num + 1):
            tmp = index
            now = 0
            while tmp:
                now += tmp % 10
                tmp //= 10
            
            if now % 2 == 0:
                res += 1
        
        return res
''',
    call='Solution().countEven(10)',
    expect=4,
    views=[
        dict(type='text', size=32, h=110, fn=_txt),
        dict(type='array', var=lambda S: list(range(1, S['num'] + 1)), label='1 ~ num（绿 = 各位和为偶数，蓝 = 当前，灰 = 不是偶数）',
             pointers={'index - 1': 'blue'}, color=_color, dim=_dim, cell=110, h=230),
    ],
    watch=[('index', 'index', 'blue'), ('tmp', 'tmp'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计满足条件的个数',
        'for index in range': lambda S, B, r: (f'枚举 `index = {S.index}`：令 `tmp = index` 拆数位（别动 `index`），`now = 0` 累加各位' if S.get('tmp') is None or S.index != B.get('index') else '枚举完毕，退出循环'),
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}` 不为 0，还有数位没拆' if S.tmp else '`tmp = 0`：数位拆完了'),
        'now += tmp % 10': '`tmp % 10 = {tmp % 10}` 是最低位，加进 `now` → =={now}==',
        'tmp //= 10': '去掉最低位：`tmp` → {tmp}（注意用整除 `//`）',
        'if now % 2 == 0': lambda S, B, r: f'数位和 `now = {S.now}`，`{S.now} % 2 = {S.now % 2}` → ' + ('==偶数，计入==' if S.now % 2 == 0 else '奇数，不计'),
        'res += 1': '`{index}` 满足，`res` → =={res}==',
        'return res': '全部枚举完，一共 `{res}` 个',
    },
    skip=['tmp = index', 'now = 0'],
    max_steps=110,
    cards=dict(
        one_liner='数据很小，直接枚举每个数、拆开各位相加',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['统计 `1 ~ num` 中各位数字之和为偶数的正整数个数',
                 '示例：`4` → `2`（只有 2、4）；`30` → `14`',
                 '本视频：`num = 10` → `4`（2、4、6、8；10 的数位和是 1）'],
        quote='本题最好的做法应该是基于数位的动态规划，不过由于本题的数据规模很小，所以我直接采用的暴力法，枚举2到num之间的所有数',
        quote_src='—— yiduobo 题解原文',
        idea=['`num <= 1000`，暴力足够：从 2 枚举到 `num`',
              '每个数用 `% 10` 取最低位、`// 10` 去掉最低位，累加成 `now`',
              '`now` 是偶数就让 `res` 加一'],
        summary=['每个数拆 `O(log num)` 位，总共 `O(n log n)`，`n <= 1000` 毫无压力',
                 '原文为 Python 2 写法，`tmp /= 10` 已改为 `tmp //= 10`（Python 3 的 `/` 会得到小数，循环停不下来）',
                 '要拆数位就用临时变量 `tmp`，保留 `index` 不被改掉',
                 '作者提到更优解是数位 DP；本题其实还有规律：每 10 个数里恰有 5 个满足'],
    ),
)
