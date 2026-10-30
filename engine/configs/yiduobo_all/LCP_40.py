CONFIG = dict(
    num='LCP 40', title='心算挑战', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='奇偶分开 + 前缀和，枚举奇数张数', tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def maxmiumScore(self, cards, cnt):

        odd = []
        even = []
        for num in cards:
            if num % 2 == 0:
                even.append(num)
            else:
                odd.append(num)
        
        even.sort(reverse=True)
        odd.sort(reverse=True)

        even_s = [0]
        for num in even:
            even_s.append(even_s[-1] + num)
        odd_s = [0]
        for num in odd:
            odd_s.append(odd_s[-1] + num)
        
        res = 0
        for odd_cnt in range(0, min(len(odd), cnt) + 1, 2):
            if cnt - odd_cnt > len(even):
                continue

            res = max(res, odd_s[odd_cnt] + even_s[cnt - odd_cnt])
        
        return res
''',
    call='Solution().maxmiumScore([3,6,5,4,1,8], 3)',
    expect=18,
    views=[
        dict(type='array', var=lambda S: S['odd'] if 'odd' in S else [], label='odd（奇数，从大到小）', h=140, color=lambda S, i, v: 'orange'),
        dict(type='array', var=lambda S: S['even'] if 'even' in S else [], label='even（偶数，从大到小）', h=140, color=lambda S, i, v: 'cyan'),
        dict(type='array', var=lambda S: S['odd_s'] if 'odd_s' in S else [], label='odd_s（奇数前缀和）', h=140,
             pointers={'odd_cnt': 'pink'}),
        dict(type='array', var=lambda S: S['even_s'] if 'even_s' in S else [], label='even_s（偶数前缀和）', h=140,
             pointers={'cnt - odd_cnt': 'blue'}),
        dict(type='text', fn=lambda S: (f"奇数 `{S['odd_cnt']}` 张 + 偶数 `{S['cnt']-S['odd_cnt']}` 张" if 'odd_cnt' in S else ''), size=28),
    ],
    skip=['even = []', 'odd = []', 'for num in cards', 'if num % 2', 'even.append(num)', 'odd.append(num)', 'for num in even:', 'for num in odd:', 'even_s = [0]', 'odd_s = [0]', 'even_s.append', 'odd_s.append', 'res = 0'],
    watch=['cnt', ('odd_cnt', 'odd_cnt if "odd_cnt" in dir() else None', 'pink'), ('res', 'res if "res" in dir() else None', 'green')],
    captions={
        'even = []': '奇数、偶数分两堆放',
        'if num % 2 == 0': '`{num}` 是{"偶" if num % 2 == 0 else "奇"}数',
        'even.sort': '偶数从大到小排：`even = {even}`；同奇偶时优先选大的',
        'odd.sort': '奇数从大到小排：`odd = {odd}`；接着各自做前缀和：`odd_s[j]` 就是最大的 j 张奇数之和',
        'even_s.append': '偶数前缀和：`even_s = {even_s}`，`even_s[j]` 是最大的 j 个偶数之和',
        'odd_s.append': '奇数前缀和：`odd_s = {odd_s}`，`odd_s[j]` 是最大的 j 个奇数之和',
        'for odd_cnt in range': '枚举奇数张数 `odd_cnt = {odd_cnt}`（和为偶数 ⇒ 奇数张数是偶数）',
        'if cnt - odd_cnt > len(even)': '需要偶数 `cnt − odd_cnt = {cnt - odd_cnt}` 张，只有 `{len(even)}` 张：{"不够，跳过" if cnt - odd_cnt > len(even) else "够用"}',
        'res = max': '`odd_s[{odd_cnt}] + even_s[{cnt - odd_cnt}] = {odd_s[odd_cnt]} + {even_s[cnt - odd_cnt]}`，`res` = =={res}==',
        'return res': '最大有效得分 =={res}==',
    },
    cards=dict(
        one_liner='和为偶数 ⇒ 奇数张数是偶数：枚举奇数选几张',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['从 `cards` 选 `cnt` 张，数字和是偶数才有效，得分是和',
                 '求最大有效得分，无有效方案返回 `0`',
                 '示例：`[1,2,8,9], cnt=3` → `18`'],
        quote='最终答案一定是由偶数个奇数卡牌以及部分偶数卡牌组成。……枚举最终选择的奇数卡牌数量odd_cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['和是偶数 ⇒ ==选中的奇数一定有偶数张==',
              '奇、偶各自从大到小排，做前缀和',
              '枚举奇数张数 `odd_cnt = 0,2,4…`：取最大的 odd_cnt 个奇数 + 最大的 `cnt-odd_cnt` 个偶数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`odd_cnt` 步长为 2，从 0 开始',
                 '易错：偶数不够 `cnt - odd_cnt` 张时要跳过',
                 '对比灵神：灵神取最大 cnt 个再替换一个；yiduobo 直接枚举奇数张数',
                 '原文为 Python 2 风格，本题代码无需改动（方法名 `maxmiumScore` 为原文拼写）'],
    ),
)
