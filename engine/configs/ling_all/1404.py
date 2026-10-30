CONFIG = dict(
    num=1404, title='将二进制表示减到 1 的步骤数', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='从低位模拟 · 进位',
    code='''
class Solution:
    def numSteps(self, s: str) -> int:
        ans = len(s) - 1  # 除了最高位，其余每一位都要执行一次「除以 2」
        carry = 0
        for i in range(len(s) - 1, 0, -1):
            sum_ = int(s[i]) + carry
            ans += sum_ % 2  # 如果 s[i] 变成 1，需要执行「加上 1」
            carry = (sum_ + sum_ % 2) // 2
        # 如果在最高位还有进位，由于 1 + 1 = 10，需要再执行一次「除以 2」
        return ans + carry
''',
    call="Solution().numSteps('1101')",
    expect=6,
    views=[
        dict(type='string', var='s', label='s（右边是低位）', h=130, pointers={'i': 'blue'}),
        dict(type='text', h=70, fn=lambda S: (f"`sum_` = `s[{S['i']}]` + `carry` = {S['sum_']}" if 'sum_' in S and 'i' in S else '')),
        dict(type='text', h=70, fn=lambda S: (f"`ans` = =={S['ans']}==，`carry` = =={S['carry']}==" if 'carry' in S else '')),
    ],
    watch=['i', 'sum_', ('carry', 'carry', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = len(s) - 1': '先把「除以 2」的次数算上：除最高位外每位一次 → `ans = {len(s)} − 1` = =={ans}==',
        'carry = 0': '进位 `carry` 从 0 开始',
        'for i in range': '处理低位 `s[{i}]`',
        'sum_ = int': '`sum_ = {int(s[i])} + carry({B.carry})` = =={sum_}==',
        'ans += sum_ % 2': lambda S, B, r: (f'`sum_ = {S.sum_}` 是奇数 → 要先「加 1」再除 2，`ans` +1 → =={S.ans}==' if S.sum_ % 2 else f'`sum_ = {S.sum_}` 是偶数 → 直接除 2，不用加 1，`ans` 不变'),
        'carry = (sum_': lambda S, B, r: f'新的进位：`({S.sum_} + {S.sum_ % 2}) // 2` = =={S.carry}==' + ('（一旦进位，后面每位都会进位）' if S.carry else ''),
        'return ans + carry': '最高位若还有进位 `{carry}`，要再除一次 2：`{ans} + {carry}` = =={ans + carry}==',
    },
    cards=dict(
        one_liner='操作都发生在最低位，从右往左带着进位模拟',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数 `s`：偶数除以 2，奇数加 1，直到变成 1',
                 '求所需步骤数',
                 '示例：`"1101"`（13）→ `6`'],
        quote='由于除以 2、加上 1 这些操作发生在 s 的最低位，所以我们要从右往左遍历 s，模拟计算过程。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`ans` 先记上 `n-1` 次「除以 2」，循环里只数「加 1」',
              '`sum_ = s[i] + carry`，`sum_` 为奇数就要加 1',
              '一旦进位，后面每一位都会进位；最高位有进位再多除一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环到 `i = 1` 为止，最高位单独在最后处理',
                 '方法二公式：设最右的 1 在下标 i，`i>0` 时答案 = n−1 + [1,i−1] 中 0 的个数 + 2',
                 '本视频用示例 `"1101"` 演示方法一'],
    ),
)
