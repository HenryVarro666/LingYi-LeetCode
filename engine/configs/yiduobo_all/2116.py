S0, L0 = '))()))', '010100'


def _col(S, i, v):
    return 'purple' if S['locked'][i] == '0' else None


def _info(S):
    if 'cnt' not in S:
        return '先从左到右、再从右到左，各扫一遍'
    ln = S['_line']
    d = '从左往右（缺 `(` 时借可变括号）' if ln <= 24 else '从右往左（左右地位互换）'
    return f'{d}：落单 `cnt = {S["cnt"]}`，可变 `change_able = {S["change_able"]}`'


CONFIG = dict(
    num=2116, title='判断一个括号字符串是否有效', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='正反各扫一遍 · 可变括号补位',
    tags=['栈', '合法括号字符串', '难度分 2038'],
    code='''
class Solution(object):
    def canBeValid(self, s, locked):

        n = len(s)
        if n % 2 == 1:
            return False

        cnt = 0
        change_able = 0
        for index in range(n):
            if s[index] == '(':
                cnt += 1
            else:
                if locked[index] == '0':
                    change_able += 1
                if cnt == 0:
                    if change_able > 0:
                        change_able -= 1
                        cnt = 1
                    else:
                        return False
                else:
                    cnt -= 1

        cnt = 0
        change_able = 0
        for index in range(n - 1, -1, -1):
            if s[index] == ')':
                cnt += 1
            else:
                if locked[index] == '0':
                    change_able += 1
                if cnt == 0:
                    if change_able > 0:
                        change_able -= 1
                        cnt = 1
                    else:
                        return False
                else:
                    cnt -= 1
                
        return True
''',
    call=f'Solution().canBeValid({S0!r}, {L0!r})',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26, h=100),
        dict(type='string', var='s', label='s（紫 = 可改的括号）', pointers={'index': 'blue'}, window=('index', 'index'),
             color=_col, cell=90, h=230),
        dict(type='string', var='locked', label='locked（0 = 可改，1 = 不能改）', pointers={'index': 'blue'}, window=('index', 'index'),
             cell=90, h=200, color=_col),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'pink'), ('change_able', 'change_able', 'purple')],
    captions={
        'n % 2 == 1': '长度是奇数，必有括号落单 → `False`；这里 `n = {n}`，继续',
        8: '`cnt`：当前落单（还没配对）的括号个数',
        9: '`change_able`：目前见过的==可变括号==个数，缺括号时拿来救急',
        25: '第二遍从右往左：`cnt`、`change_able` 清零重来',
        26: '`change_able` 清零',
        10: lambda S, B, ret: ('从左往右扫完，没有无解 → 再从右往左扫一遍' if 'index' in B and B.index == S.index else f'`index = {S.index}`，看 `s[{S.index}] = {S.s[S.index]}`'),
        27: lambda S, B, ret: ('从右往左扫完，也没有无解' if 'index' in B and B.index == S.index and B.index == 0 else f'反向扫描：`index = {S.index}`，看 `s[{S.index}] = {S.s[S.index]}`'),
        11: lambda S, B, ret: (f"`s[{S.index}] = '('`：落单左括号" if S.s[S.index] == '(' else f"`s[{S.index}] = ')'`：右括号，要找落单左括号配对"),
        28: lambda S, B, ret: (f"`s[{S.index}] = ')'`：落单右括号" if S.s[S.index] == ')' else f"`s[{S.index}] = '('`：左括号，要找落单右括号配对"),
        12: '`cnt` +1 → {cnt}',
        29: '`cnt` +1 → {cnt}',
        14: lambda S, B, ret: (f'`locked[{S.index}] = 0`：这个括号可变' if S.locked[S.index] == '0' else f'`locked[{S.index}] = 1`：不能改，不记'),
        31: lambda S, B, ret: (f'`locked[{S.index}] = 0`：这个括号可变' if S.locked[S.index] == '0' else f'`locked[{S.index}] = 1`：不能改，不记'),
        15: '可变括号 +1：`change_able = {change_able}`',
        32: '可变括号 +1：`change_able = {change_able}`',
        16: lambda S, B, ret: (f'`cnt = 0`：没有落单括号可以配对，需要从可变括号里借一个' if S.cnt == 0 else f'`cnt = {S.cnt} > 0`：有落单括号，直接配对'),
        33: lambda S, B, ret: (f'`cnt = 0`：没有落单括号可以配对，需要从可变括号里借一个' if S.cnt == 0 else f'`cnt = {S.cnt} > 0`：有落单括号，直接配对'),
        17: lambda S, B, ret: (f'`change_able = {S.change_able} > 0`：把一个可变括号改成需要的方向' if S.change_able > 0 else '`change_able = 0`：没有可变括号可借 → ==无解=='),
        34: lambda S, B, ret: (f'`change_able = {S.change_able} > 0`：把一个可变括号改成需要的方向' if S.change_able > 0 else '`change_able = 0`：没有可变括号可借 → ==无解=='),
        18: '用掉一个可变括号：`change_able` → {change_able}',
        35: '用掉一个可变括号：`change_able` → {change_able}',
        19: '改成需要的括号后，它自己又成了一个落单括号：`cnt = 1`',
        36: '改成需要的括号后，它自己又成了一个落单括号：`cnt = 1`',
        23: '配对成功：`cnt` → {cnt}',
        40: '配对成功：`cnt` → {cnt}',
        'return True': '正反两遍都没出现无解 → ==可以改成有效括号串== `True`',
    },
    cards=dict(
        one_liner='缺括号时拿前面的可变括号补位；正反各扫一遍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`locked[i] = 0` 的位置可以改成 `(` 或 `)`',
                 '问能否改成有效括号字符串',
                 '示例：`s = "))()))"`，`locked = "010100"` → `true`'],
        quote='使用另一个变量 change_able，记录当前可变右括号的数目，当出现左括号不足的情况时，选择将之前的某个可变右括号变为左括号即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['常规做法：`cnt` 记落单左括号，出现 `)` 配不上就失败',
              '这里：`)` 配不上时，把之前可变的括号改成 `(` 来救急',
              '但左括号可能多出来 → 从右向左再做一遍，两个方向都不缺括号，才算有解'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '长度是奇数直接 `False`',
                 '易错：反向扫描时左右括号地位互换，判断的是 `)` 而不是 `(`',
                 '对比灵神：灵神用 `[mn, mx]` 一遍扫；yiduobo 用两遍扫描 + 可变括号计数'],
    ),
)
