def _txt(S):
    if 'res' not in S:
        return f"最多 `{S['n']}` 位，每位最大 9：总和上限 `9n = {9 * S['n']}`；`s = {S['s']}`"
    return f"还剩 `s = {S['s']}` 没分配；从高位到低位，每位尽量填大"


CONFIG = dict(
    num=4000, title='给定数位和的最大整数', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='从左到右贪心 · 先填 9',
    tags=['灵神题单', '难度分 1200'],
    code='''
class Solution:
    def largestInteger(self, n: int, s: int) -> int:
        if s > n * 9:
            return -1
        if s == 0:
            return 0

        res = ['0'] * n
        for i in range(n):
            if s <= 9:
                res[i] = str(s)
                break
            res[i] = '9'
            s -= 9
        return int(''.join(res))
''',
    call='Solution().largestInteger(5, 20)',
    expect=99200,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='res', pointers={'i': 'blue'}, label='res（从高位到低位填数字）',
             color=lambda S, i, v: 'green' if v != '0' else None, h=240),
    ],
    watch=[('n', 'n', 'cyan'), ('s', 's', 'yellow'), ('i', 'i', 'blue')],
    captions={
        'if s > n * 9': lambda S, B, r: (f'每位最多 9，`n * 9 = {S["n"] * 9}`，`s = {S["s"]}` 没超过 → 有解' if S['s'] <= S['n'] * 9 else '`s` 超过 `9n`，填满 9 也不够 → 返回 -1'),
        'if s == 0': '`s != 0`：继续构造' ,
        "res = ['0']": '先准备 `n` 个 `0`：不够的位置自然是 0，位数打满才最大',
        'for i in range': '填第 `{i}` 位（高位在前，高位越大整数越大）',
        'if s <= 9': lambda S, B, r: (f'`s = {S["s"]} <= 9`：剩下的数一位就能装下' if S['s'] <= 9 else f'`s = {S["s"]} > 9`：这一位可以放满 9'),
        'res[i] = str(s)': '这一位填 `{s}`，后面的位保持 0，==结束==',
        "res[i] = '9'": '这一位填 `9`：能填大就填大',
        's -= 9': '还剩 `s = {s}` 要分配',
        'return int': '拼起来：`{"".join(res)}` → =={int("".join(res))}==',
    },
    cards=dict(
        one_liner='从高位到低位，每位尽量填 9',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['非负整数 `n` 和 `s`：求最多 `n` 位、各位数字之和等于 `s` 的最大整数',
                 '不存在则返回 `-1`',
                 '本视频：`n = 5, s = 20` → `99200`'],
        quote='由于最多填 n 个 9，所以如果 s>9n，则无解，返回 -1。否则可以从高到低填：如果 s > 9，那么这一位填 9；否则这一位填 s。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先判无解：`s > 9n`；`s == 0` 只能是 0',
              '位数越多整数越大，高位越大整数越大：所以填满 `n` 位且高位先填 9',
              '`s <= 9` 时把余下的全填进当前位，后面补 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`s == 0` 要单独返回 0；`s > 9n` 要先返回 -1',
                 '写法二不用字符串：`d = min(s, 9)`，`ans = ans * 10 + d`',
                 '方法二数学：先填 `s // 9` 个 9，再填 `s % 9`，最后补 0，`O(1)`'],
    ),
)
