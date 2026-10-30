CONFIG = dict(
    num=929, title='独特的电子邮件地址', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表 + 集合 · 字符串规范化',
    tags=[],
    code='''
class Solution(object):
    def numUniqueEmails(self, emails):

        email_dict = {}
        for email in emails:
            part1, part2 = email.split('@')
            part1 = part1.split('+', 1)[0].replace('.', '')
            if part2 not in email_dict:
                email_dict[part2] = set()
            email_dict[part2].add(part1)
        
        res = 0
        for value in email_dict.values():
            res += len(value)
        
        return res
''',
    call="Solution().numUniqueEmails(['a.b+c@x.com', 'ab@x.com', 'a.b@y.com', 'ab+z@y.com'])",
    expect=2,
    views=[
        dict(type='queue', var='emails', h=200, fmt=lambda x: x),
        dict(type='text', fn=lambda S: f"本地名 `{S['part1']}`　域名 `{S['part2']}`" if 'part2' in S else ''),
        dict(type='map', var='email_dict', h=300, fmt=lambda k, v: f"{k}: {sorted(v) if isinstance(v, set) else v}"),
    ],
    watch=['email', 'part1', 'part2', ('res', 'res', 'green')],
    captions={
        'email_dict = {}': '哈希表：键是域名，值是该域名下不同本地名的集合',
        'for email in emails': '处理邮箱 `{email}`',
        "split('@')": '用 `@` 切开：本地名 `{part1}`，域名 `{part2}`',
        "split('+', 1)": '只保留 `+` 之前，并去掉所有 `.` → 规范本地名 `{part1}`（域名里的点不能去）',
        'not in email_dict': '`{part2}` {"还没出现过" if part2 not in email_dict else "已经有集合了"}，{"先建一个空集合" if part2 not in email_dict else "跳过"}',
        'email_dict[part2] = set()': '为 `{part2}` 新建空集合',
        '.add(part1)': '把 `{part1}` 放进 `{part2}` 的集合，重复的自动去重',
        'res = 0': '`res` 统计不同地址总数',
        'for value in': '看某个域名的集合 `{value}`',
        'res += len': '这个域名下有 `{len(value)}` 个不同本地名 → `res = {res}`',
        'return res': '不同的实际收件地址一共 `{res}` 个',
    },
    cards=dict(
        one_liner='按 @ 拆开，本地名去掉加号后缀与点，再用集合去重',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['邮箱本地名中 `.` 会被忽略，第一个 `+` 之后的内容也会被忽略（域名不受影响）',
                 '求规则化之后，实际收到邮件的不同地址有几个',
                 '本视频：`a.b+c@x.com`、`ab@x.com`、`a.b@y.com`、`ab+z@y.com` → `2`'],
        quote='对于前半部分，只选取\'+\'前面的部分，然后将其中的\'.\'去除掉。再次感叹python处理这类问题太好用了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split(\'@\')` 把地址分成本地名和域名', '本地名：`split(\'+\', 1)[0]` 取加号前，`replace(\'.\', \'\')` 去点',
              '以域名为键、规范本地名集合为值放进哈希表；最后把各集合大小相加'],
        summary=['时间、空间都与总字符数成正比',
                 '点和加号规则只作用于本地名，域名里的 `.` 不能去掉',
                 '`split(\'+\', 1)` 限制只切一次，取 `[0]` 即加号前面部分',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串'],
    ),
)
