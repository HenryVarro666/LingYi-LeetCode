def _top(S):
    if 'index' not in S:
        return ''
    p = S['p']
    if p is None:
        return f"`number[{S['index']}] = {S['number'][S['index']]}` 不是 digit，跳过"
    return f"最近一个 digit 的位置：`p = {p}`（遇到更靠后的就覆盖它）"


CONFIG = dict(
    num=2259, title='移除指定数字得到的最大结果', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='比较 num[p] 与 num[p+1]',
    tags=['灵神题单', '贪心算法'],
    code='''
class Solution(object):
    def removeDigit(self, number, digit):

        n = len(number)
        p = None
        for index in range(n):
            if number[index] == digit:
                p = index
                if index < n -1 and number[index] < number[index + 1]:
                    break
        
        return number[:p] + number[p + 1:]
''',
    call='Solution().removeDigit("732334", "3")',
    expect='73234',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='number', label='number（黄 = digit，蓝 = 当前扫描，粉 = 候选删除位 p）', cell=84,
             pointers={'index': 'blue', 'p': 'pink'},
             color=lambda S, k, v: ('pink' if S.get('p') == k else 'blue' if S.get('index') == k
                                    else ('yellow' if v == S['digit'] else None))),
        dict(type='text', fn=lambda S: ('比较 `number[p] = ' + S['number'][S['p']] + '` 与 `number[p+1] = ' + S['number'][S['p'] + 1] + '`：'
                                        + ('后者更大 → 删 p 位变大' if S['number'][S['p']] < S['number'][S['p'] + 1] else '不更大 → 先不删，留作候选')
                                        ) if S.get('p') is not None and S['p'] + 1 < len(S['number']) else '', size=24),
    ],
    watch=['digit', 'n', ('index', 'index', 'blue'), ('p', 'p', 'pink')],
    captions={
        'n = len': '`n = {n}`',
        'p = None': '`p` 记录准备删除的位置，还没有',
        'for index in range': '扫描 `index = {index}`，数字是 `{number[index]}`',
        'if number[index] == digit': lambda S, B, r: (f"`number[{S.index}] = {S.number[S.index]}` == digit `{S.digit}` → 是候选位置"
                                                      if S.number[S.index] == S.digit else f"`number[{S.index}] = {S.number[S.index]}` ≠ digit，跳过"),
        'p = index': '候选位置 `p = {p}`（越靠后的相等 digit 先留着，作为全都不优时的兜底）',
        'if index < n -1': lambda S, B, r: (f"`number[{S.index}] = {S.number[S.index]}`，`number[{S.index + 1}] = {S.number[S.index + 1]}`：{S.number[S.index]} < {S.number[S.index + 1]} → ==删它能变大==，break"
                                            if S.index < S.n - 1 and S.number[S.index] < S.number[S.index + 1]
                                            else (f"已是最后一位，没有更大的后继" if S.index >= S.n - 1
                                                  else f"`{S.number[S.index]}` ≥ `{S.number[S.index + 1]}`：删它不会变好（相等时与删下一个等价）→ 继续向后")),
        'return number[:p]': '删掉位置 `p = {p}`，得到 `{ret}`',
    },
    cards=dict(
        one_liner='遇到 digit 且右边更大就删它；否则删最后一个 digit',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`number` 是正整数字符串，`digit` 至少出现一次',
                 '恰好删掉一个等于 `digit` 的字符，使结果最大',
                 '示例：`"1231"`，`digit = "1"` → `"231"`'],
        quote='当num[p]小于num[p + 1]时，无论后面q的位置如何，移除后都可以得到更好的结果。反过来，若num[p]大于num[p + 1]，那么就不应该执行移除。',
        quote_src='—— yiduobo 题解原文',
        idea=['位置越靠高位，影响越大：能优先删高位就删高位',
              '比较删 p 和删 q（p < q）：差别只在 `num[p]` 与 `num[p+1]` 的大小',
              '`num[p] < num[p+1]`：删 p 一定更好，立即返回；相等则两者等价，继续往后看',
              '扫完都没删：只能被迫删最后一个 digit，因为它影响最小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`p` 每遇到 digit 就更新，所以不 break 时 `p` 就是最后一个 digit',
                 '易错：`index < n - 1` 防止最后一位越界比较',
                 '对比灵神：灵神一行暴力枚举取 max，yiduobo 用贪心一趟扫描'],
    ),
)
