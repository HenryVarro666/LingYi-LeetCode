CONFIG = dict(
    num=1694, title='重新格式化电话号码', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · 三个一组 · 收尾修正',
    code='''
class Solution(object):
    def reformatNumber(self, number):

        res = []
        cnt = 0
        for char in number:
            if char == '-' or char == ' ':
                continue
            res.append(char)
            cnt += 1
            if cnt == 3:
                res.append('-')
                cnt = 0
        
        if cnt == 0:
            res.pop()
        elif cnt == 1:
            res[-2] = res[-3]
            res[-3] = '-'

        return ''.join(res)
''',
    call="Solution().reformatNumber('123 4-567')",
    expect='123-45-67',
    views=[
        dict(type='string', var='number', h=170, label='number', pointers={}, color=lambda S, i, v: 'blue' if 'char' in S and S['number'].find(S['char'], 0) >= 0 and i == S.get('_idx', -1) else None),
        dict(type='array', var='res', h=200, label='res（每个格子一个字符）'),
        dict(type='text', h=100, fn=lambda S: f"`cnt = {S['cnt']}`，当前结果：=={''.join(S['res'])}==" if 'cnt' in S else ''),
    ],
    watch=['char', ('cnt', 'cnt', 'blue'), ('res', "''.join(res)", 'green')],
    captions={
        'res = []': '`res` 存结果的每个字符，最后拼接',
        "if char == '-'": lambda S, B, r: (f"`'{S.char}'` 是分隔符 → 直接跳过" if S.char in '- ' else f"`'{S.char}'` 是数字 → 要加入答案"),
        'continue': '跳过，处理下一个字符',
        'res.append(char)': '数字 `{char}` 加入答案：`{res}`',
        'cnt += 1': '这一组有 `{cnt}` 个数字',
        'if cnt == 3': lambda S, B, r: ('凑够 3 个 → 这一组结束，后面补一个 `-`' if S.cnt == 3 else f'`cnt = {S.cnt}` 不到 3 个，继续收集'),
        "res.append('-')": '补上破折号：`{res}`',
        'cnt = 0': lambda S, B, r: ('`cnt` 记录当前这一组已经放了几个数字' if not S.res else '`cnt` 清零，开始下一组'),
        'if cnt == 0': lambda S, B, r: ('`cnt = 0`：恰好分完，末尾多了一个多余的 `-`，要删掉' if S.cnt == 0 else f'`cnt = {S.cnt}` ≠ 0，不用删末尾的 `-`'),
        'res.pop()': '删掉末尾多余的 `-`',
        'elif cnt == 1': lambda S, B, r: ('`cnt = 1`：最后落单了 1 个数字，不合法 → 要和上一组重新分' if S.cnt == 1 else f'`cnt = {S.cnt}`（2 个）：最后一组长度 2，合法，不用处理'),
        'res[-2] = res[-3]': '把倒数第 3 个数字 `{res[-2]}` 移到倒数第 2 位',
        "res[-3] = '-'": '倒数第 3 位放破折号 → 最后变成 `2 + 2` 两组：`{res}`',
        'return': "拼接得到 `'{ret}'`",
    },
    cards=dict(
        one_liner='三个一组加破折号，最后按剩余数字个数修正',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['号码由数字、空格、破折号组成：先去掉空格和破折号',
                 '再从左到右每 3 个数字一组，用破折号连接',
                 '最后剩 2 个数字就单独成组；剩 4 个则分成两组各 2 个，不能有 1 个的组',
                 '示例：`"123 4-567"` → `"123-45-67"`'],
        quote='若cnt=1，说明最后出现了一个落单的字符，是不符合题目要求的。此时应该将其与倒数第二组的三个字符综合起来分成两个长度为2的部分，具体操作只需要将倒数第二个破折号与倒数第三个数字对调即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按「每 3 个数字加一个 `-`」扫一遍，`cnt` 计当前组大小',
              '`cnt == 0`：最后多出一个 `-`，`pop` 掉',
              '`cnt == 1`：把 `-` 和前面的数字对调，变成 `2 + 2`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：恰好分完时末尾有多余破折号；剩 1 个时要借上一组的一个数字',
                 '`cnt == 1` 时 `res[-2]` 是破折号，`res[-3]` 是上一组最后一个数字，对调即可',
                 '剩 2 个数字不需要处理'],
    ),
)
