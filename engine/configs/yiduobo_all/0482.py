CONFIG = dict(
    num=482, title='密钥格式化', difficulty='Easy', category='字符串',
    author='yiduobo', technique='去破折号 + 一趟扫描分组',
    code='''
class Solution(object):
    def licenseKeyFormatting(self, S, K):

        S = S.replace('-', '')
        l = len(S)
        cnt = l % K
        if cnt > 0:
            cnt = K - cnt
        
        res = ''
        for index in range(len(S)):
            char = S[index]
            if char >= 'a':
                char = chr(ord(char) - 32)
            res += char
            cnt += 1
            if cnt == K:
                if index != len(S) - 1:
                    res += '-'
                cnt = 0
        
        return res
''',
    call="Solution().licenseKeyFormatting('2-5g-3-J', 2)",
    expect='2-5G-3J',
    views=[
        dict(type='string', var='S', label='S（去掉 - 之后）', h=230, pointers={'index': 'blue'}),
        dict(type='text', fn=lambda S: f"本组已有 `cnt = {S['cnt']}` 个字符，满 `K = {S['K']}` 个就加 `-`" if 'cnt' in S else '', size=32, h=70),
        dict(type='text', fn=lambda S: f"res = `'{S['res']}'`" if 'res' in S else '', size=40, h=90),
    ],
    watch=[('K', 'K', 'orange'), 'cnt', 'char', ('res', 'res', 'green')],
    captions={
        "S = S.replace": '先去掉所有破折号，只剩字符：`S = {S!r}`',
        'l = len(S)': '字符总数 `l = {l}`',
        'cnt = l % K': '`{l} % {K}` = `{cnt}`：这就是==第一组==的长度（0 表示每组都满）',
        'cnt = K - cnt': '第一组只有 `{B.cnt}` 个字符，所以让 `cnt` 预先等于 `K - {B.cnt}` = =={cnt}==：再来 `{B.cnt}` 个字符就满 K 个',
        'if char >= ': lambda S, B, r: (f"`{S.char!r} >= 'a'` 成立：是小写字母，要转成大写" if S.char >= 'a' else f"`{S.char!r} >= 'a'` 不成立：是数字或大写，原样保留"),
        'char = chr(': '小写转大写：ASCII 码减 32 → `{char!r}`',
        'res += char': '把 `{char!r}` 接到结果后面：`res = {res!r}`',
        'cnt += 1': '本组字符数 +1 → `cnt = {cnt}`',
        'if cnt == K': lambda S, B, r: (f'`cnt = {S.cnt} == K = {S.K}`：这一组满了' if S.cnt == S.K else f'`cnt = {S.cnt} < K = {S.K}`：本组还没满，继续'),
        'if index != len(S) - 1': lambda S, B, r: (f"`index = {S.index}`，最后一个下标是 `{len(S.S) - 1}`：不是最后一个 → 要加 `-`" if S.index != len(S.S) - 1 else f"`index = {S.index}` 已经是最后一个字符：==末尾不能多出破折号==，不加"),
        "res += '-'": '加破折号：`res = {res!r}`',
        'cnt = 0': '开始下一组，`cnt` 清零',
        'return res': '格式化完成：`{res!r}`',
    },
    cards=dict(
        one_liner='先算出第一组的长度，再一趟扫描，满 K 个就加破折号',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `S` 由字母、数字和破折号组成，整数 `K`',
                 '去掉原有破折号，每 `K` 个字符一组，用 `-` 连接，==小写转大写==',
                 '只有第一组可以比 `K` 短（但不能为空）',
                 '本视频：`S = "2-5g-3-J"`，`K = 2` → `"2-5G-3J"`'],
        quote='去掉字符串中的破折号之后，计算字符串的长度以及第一段的长度，然后一趟扫描逐个处理每个字符即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 `l`，`l % K` 就是第一段的长度（为 0 表示每段都是 K）',
              '用 `cnt` 记录当前组“算上预填”的字符数，开头预填 `K − 第一组长度`',
              '每放一个字符 `cnt += 1`，到 `K` 就加 `-` 并清零，最后一个字符后不加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`l % K` 为 0 时 `cnt` 保持 0，第一组也是满的 K 个',
                 '最后一个字符后面不能加破折号，要判断 `index != len(S) - 1`',
                 '小写转大写用 `ord - 32`，只对字母有效，数字小于 `a` 不会被改',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改'],
    ),
)
