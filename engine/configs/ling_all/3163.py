CONFIG = dict(
    num=3163, title='压缩字符串 III', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='分组循环 + divmod',
    code='''
class Solution:
    def compressedString(self, word: str) -> str:
        t = []
        i0 = -1
        for i, c in enumerate(word):
            if i + 1 == len(word) or c != word[i + 1]:
                k, rem = divmod(i - i0, 9)
                t.append(("9" + c) * k)
                if rem:
                    t.append(str(rem))
                    t.append(c)
                i0 = i
        return ''.join(t)
''',
    call="Solution().compressedString('aaaaaaaaaaaaaabb')",
    expect='9a5a2b',
    views=[
        dict(type='string', var='word', label='word（框 = 当前这一段连续相同字母）', cell=70, h=190,
             pointers={'i': 'blue', 'i0': 'pink'}, window=(lambda S: S['i0'] + 1, 'i')),
        dict(type='array', var='t', label='t（压缩结果的片段）', h=150),
        dict(type='text', h=80, size=30,
             fn=lambda S: f"这一段长 `{S['i'] - S['i0']}` = `9 × {S['k']} + {S['rem']}`" if 'k' in S and 'i' in S else ''),
    ],
    watch=['i', 'i0', 'c', 'k', 'rem'],
    captions={
        'i0 = -1': '`i0` 是上一段的结尾下标，初始为 -1，这样段长 = `i - i0`',
        'if i + 1 == len': '`i = {i}`：{"到末尾了，这一段结束" if i + 1 == len(word) else ("下一个字母 " + word[i+1] + " 和 " + c + (" 不同 → 这一段结束" if c != word[i+1] else " 相同 → 段还没完，继续"))}',
        'divmod': '这一段长 `{i - i0}`，每 9 个一组：`divmod({i - i0}, 9)` → `k = {k}` 个 "9{c}"，剩 `rem = {rem}`',
        '("9" + c) * k': '整组的 9 先写 `{k}` 次 `9{c}`{"" if k == 0 else " → 追加 " + ("9"+c)*k}{" （不足 9 个，什么也不加）" if k == 0 else ""}',
        'if rem': '`rem = {rem}`：{"还有零头，要再写一组" if rem else "刚好整除，没有零头"}',
        't.append(str(rem))': '零头长度 `{rem}` 写进去',
        't.append(c)': '再写字母 `{c}`',
        'i0 = i': '这一段处理完，`i0` 移到 `{i0}`，下一段从 `{i0 + 1}` 开始',
        'return': "把片段拼起来：`{ret}`",
    },
    cards=dict(
        one_liner='找出每段连续相同字母，每 9 个切一组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['反复删去最长的单字符前缀（长度最多 9），把「长度+字符」追加到结果',
                 '示例：`"aaaaaaaaaaaaaabb"` → `"9a5a2b"`',
                 '示例：`"abcde"` → `"1a1b1c1d1e"`'],
        quote='统计连续相同字母的长度，按题意模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分组循环：下一个字母不同（或到末尾）就是一段的结尾', '段长 `i - i0`，`divmod(段长, 9)` 得到整组数 `k` 和零头 `rem`',
              '先写 `k` 个 `9c`，零头不为 0 再写 `rem` 和 `c`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：字符串拼接用列表收集再 `join`，避免反复拼接',
                 '易错点：`rem == 0` 时不能写 `0c`',
                 '段末判断要先看 `i + 1 == len(word)`，防止越界'],
    ),
)
