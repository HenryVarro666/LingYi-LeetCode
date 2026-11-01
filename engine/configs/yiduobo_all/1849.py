def _top(S):
    if 'start' not in S:
        return ''
    if S['_line'] == 13:
        return f'试 `first` 以 `s[{S["index"]}]` 结尾'
    if 'first' in S and 'index' in S and S['first'] > 0:
        s = S['s']
        txt = f'第一个数 `first` = =={S["first"]}==（`s[{S["start"]}..{S["index"]}]`）'
        if 'last' in S:
            txt += f'，上一个数 `last = {S["last"]}`，下一个必须是 ==`{S["last"] - 1}`=='
        return txt
    return f'跳过前导零：`start = {S["start"]}`'


def _while_p(S, B, ret):
    if S.p < S.n:
        return f'`p = {S.p} < n`：还有字符，继续凑下一个数'
    return '`p` 走到末尾：整串都分完了'


def _now(S, B, ret):
    return f'`now` 先取 `s[{S.p}] = {S.now}`（`p` 随后后移），要凑成 ==`{S.last - 1}`=='


def _grow(S, B, ret):
    if S.p < S.n and S.now < S.last - 1:
        return f'`now = {S.now}` 还小于 `last - 1 = {S.last - 1}` → 再接一位 `s[{S.p}]`'
    return f'`now = {S.now}` 已不小于 `last - 1 = {S.last - 1}`（或字符用完）→ 不再接'


def _chk(S, B, ret):
    if S.now != S.last - 1:
        return f'`now = {S.now}` ≠ `last - 1 = {S.last - 1}` → ==这个 first 不行=='
    return f'`now = {S.now}` == `last - 1` → 这一段对上了'


CONFIG = dict(
    num=1849, title='将字符串拆分为递减的连续值', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='枚举第一个数 + 逐个凑下一个数',
    tags=['链表树与回溯', '难度分 1747'],
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
    call='Solution().splitString("10009998")',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝 = first，绿 = 已凑出的数，粉箭头 = p）', cell=70,
             pointers={'p': 'pink'}, pointer_labels={'p': 'p'},
             color=lambda S, k, v: ('blue' if 'index' in S and S['start'] <= k <= S['index'] else
                                    ('green' if 'p' in S and S['index'] < k < S['p'] else None)) if 'index' in S else None,
             dim=lambda S, k, v: k < S['start'] if 'start' in S else False),
        dict(type='text', fn=lambda S: (f'当前 `now = {S["now"]}`' if 'now' in S and 'p' in S and S['_line'] >= 21 else ''), size=28),
    ],
    watch=[('start', 'start', 'cyan'), ('first', 'first', 'blue'), ('last', 'last', 'orange'), ('p', 'p', 'pink'), ('now', 'now', 'green'), 'flag'],
    captions={
        'n = len(s)': '`n = {n}`',
        'start = 0': '先数出前导零：前导零不影响数值，可以忽略',
        'start += 1': '`s[{start-1}]` 是 `0`，跳过 → `start = {start}`',
        'if start >= n - 1': '`start = {start}`，至少要留两位才能拆成两段；这里够，继续',
        'first = 0': '`first` 累计第一个数',
        'for index in range': '枚举第一个数的结尾 `index = {index}`',
        'first = first * 10': '`first` 接上 `s[{index}]` → =={first}==',
        'last = first': '`last` 记录上一个数 = `{last}`',
        'p = index + 1': '`p` 指向下一个数的开头：`{p}`',
        'flag = True': '`flag` 先假设这个 first 能成功',
        18: _while_p,
        'if last == 0': lambda S, B, ret: ('上一个数已经是 `0`，后面只能剩下零了' if S.last == 0 else '`last = {0}` ≠ 0，还能继续递减'.format(S.last)),
        20: '`last = 0`：剩下的字符必须全是 `0`，这里 `p = {p}`，向后吃零',
        'break': '`break`：这个 first 到此为止，回到外层',
        'if p != n': '`p != n`：还有非零字符 → `flag = False`',
        'now = int(s[p])': _now,
        28: _grow,
        'now = now * 10': '接上 `s[{p}]`：`now = {now}`，`p` 后移',
        'if now != last - 1': _chk,
        'last = now': '`last = {last}`：继续找下一个数',
        'flag = False': '`flag = False`，==放弃这个 first==，试更长的',
        'if flag': lambda S, B, ret: ('`flag` 为真：整串拆完了 → 成功' if S.flag else '`flag` 为假：换下一个 first'),
        'return True': '存在合法拆分 → `True`',
        'return False': '所有 first 都不行 → `False`',
    },
    skip=['p += 1'],
    max_steps=90,
    cards=dict(
        one_liner='第一个数一确定，后面所有数都被钉死，往后逐个对',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['数字串 `s` 拆成至少两段，数值依次递减，相邻差 `1`',
                 '示例：`"050043"` → `[5,4,3]` → `true`',
                 '本视频：`"10009998"` → `[100,99,98]` → `true`'],
        quote='由于题目要求的是逐一递减的连续值，那么在确定了第一个数之后，后面的每一个数也就确定下来了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先跳过前导零，从头向后枚举第一个数 `first`',
              '之后每个数 `now` 从 `p` 起逐位拼，直到不小于 `last - 1`；必须恰好 `== last - 1`',
              '数列降到 `0` 时，剩下的字符必须全是零'],
        result='`first = 100` 时依次拼出 `99`、`98` 正好用完 → True ✓',
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '先跳前导零，且要保证 `first` 之后还剩至少一位',
                 '递减到 `0` 要单独处理：后面全零才算对',
                 '对比灵神：灵神每轮 `str(v)` 做前缀匹配；yiduobo 逐位拼数字比数值'],
    ),
)
