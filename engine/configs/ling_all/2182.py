def _cnt(S):
    return {chr(97 + i): c for i, c in enumerate(S['cnt']) if c}


def _ans(S):
    return list(S['ans'])


CONFIG = dict(
    num=2182, title='构造限制重复的字符串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 从大到小填字母（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1680'],
    code='''
class Solution:
    def repeatLimitedString(self, s: str, repeatLimit: int) -> str:
        cnt = [0] * 26
        for b in s:
            cnt[ord(b) - ord('a')] += 1
        ans = []
        for i in range(25, -1, -1):  # 从大到小填字母
            k = i - 1
            while True:
                j = 0
                while j < repeatLimit and cnt[i] > 0:  # 填充 min(repeatLimit, cnt[i]) 个字母 i
                    cnt[i] -= 1
                    ans.append(chr(ord('a') + i))
                    j += 1
                if cnt[i] == 0:  # i 用完了，找下一个更小的字母
                    break
                while k >= 0 and cnt[k] == 0:
                    k -= 1
                if k < 0:
                    break
                # i 没用完，插入一个字母 k，这样可以继续填 i
                cnt[k] -= 1
                ans.append(chr(ord('a') + k))
        return ''.join(ans)
''',
    call='Solution().repeatLimitedString("zzzzyyx", 2)',
    expect="zzyzzyx",
    views=[
        dict(type='text', fn=lambda S: (f"当前最大字母 `{chr(97 + S['i'])}`（剩 `{S['cnt'][S['i']]}` 个），插入备选 `{chr(97 + S['k']) if S.get('k', -1) >= 0 else '无'}`；限制连续 `{S['repeatLimit']}` 个" if 'i' in S and 'k' in S else '统计各字母个数后，从大到小填'), size=26),
        dict(type='map', var=_cnt, label='cnt（剩余个数）', h=220),
        dict(type='array', var=_ans, label='ans（已构造）', h=200),
    ],
    max_steps=80,
    watch=[('i', "chr(97+i) if 'i' in S else ''", 'pink'), ('k', "chr(97+k) if k >= 0 else '无'", 'blue'), ('ans', "''.join(ans)", 'green')],
    captions={
        'cnt = [0] * 26': '`cnt[c]` 统计每个字母剩余个数',
        'for i in range(25': lambda S, B, r: f"现在考虑字母 `{chr(97 + S.i)}`（还剩 `{S.cnt[S.i]}` 个）：字典序越大越优先",
        'k = i - 1': '`k` 指向比 `i` 小的下一个候选字母，用来当"隔板"',
        'while j < repeatLimit and cnt[i] > 0': lambda S, B, r: (f"`j = {S.j} < {S.repeatLimit}` 且还有 `{chr(97 + S.i)}` → ==再填一个== `{chr(97 + S.i)}`" if (S.j < S.repeatLimit and S.cnt[S.i] > 0) else (f"已连续填满 `{S.repeatLimit}` 个，不能再填 `{chr(97 + S.i)}`" if S.cnt[S.i] > 0 else f"`{chr(97 + S.i)}` 用完了")),
        'cnt[i] -= 1': '`{chr(97 + i)}` 剩 `{cnt[i]}` 个',
        'ans.append(chr(ord(\'a\') + i))': '`ans` 末尾加入 `{chr(97 + i)}` → `{"".join(ans)}`',
        'if cnt[i] == 0': lambda S, B, r: (f"`{chr(97 + S.i)}` 用完了 → ==换下一个更小的字母==" if S.cnt[S.i] == 0 else f"`{chr(97 + S.i)}` 还剩 `{S.cnt[S.i]}` 个但已连续 `{S.repeatLimit}` 个 → ==必须插一个更小的字母隔开=="),
        'while k >= 0 and cnt[k] == 0': lambda S, B, r: (f"`{chr(97 + S.k)}` 已用完，`k` 继续往小的找" if (S.k >= 0 and S.cnt[S.k] == 0) else (f"没有更小的字母可当隔板 → 只能到此为止" if S.k < 0 else f"找到隔板字母 `{chr(97 + S.k)}`（还剩 `{S.cnt[S.k]}` 个）")),
        'k -= 1': '`k` → {k}',
        'if k < 0': lambda S, B, r: ('`k < 0`：没有更小的字母了，==剩下的 i 填不进去，break==' if S.k < 0 else '`k >= 0`：有字母可以当隔板'),
        'cnt[k] -= 1': '用掉一个隔板字母 `{chr(97 + k)}`，它还剩 `{cnt[k]}` 个',
        "ans.append(chr(ord('a') + k))": '隔板 `{chr(97 + k)}` 放在最大字母后面 → `{"".join(ans)}`，然后回去继续填大字母',
        "return ''.join(ans)": '构造结果 =={ret}==',
    },
    cards=dict(
        one_liner='从大到小填字母，填满限制就插一个小字母当隔板',
        complexity='时间 `O(n + 26^2)`，空间 `O(26)`（除答案外）',
        problem=['字符串 `s`，任何字母连续出现不能超过 `repeatLimit` 次',
                 '不必用完所有字符，求字典序最大的构造结果',
                 '示例：`s = "cczazcc", repeatLimit = 3` → `"zzcccac"`；本视频：`"zzzzyyx"`，限制 2'],
        quote='要使字典序最大，应优先选择最大的字母 i，选择 min(cnt[i], repeatLimit) 个。如果字母 i 未被选完，为了不让字母 i 连续出现次数超过 repeatLimit，我们可以选择一个较小的字母放在后面，然后再继续选择字母 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先统计每个字母个数 `cnt`，从 `z` 往 `a` 填',
              '每次最多填 `repeatLimit` 个当前字母；填不完就插一个更小的字母隔开',
              '用指针 `k` 单调往小移动找隔板，找不到就结束这个字母'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（选用原文第二种用指针 `k` 的写法，第一种用 `goto` 重复查找）',
                 '时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '易错点：隔板只放一个，放完要回到最大字母继续填',
                 '隔板找不到时，剩下的大字母只能丢弃，不要硬放'],
    ),
)
