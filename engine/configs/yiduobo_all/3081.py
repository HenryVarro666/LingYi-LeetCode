CONFIG = dict(
    num=3081, title='替换字符串中的问号使分数最小', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='排序 + 逐档拉平次数',
    tags=['常用数据结构', '贪心与思维', '难度分 1905'],
    code='''
class Solution(object):
    def minimizeStringValue(self, s):

        freq = [0] * 26
        r = 0
        for char in s:
            if char == '?':
                r += 1
            else:
                freq[ord(char) - 97] += 1
        
        rank = sorted(range(26), key=lambda d:(freq[d], d))

        p = 1  
        for index in range(25):
            diff = (freq[rank[index + 1]] - freq[rank[index]]) * (index + 1)
            if diff <= r:
                r -= diff
                p += 1
            else:
                break
        
        v = freq[rank[p - 1]] + r // p
        r %= p

        res = []
        cnt = 0
        x = 0
        for char in s:
            if char == '?':
                if cnt < r:
                    bound = v + 1
                else:
                    bound = v
                
                while freq[x] >= bound:
                    x += 1
                
                res.append(chr(x + 97))
                freq[x] += 1
                if freq[x] == bound:
                    x += 1
                    cnt += 1
                
            else:
                res.append(char)

        return ''.join(res)
''',
    call='Solution().minimizeStringValue("a?a?b?")',
    expect='acadbe',
    views=[
        dict(type='string', var=lambda S: ''.join(S['res']) + S['s'][len(S['res']):] if 'res' in S else S['s'], label='字符串（左边是已填好的部分）', h=150),
        dict(type='array', var='freq', label='freq（a~z 各出现几次）', cell=36, index=False, h=150,
             pointers={'x': 'pink'}),
        dict(type='text', fn=lambda S: (f'`p = {S["p"]}`：最少的前 p 个字母（按次数、字母序）已被拉平；剩 `r = {S["r"]}` 个问号' if 'p' in S else '先按（次数, 字母）排序，从最少的字母开始补'), size=24, h=90),
    ],
    watch=['r', 'p', 'v', 'cnt', ('x', 'x', 'pink')],
    skip=[5, 6, 7, 15, 16, 18, 19, 21, 26, 27, 28, 29, 30, 32, 34, 39, 42, 43, 46],
    captions={
        'freq[ord(char) - 97] += 1': '统计已有字母：`{char}` 出现 =={freq[ord(char) - 97]}== 次',
        'r += 1': '问号个数 `r = {r}`',
        'rank = sorted': '按（次数, 字母）排序：次数少的先补；==次数相同时字母靠前的先补，保证字典序最小==',
        'p = 1': '`p` = 已被拉平的字母个数，先是 1（只有最少的那个）',
        'if diff <= r': '{"最少的 `" + str(index + 1) + "` 个字母次数相同，不用花问号" if diff == 0 else "把前 `" + str(index + 1) + "` 个字母抬到下一档要 `" + str(diff) + "` 个问号，剩 `r = " + str(r) + "` 个 → " + ("==够，花掉继续抬==" if diff <= r else "==不够，停在这一档==")}',
        'p += 1': '前 `{p}` 个字母次数一样了',
        'v = freq': '剩下的 `r` 平均分给 `p = {p}` 个字母：目标次数 `v = {freq[rank[p-1]]} + {r}//{p}` = =={v}==',
        'r %= p': '除不尽的余数 `r = {r}`：==字母序最小的 r 个字母再多 1 次==',
        'if cnt < r': '已给 `{cnt}` 个字母多 1 次的名额，共 `r = {r}` 个：{"==还有名额==，目标是 v+1，即 " + str(v + 1) if cnt < r else "名额用完，目标是 v，即 " + str(v)}',
        'while freq[x] >= bound': '字母 `{chr(97 + x)}` 次数 `{freq[x]}` ≥ 目标 `{bound}`？{"==是，换下一个字母==" if freq[x] >= bound else "否，可以用它"}',
        'x += 1': '`x` → `{x}`（字母 `{chr(97 + x) if x < 26 else "-"}`）',
        'freq[x] += 1': '用字母 `{chr(97 + x)}` 填这个问号，它的次数变成 `{freq[x]}`',
        'if freq[x] == bound': '`{chr(97 + x)}` 到目标 `{bound}` 了吗？{"==到了，x 后移，名额 cnt+1==" if freq[x] == bound else "还没到，下一个问号继续用它"}',
        'res.append(char)': '不是问号，原样放入',
    },
    cards=dict(
        one_liner='每个问号补给当前出现次数最少的字母',
        complexity='时间 `O(n + 26 log 26)`，空间 `O(26)`',
        problem=['字符串 `s` 由小写字母和 `?` 组成，`cost(i)` = `t[i]` 之前相同字母的个数',
                 '把 `?` 全换成小写字母，使总分最小；分数相同取字典序最小',
                 '示例：`s="a?a?"` → `"abac"`'],
        quote='若 char 最终出现的次数为 freq[char]，那么 char 提供的分数就是 freq[char]×(freq[char]−1)/2。为了使得最终的分数最小，那么就应该将问号变为当前出现次数最少的字符。',
        quote_src='—— yiduobo 题解',
        idea=['证明：两个字母 x、y，`freq[x] < freq[y]`，补给 x 比补给 y 的分数差 `freq[x]-freq[y] < 0`',
              '排序后逐档分配：先把最少的抬到和第二少一样，再两个一起抬……',
              '问号不够抬下一档时，剩余平均分给这 p 个字母，余数给字母序靠前的'],
        summary=['时间 `O(n + 26 log 26)`，空间 `O(26)`',
                 '排序要用 `(次数, 字母)` 两个关键字，否则字典序不是最小',
                 '填字符时从左到右，每个字母到目标次数就让 `x` 后移',
                 '原文为 Python 2 写法，`r / p` 是整数除法，已改为 `r // p`'],
    ),
)
