def _tgt_txt(S):
    if 'limit' not in S:
        return '目标：问号补完后，26 种字母的次数要==尽量接近==（均值不等式）'
    if 'target' not in S:
        return f'`limit = {S["limit"]}`：次数小于它的字母都补到 `limit`；多出 `extra = {S["extra"]}` 个问号再各多给 1 个'
    return f'`target` = 补完后每种字母的次数；当前填到字母 `{chr(97 + S["j"]) if "j" in S and S["j"] < 26 else "-"}`'


CONFIG = dict(
    num=3081, title='替换字符串中的问号使分数最小', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='均值不等式 · 贪心分配次数',
    tags=['常用数据结构', '贪心与思维', '难度分 1905'],
    code='''
class Solution:
    def minimizeStringValue(self, s: str) -> str:
        freq = [0] * 26
        for c in s:
            if c != '?':
                freq[ord(c) - ord('a')] += 1

        f = sorted(freq) + [inf]  # 哨兵
        q = s.count('?')
        for i in count(1):
            need = i * (f[i] - f[i - 1])
            if q <= need:
                limit, extra = f[i - 1] + q // i, q % i
                break
            q -= need

        target = freq.copy()
        for i in range(26):
            if target[i] > limit:
                continue
            target[i] = limit
            if extra:  # 还可以多分配一个
                extra -= 1
                target[i] += 1

        ans = list(s)
        j = 0
        for i, c in enumerate(ans):
            if c != '?':
                continue
            while freq[j] == target[j]:
                j += 1
            freq[j] += 1
            ans[i] = ascii_lowercase[j]
        return ''.join(ans)
''',
    call='Solution().minimizeStringValue("a?a?b?")',
    expect='acadbe',
    setup='from itertools import count\nfrom string import ascii_lowercase',
    views=[
        dict(type='string', var=lambda S: ''.join(S['ans']) if 'ans' in S else S['s'], label='字符串（? 逐个被替换）', h=150,
             color=lambda S, i, v: 'green' if 'ans' in S and S['s'][i] == '?' and S['ans'][i] != '?' else None),
        dict(type='array', var='freq', label='freq（a~z 各出现几次）', cell=36, index=False, h=150,
             pointers={'j': 'pink'}),
        dict(type='array', var=lambda S: S.get('target'), label='target（补完后各自应有的次数）', cell=36, index=False, h=130),
        dict(type='text', fn=_tgt_txt, size=24, h=90),
    ],
    skip=[4, 5, 10, 11, 14, 15, 18, 19, 20, 21, 22, 23, 28, 29, 30],
    watch=['q', 'limit', 'extra', ('j', 'j', 'pink')],
    captions={
        'freq[ord(c) - ord': '统计已有字母：`{c}` 出现了 =={freq[ord(c) - ord("a")]}== 次',
        'f = sorted(freq)': '次数从小到大排序，末尾放哨兵 `inf` → ==好找“把最小的几个拉平到哪一档”==',
        'q = s.count': '一共有 `{q}` 个问号可以分配',
        'if q <= need': '{"最小的 `" + str(i) + "` 个字母次数相同，不用花问号" if need == 0 else "把最小的 `" + str(i) + "` 个字母抬到 `" + str(f[i]) + "` 次要 `" + str(need) + "` 个问号，剩 `" + str(q) + "` 个 → ==不够用 `" + str(need) + "` 个，停在这一档==" if q <= need else "把最小的 `" + str(i) + "` 个字母抬到 `" + str(f[i]) + "` 次要 `" + str(need) + "` 个，剩 `" + str(q) + "` 个，够用，继续"}',
        'limit, extra =': '均分：`limit = {f[i-1]} + {q}//{i}` = =={limit}==，多出 `extra = {q} % {i}` = =={extra}== 个再各多给 1',
        'target = freq.copy': 'target 先抄一份现有次数',
        'if target[i] > limit': '字母 `{chr(97 + i)}` 次数 `{target[i]}` > `limit {limit}` → ==不补，保持原样==' ,
        'target[i] = limit': '字母 `{chr(97 + i)}` 补到 `limit = {limit}`',
        'if extra:': '还有 `extra = {extra}` 个多余名额？字母靠前先得 → 字典序最小',
        'target[i] += 1': '字母 `{chr(97 + i)}` 先补到 `limit = {limit}`，再领一个多余名额 → =={target[i]}== 次（靠前先领）',
        'while freq[j] == target[j]': '字母 `{chr(97 + j)}` 已经到目标了吗？`{freq[j]}` vs `{target[j]}`',
        'j += 1': '到目标了 → ==换下一个字母== `{chr(97 + j)}`',
        'freq[j] += 1': '用字母 `{chr(97 + j)}` 填这个问号，次数变成 `{freq[j]}`',
        'ans[i] = ascii': '第 `{i}` 位的 `?` 换成 =={ascii_lowercase[j]}==：从左到右填，字典序最小',
    },
    cards=dict(
        one_liner='次数尽量均匀，再从左往右填最小字母',
        complexity='时间 `O(n + 26 log 26)`，空间 `O(26)`',
        problem=['字符串 `s` 含小写字母和 `?`；`cost(i)` = `t[i]` 之前出现过几次相同字母',
                 '把所有 `?` 换成小写字母，使总分最小；分数相同取字典序最小',
                 '示例：`s="a?a?"` → `"abac"`'],
        quote='字母 i 对 res 的贡献就是 1+2+⋯+(freq[i]−1)=freq[i](freq[i]−1)/2。由基本不等式可知，要使 res 尽量小，这 26 种字母的出现次数应当尽量接近。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总分 = 各字母 `freq×(freq-1)/2` 之和 → ==次数越均匀越小==',
              '找最小的 `limit`，把次数小于它的字母都补到 `limit`，余下 `extra` 个给靠前的字母',
              '再扫一遍 `s`，让 `freq` 追上 `target`，从 a 开始填，保证字典序最小'],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
                 '方法一：最小堆每次取次数最少的字母，再排序，`O(n log n)`',
                 '易错：同次数时字母靠前的先拿 `extra`；问号按位置从左到右填',
                 '`inf` 哨兵让最后一档也能停下'],
    ),
)
