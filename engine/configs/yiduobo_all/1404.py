CONFIG = dict(
    num=1404, title='将二进制表示减到 1 的步骤数', difficulty='Medium', category='模拟',
    author='yiduobo', technique='倒序数组模拟 · 进位累加',
    code='''
class Solution(object):
    def numSteps(self, s):

        num_list = [int(char) for char in s][::-1]
        n = len(num_list)
        now = 0
        res = 0
        while now < n:
            if num_list[now] == 1:
                if now == n - 1:
                    break
                else:
                    num_list[now + 1] += 1
                    res += 2
                    now += 1
            else:
                if num_list[now] == 2:
                    if now == n - 1:
                        num_list.append(1)
                        n += 1
                    else:
                        num_list[now + 1] += 1
                res += 1
                now += 1
        
        return res
''',
    call="Solution().numSteps('1101')",
    expect=6,
    views=[
        dict(type='array', var='num_list', label='num_list（倒序：左边是低位）', h=150, pointers={'now': 'blue'}),
        dict(type='text', h=70, fn=lambda S: (f"`now` = {S['now']}，`num_list[now]` = {S['num_list'][S['now']]}" if 'now' in S and S['now'] < len(S['num_list']) else '')),
        dict(type='text', h=70, fn=lambda S: (f"已用步骤 `res` = =={S['res']}==" if 'res' in S else '')),
    ],
    watch=['now', 'n', ('res', 'res', 'green')],
    captions={
        'num_list = [int': '字符串转数组并倒过来：从前往后就是从低位到高位 → `{num_list}`',
        'now = 0': '`now` 指向当前处理的位，从最低位开始',
        'while now < n': '`now = {now}`，还没处理完',
        'if num_list[now] == 1': lambda S, B, r: f'当前位 `{S.num_list[S.now]}` ' + ('是 1' if S.num_list[S.now] == 1 else '不是 1（是 0 或收到进位的 2）') + '，分情况处理',
        'if now == n - 1': lambda S, B, r: ('已是最后一位且为 1：数字已经变成 1 → ==退出循环==' if S.now == S.n - 1 else '不是最后一位') if S.num_list[S.now] == 1 else ('是最高位：进位要在末尾新增一个 1' if S.now == S.n - 1 else '不是最高位：进位加到下一位'),
        13: '大于 1 的奇数：先加 1 变偶数，再除 2。等价于把下一位加 1 → `{num_list}`',
        22: '收到的进位传给下一位：`num_list` → `{num_list}`',
        'res += 2': '「加 1」和「除以 2」各一步：`res` → =={res}==',
        'now += 1': '跳过这一位（相当于除以 2）：`now` → {now}',
        'num_list.append(1)': '最高位进位：末尾新增一个 1 → `{num_list}`',
        'n += 1': '长度加一：`n` → {n}',
        23: '这一位为 0 或已处理完进位，只需除以 2 一步：`res` → =={res}==',
        'return res': '一共 `{res}` 步',
    },
    cards=dict(
        one_liner='倒过来存，从低位往高位走，遇到 1 就进位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制数 `s`：偶数除以 2，奇数加 1，直到变成 1',
                 '求所需步骤数',
                 '示例：`"1101"`（13）→ `6`'],
        quote='方便起见，可以想将字符串转化成数组，然后倒过来，这样一来，从前向后的顺序就是从低位向高位了。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前位是 1 且不是末位：加 1 再除 2 共 2 步，进位给下一位',
              '当前位是 2（收到进位）：先把进位传给下一位，本位变 0，再除 2 一步',
              '当前位是 0：除以 2 一步；末位是 1 就结束'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：当前位为 2 且在末尾时，要在数组末尾新增一个 1',
                 '末位的 1 表示数字已变成 1，不再计步',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神用 carry 变量不改数组，并提前加上除以 2 的次数'],
    ),
)
