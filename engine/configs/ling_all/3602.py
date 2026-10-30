CONFIG = dict(
    num=3602, title='十六进制和三十六进制转化', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='进制转换 · 库函数 base_repr',
    tags=[],
    setup='''
# 缺第三方库 numpy：这里写一个等价的 np.base_repr（原文的 import numpy as np 在代码面板里省略）
import types
def base_repr(number, base=2, padding=0):
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num = abs(number)
    res = []
    while num:
        res.append(digits[num % base])
        num //= base
    if not res:
        res.append('0')
    if number < 0:
        res.append('-')
    return ''.join(reversed(res))
np = types.SimpleNamespace(base_repr=base_repr)
''',
    code='''
class Solution:
    def concatHex36(self, n: int) -> str:
        return np.base_repr(n ** 2, base=16) + np.base_repr(n ** 3, base=36)
''',
    call='Solution().concatHex36(13)',
    expect='A91P1',
    views=[
        dict(type='text', size=30, h=130, fn=lambda S: f"`n = {S['n']}`　`n² = {S['n'] ** 2}`　`n³ = {S['n'] ** 3}`" if 'n' in S else ''),
        dict(type='text', size=30, h=130, fn=lambda S: (
            "十六进制：`169 = 10×16 + 9` → ==A9==（10 记作 `A`）" if S.get('n') == 13 else '')),
        dict(type='text', size=30, h=130, fn=lambda S: (
            "三十六进制：`2197 = 1×36² + 25×36 + 1` → ==1P1==（25 记作 `P`）" if S.get('n') == 13 else '')),
    ],
    watch=['n'],
    captions={
        'return np.base_repr': '`np.base_repr(n ** 2, base=16)` 把 `{n ** 2}` 转成十六进制 `A9`；`np.base_repr(n ** 3, base=36)` 把 `{n ** 3}` 转成三十六进制 `1P1`；拼接得 =={ret}==',
    },
    cards=dict(
        one_liner='n² 转十六进制，n³ 转三十六进制，拼起来',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['给整数 `n`：返回 `n²` 的==十六进制==（`0-9A-F`）加 `n³` 的==三十六进制==（`0-9A-Z`）拼成的字符串',
                 '示例：`n = 13` → `169 = "A9"`，`2197 = "1P1"` → `"A91P1"`'],
        quote='不用库函数的思路见视频讲解。……np.base_repr(n ** 2, base=16) + np.base_repr(n ** 3, base=36)',
        quote_src='—— 灵茶山艾府题解（库函数写法）',
        idea=['`numpy.base_repr(x, base)` 直接把整数转成 `base` 进制，字母为大写',
              '两个数各转一次再拼接，一行搞定',
              '不用库：反复 `x % base` 取最低位，再 `x //= base`，最后反转'],
        after=[dict(heading='不用库函数怎么转', lines=[
            '反复 `x % base` 取最低位，再 `x //= base`，直到 `x = 0`',
            '`169`：`169 % 16 = 9`，`10 % 16 = 10 → A`，反转得 `A9`',
            '`2197`：余数依次为 `1, 25, 1`，`25 → P`，反转得 `1P1`']),],
        result='`n = 13`：`"A9" + "1P1"` = `"A91P1"` ✓',
        summary=['`n ≤ 1000`，`n³ ≤ 10⁹`，位数只有几位，复杂度 `O(log n)`',
                 '易错：`base_repr` 输出的是大写字母，正好符合题目要求',
                 '本机没有 numpy 时，视频里用 `setup` 补了一个等价的 `base_repr`，作者代码一字未改',
                 '手写版见 yiduobo 题解：取模、除法、反转'],
    ),
)
