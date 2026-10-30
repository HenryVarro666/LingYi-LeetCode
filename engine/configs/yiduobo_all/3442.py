CONFIG = dict(
    num=3442, title='奇偶频次间的最大差值 I', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表计数 + 遍历找奇偶极值', tags=[],
    code='''
class Solution(object):
    def maxDifference(self, s):
        
        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        max_odd = None
        min_even = None
        for char in cnt:
            if cnt[char] % 2 == 1:
                if max_odd is None or max_odd < cnt[char]:
                    max_odd = cnt[char]
            else:
                if min_even is None or min_even > cnt[char]:
                    min_even = cnt[char]
        
        return max_odd - min_even
''',
    call='Solution().maxDifference("aaaaabbcc")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s', cell=80, h=140,
             pointers={}, color=lambda S, i, v: 'blue' if S.get('char') == v and 'cnt' in S and 'max_odd' not in S else None),
        dict(type='map', var='cnt', label='cnt（字母 → 出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"最多的奇数次 ==`{S['max_odd']}`==，最少的偶数次 ==`{S['min_even']}`==" if 'max_odd' in S else '')),
    ],
    watch=['char', 'max_odd', 'min_even'],
    captions={
        'cnt = {}': '用哈希表 `cnt` 统计每个字符出现的次数',
        'cnt[char] = cnt.get': '`{char}` 出现次数 → {cnt[char]}',
        'max_odd = None': '`max_odd` 记录出现==奇数次==里最多的次数，先空着',
        'min_even = None': '`min_even` 记录出现==偶数次==里最少的次数，先空着',
        'if cnt[char] % 2 == 1': '`{char}` 出现 `{cnt[char]}` 次，{"是奇数" if cnt[char] % 2 == 1 else "是偶数"} → {"归入 a 的候选" if cnt[char] % 2 == 1 else "归入 b 的候选"}',
        'if max_odd is None': '还没有奇数候选，或 `{cnt[char]}` 比当前 `{max_odd}` 更大吗？ → {"是，要更新" if (B.max_odd is None or B.max_odd < cnt[char]) else "否，保持"}',
        'max_odd = cnt[char]': '`max_odd` 更新为 =={max_odd}==',
        'if min_even is None': '还没有偶数候选，或 `{cnt[char]}` 比当前 `{min_even}` 更小吗？ → {"是，要更新" if (B.min_even is None or B.min_even > cnt[char]) else "否，保持"}',
        'min_even = cnt[char]': '`min_even` 更新为 =={min_even}==',
        'return max_odd': '差值最大 = 最多奇数次 − 最少偶数次 = `{max_odd} - {min_even}` = =={ret}==',
    },
    cards=dict(
        one_liner='a 取奇数次里最多的，b 取偶数次里最少的',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['字符串 `s`，选出现奇数次的 `a`、出现偶数次的 `b`，求 `a 的次数 - b 的次数` 的最大值',
                 '题目保证两类字符都至少有一个',
                 '本视频：`"aaaaabbcc"` → `5 - 2 = 3`'],
        quote='为了使得差值最大，那么就应该取出现次数为奇数中次数最多的字符作为a，同时取出现次数为偶数中次数最少的字符作为b',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟遍历：用哈希表 `cnt` 数出每种字符的次数',
              '第二趟遍历哈希表：奇数次的更新 `max_odd`，偶数次的更新 `min_even`',
              '两个变量初值用 `None`，所以每次先判空再比较'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '`None` 初值要先判断 `is None`，不能直接比较大小',
                 '偶数候选只来自 `cnt` 里出现过的字符，次数至少为 2',
                 '对比灵神：灵神用 `Counter` 加生成器一行取极值，yiduobo 手写两趟循环'],
    ),
)
