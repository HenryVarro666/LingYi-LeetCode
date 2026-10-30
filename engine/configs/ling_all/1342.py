def _b(x):
    return list(format(x, 'b'))

CONFIG = dict(
    num=1342, title='将数字变成 0 的操作次数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='模拟（附位运算公式）',
    tags=['位运算', '基础题'],
    code='''
class Solution:
    def numberOfSteps(self, num: int) -> int:
        ans = 0
        while num:
            if num % 2:
                num -= 1
            else:
                num //= 2
            ans += 1
        return ans
''',
    call='Solution().numberOfSteps(14)',
    expect=6,
    views=[
        dict(type='string', var=lambda S: _b(S['num']) if S.get('num') else ['0'], label='num 的二进制', h=200,
             color=lambda S, i, v: 'yellow' if v == '1' else None),
        dict(type='text', fn=lambda S: f"`num = {S['num']}`，已操作 =={S['ans']}== 次", size=34),
    ],
    watch=['num', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '操作次数从 0 开始',
        'while num': lambda S, B, r: (f'`num = {S.num}`，还没到 0 → 继续' if S.num else '`num = 0`：已经变成 0 → 结束'),
        'if num % 2': '`num = {num}`，`num % 2` = {num % 2} → {"奇数，要减 1" if num % 2 else "偶数，要除以 2"}',
        'num -= 1': '奇数减 1，只是把最低位的 1 变成 0：`num` = {num}',
        'num //= 2': '偶数除以 2，二进制少一位（右移）：`num` = {num}',
        'ans += 1': '这一步算一次操作：`ans` → {ans}',
        'return': '一共 =={ret}== 步',
    },
    cards=dict(
        one_liner='题目怎么说，就怎么做',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['`num` 是偶数就除以 2，奇数就减 1',
                 '求变成 0 所需的步数',
                 '示例：`num=14` → `6`'],
        quote='题目说什么，我们就怎么做。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['写一个循环：`num` 不为 0 就继续',
              '偶数除以 2，奇数减 1，每次计数加一',
              '每两步内必有一次除以 2，所以只循环 `O(log num)` 次'],
        summary=['时间 `O(log num)`，空间 `O(1)`',
                 '灵神方法二：答案 = `L + K - 1`，L 是二进制长度，K 是 1 的个数',
                 '即 `num.bit_length() + num.bit_count() - 1`，`num=0` 要特判为 0',
                 '本视频演示的是方法一的循环写法'],
    ),
)
