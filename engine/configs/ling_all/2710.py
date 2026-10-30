def _tz(s):
    return len(s) - len(s.rstrip('0'))

CONFIG = dict(
    num=2710, title='移除字符串中的尾随零', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='rstrip 去尾零', tags=[],
    code='''
class Solution:
    def removeTrailingZeros(self, num: str) -> str:
        return num.rstrip('0')
''',
    call="Solution().removeTrailingZeros('51230100')",
    expect='512301',
    views=[
        dict(type='string', var='num', h=200,
             color=lambda S, i, v: 'red' if i >= len(S['num']) - _tz(S['num']) else 'green'),
        dict(type='text', h=120, fn=lambda S: f"末尾连续的 `0` 有 =={_tz(S['num'])}== 个（红色），去掉后剩 `{S['num'].rstrip('0')}`"),
    ],
    watch=[('num', 'num', 'blue')],
    captions={
        'return': "`num.rstrip('0')`：从右往左删掉所有 `0`，直到遇到非 0 的 `{num[len(num.rstrip(chr(48)))-1]}` 停下 → =={ret}==",
    },
    cards=dict(
        one_liner='输入是正整数，直接把末尾的 0 全部删掉',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['给你一个表示正整数的字符串 `num`，返回去掉尾随零后的字符串',
                 '例如 `"51230100"` 有 2 个尾随零，去掉后得到 `"512301"`',
                 '示例 2：`"123"` 没有尾随零 → `"123"`'],
        quote='由于输入保证是正整数，所以去掉所有的尾零 0 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['保证是正整数 ==意味着至少有一个非 0 数位==，不会删成空串',
              '`rstrip(\'0\')` 只从右边删，中间的 0 不动（如 `51230100` 中间的 0 保留）'],
        after=[dict(heading='为什么不会删空', lines=['题目保证 `num` 是正整数、不含前导零', '所以至少有一位非 0，`rstrip` 删到它就停', '换成全 0 的字符串才会得到空串，但这不会出现']),
               dict(heading='和手写循环等价', lines=['也可以从后往前找第一个非 0 的下标再切片', '`rstrip` 就是把这个循环封装好了', '灵神直接用库函数，一行搞定'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：用 `replace` 或 `strip` 会误删中间或开头的 0',
                 '==能用 `rstrip` 一行解决，是因为题目保证正整数=='],
    ),
)
