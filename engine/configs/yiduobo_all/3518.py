def _txt(S):
    p = S.get('p')
    if p is None:
        return '逐位填前半段：每一位从 a 到 z 试，`calc` 算出剩下字符的排列数 `tot`'
    ch = chr(S['index'] + 97) if 'index' in S else '?'
    tot = S.get('tot')
    s = f'第 `{p}` 位试填 `{ch}`，剩 `k = {S["k"]}`'
    if tot is not None:
        s += f'；剩余排列数 `tot = {tot}`'
    return s


CONFIG = dict(
    num=3518, title='最小回文排列 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='逐位填充 · 选位置法算排列数',
    tags=['组合数学', '难度分 2375'],
    code='''
class Solution(object):
    def smallestPalindrome(self, s, k):
        
        n = len(s)
        cnt = [0] * 26
        for char in s[:n // 2]:
            cnt[ord(char) - 97] += 1
        
        def calc(cnt, length):
            tot = 1
            for index in range(26):
                if cnt[index] > 0:
                    t = min(cnt[index], length - cnt[index])
                    for x in range(1, t + 1):
                        tot = tot * (length - x + 1) // x
                        if tot >= k:
                            return k
                    length -= cnt[index]
            
            return tot

        left = []
        for p in range(n // 2):
            choose = None
            for index in range(26):
                if cnt[index] == 0:
                    continue

                cnt[index] -= 1
                tot = calc(cnt, n // 2 - p - 1)
                if tot >= k:
                    choose = index
                    break
                
                k -= tot
                cnt[index] += 1

            if choose is None:
                return ""
            else:
                left.append(chr(choose + 97))

        for index in range(26):
            if cnt[index] > 0:
                left.append(chr(index + 97))
                break

        left = ''.join(left)
        right = left[::-1]
        mid = ''
        if n % 2 == 1:
            mid = s[n // 2]
        return left + mid + right
''',
    call="Solution().smallestPalindrome('aabbcbbaa', 5)",
    expect='babacabab',
    skip=['continue', 'if cnt[index] == 0', 'if cnt[index] > 0', 'for index in range(26)', 'for x in range', 'n = len(s)',
          'for char in', 'choose = None', 'cnt[ord(char)', 'break', 'tot = 1', 'length -= cnt'],
    max_steps=75,
    views=[
        dict(type='string', var='s', label='s（回文，只排前半段）', h=130, cell=60),
        dict(type='array', var='cnt', label='cnt：还没用掉的字符个数（下标 0=a, 1=b, …）', h=165, cell=34, pointers={'index': 'pink'},
             color=lambda S, i, v: 'blue' if v else None, dim=lambda S, i, v: v == 0),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='left', label='left：前半段已填的字符', h=130, cell=70),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'pink'), ('tot', 'tot', 'green'), ('k', 'k', 'yellow')],
    captions={
        'cnt = [0] * 26': '`cnt` 统计前半段每个字母出现几次',
        'tot = tot * (length - x + 1) // x': '选位置法：`tot` 乘 `{length - x + 1}` 再除 `{x}` → {tot}（C(length, t) 一点点累乘）',
        16: lambda S, B, r: (f'`tot = {S.tot} ≥ k = {S.k}`：已经够 k 个，不必再算，==直接返回 k==' if S.tot >= S.k
                                         else f'`tot = {S.tot} < k = {S.k}`，继续累乘'),
        'return k': '`tot` 已经 ≥ k：不用再算，直接返回 `k` 表示「够了」',
        'return tot': '剩余字符一共能排出 `{tot}` 种',
        't = min(': '`C(length, t)` 取 `t = min(个数, length − 个数)`，保证越乘越大、不用高精度',
        'for p in range': lambda S, B, r: (f'填前半段第 `{S.p}` 位' if S.p != B.get('p') else '前半段 4 位都填完了'),
        'cnt[index] -= 1': '先假设这一位填 `{chr(index + 97)}`，用掉一个',
        'tot = calc(': '算剩下 `{n // 2 - p - 1}` 个位置、剩余字符能排出的方案数：`tot` = =={tot}==',
        31: lambda S, B, r: (f'`tot = {S.tot} ≥ k = {S.k}` → ==这一位就是 {chr(S.index + 97)}==' if S.tot >= S.k
                                         else f'`tot = {S.tot} < k = {S.k}`：填它的方案都排在第 k 小之前'),
        'k -= tot': '跳过这 `{tot}` 种：`k -= {tot}` → =={k}==，把字符放回，试下一个字母',
        'cnt[index] += 1': '把 `{chr(index + 97)}` 放回 `cnt`',
        'left.append(chr(choose + 97))': '确定第 `{p}` 位 = `{chr(choose + 97)}`，`left` = {left}',
        'return ""': '所有字符都试过仍找不到 → 不足 k 个，返回空串',
        "left = ''.join": '前半段 `{left}`；翻转得到后半段',
        'return left + mid': '前半段 + 中间字符 + 翻转 = =={ret}==',
    },
    cards=dict(
        one_liner='像康托展开：逐位填，用「剩下字符的排列数」决定填谁',
        complexity='时间 `O(n·26·(26+log k))`，空间 `O(n)`',
        problem=['给回文串 `s` 和 `k`，求字典序第 `k` 小的回文排列，没有就返回空串',
                 '只需排前半段，后半段是它的翻转，奇数长度再夹一个中间字符',
                 '示例：`s = "aabbcbbaa", k = 5` → `"babacabab"`'],
        quote='这样一来，就避开了高精度的计算。……如果已经大于等于k了，那么就不需要继续向下计算了，直接返回可以填充的信号就可以了。',
        quote_src='—— yiduobo 题解原文',
        idea=['每位从 a 到 z 试填：剩余排列数 `tot ≥ k` 就定下这一位，否则 `k -= tot` 看下一个',
              '排列数用「选位置法」：从 length 个位置选 t 个放某字母，C(length, t) 依次相乘',
              'k 最大 10^6，累乘中途一旦 `≥ k` 就返回，不会溢出'],
        summary=['原文本来就是整数除法 `//`，代码无需改动',
                 '`t = min(cnt, length - cnt)` 让组合数每一步都变大，提前退出才成立',
                 '某位所有字母都试完没找到 → 返回空串（`k` 太大）',
                 '对比灵神：灵神倒着填、用公式一次推导排列数，这里是每位从头重算'],
    ),
)
