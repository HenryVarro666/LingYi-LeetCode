CONFIG = dict(
    num=1860, title='增长的内存泄露', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='直接模拟（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def memLeak(self, a: int, b: int) -> List[int]:
        i = 1
        while i <= a or i <= b:
            if a >= b:
                a -= i
            else:
                b -= i
            i += 1
        return [i, a, b]
''',
    call='Solution().memLeak(8, 11)',
    expect=[6, 0, 4],
    views=[
        dict(type='bars', var=lambda S: [S['a'], S['b']], h=330, label='剩余内存 [a, b]', vmax=11),
        dict(type='text', size=30, h=80, fn=lambda S: f"第 `{S['i']}` 秒：a = `{S['a']}`，b = `{S['b']}`" if 'i' in S else ''),
    ],
    watch=['i', ('a', 'a', 'blue'), ('b', 'b', 'pink')],
    captions={
        'i = 1': '从第 1 秒开始分配',
        'while i <= a': lambda S, B, r: (f'`i = {S.i}`，至少有一条内存够 `i` 位（`a = {S.a}`，`b = {S.b}`）→ 继续' if (S.i <= S.a or S.i <= S.b)
                                         else f'`i = {S.i}` 比两条内存都大 → 程序意外退出'),
        'if a >= b': '`a = {a}`，`b = {b}`：`a >= b` → {"a 剩得多（相等给 a），分给 a" if a >= b else "b 剩得多，分给 b"}',
        'a -= i': '第 {i} 秒给 a 分配 {i} 位：a → =={a}==',
        'b -= i': '第 {i} 秒给 b 分配 {i} 位：b → =={b}==',
        'i += 1': '进入下一秒：`i = {i}`',
        'return': '退出时间 {i}，剩余 `{a}` 和 `{b}`：`{ret}`',
    },
    cards=dict(
        one_liner='谁剩得多就分给谁，模拟到分不动为止',
        complexity='时间 `O(sqrt(a+b))`，空间 `O(1)`',
        problem=['第 `i` 秒要分配 `i` 位内存，给剩余较多的那条（相等给第一条）',
                 '两条都不足 `i` 位时程序崩溃，返回 `[崩溃秒, 剩余1, 剩余2]`',
                 '示例：`memory1 = 8, memory2 = 11` → `[6, 0, 4]`'],
        quote='func memLeak(a, b int) []int { i := 1; for ; i <= a || i <= b; i++ { if a >= b { a -= i } else { b -= i } } ... }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['循环条件 `i <= a or i <= b`：只要有一条放得下就继续',
              '`a >= b` 分给 a，否则分给 b，直接照题意模拟',
              '总消耗是 `1+2+...+i`，增长很快，所以循环只有 `O(sqrt)` 次'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for ; cond; i++` 写成 `while` + `i += 1`）',
                 '时间 `O(sqrt(a+b))`，空间 `O(1)`',
                 '易错点：相等时给第一条（`a >= b`）',
                 '循环结束时的 `i` 就是崩溃时间，不要再加减 1'],
    ),
)
