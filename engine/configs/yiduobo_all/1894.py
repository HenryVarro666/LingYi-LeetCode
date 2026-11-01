CONFIG = dict(
    num=1894, title='找到需要补充粉笔的学生编号', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='前缀和 + 二分',
    tags=[],
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
    call='Solution().chalkReplacer([5,1,5,2,3,4], 47)',
    expect=2,
    views=[
        dict(type='text', size=32, h=80, fn=lambda S: f"粉笔数 `k = {S['k']}`" + (f"；前缀和最后一项 `s[-1] = {S['s'][-1]}`" if S.get('s') else '')),
        dict(type='array', var='chalk', h=190, label='chalk（每人每次用量）', cell=70),
        dict(type='array', var='s', h=330, label='s（前缀和：到该学生为止累计消耗）', cell=70,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, window=('l', 'r')),
    ],
    watch=['k', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        's = [chalk[0]]': '`s[i]` 记第 `0..i` 号学生用完后的总消耗，先放 `s[0] = {chalk[0]}`',
        's.append': '`s[-1] + {num}`：前缀和追加 =={s[-1]}==',
        'k %= s[-1]': '整轮总消耗是 `s[-1] = {s[-1]}`，先取模：=={B.k} → {k}==，只看最后不完整的一轮',
        'if k < s[0]': lambda S, B, r: (f'`k = {S.k} < s[0] = {S.s[0]}` → 第 0 个学生就不够，答案 0（不用二分）'
                                        if S.k < S.s[0] else f'`k = {S.k} ≥ s[0] = {S.s[0]}` → 答案不是 0，需要二分'),
        'l = 0': '要找 `s[i-1] <= k < s[i]` 的 `i`：左端点 `l = 0`',
        'r = len(chalk) - 1': '右端点 `r = {r}`（取模后 `k < s[-1]`，答案一定在范围内）',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，区间还没缩成一个点' if S.l < S.r
                                        else f'`l = r = {S.l}`：区间缩成一点，找到了'),
        'mid = ': '取中点 `mid = ({l} + {r}) >> 1 = {mid}`',
        'if s[mid] > k': lambda S, B, r: (f'`s[{S.mid}] = {S.s[S.mid]} > k = {S.k}` → 第 {S.mid} 个学生用完前粉笔就没了，答案在左半（含 mid）'
                                          if S.s[S.mid] > S.k else f'`s[{S.mid}] = {S.s[S.mid]} ≤ k = {S.k}` → 他还够用，答案在 mid 右边'),
        'r = mid': '`r = mid` → =={r}==（mid 本身可能就是答案，不能 -1）',
        'l = mid + 1': '`l = mid + 1` → =={l}==',
        'return l': '`s[{l}-1] <= k < s[{l}]`，学生 =={l}== 需要补充粉笔',
    },
    cards=dict(
        one_liner='整轮取模后，前缀和里二分找第一个超过 k 的位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['学生按编号轮流答题，第 `i` 个用 `chalk[i]` 支粉笔',
                 '剩余粉笔严格少于所需就要补充，返回这个学生的编号',
                 '本视频：`chalk=[5,1,5,2,3,4], k=47` → `2`'],
        quote='题目实际上就是要找到一个i，满足s[i - 1] <= k < s[i]，于是在这里可以先将前缀和全部计算出来，然后在其中二分取模后的k。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `k` 对整轮消耗取模：多余的整轮不影响谁先不够',
              '前缀和 `s[i]` 是学生 `i` 答完后的总消耗，答案是第一个 `s[i] > k` 的 `i`',
              '前缀和单调递增，所以可以二分；`k < s[0]` 时答案就是 0'],
        summary=['时间 `O(n)`（前缀和）+ `O(log n)`（二分），空间 `O(n)`',
                 '二分是「找第一个 `s[mid] > k`」：`s[mid] > k` 时 `r = mid`，否则 `l = mid + 1`',
                 '易错点：先取模再比较；`k < s[0]` 的情形原文单独处理',
                 '对比灵神：灵神一边累加一边扣减，省掉前缀和数组与二分'],
    ),
)
