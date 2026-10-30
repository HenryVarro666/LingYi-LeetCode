CONFIG = dict(
    num=1839, title='所有元音按顺序排布的最长子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 按元音顺序匹配（Go 原文转写）',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1580'],
    code='''
class Solution:
    def longestBeautifulSubstring(self, s: str) -> int:
        ans = 0
        vowel = "aeiou"
        cur, sum = 0, 0
        i, n = 0, len(s)
        while i < n:
            start = i
            ch = s[start]
            while i < n and s[i] == ch:
                i += 1

            if ch != vowel[cur]:
                cur, sum = 0, 0
                if ch != vowel[0]:
                    continue

            sum += i - start
            cur += 1
            if cur == 5:
                if sum > ans:
                    ans = sum
                cur, sum = 0, 0
        return ans
''',
    call='Solution().longestBeautifulSubstring("aeiaaeiioouu")',
    expect=9, max_steps=80,
    views=[
        dict(type='text', fn=lambda S: (f"正在匹配元音 `{S['vowel'][S['cur']]}`（第 {S['cur']+1} 个），已累计长度 ==`{S['sum']}`==" if 'cur' in S and S['cur'] < 5 else ''), size=30),
        dict(type='string', var='s', cell=60, pointers={'start': 'blue', 'i': 'pink'}, h=260,
             color=lambda S, i, v: ('green' if 'start' in S and S['_line'] >= 14 and S['start'] <= i < S['i'] else None)),
        dict(type='string', var='vowel', pointers={'cur': 'orange'}, label='目标元音顺序', h=200),
    ],
    watch=[('start', 'start', 'blue'), ('i', 'i', 'pink'), 'ch', ('cur', 'cur', 'orange'), ('sum', 'sum', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cur, sum = 0, 0': lambda S, B, r: ('`cur = sum = 0`：重新开始找美丽子串' if 'start' in S and S.ch != S.vowel[B.cur] else '`cur` 指向第一个元音 `a`，`sum` 累计长度'),
        'start = i': '新的一组从 `start = {i}` 开始',
        'ch = s[start]': '这一组的字母是 `{ch}`',
        'i += 1': '同一组字母，`i` 右移到 {i}',
        'if ch != vowel[cur]': '`{ch}` 和期望的 `{vowel[cur]}` {"不同 → 顺序断了" if ch != vowel[cur] else "相同 → 顺序对得上"}',
        'if ch != vowel[0]': '`{ch}` {"也不是 a → 这一组没法做开头，跳过" if ch != vowel[0] else "就是 a → 可以作为新美丽串的开头"}',
        'continue': '直接处理下一组',
        'sum += i - start': '这一组长 `{i-start}`，==累加== 到 `sum = {sum}`',
        'cur += 1': '`cur = {cur}`：下一个该是 `{vowel[cur] if cur < 5 else "（五个都齐了）"}`',
        'if cur == 5': '`cur == 5`？{"五个元音都出现过且有序 → 美丽子串" if cur == 5 else "还没凑齐"}',
        'if sum > ans': '`sum = {sum}` 和 `ans = {ans}` 比较 → {"更长，更新" if sum > ans else "不更长"}',
        'ans = sum': '`ans = {ans}`',
        'return ans': '最长美丽子串长度 `{ans}`',
    },
    cards=dict(
        one_liner='每次吃掉一整组相同字母，按 aeiou 顺序接龙',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定只含元音的字符串，美丽子串：==五个元音都出现，且按字典序排列==',
                 '求最长美丽子串长度，没有返回 `0`',
                 '本视频：`aeiaaeiioouu` → `9`'],
        quote='采用分组遍历的写法来寻找美丽子字符串。（每次遍历处理一组相同的连续字母）',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cur` 是当前期望的元音下标，`sum` 是已拼出的长度',
              '这组字母和 `vowel[cur]` 对不上：清零，若恰好是 `a` 就当作新开头',
              '对上了：累加长度，`cur` 前进；`cur == 5` 就是一个美丽子串'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，每个字符只被扫一次；空间 `O(1)`',
                 '易错：失配后若新字母是 `a`，要当作新开头而不是丢弃',
                 '灵神还给了正则写法 `a+e+i+o+u+`，取最长匹配',
                 '同类题：分组循环模板（题单「六、分组循环」）'],
    ),
)
