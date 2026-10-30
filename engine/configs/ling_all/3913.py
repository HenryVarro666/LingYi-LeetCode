CONFIG = dict(
    num=3913, title='按频率对元音排序', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='计数 + 稳定排序 + 回填元音',
    code='''
class Solution:
    def sortVowels(self, s: str) -> str:
        cnt = {}
        vowels = []  # 长度至多为 5
        for ch in s:
            if ch not in "aeiou":
                continue
            if ch not in cnt:
                cnt[ch] = 1
                vowels.append(ch)
            else:
                cnt[ch] += 1

        # 把 aeiou 按照出现次数从大到小排序
        vowels.sort(key=lambda ch: -cnt[ch])

        t = list(s)
        j = 0
        for i, ch in enumerate(t):
            if ch not in "aeiou":
                continue
            t[i] = c = vowels[j]
            cnt[c] -= 1
            if cnt[c] == 0:
                j += 1  # c 消耗完了，切换到下一种元音
        return ''.join(t)
''',
    call='Solution().sortVowels("leetcode")',
    expect='leetcedo',
    views=[
        dict(type='string', var='s', label='s（原串）', h=150, cell=80),
        dict(type='map', var='cnt', label='cnt（元音出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=110, font=30),
        dict(type='array', var='vowels', label='vowels（按首次出现顺序，排序后按次数从大到小）', h=170, cell=70, pointers={'j': 'pink'}),
        dict(type='string', var='t', label='t（回填元音后的结果）', h=190, cell=80, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and S['_line'] >= 21 and i <= S['i'] and v in 'aeiou' else None),
    ],
    watch=['ch', ('j', 'j', 'pink'), 'i', ('vowels', 'vowels', 'cyan')],
    skip=['for ch in s', 'for i, ch in enumerate(t)'],
    captions={
        'cnt = {}': '`cnt` 统计每种元音出现的次数',
        'vowels = []': '`vowels` 按==首次出现的顺序==记录出现过的元音（至多 5 个）',
        'if ch not in "aeiou"': lambda S, B, r: (f"看到 `'{S.ch}'`，不是元音 → 跳过，不动它" if S.ch not in 'aeiou' else (f"看到 `'{S.ch}'`，是元音 → 要统计" if S['_line'] < 17 else f"位置 `{S.i}` 是元音 `'{S.ch}'` → 要换成排好序的元音")),
        'continue': '辅音留在原位，直接看下一个',
        'if ch not in cnt': lambda S, B, r: (f"`'{S.ch}'` 第一次出现 → 记入 cnt 和 vowels" if S.ch not in S.cnt else f"`'{S.ch}'` 已出现过 → 次数 +1"),
        'cnt[ch] = 1': "新元音 `'{ch}'`：次数 1，同时 ==按首次出现顺序== 加进 `vowels`",
        'vowels.append(ch)': '`vowels` = {vowels}（顺序 = 首次出现顺序）',
        'cnt[ch] += 1': "`cnt['{ch}']` → {cnt[ch]}",
        'vowels.sort': '按次数从大到小排序：{vowels}。==稳定排序==，次数相同的保持首次出现的先后',
        't = list(s)': '转成列表 `t`，准备把元音按新顺序填回去',
        'j = 0': '`j` 指向当前要填的元音种类',
        't[i] = c': "位置 `{i}` 是元音：填入 `vowels[{j}] = '{c}'`",
        'cnt[c] -= 1': "`'{c}'` 还剩 {cnt[c]} 个没填",
        'if cnt[c] == 0': lambda S, B, r: (f"`'{S.c}'` 填完了 → 切换到下一种元音" if S.cnt[S.c] == 0 else f"`'{S.c}'` 还没填完，下个元音位置继续填它"),
        'j += 1': '`j` → {j}，下一种元音',
        'return': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='统计元音次数，稳定排序后，按顺序填回元音位置',
        complexity='时间 `O(n + |Σ|log|Σ|)`，空间 `O(n)`',
        problem=['只重排 `s` 里的==元音==，让它们按出现次数非递增排列',
                 '次数相同则按在 `s` 中==首次出现==的先后',
                 '示例：`"leetcode"` → `"leetcedo"`（e×3 在前，o×1 在后）'],
        quote='把这些元音按照其出现次数从大到小排序。这里的排序是稳定排序，这样在出现次数相同时，会自动把位置靠前的元音排在前面。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历时顺便按首次出现的顺序把元音存进 `vowels`',
              '稳定排序：次数相同的元音不会交换先后，免去手写第二关键字',
              '再遍历一遍，遇到元音就填 `vowels[j]`，用完切换 `j`'],
        summary=['时间 `O(n + |Σ|log|Σ|)`，|Σ| = 5，排序可视作常数',
                 '易错：`vowels` 必须按首次出现顺序加入，稳定排序才能保证同频次的先后',
                 '易错：辅音不动，用 `continue` 跳过；填完一种元音要 `j += 1`',
                 '字符串不可变，所以先 `list(s)`，最后 `join`'],
    ),
)
