def _txt(S):
    if 'ma_f' not in S:
        return ''
    return f"当前最大「次数的次数」`ma = {S['ma']}`，对应次数 `ma_f = {S['ma_f']}`"


CONFIG = dict(
    num=3692, title='众数频率字符', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='两层哈希表计数', tags=[],
    code='''
class Solution(object):
    def majorityFrequencyGroup(self, s):
        
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1
        
        freq_group = {}
        for f in freq.values():
            freq_group[f] = freq_group.get(f, 0) + 1
        
        ma = 0
        ma_f = None
        for f in freq_group:
            if freq_group[f] > ma or (freq_group[f] == ma and f > ma_f):
                ma = freq_group[f]
                ma_f = f
        
        res = []
        for c in freq:
            if freq[c] == ma_f:
                res.append(c)
        
        return ''.join(res)
''',
    call="Solution().majorityFrequencyGroup('pfpfgi')",
    expect='pf',
    views=[
        dict(type='string', var='s', label='s', cell=70, h=130),
        dict(type='map', var='freq', label='freq（字母 → 次数）', fmt=lambda k, v: f"'{k}': {v}", h=190, font=30),
        dict(type='map', var='freq_group', label='freq_group（次数 → 次数的次数）', fmt=lambda k, v: f"{k}: {v}", h=150, font=30),
        dict(type='text', h=60, size=28, fn=_txt),
    ],
    watch=[('c', 'c', 'blue'), ('f', 'f', 'cyan'), ('ma', 'ma', 'green'), ('ma_f', 'ma_f', 'orange'), ('res', 'res', 'pink')],
    captions={
        'freq[c] = ': '字母 `{c}` 的次数加一：`freq[{c!r}] = {freq[c]}`',
        'freq_group[f] = ': '有一个字母出现了 `{f}` 次：`freq_group[{f}] = {freq_group[f]}`（统计「次数的次数」）',
        'ma = 0': '`ma` 记录目前最大的「次数的次数」',
        'ma_f = None': '`ma_f` 记录取得最大值时对应的出现次数',
        'if freq_group[f] > ma': lambda S, B, r: (
            f"比较：出现 `{S.f}` 次的字母有 `{S.freq_group[S.f]}` 个，当前最大 `{S.ma}` 个 → "
            + ('==更大或并列且次数更大==，更新' if (S.freq_group[S.f] > S.ma or (S.freq_group[S.f] == S.ma and S.f > S.ma_f)) else '不够，保持')),
        'ma = freq_group[f]': '`ma` 更新为 `{ma}`',
        'ma_f = f': '`ma_f` 更新为 `{ma_f}`：并列时次数大的优先',
        'if freq[c] == ma_f': '字母 `{c}` 出现 `{freq[c]}` 次，是否等于 `ma_f = {ma_f}` → {"是" if freq[c] == ma_f else "否"}',
        'res.append': '字母 `{c}` 属于众数频率组，加入 `res`：`{res}`',
        'return': '答案：`{ret!r}`',
    },
    cards=dict(
        one_liner='数两次：先数字母次数，再数「次数的次数」',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['出现次数相同的字母组成一个频率组，选字母数最多的组',
                 '并列时取出现次数更大的组，返回其中所有字母',
                 '本视频：`"pfpfgi"` → `"pf"`（频率 2 和 1 的组都有 2 个字母，取 2）'],
        quote='先计算出字符串中每种字符出现的次数，接下来计算出这些次数出现的次数，然后取其中次数的次数最大的那一组。若有多个次数的次数最大，则取对应次数最大的那一组。',
        quote_src='—— yiduobo 题解原文',
        idea=['`freq` 记每个字母的次数；`freq_group` 记每个次数出现了几次',
              '再扫一遍 `freq_group`，取次数的次数最大的，并列取次数大的，记为 `ma_f`',
              '最后扫 `freq`，把次数恰好等于 `ma_f` 的字母收集起来'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '易错：并列时要比 `f > ma_f`，所以三个条件写在同一个 if 里',
                 '`ma_f` 初值 None 不会出错：第一次 `freq_group[f] > 0` 必然成立，短路不会比较 None',
                 '对比灵神：灵神一遍遍历 cnt 就边分组边更新答案；yiduobo 分成四趟，思路更直白'],
    ),
)
