CONFIG = dict(
    num=1894, title='找到需要补充粉笔的学生编号', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='前缀和 + 取模 + 二分',
    code='''
class Solution(object):
    def chalkReplacer(self, chalk, k):

        s = [chalk[0]]
        for num in chalk[1:]:
            s.append(s[-1] + num)
        
        k %= s[-1]
        if k < s[0]:
            return 0
        
        l = 0
        r = len(chalk) - 1
        while l < r:
            mid = (l + r) >> 1
            if s[mid] > k:
                r = mid
            else:
                l = mid + 1
        
        return l
''',
    call='Solution().chalkReplacer([3,4,1,2], 25)',
    expect=1,
    views=[
        dict(type='array', var='chalk', label='chalk', cell=96, h=190),
        dict(type='array', var='s', label='s（前缀和）', cell=96, h=240,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}),
        dict(type='text', size=34, h=100,
             fn=lambda S: f"`k = {S['k']}`，找第一个 `s[i] > k` 的 i" if 'l' in S else (f"`k = {S['k']}`" if 'k' in S else '')),
    ],
    watch=['k', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        's = [chalk[0]]': '前缀和数组从 `chalk[0] = {chalk[0]}` 开始',
        'for num in chalk[1:]': '取下一个学生要用的粉笔 `num = {num}`',
        's.append': '`s[i] = s[i-1] + {num}` → 前缀和 `{s}`',
        'k %= s[-1]': '一整轮共用 `{s[-1]}` 支，整轮都够就不用管：`k` 取模 `{s[-1]}` 后 = =={k}==（原来 {B.k}）',
        'if k < s[0]': lambda S, B, r: (f'`k = {S.k} < s[0] = {S.s[0]}`：第 0 个学生就不够 → 答案 0' if S.k < S.s[0]
                                        else f'`k = {S.k} ≥ s[0] = {S.s[0]}`：学生 0 够用，需要二分找位置'),
        'l = 0': '二分范围左端 `l = 0`',
        'r = len': '右端 `r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，区间还没缩成一个点' if S.l < S.r else f'`l = {S.l}`，`r = {S.r}`，区间收缩完毕'),
        'mid = (l + r)': '取中点 `mid = ({l} + {r}) >> 1 = {mid}`',
        'if s[mid] > k': lambda S, B, r: (f'`s[{S.mid}] = {S.s[S.mid]} > k = {S.k}`：粉笔在 mid 之前或恰在 mid 用完 → 答案在左半（含 mid）' if S.s[S.mid] > S.k
                                         else f'`s[{S.mid}] = {S.s[S.mid]} ≤ k = {S.k}`：到 mid 为止都够用 → 答案在右半'),
        'r = mid': '`r = mid = {r}`：保留 mid，它可能就是答案',
        'l = mid + 1': '`l = mid + 1 = {l}`：mid 够用，排除它',
        'return l': '`l = {l}` 是第一个 `s[i] > k` 的位置 → 学生 =={l}== 需要补充粉笔',
    },
    cards=dict(
        one_liner='先对一整轮取模，再在前缀和上二分第一个大于 k 的位置',
        complexity='时间 `O(n)`（建前缀和）+ `O(log n)`（二分），空间 `O(n)`',
        problem=['`n` 个学生轮流回答，学生 `i` 用 `chalk[i]` 支粉笔；粉笔不够用的学生要补充',
                 '总共 `k` 支，问最先需要补充的学生编号',
                 '示例：`chalk=[3,4,1,2], k=25` → `1`'],
        quote='先将k对所有学生都回答一次问题消耗的粉笔数取模，然后再进行判断。……题目实际上就是要找到一个i，满足s[i - 1] <= k < s[i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 超过一整轮，就先对整轮总量取模，只看最后不完整的一轮',
              '前缀和 `s[i]` 是学生 0…i 用完的总量，找满足 `s[i-1] <= k < s[i]` 的 i',
              '前缀和递增，可以二分；`k < s[0]` 时答案就是 0'],
        summary=['时间 `O(n)`，空间 `O(n)`（前缀和），二分本身 `O(log n)`',
                 '`k %= s[-1]` 是关键，否则 k 到 1e9 没法直接模拟',
                 '要找的是第一个 `s[i] > k`，相等时 mid 够用，要右移：用 `>` 不是 `>=`',
                 '二分是左闭右闭收缩：`r = mid`、`l = mid + 1`，保证循环结束 `l == r`'],
    ),
)
