CONFIG = dict(
    num=2243, title='计算字符串的数字和', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='模拟（Go 原文转写）', tags=[],
    code='''
class Solution:
    def digitSum(self, s: str, k: int) -> str:
        while len(s) > k:
            t = []
            while True:
                sum = 0
                for i in range(min(len(s), k)):
                    sum += ord(s[i]) & 15
                t.append(str(sum))
                if len(s) <= k:
                    break
                s = s[k:]
            s = ''.join(t)
        return s
''',
    call='Solution().digitSum("123456789", 3)',
    expect='126',
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, h=200, label='s（当前剩余的字符串）'),
        dict(type='array', var='t', h=200, label='t（已算出的各组数字和）'),
        dict(type='text', fn=lambda S: f"当前这一组数字和 `sum` = =={S['sum']}==" if 'sum' in S else '', h=90),
    ],
    watch=['k', ('sum', 'sum', 'green'), 'i', ('len(s)', 'len(s)', 'blue')],
    captions={
        'while len(s) > k': lambda S, B, r: (f'`len(s) = {len(S.s)} > k = {S.k}`：长度还大于 k → 再来一轮拆分-求和' if len(S.s) > S.k else f'`len(s) = {len(S.s)} <= k = {S.k}`：不用再操作了，退出循环'),
        't = []': '准备一个空的 `t`，收集这一轮每组的数字和',
        'while True': '一组一组地处理 `s`，直到最后一组',
        'sum = 0': '新的一组：数字和清零',
        'sum += ': '`s[{i}]` 的数字是 `{ord(s[i]) & 15}`（ASCII 低 4 位就是数字值）→ `sum = {sum}`',
        't.append': '这一组的数字和 `{sum}` 追加进 `t`，得到 `{t}`',
        'if len(s) <= k': lambda S, B, r: (f'剩余长度 `{len(S.s)} <= {S.k}`：这是最后一组 → 结束本轮' if len(S.s) <= S.k else f'剩余长度 `{len(S.s)} > {S.k}`：后面还有组，继续'),
        's = s[k:]': '切掉已处理的前 k 个字符，`s = "{s}"`',
        "s = ''.join": '这一轮结束：把各组和拼起来，新的 `s = "{s}"`，回去检查长度是否仍大于 k',
        'return s': '`len(s) <= k`，不再操作 → 返回 `"{s}"`',
    },
    cards=dict(
        one_liner='每轮：按 k 个一组求数字和，拼成新串，直到长度不超过 k',
        complexity='时间 `O(n^2)` 量级（每轮长度大致缩小到约 1/k × 位数），空间 `O(n)`',
        problem=['把数字串 `s` 每 `k` 个分一组，每组换成数字和的字符串，拼接',
                 '长度仍大于 `k` 就重复，最后返回 `s`',
                 '示例：`s="123456789", k=3` → `"126"`'],
        quote='（灵神题解仅给出 Go 代码：外层 `for len(s) > k`，内层逐组累加，用 `s = s[k:]` 切掉已处理部分）',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['外层 `while`：只要 `len(s) > k` 就再来一轮',
              '内层 `while True`：每次累加前 `min(len(s), k)` 位，写入 `t`，再把 `s` 切掉前 k 位',
              '`ord(ch) & 15` 取字符的数字值，免去 `int(ch)`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`strings.Builder` → list + `join`，`ch & 15` → `ord(ch) & 15`',
                 '复杂度：每轮长度至少缩小一部分，总体 `O(n^2)`，`n ≤ 100` 完全够',
                 '易错点：最后一组可能不足 k 位；一组的和可能是两位数，会让下一轮变长',
                 '每轮结束都要重新判断 `len(s) > k`'],
    ),
)
