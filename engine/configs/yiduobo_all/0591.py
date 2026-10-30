CONFIG = dict(
    num=591, title='标签验证器', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='一趟扫描 · 标签栈',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def isValid(self, code):

        l = len(code)
        pos = 0
        stack = []
        tag_flag = False
        if code[0] != '<':
            return False
        while pos < l:
            if not stack and tag_flag:
                return False
            if code[pos] == '<':
                if stack and pos + 1 < l and code[pos + 1] == '!':
                    cdata_right = code.find(']]>', pos + 2)
                    if cdata_right < 0:
                        return False
                    if code[pos + 2: cdata_right].find("[CDATA[") != 0:
                        return False
                    pos = cdata_right + 1
                else:
                    if pos + 1 < l and code[pos + 1] == '/':
                        tag_end = True
                        tag_name_left = pos + 2
                    else:
                        tag_end = False
                        tag_name_left = pos + 1
                    
                    tag_name_right = code.find('>', tag_name_left)
                    if tag_name_right < 0:
                        return False
                    tag_len = tag_name_right - tag_name_left 
                    if tag_len < 1 or tag_len > 9:
                        return False
                    for index in range(tag_name_left, tag_name_right):
                        if code[index] < 'A' or code[index] > 'Z':
                            return False
                    
                    if tag_end:
                        if not stack or stack[-1] != code[tag_name_left:tag_name_right]:
                            return False
                        stack.pop()
                    else:
                        tag_flag = True
                        stack.append(code[tag_name_left:tag_name_right])
                
                    pos = tag_name_right + 1
            else:
                pos += 1

        if stack:
            return False
        return tag_flag
''',
    call='Solution().isValid("<A><B>x</B><![CDATA[y]]></A>")',
    expect=True,
    views=[
        dict(type='string', var='code', label='code（蓝箭头 = 扫描位置 pos）', pointers={'pos': 'blue'}, cell=30, h=150,
             dim=lambda S, i, v: 'pos' in S and i < S['pos'],
             color=lambda S, i, v: 'yellow' if 'tag_name_left' in S and S.get('_line', 0) >= 29 and S['tag_name_left'] <= i < S.get('tag_name_right', -1) else None),
        dict(type='stack', var='stack', label='stack（还没闭合的开始标签，栈顶在右）', fmt=lambda x: f'<{x}>', h=130, font=34),
        dict(type='text', fn=lambda S: (f"tag_flag = `{S['tag_flag']}`（出现过标签）" if 'tag_flag' in S else ''), size=28, h=70),
    ],
    watch=[('pos', 'pos', 'blue'), ('tag_end', 'tag_end', 'pink'), ('tag_name', 'code[tag_name_left:tag_name_right] if tag_name_right >= 0 else None', 'yellow'), ('tag_flag', 'tag_flag', 'green')],
    skip=[4, 35, 36, 5, 11, 26, 30, 32],
    max_steps=90,
    captions={
        6: '`stack` 保存还没闭合的开始标签名，用来处理==标签套娃==',
        7: '`tag_flag`：是否出现过标签，用来拒绝「闭合标签之外还有内容」',
        8: '整段代码必须以 `<` 开头，否则一定不是合法标签',
        10: '`pos = {pos}`，还没扫完 → 继续',
        11: lambda S, B, r: ('栈空且出现过标签：说明最外层标签已闭合，后面还有字符 → ==非法==' if (not S.stack and S.tag_flag)
                             else '栈非空，或还没出现过标签 → 没问题'),
        13: lambda S, B, r: (f"`code[{S.pos}] = '<'` → 可能是标签或 CDATA" if S.code[S.pos] == '<'
                             else f"`code[{S.pos}] = '{S.code[S.pos]}'` 是普通内容字符"),
        14: lambda S, B, r: (f"栈非空且 `<` 后是 `!` → ==CDATA== 段，进去找结尾 `]]>`" if (S.stack and S.code[S.pos + 1] == '!')
                             else '不是 CDATA → 当成起始标签或结束标签'),
        15: '找 CDATA 的结尾 `]]>`：`cdata_right = {cdata_right}`',
        16: '`cdata_right = {cdata_right}`，找到了 → 合法',
        18: lambda S, B, r: ('`<![` 后面必须以 `[CDATA[` 开头 → 符合' if S.code[S.pos + 2:S.cdata_right].find('[CDATA[') == 0 else '不以 `[CDATA[` 开头 → 非法'),
        20: 'CDATA 内容随便写，==整段跳过==：`pos = {pos}`，落在 `]]>` 中间，剩下的 `]>` 当普通字符',
        22: lambda S, B, r: ('`<` 后是 `/` → ==结束标签==' if (S.pos + 1 < len(S.code) and S.code[S.pos + 1] == '/') else '`<` 后不是 `/` → ==起始标签=='),
        23: '`tag_end = True`',
        24: '结束标签 `</` 占两格，标签名从 `pos + 2 = {tag_name_left}` 开始',
        26: '`tag_end = False`',
        27: '起始标签 `<` 占一格，标签名从 `pos + 1 = {tag_name_left}` 开始',
        29: '找第一个 `>`：标签名在 `[{tag_name_left}, {tag_name_right})`，即 `{code[tag_name_left:tag_name_right]}`',
        30: '`tag_name_right = {tag_name_right}`：有 `>` 才算完整标签',
        32: '标签名长度 `tag_len = {tag_len}`',
        33: lambda S, B, r: f'长度必须在 1–9 之间：`{S.tag_len}` → ' + ('合法' if 1 <= S.tag_len <= 9 else '==非法=='),
        39: lambda S, B, r: '是结束标签 → 要和栈顶的开始标签配对' if S.tag_end else '是起始标签 → 要压栈等它的结束标签',
        40: lambda S, B, r: (f"栈顶 `{S.stack[-1]}` 和结束标签 `{S.code[S.tag_name_left:S.tag_name_right]}` 一致 → 配对成功" if S.stack and S.stack[-1] == S.code[S.tag_name_left:S.tag_name_right]
                             else '栈空或标签名对不上 → ==非法=='),
        42: '配对成功，栈顶出栈：`stack = {stack}`',
        44: '`tag_flag = True`：出现过标签了',
        45: '起始标签 `{stack[-1]}` 入栈：`stack = {stack}`',
        47: '标签处理完，`pos` 跳到 `>` 后面：{pos}',
        49: '普通内容字符，直接跳过：`pos` → {pos}',
        51: lambda S, B, r: '扫完了，栈里还有没闭合的标签 → ==非法==' if S.stack else '扫完了，栈是空的：标签都闭合了',
        52: '栈非空 → 返回 `False`',
        53: '栈空，且出现过标签 → 返回 =={tag_flag}==',
    },
    cards=dict(
        one_liner='一趟扫描，遇到标签入栈、闭合标签出栈匹配，CDATA 整段跳过',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断一段代码是否是合法的 XML 风格片段：被一个闭合标签包住，标签名是 1–9 位大写字母',
                 '标签必须成对、嵌套正确；`<![CDATA[...]]>` 里的内容可以是任意字符',
                 '本视频：`"<A><B>x</B><![CDATA[y]]></A>"` → `True`'],
        quote='看着题目描述一大堆，实际上还没有带括号的四则运算难做。对于这类线性的可能出现套娃的字符串处理问题，一般就是一趟扫描判断各种情况，遇到套娃时则交个栈来处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['`<!` 开头：找 `]]>`，中间必须含 `[CDATA[`，合法就==整段跳过==',
              '其他 `<`：找第一个 `>` 取标签名，校验长度和大写；开始标签入栈，结束标签和栈顶配对',
              '用 `tag_flag` 记录出现过标签：栈空后还有字符就是非法'],
        summary=['时间 `O(n)`，空间 `O(n)`：栈深 = 标签嵌套层数',
                 '结束时栈必须为空，且必须出现过标签（`tag_flag`）',
                 '栈空后（最外层闭合后）再出现任何字符都非法；CDATA 只在标签内部才有效',
                 '易错：标签名长度 1–9、只能是大写字母；`]]>` 找不到也算非法'],
    ),
)
