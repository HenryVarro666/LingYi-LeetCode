def _wl(S):
    if 'right' not in S or S['right'] <= S['left']:
        return None
    return S['left']


def _wr(S):
    if 'right' not in S or S['right'] <= S['left']:
        return None
    return S['right'] - 1


CONFIG = dict(
    num=2516, title='每种字符至少取 K 个', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='转化为最长合法子数组 · 变长滑动窗口',
    tags=['滑动窗口与双指针', '难度分 1948'],
    code='''
class Solution(object):
    def takeCharacters(self, s, k):

        tot = [0] * 3
        for char in s:
            tot[ord(char) - 97] += 1
        
        if min(tot) < k:
            return -1
        
        cnt = [0] * 3
        right = 0
        res = len(s)
        for left in range(len(s)):
            if right < left:
                right = left
            
            while right < len(s) and cnt[ord(s[right]) - 97] + 1 + k <= tot[ord(s[right]) - 97]:
                cnt[ord(s[right]) - 97] += 1
                right += 1

            res = min(res, len(s) - (right - left))

            if left < right:
                cnt[ord(s[left]) - 97] -= 1
        
        return res
''',
    call="Solution().takeCharacters('aabbcabca', 2)",
    expect=6,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口 [left, right) = 不取走的中间部分）', pointers={'left': 'pink', 'right': 'blue'},
             window=(_wl, _wr), h=230, cell=90),
        dict(type='array', var='tot', label='tot：s 中 a / b / c 的总个数', h=150, cell=90, color=lambda S, i, v: 'cyan'),
        dict(type='array', var='cnt', label='cnt：窗口内 a / b / c 的个数（不能超过 tot − k）', h=150, cell=90,
             color=lambda S, i, v: 'yellow' if 'tot' in S and 'k' in S and v >= S['tot'][i] - S['k'] else None),
    ],
    watch=[('left', 'left', 'pink'), ('right', 'right', 'blue'), ('res', 'res', 'green')],
    captions={
        'tot = [0] * 3': '`tot[0..2]` 依次统计 `a`、`b`、`c` 在 `s` 里的总个数',
        'tot[ord(char) - 97] += 1': '`{char}` 的下标是 `ord(char) - 97 = {ord(char) - 97}`，`tot` → {tot}',
        'if min(tot) < k': '最少的字符只有 `{min(tot)}` 个，{"不到 k → 肯定取不够" if min(tot) < k else "都 >= k，有解"}',
        'return -1': '某个字符总数不足 `k` → 返回 `-1`',
        'cnt = [0] * 3': '`cnt` 记窗口内各字符个数；窗口里最多留 `tot - k` 个，其余必须被取走',
        'right = 0': '`right` 是窗口右边界（开区间），只增不减',
        'res = len(s)': '`res` 记最少取走的个数，初始为取走全部 `{len(s)}`',
        'right = left': '右边界落到 `left` 后面了（窗口为空）→ 追上来：`right = left = {left}`',
        'while right < len(s) and': '{"右边界已到末尾，不能再扩" if right >= len(s) else "能再多留下 s[" + str(right) + "]（" + s[right] + "）吗？窗口内个数 + 1 + k 不能超过总数：" + ("可以" if cnt[ord(s[right]) - 97] + 1 + k <= tot[ord(s[right]) - 97] else "不行，停下")}',
        'cnt[ord(s[right]) - 97] += 1': '`{s[right]}` 进窗口，窗口内个数变成 `{cnt}`',
        'right += 1': '`right` → {right}',
        'res = min': '窗口长 `{right - left}`，要取走 `{len(s)} − {right - left} = {len(s) - (right - left)}`，`res = min({B.res}, …) = {res}`',
        'if left < right': '窗口{"非空：左端点要离开窗口" if left < right else "是空的，没有东西可移出"}',
        'cnt[ord(s[left]) - 97] -= 1': '`{s[left]}` 离开窗口，窗口内个数变成 `{cnt}`',
        'return res': '最少取走 `{res}` 个',
    },
    skip=['right += 1', 'if left < right', 'if right < left', 'for char in s', 'for left in range'],
    max_steps=110,
    cards=dict(
        one_liner='两端取走 = 中间留下：找最长、且各字符不超限的子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a b c`，每次只能取走最左或最右的字符',
                 '每种字符至少取 `k` 个，求最少取几个；取不够返回 `-1`',
                 '本视频：`s="aabbcabca"`，`k=2` → `6`'],
        quote='题目要求从数组的两端各取一些字符，那么剩下的就是一段连续子数组，同时这段子数组中各个字符出现的次数均不超过其出现总数减去k。',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计总数，任何字符不足 `k` 直接 `-1`',
              '剩下的中间段里，每种字符最多 `tot - k` 个，要这段==最长==',
              '枚举左边界，右边界单调不减：能多留就往右扩',
              '答案 = `len(s)` 减去最长合法窗口长度'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先判 `-1`；窗口内某字符个数 `+1+k <= tot` 才能再扩',
                 '`right < left` 时要把 `right` 追到 `left`，保证窗口不会反过来',
                 '代码本身可在 Python 3 直接运行，未改动',
                 '对比灵神：灵神维护窗口==外==的个数、不够就收缩；yiduobo 维护窗口==内==的个数、够留就扩'],
    ),
)
