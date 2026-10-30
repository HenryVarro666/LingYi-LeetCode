CONFIG = dict(
    num=1849, title='将字符串拆分为递减的连续值', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='枚举第一个数 · 顺推验证',
    tags=['灵神题单', '链表树与回溯', '难度分 1747'],
    code='''
class Solution(object):
    def splitString(self, s):

        n = len(s)
        start = 0
        while start < n and s[start] == '0':
            start += 1
        
        if start >= n - 1:
            return False
        
        first = 0
        for index in range(start, n - 1):
            first = first * 10 + int(s[index])
            last = first
            p = index + 1
            flag = True
            while p < n:
                if last == 0:
                    while p < n and s[p] == '0':
                        p += 1
                    if p != n:
                        flag = False
                    break

                now = int(s[p])
                p += 1
                while p < n and now < last - 1:
                    now = now * 10 + int(s[p])
                    p += 1

                if now != last - 1:
                    flag = False
                    break
                last = now

            if flag:
                return True
        
        return False
''',
    call='Solution().splitString("050043")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（蓝 = 枚举的第一个数，绿 = p 之前已匹配）', cell=84, h=190,
             pointers={'p': 'pink'},
             color=lambda S, i, v: ('blue' if 'index' in S and S['start'] <= i <= S['index'] else
                                    'green' if 'index' in S and i < S.get('p', 0) else None),
             dim=lambda S, i, v: i < S.get('start', 0)),
        dict(type='text', size=28, h=70,
             fn=lambda S: (f"第一个数 `first = {S['first']}`，上一个数 `last = {S['last']}`，要找 `{S['last'] - 1}`" if 'last' in S and S['last'] > 0
                           else (f"上一个数是 `0`，剩下的必须全是 `0`" if 'last' in S else ''))),
    ],
    watch=[('start', 'start', 'cyan'), ('index', 'index', 'blue'), ('first', 'first', 'blue'),
           ('last', 'last', 'orange'), ('p', 'p', 'pink'), ('flag', 'flag', 'green')],
    skip=['n = len(s)', 'start = 0', 'first = 0'],
    captions={
        "s[start] == '0'": lambda S, B, ret: (f"`s[{S.start}] = '0'` 是前导零 → 值没有影响，跳过" if S.start < S.n and S.s[S.start] == '0'
                                              else f"`s[{S.start}] = '{S.s[S.start]}'`，前导零跳完了" if S.start < S.n else '全是零'),
        'if start >= n - 1': lambda S, B, ret: (f'`start = {S.start} >= n - 1`：至多剩 1 个字符，拆不成两段 → False' if S.start >= S.n - 1
                                                else f'`start = {S.start}`，剩下至少 2 个字符，可以尝试拆分'),
        'for index in range': '枚举第一个数的结尾 `index`（最后至少留 1 个字符）',
        'first = first * 10': '第一个数 `first` 扩一位：`{first}`（==确定第一个数，后面每个数就唯一确定==）',
        'last = first': '`last` = 上一个数 = `{last}`',
        'p = index + 1': '`p` 指向下一个数的起点 `{p}`',
        'while p < n:': lambda S, B, ret: (f'`p = {S.p} < n`：还有字符要匹配' if S.p < S.n else f'`p = n`：刚好用完所有字符'),
        'if last == 0': lambda S, B, ret: ('`last == 0`：数列到 0 就不能再减了 → 剩余字符必须全是 `0`' if S.last == 0
                                           else f'`last = {S.last}` 不为 0，继续找下一个数 `{S.last - 1}`'),
        "while p < n and s[p] == '0'": '吞掉剩余的零（它们都是前导零，合起来还是 0）',
        'if p != n': lambda S, B, ret: ('剩下有非零字符 → ==不行==' if S.p != S.n else '剩余的全是零 → 合法'),
        'now = int(s[p])': '下一个数从 `s[{p}]` 起步：`now = {now}`',
        'while p < n and now < last - 1': lambda S, B, ret: (f'`now = {S.now}` < `last - 1 = {S.last - 1}`：再接一位数字（前导零照常计入数值）' if S.p < S.n and S.now < S.last - 1 else f'`now = {S.now}` 已不小于 `last - 1 = {S.last - 1}`（或字符用完）：停止拼接'),
        'if now != last - 1': lambda S, B, ret: (f'`now = {S.now}` ≠ `last - 1 = {S.last - 1}` → ==这个第一个数不行==' if S.now != S.last - 1
                                                else f'`now = {S.now}` == `last - 1` → 匹配上，继续'),
        'last = now': '`last` 更新为 `{last}`，继续找 `{last - 1}`',
        'if flag': lambda S, B, ret: ('`flag = True`：从头到尾都匹配 → 找到合法拆分' if S.flag else '这个第一个数失败，换下一个'),
        'return True': '拆分成功 → `True`',
        'return False': '所有第一个数都试过了 → `False`',
    },
    max_steps=110,
    cards=dict(
        one_liner='第一个数一定，后面每个数都被唯一确定',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['把数字串 `s` 拆成 ==两段或以上==，使数值依次递减且相邻差恰为 `1`',
                 '示例：`"050043"` → `true`，拆成 `[05, 004, 3]` 即 `5,4,3`',
                 '`"1234"` → `false`'],
        quote='在确定了第一个数之后，后面的每一个数也就确定下来了。于是可以从头开始向后枚举第一个数，然后根据上一个数的数值判断当前剩余字符串的前缀能否构成下一个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举第一个数的结尾 `index`，用 `last` 记录上一个数',
              '下一个数必须等于 `last - 1`：从 `p` 起逐位拼，拼到不小于 `last - 1` 为止，看是否恰好相等',
              '数列到 `0` 时，剩下的字符必须全是 `0`；开头的前导零直接跳过'],
        result='`first = 5` 时 `5,4,3` 恰好用完 → True',
        summary=['时间 `O(n²)`，空间 `O(1)`，`n <= 20`',
                 '易错：前导零不影响数值，开头先跳过；第一个数至少要留 1 个字符给后面',
                 '结尾为 `0` 时，剩余字符必须全是 `0`，如 `"10"`、`"1000"` 里的零',
                 '与灵神的划分型回溯不同：这里不用回溯，第一个数定了后面唯一确定',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
