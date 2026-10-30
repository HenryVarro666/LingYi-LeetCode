CONFIG = dict(
    num=2423, title='删除字符使频率相同', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='次数的次数 cnt_of_cnt',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def equalFrequency(self, word):

        cnt_dict = {}
        for char in word:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        cnt_of_cnt = {}
        for cnt in cnt_dict.values():
            cnt_of_cnt[cnt] = cnt_of_cnt.get(cnt, 0) + 1

        if len(cnt_of_cnt) == 1:
            return min(cnt_of_cnt.values()) == 1 or min(cnt_of_cnt.keys()) == 1
        
        if len(cnt_of_cnt) == 2:
            if cnt_of_cnt[max(cnt_of_cnt.keys())] == 1 and min(cnt_of_cnt.keys()) == max(cnt_of_cnt.keys()) - 1:
                return True
            if min(cnt_of_cnt.keys()) == 1 and cnt_of_cnt[1] == 1:
                return True
        
        return False
''',
    call='Solution().equalFrequency("bacbc")',
    expect=True,
    views=[
        dict(type='string', var='word', label='word', h=150),
        dict(type='map', var='cnt_dict', label='cnt_dict：字母 → 出现次数', fmt=lambda k, v: f"'{k}': {v}", h=190, font=32),
        dict(type='map', var='cnt_of_cnt', label='cnt_of_cnt：出现次数 → 有几种字母', fmt=lambda k, v: f"{k} 次: {v} 种", h=190, font=32),
    ],
    watch=['char', 'cnt'],
    skip=['cnt_dict = {}', 'cnt_of_cnt = {}'],
    max_steps=60,
    captions={
        'cnt_dict[char]': '字母 `{char}` 出现次数 → `{cnt_dict[char]}`',
        'cnt_of_cnt[cnt]': '有 `{cnt_of_cnt[cnt]}` 种字母出现了 `{cnt}` 次',
        'if len(cnt_of_cnt) == 1': lambda S, B, r: (f'`len(cnt_of_cnt) = {len(S.cnt_of_cnt)}`：所有字母出现次数相同，要删一个后还相同，只能「每种只出现 1 次」或「只有一种字母」'
                                                  if len(S.cnt_of_cnt) == 1 else f'`len(cnt_of_cnt) = {len(S.cnt_of_cnt)}`：不是只有一种次数'),
        'if len(cnt_of_cnt) == 2': lambda S, B, r: (f'`len(cnt_of_cnt) = 2`：次数恰好有两种，要把它们变成一种，进入细分' if len(S.cnt_of_cnt) == 2
                                                  else f'次数有 {len(S.cnt_of_cnt)} 种，不可能删一个就统一 → 走到 `return False`'),
        'cnt_of_cnt[max(cnt_of_cnt.keys())] == 1 and': lambda S, B, r: (
            '较大的次数只有一种字母，且恰好比较小的多 1 → 删掉它一个就齐了' if (S.cnt_of_cnt[max(S.cnt_of_cnt)] == 1 and min(S.cnt_of_cnt) == max(S.cnt_of_cnt) - 1)
            else f'较大次数 `{max(S.cnt_of_cnt)}` 对应 `{S.cnt_of_cnt[max(S.cnt_of_cnt)]}` 种字母，或与较小次数 `{min(S.cnt_of_cnt)}` 相差不是 1 → 这条不成立'),
        'min(cnt_of_cnt.keys()) == 1 and cnt_of_cnt[1]': lambda S, B, r: (
            '较小次数是 1 且只有一种字母 → 把这个只出现一次的字母删掉，其余次数相同' if (min(S.cnt_of_cnt) == 1 and S.cnt_of_cnt[1] == 1)
            else '这条也不成立'),
        'return True': '满足条件 → 返回 `True`',
        'return False': '没有任何一种删法能让次数统一 → 返回 `False`',
    },
    cards=dict(
        one_liner='先数字母次数，再数「次数」的次数',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['字符串 `word`，==恰好删除一个字符==',
                 '问删完后每个字母出现次数是否都相同',
                 '示例：`"abcc"` → `true`；`"aazz"` → `false`'],
        quote='我在这里采用的是统计每个字符出现的次数cnt，以及cnt.values()中每种次数出现的次数cnt_of_cnt，然后根据这两种次数来进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt_dict`：字母 → 次数；`cnt_of_cnt`：次数 → 有几种字母',
              '次数只能有 1 种或 2 种，否则一次删除救不回来',
              '只有 1 种：只能是每个字母各 1 次，或整串只有一种字母',
              '有 2 种：较大的那种只有一个字母且多 1；或较小的是 1 且只有一个字母'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '`len(cnt_of_cnt) == 1` 时：次数全是 2 以上（如 `"aabbcc"`）要返回 False',
                 '有两种次数时，「不合群」的那种次数只能对应一个字母',
                 '对比灵神：灵神把次数排序后直接比较；yiduobo 用字典统计「次数的次数」'],
    ),
)
