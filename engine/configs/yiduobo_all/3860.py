CONFIG = dict(
    num=3860, title='不同邮件组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='规范化 · 集合去重',
    code='''
class Solution(object):
    def uniqueEmailGroups(self, emails):
        
        emails_set = set()

        for e in emails:
            local, domain = e.split('@')
            local = local.split('+', 1)[0].replace('.', '').lower()
            domain = domain.lower()
            final = local + '@' + domain
            emails_set.add(final)
        
        return len(emails_set)
''',
    call="Solution().uniqueEmailGroups(['A.b+x@Mail.com', 'ab@mail.com', 'a.b@mail.com', 'c@Mail.com'])",
    expect=2,
    views=[
        dict(type='array', var='emails', h=300, cell=230,
             color=lambda S, i, v: 'blue' if 'e' in S and v == S['e'] else None),
        dict(type='set', var='emails_set', h=200, fmt=lambda x: x),
        dict(type='text', fn=lambda S: (f"`{S['e']}` → local `{S['local']}`，domain `{S['domain']}`" if 'domain' in S and 'e' in S else ''), size=30),
    ],
    watch=['e', 'local', 'domain', 'final'],
    captions={
        'emails_set = set()': '用集合记录不同的邮件组，重复的规范化结果会自动合并',
        "local, domain = e.split('@')": "按 `'@'` 拆开：本地名 `{local}`，域名 `{domain}`",
        "local = local.split": "规范化本地名：取第一个 `+` 之前、去掉所有 `.`、转小写 → `{local}`",
        'domain = domain.lower()': '域名只需转小写 → `{domain}`',
        'final = ': '拼回规范邮箱 `{final}`',
        'emails_set.add': lambda S, B, r: (f'`{S.final}` 已在集合里 → 同一组，数量不变' if S.final in B.emails_set
                                          else f'`{S.final}` 是新的一组，加入集合（共 {len(S.emails_set)} 组）'),
        'return len': '不同的规范邮箱共 `{len(emails_set)}` 个 → 答案',
    },
    cards=dict(
        one_liner='把每个邮箱规范化，再用集合数有几种',
        complexity='时间 `O(L)`（`L` 为所有邮箱总长度），空间 `O(L)`',
        problem=['规范化：本地名（`@` 前）忽略所有 `.`，忽略第一个 `+` 及之后内容，转小写；域名转小写',
                 '规范化结果相同的邮箱算同一组，求组数',
                 '本视频：`A.b+x@Mail.com`、`ab@mail.com`、`a.b@mail.com`、`c@Mail.com` → `2`'],
        quote='使用一个集合emails_set记录不同的电子邮件组。先通过\'@\'进行split，得到本地名称local以及域名domain。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个地址先按 `@` 拆成本地名和域名',
              '本地名：`split(\'+\', 1)[0]` 取加号前，`replace` 去点，`lower` 转小写',
              '拼回 `final` 放进集合，集合大小就是组数'],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '`split(\'+\', 1)[0]` 只按第一个加号切，且加号前可以没有加号',
                 '域名里的 `.` 不能去掉，只有本地名才忽略点',
                 '原文代码在 Python 3 下可直接运行，未作改动；题面简报缺失，题意按原文推导整理'],
    ),
)
