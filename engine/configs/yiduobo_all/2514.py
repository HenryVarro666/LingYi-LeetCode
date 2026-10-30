def _txt(S):
    if 'res' not in S:
        return '每个单词独立：`res` 累乘 word_len!，`divide` 累乘各字母次数的阶乘'
    return f"`res` = =={S['res']}==　`divide` = =={S['divide']}==　（答案 = res × divide^(mod−2)）"


CONFIG = dict(
    num=2514, title='统计同位异构字符串数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='阶乘预处理 · 快速幂求逆元',
    tags=['灵神题单', '数学算法', '难度分 2070'],
    code='''
class Solution(object):
    def countAnagrams(self, s):

        mod = 10 ** 9 + 7

        def quickPow(base, k):
            if k == 1:
                return base
            
            p = quickPow(base, k // 2)
            p *= p
            if k & 1:
                p *= base
            
            return p % mod

        res = 1
        divide = 1
        fac_len = 1
        fac = [1]
        for word in s.split(' '):
            word_len = len(word)
            cnt = {}
            for char in word:
                cnt[char] = cnt.get(char, 0) + 1
            
            if word_len >= fac_len:
                for index in range(fac_len, word_len + 1):
                    fac.append(fac[-1] * index % mod)
                fac_len = word_len + 1
            
            res *= fac[word_len]
            res %= mod

            for char in cnt:
                divide *= fac[cnt[char]]
                divide %= mod

            
        return res * quickPow(divide, mod - 2) % mod
''',
    call='Solution().countAnagrams("too hot")',
    expect=18,
    views=[
        dict(type='array', var='fac', label='fac[i] = i!（按需增长）', cell=110, h=170),
        dict(type='map', var='cnt', label='cnt：当前单词的字母次数', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', h=100, size=28, fn=_txt),
        dict(type='calls', h=150),
    ],
    watch=[('word', 'word'), ('word_len', 'word_len', 'blue'), ('res', 'res', 'green'), ('divide', 'divide', 'orange')],
    captions={
        'mod = ': '结果对 `{mod}` 取模',
        'def quickPow': '定义快速幂：求 `base^k % mod`，一会儿用来求逆元',
        'res = 1': '`res` 存各单词 `word_len!` 的乘积',
        'divide = 1': '`divide` 存去重要除的 ∏ `次数!`（先攒着，最后统一求逆元）',
        'fac_len = 1': '`fac[i]` 是 `i!`，只在需要时往后补',
        'for word in s.split': lambda S, B, r: ('所有单词都处理完了' if 'word' in B and B.word == S.word
                                                else f'单词之间互不相关 → 乘法原理，逐个处理 `{S.word!r}`'),
        'word_len = len': '这个单词长 `{word_len}`，全排列有 `{word_len}!` 种',
        'cnt = {}': '统计这个单词里每个字母出现几次',
        'for char in word': lambda S, B, r: ('这个单词的字母数完了' if sum(S.cnt.values()) == len(S.word)
                                             else f'看字母 `{S.char!r}`'),
        'cnt[char] =': '`cnt[{char!r}] = {cnt[char]}`',
        'if word_len >= fac_len': lambda S, B, r: (f'`fac` 只算到 `{S.fac_len - 1}!`，不够 `{S.word_len}!` → 补' if S.word_len >= S.fac_len
                                                   else f'`fac` 已经够用，不用补'),
        'for index in range(fac_len': lambda S, B, r: ('补完了' if len(S.fac) - 1 == S.index
                                                       else f'补阶乘：`fac[{S.index}] = fac[{S.index - 1}] × {S.index}`'),
        'fac.append': '`fac` = `{fac}`',
        'fac_len = word_len': '`fac` 现在算到 `{word_len}!`',
        'res *= fac': '`res` × `{word_len}!` = `{fac[word_len]}`',
        'res %= mod': '取模 → `res = {res}`',
        'for char in cnt': lambda S, B, r: ('这个单词处理完毕' if B.get('char') == S.char and B.get('_line') != 28
                                            else f'字母 `{S.char!r}` 出现 `{S.cnt[S.char]}` 次，重复的排列要除掉 `{S.cnt[S.char]}!`'),
        'divide *= fac': '`divide` 先乘上 `{cnt[char]}!` = `{fac[cnt[char]]}`（不直接除，免得取模后不能整除）',
        'divide %= mod': '取模 → `divide = {divide}`',
        'if k == 1': '快速幂：`k = {k}`，{"到底了，返回 base" if k == 1 else "继续折半"}',
        'p = quickPow': '递归：先算一半的幂 `quickPow(base, k // 2)`',
        'p *= p': '平方 → `{p}`',
        'if k & 1': '`k = {k}` 是{"奇数，还要再乘一个 base" if k & 1 else "偶数，不用再乘"}',
        'p *= base': '再乘一个 `base`',
        'return p % mod': '返回 `{p % mod}`',
        'return res *': '`divide` 的逆元 = `divide^(mod−2)`（费马小定理），用快速幂算：`{divide}` 的 `{mod - 2}` 次方',
    },
    max_steps=75,
    cards=dict(
        one_liner='排列数 / 重复数：分子分母各攒一个变量，最后求一次逆元',
        complexity='时间 `O(n + log mod)`，空间 `O(n)`',
        problem=['单词内字母可任意重排，单词位置不变，求不同的同位异构字符串数（对 `10^9+7` 取模）',
                 '示例：`"too hot"` → `18`',
                 '`"aa"` → `1`'],
        quote='为了避免重复的计算，可以先将单词长度的阶乘和去重时除以单个字符串出现次数的阶乘分别使用两个变量累乘起来并取模，然后对去重用的这个乘积计算乘法逆元。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词互不相关，每个单词的方案数相乘',
              '长 `L` 的单词：`L!` 除以每种字母 `次数!`',
              '用 `fac` 数组缓存阶乘，`res` 累乘分子，`divide` 累乘分母',
              '最后 `divide^(mod-2)` 就是逆元'],
        summary=['时间 `O(n + log mod)`，空间 `O(max_len)`',
                 '原文为 Python 2 写法，`quickPow` 里的 `k / 2` 已改为 `k // 2`',
                 '取模后不能直接除，必须用乘法逆元',
                 '`quickPow` 递归到 `k == 1`，所以 `k` 不能为 0',
                 '对比灵神：灵神把 `i` 和 `cnt[c]` 当乘数在循环里直接累乘，不用阶乘数组'],
    ),
)
