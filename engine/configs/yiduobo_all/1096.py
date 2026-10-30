def _fs(x):
    return ','.join(sorted(x)) if isinstance(x, set) else str(x)


def _layer(layer):
    return ' '.join('{' + _fs(e) + '}' if isinstance(e, set) else e for e in layer) or '空'


CONFIG = dict(
    num=1096, title='花括号展开 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='一趟扫描 · 栈按括号分层 · 集合 + / ×',
    tags=['灵神题单', '难度分 2349'],
    code='''
class Solution(object):
    def braceExpansionII(self, expression):

        expression = '{' + expression + '}'

        stack = [[]]
        now_s = ''
        now_set = set()
        for char in expression:
            if char == '{':
                if now_s:
                    now_set.add(now_s)
                    now_s = ''
                if len(now_set) > 0:
                    stack[-1].append(now_set)
                    stack[-1].append('*')
                    now_set = set()
                stack.append([])

            elif char == '}':
                res = set()
                if now_s:
                    now_set.add(now_s)
                    now_s = ''
                while stack[-1]:
                    symbol = stack[-1].pop()
                    v = stack[-1].pop()
                    if symbol == '*':
                        tmp = set()
                        for x in v:
                            for y in now_set:
                                tmp.add(x + y)
                        now_set = tmp
                    else:
                        res.update(now_set)
                        now_set = v
                now_set.update(res)
                stack.pop()

            elif char == ',':
                if now_s:
                    now_set.add(now_s)
                    now_s = ''
                stack[-1].append(now_set)
                stack[-1].append('+')
                now_set = set()
            
            else:
                if len(now_set) > 0:
                    stack[-1].append(now_set)
                    stack[-1].append('*')
                    now_set = set()
                
                now_s += char

        return sorted(list(now_set))
''',
    call='Solution().braceExpansionII("{a,b}c,d")',
    expect=['ac', 'bc', 'd'],
    views=[
        dict(type='string', var='expression', label='expression（外面已套上一层花括号）', cell=50, h=130),
        dict(type='stack', var='stack', label='stack（每层 = 一对括号；{集合} 后跟 * 或 +，栈顶在右）', fmt=_layer, font=26, h=170),
        dict(type='set', var='now_set', label='now_set（当前集合）', fmt=lambda x: x, font=30, h=110),
        dict(type='text', fn=lambda S: f"now_s（正在拼的字符串）= `{S['now_s']}`" if 'now_s' in S else '', size=28, h=70),
    ],
    watch=[('char', 'char', 'yellow'), ('now_s', 'now_s', 'blue'), ('symbol', 'symbol', 'pink')],
    skip=[10, 20, 40, 11, 14, 22, 41, 49, 29, 30, 31, 4, 6, 7],
    max_steps=110,
    captions={
        8: '`now_set` 是当前集合，`now_s` 是正在拼的字符串，`stack` 按括号分层保存上文：每层里 `集合, *` 表示稍后做乘法，`集合, +` 表示稍后做加法',
        9: lambda S, B, r: f"读到 `{S.char}`：" + {'{': '左括号', '}': '右括号', ',': '逗号'}.get(S.char, '小写字母'),
        12: '遇到括号，`now_s = {now_s!r}` 已经结束 → 变成 `now_set` 的一项',
        13: '`now_s` 清空',
        15: '`now_set` 不为空：它要和括号里的内容相乘 → 先==压栈保存==',
        16: '标上 `*`：以后做笛卡尔积',
        17: '`now_set` 清空，准备装括号里的内容',
        18: '==新开一层==：栈里多一层 `[]`，对应这一对括号',
        21: '右括号：这一层要收拢成一个集合，`res` 存加法的累计结果',
        23: '`now_s = {now_s!r}` 结束 → 并入 `now_set`',
        24: '`now_s` 清空',
        25: lambda S, B, r: ('这一层栈里还有待处理的 `(集合, 运算符)` → 继续' if S.stack[-1] else '这一层处理完了 → 汇总'),
        26: '弹出运算符 `{symbol}`',
        27: lambda S, B, r: f'弹出它前面的集合 `v = {{{_fs(S.v)}}}`',
        28: lambda S, B, r: ('运算符是 `*` → 做==笛卡尔积==（相接）' if S.symbol == '*' else '运算符是 `+` → 做==并集==（逗号并列）'),
        32: '`tmp` 加入 `{x}` + `{y}` = `{x + y}`',
        33: lambda S, B, r: f'乘法结果覆盖：`now_set = {{{_fs(S.now_set)}}}`',
        35: lambda S, B, r: f'加法：当前 `now_set` 并入 `res = {{{_fs(S.res)}}}`',
        36: '`now_set` 换成前面的集合 `v`，它可能还要和更前面的内容乘',
        37: lambda S, B, r: f'这一层弄完，把加法累计的 `res` 并进来：`now_set = {{{_fs(S.now_set)}}}`',
        38: '这一对括号处理完毕，弹出这一层',
        42: '`now_s = {now_s!r}` 结束 → 并入 `now_set`',
        43: '`now_s` 清空',
        44: '逗号是加法：把 `now_set` 压栈保存',
        45: '标上 `+`：以后做并集',
        46: '`now_set` 清空，重新装逗号后面的内容',
        50: '前面已有集合 `now_set`，现在又来字母 → 触发==乘法==，先压栈',
        51: '标上 `*`',
        52: '`now_set` 清空',
        54: '字母接到 `now_s` 末尾：`now_s = {now_s!r}`',
        56: lambda S, B, r: f'全部扫完，`now_set` 排序后返回 `{r}`',
    },
    cards=dict(
        one_liner='栈按括号分层，存「集合 + 运算符」，括号里收拢时再算',
        complexity='时间约 `O(结果数 × n)`，空间 `O(结果数)`',
        problem=['花括号展开：逗号并列取并集，相接取笛卡尔积，可以嵌套；返回不重复的有序列表',
                 '示例：`"{a,b}c,d"` 表示 `{a,b}c` 与 `d` 的并集',
                 '本视频：`"{a,b}c,d"` → `["ac","bc","d"]`'],
        quote='将栈按照括号同步分层是比较有利于处理优先级相关的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描，`now_set` 是当前集合，`now_s` 是正在拼的字符串，先在外面套一层 `{}`',
              '逗号 = 压栈 `(集合, +)`；字母或左括号遇到非空集合 = 压栈 `(集合, *)`',
              '遇到右括号：从后往前弹栈，`*` 做笛卡尔积，`+` 并入 `res`，收拢成一个集合'],
        result='扫描结束，`now_set` 排序后就是答案',
        summary=['时间随结果个数增长（结果数可达 `3^(n/7)`），空间 `O(结果数)`',
                 '易错：栈要按括号分层，右括号只收拢最上面一层',
                 '`+` 收拢时 `now_set` 要换成前面的集合，才能继续触发前面的乘法',
                 '外面套一层 `{}`，最后一层收拢的结果就在 `now_set` 里',
                 '对比灵神：灵神用递归 + `res/cur` 两个集合；yiduobo 用一个栈显式保存「集合 + 运算符」'],
    ),
)
