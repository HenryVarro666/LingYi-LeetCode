def _inner(name):
    return lambda S: S['_inner'].get(name)


def _lp(S):
    v = S['_inner'].get('last_pos')
    if v is None:
        v = S['_inner'].get('index')
    return v if isinstance(v, int) and 0 <= v < len(S['num']) else None


CONFIG = dict(
    num=282, title='给表达式添加运算符', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='回溯切分 + 记录上一步变化量处理乘法',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def addOperators(self, num, target):

        res = []
        now = 0
        for index, char in enumerate(num):
            if now == 0 and index != 0:
                break
            now = now * 10 + int(char)
            self.dfs(num, index, now, now, str(now), target, res)

        return res

    def dfs(self, num, last_pos, now, last_delta, expr, target, res):
        if last_pos == len(num) - 1:
            if now == target:
                res.append(expr)
            return

        tmp = 0
        for index in range(last_pos + 1, len(num)):
            if tmp == 0 and index != last_pos + 1:
                break
            tmp = tmp * 10 + int(num[index])
            self.dfs(num, index, now + tmp, tmp, expr + '+' + str(tmp), target, res)
            self.dfs(num, index, now - tmp, -tmp, expr + '-' + str(tmp), target, res)
            self.dfs(num, index, now - last_delta + last_delta * tmp, last_delta * tmp, expr + '*' + str(tmp), target, res)
''',
    call='Solution().addOperators("123", 6)',
    expect=['1+2+3', '1*2*3'],
    views=[
        dict(type='string', var='num', label='num（蓝 = 已经用掉到这里）', cell=70, h=170, pointers={_lp: 'blue'}, pointer_labels={_lp: 'last_pos'}),
        dict(type='text', fn=lambda S: (f"表达式 `{S['_inner']['expr']}` = =={S['_inner']['now']}==，目标 `{S['_inner']['target']}`"
                                        if 'expr' in S['_inner'] else ''), h=70),
        dict(type='calls', h=210, hide=('num', 'target', 'res')),
        dict(type='stack', var='res', label='res（凑出 target 的表达式）', h=100),
    ],
    watch=[('now', _inner('now'), 'blue'), ('last_delta', _inner('last_delta'), 'pink'), ('tmp', _inner('tmp'), 'cyan'),
           ('target', 'target', 'green')],
    skip=[18, 'if tmp == 0 and index', 'res = []', 'now = 0', 'tmp = 0', 'for index, char in enumerate(num)', 'for index in range(last_pos + 1'],
    captions={
        'if now == 0 and index != 0': lambda S, B, r: (
            '`now == 0` 且不是第一位：说明这个数以 ==0 开头==（如 `05`），不合法 → break' if (S.now == 0 and S.index != 0)
            else f'第一个数可以取前 `{S.index + 1}` 位，没有前导零'),
        'now = now * 10': '第一个数取前 `{index + 1}` 位：`now = {now}`',
        'self.dfs(num, index, now, now, str': '开头的数 `{now}` 选好了：`last_delta = {now}`（上一项的变化量）；继续切后面的数',
        'if last_pos == len(num) - 1': lambda S, B, r: (
            f'`last_pos = {S.last_pos}` 已是最后一位：表达式 `{S.expr}` = =={S.now}==' if S.last_pos == len(S.num) - 1
            else f'还剩 `{len(S.num) - 1 - S.last_pos}` 位没用：继续切下一个数，并在前面加运算符'),
        'if now == target': lambda S, B, r: (
            f'`{S.now} == {S.target}` → ==凑出 target==' if S.now == S.target else f'`{S.now} != {S.target}` → 这个表达式不对'),
        'res.append(expr)': '`{expr}` 加入答案 `res`',
        'tmp = tmp * 10 + int': '下一个数取 `num[{last_pos + 1}..{index}]`：`tmp = {tmp}`（以 0 开头的多位数会在上一行被 break 掉）',
        "expr + '+'": '加 `{B.tmp}`：`now = {B.now} + {B.tmp} = {B.now + B.tmp}`，这一项的变化量是 `{B.tmp}`',
        "expr + '-'": '减 `{B.tmp}`（当成加 `-{B.tmp}`）：`now = {B.now - B.tmp}`，变化量是 `-{B.tmp}`',
        "expr + '*'": '乘 `{B.tmp}`：先==撤销上一项==的变化量 `{B.last_delta}`，再加上 `{B.last_delta} × {B.tmp}`：`now = {B.now} - ({B.last_delta}) + {B.last_delta * B.tmp} = {B.now - B.last_delta + B.last_delta * B.tmp}`',
        'return res': '共 `{len(ret)}` 个表达式等于目标：`{ret}`',
    },
    max_steps=58,
    cards=dict(
        one_liner='把减法当加负数，乘法时撤销上一项再补上乘积',
        complexity='时间 `O(n·4^n)`，空间 `O(n)`（不计返回值）',
        problem=['给定只含数字的字符串 `num` 和整数 `target`，在数字之间插入 `+ - *` 或什么都不插',
                 '返回所有结果等于 `target` 的表达式；数字不能有前导零',
                 '示例：`num="123", target=6` → `["1+2+3","1*2*3"]`'],
        quote='需要采取经典的做法，将减法看做负数的加法，那么整个过程就变成了加上某数，或者加上某个乘积。当需要进行乘法运算时，只需要将当前的结果减去上一轮的变化量，然后加上这个变化量乘以当前数字的结果即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['原本想用区间 DP，但乘法优先级让 `f[0][1] * f[2][2]` 这类合并出错，于是改成暴力搜索',
              '`dfs` 每次枚举下一个数 `tmp` 的切分点，对它做加、减、乘三种操作',
              '`last_delta` 记录上一项对 `now` 的贡献：乘法时 `now - last_delta + last_delta * tmp`',
              '例：`1+2` 再乘 3：`3 - 2 + 2*3 = 7`，不是 `9`'],
        result='共 2 个表达式：`1+2+3` 和 `1*2*3` ✓',
        summary=['时间约 `O(n·4^n)`，空间 `O(n)`；每个间隙有 `+ - * 不插` 四种选择',
                 '前导零：`tmp == 0 and index != last_pos + 1` 时 break，`05` 这样的数不能用',
                 '乘法要用 `last_delta`（上一项变化量），减法的变化量是 `-tmp`',
                 '原文就是 Python 3 也能直接运行的写法，未做任何修改'],
    ),
)
