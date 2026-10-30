def _fmt_set(x):
    return '""' if x == '' else x


CONFIG = dict(
    num=1096, title='花括号展开 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='递归 · 并列取并集 · 相接取笛卡尔积',
    tags=['灵神题单', '难度分 2349'],
    code='''
class Solution:
    def braceExpansionII(self, expression: str) -> list[str]:
        i = 0

        def dfs() -> set[str]:
            nonlocal i
            res = set()
            cur = {""}  # 加个空串，简化后续判断逻辑

            while i < len(expression):
                ch = expression[i]
                i += 1

                if ch == '}':  # 归
                    break
                if ch == ',':  # 取并集
                    res |= cur  # 把 cur 中的字符串都添加到 res 中
                    cur = {""}
                elif ch == '{':  # 递
                    sub_res = dfs()
                    cur = {s + t for s in cur for t in sub_res}  # 计算 cur 和 sub_res 的笛卡尔积
                else:  # ch 是字母
                    cur = {s + ch for s in cur}  # 把 ch 添加到 cur 每个字符串的末尾

            return res | cur

        return sorted(dfs())
''',
    call='Solution().braceExpansionII("{a,b}{c,{d,e}}")',
    expect=['ac', 'ad', 'ae', 'bc', 'bd', 'be'],
    views=[
        dict(type='string', var='expression', label='expression（蓝箭头 = 下一个要读的字符 i；暗 = 已读）', pointers={'i': 'blue'}, cell=52, h=150,
             dim=lambda S, i, v: 'i' in S and i < S['i']),
        dict(type='set', var=lambda S: S['_inner'].get('res'), label='res（并列的结果：已经「,」分开的部分）', fmt=_fmt_set, font=30, h=110),
        dict(type='set', var=lambda S: S['_inner'].get('cur'), label='cur（正在相接的这一段）', fmt=_fmt_set, font=30, h=110),
        dict(type='calls', h=200),
    ],
    watch=[('i', 'i', 'blue'), ('ch', lambda S: S['_inner'].get('ch'), 'yellow')],
    skip=[7, 10, 11, 14, 16, 19],
    max_steps=100,
    captions={
        3: '`i` 是当前读到的下标，放在递归函数外面，所有层共用',
        8: '新的一层 `dfs`：`res` 收集逗号分开的结果，`cur` 是正在相接的一段，`cur = {{""}}`（含一个空串，相接起点）',
        12: lambda S, B, r: ('读到 `ch = %r`，`i` → %d：' % (S['_inner']['ch'], S.i) + {
            '{': '左括号 → 递归处理括号里面', '}': '右括号 → 这一层结束，==归==', ',': '逗号 → 并列，结算当前的 `cur`'}.get(S['_inner']['ch'], '字母 → 接到 `cur` 每个串末尾')),
        15: '遇到 `}`：括号里的内容读完了，`break` 跳出，把 `res | cur` 返回给上一层',
        17: '逗号两边是并列：把 `cur = {cur}` 并入 `res`，==并集==',
        18: '`cur` 重新从空串开始，处理逗号后面这一段',
        20: '遇到 `{`：括号里是一个独立的子表达式，==递归== `dfs()` 求出它展开后的集合 `sub_res`',
        21: '括号和前面相接：`cur` 里每个串 `s` 配上 `sub_res` 里每个串 `t` → ==笛卡尔积==，新的 `cur = {cur}`',
        23: '字母：把 `{ch}` 接到 `cur` 每个串末尾 → `{cur}`',
        25: lambda S, B, r: f'这一层结束：`res | cur` = `{sorted(r)}`，最后一段也要并进来',
        27: '`dfs()` 求出整个表达式展开后的集合，外面再 `sorted` 排成有序列表',
    },
    cards=dict(
        one_liner='并列像加法取并集，相接像乘法取笛卡尔积，括号递归',
        complexity='时间 `O(n^2 3^(n/7))`，空间 `O(3^(n/7))`',
        problem=['花括号展开：`{a,b}` 取并集；`{a,b}{c,d}` 相接，各取一个拼起来；可以嵌套',
                 '返回所有不重复的字符串，按字典序排序',
                 '本视频：`"{a,b}{c,{d,e}}"` → `["ac","ad","ae","bc","bd","be"]`'],
        quote='处理表达式时，注意运算的优先级：并列像加法，相接像乘法。实现时，我们要准备两个哈希集合：res 保存整个表达式展开后的所有字符串；cur 保存当前正在处理的相接表达式的字符串集合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cur` 初始化为 `{""}`（含一个空串），字母直接接到每个串末尾，不用特判空集',
              '逗号：把 `cur` 并入 `res`，`cur` 重新开始；`{`：递归，返回后与 `cur` 做笛卡尔积',
              '`}` 或走到末尾：递归结束，返回 `res | cur`'],
        result='整个表达式展开完毕，`sorted` 后返回 6 个字符串',
        summary=['时间 `O(n^2 3^(n/7))`（瓶颈在排序），空间 `O(3^(n/7))`：字符串个数最多是指数级',
                 '并列像加法、相接像乘法：逗号并集，括号/字母做笛卡尔积',
                 '易错：`cur` 要初始化成 `{""}` 而不是空集，否则笛卡尔积永远为空',
                 '`dfs` 里的 `i` 要用 `nonlocal`，递归返回后接着往后读',
                 '灵神还给了写法二：用栈手动模拟这个递归，思路相同；相关题 394 字符串解码'],
    ),
)
