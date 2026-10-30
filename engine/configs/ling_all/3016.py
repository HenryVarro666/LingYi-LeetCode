def _formula(S):
    a = S.get('a')
    if not a or S.get('_line', 0) < 4:
        return '先数每个字母出现几次，再排序'
    return '`' + ' + '.join(f'{c}×{i // 8 + 1}' for i, c in enumerate(a)) + '` = ==' + str(sum(c * (i // 8 + 1) for i, c in enumerate(a))) + '=='


CONFIG = dict(
    num=3016, title='输入单词需要的最少按键次数 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='频次排序 + 排序不等式',
    tags=['灵神题单', '难度分 1534'],
    code='''
class Solution:
    def minimumPushes(self, word: str) -> int:
        a = sorted(Counter(word).values(), reverse=True)
        return sum(c * (i // 8 + 1) for i, c in enumerate(a))
''',
    call="Solution().minimumPushes('aabbccddeeffgghhiiiiii')",
    expect=24,
    views=[
        dict(type='string', var='word', label='word', h=190, cell=40),
        dict(type='array', var='a', label='a：各字母出现次数，从大到小（下标 i // 8 + 1 = 按键次数）', h=260, cell=70,
             color=lambda S, i, v: ['green', 'yellow', 'orange', 'pink'][min(i // 8, 3)]),
        dict(type='text', size=34, fn=_formula),
    ],
    watch=['a'],
    captions={
        'a = sorted': '统计每个字母的出现次数，==从大到小==排序：`a` = {a}',
        'return sum': '第 `i` 大的字母要按 `i // 8 + 1` 次：前 8 个按 1 次，接着 8 个按 2 次……次数 × 按键数相加 → =={ret}==',
    },
    cards=dict(
        before=[dict(heading='按键成本', lines=['`2`~`9` 共 8 个键：每个键上第 1 个字母按 1 次', '第 2 个字母按 2 次，第 3 个按 3 次……', '前 8 个字母 ==成本 1==，第 9~16 个 ==成本 2==，以此类推'])],
        after=[dict(heading='示例逐项相加', lines=['`a = [6, 2, 2, 2, 2, 2, 2, 2, 2]`', '`i = 0..7`：`6×1 + 2×1 × 7` = 20', '`i = 8`：`2 × (8 // 8 + 1)` = 4', '合计 ==24=='])],
        one_liner='出现次数多的字母放在前面，每个键第一个位置先占满',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['`2`~`9` 共 8 个键，可以任意重新分配小写字母，每个字母恰好放一个键', '按第 `k` 个位置的字母要按 `k` 次，求输入 `word` 的最少按键次数',
                 '示例：`aabbccddeeffgghhiiiiii` → `24`'],
        quote='出现次数前 8 大的字母，只需要按一次；出现次数前 9 到 16 大的字母，需要按两次；依此类推。把出现次数和对应的按键次数相乘再相加，得到的按键次数之和就是最小的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按键次数只有 8 个 1、8 个 2、8 个 3、2 个 4…… 的「名额」', '排序不等式：==次数大的字母配小的按键数==，乘积和最小',
              '所以出现次数从大到小，第 `i` 个乘 `i // 8 + 1`'],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`', '`i` 从 0 开始，所以是 `i // 8 + 1`，不是 `i // 8`',
                 '不用真的构造键盘映射，只要算「次数 × 按键数」'],
    ),
)
