CONFIG = dict(
    num=1410, title='HTML实体解析器', difficulty='Medium', category='字符串',
    author='yiduobo', technique='逐字符扫描 · 手写匹配实体',
    code='''
class Solution(object):
    def entityParser(self, text):

        res = ''
        n = len(text)
        pos = 0
        while pos < n:
            if text[pos] == '&' and pos + 3 < n:
                if text[pos + 1] == 'q' and pos + 5 < n and text[pos + 5] == ';':
                    if text[pos + 2] == 'u' and text[pos + 3] == 'o' and text[pos + 4] == 't':
                        res += '"'
                        pos += 6
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2
                elif text[pos + 1] == 'a':
                    if pos + 4 < n and text[pos + 4] == ';' and text[pos + 2] == 'm' and text[pos + 3] == 'p':
                        res += '&'
                        pos += 5
                    elif pos + 5 < n and text[pos + 5] == ';' and text[pos + 2] == 'p' and text[pos + 3] == 'o' and text[pos + 4] == 's':
                        res += "'"
                        pos += 6
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2

                elif (text[pos + 1] == 'g' or text[pos + 1] == 'l') and pos + 3 < n and text[pos + 3] == ';':
                    if text[pos + 2] == 't':
                        if text[pos + 1] == 'g':
                            res += '>'
                        else:
                            res += '<'
                        pos = pos + 4
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2

                elif text[pos + 1] == 'f' and pos + 6 < n and text[pos + 6] == ';':
                    if text[pos + 2] == 'r' and text[pos + 3] == 'a' and text[pos + 4] == 's' and text[pos + 5] == 'l':
                        res += '/'
                        pos += 7
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2

                else:
                    res += text[pos]
                    pos += 1

            else:
                res += text[pos]
                pos += 1
        
        return res
''',
    call='Solution().entityParser("a&gt;b &amp; &quot;")',
    expect='a>b & "',
    views=[
        dict(type='string', var='text', label='text（蓝 = 当前扫描位置 pos）', cell=40, pointers={'pos': 'blue'},
             dim=lambda S, i, v: 'pos' in S and i < S['pos'],
             color=lambda S, i, v: 'blue' if S.get('pos') == i else None, h=200),
        dict(type='text', fn=lambda S: f"已还原的结果 `res` = =={S['res']}==" if 'res' in S else '', size=34, h=90),
        dict(type='text', fn=lambda S: (f"从 pos 往后看：`{S['text'][S['pos']:S['pos']+7]}`" if 'pos' in S and S['pos'] < len(S['text']) else ''), size=28, h=80),
    ],
    watch=[('pos', 'pos', 'blue'), ('n', 'n'), ('res', 'res', 'green')],
    captions={
        'res = ': '`res` 存还原后的字符',
        'pos = 0': '`pos` 从 0 开始逐个字符扫描',
        'while pos < n': lambda S, B, r: (f'`pos = {S.pos} < n = {S.n}`，继续扫描' if S.pos < S.n else f'`pos = {S.pos} == n`：扫描完了'),
        "text[pos] == '&' and pos + 3 < n": lambda S, B, r: (f"`text[{S.pos}] = '{S.text[S.pos]}'` 是 `&`，后面还够 3 个字符，可能是实体 → 继续判断" if S.text[S.pos] == '&' and S.pos + 3 < S.n
                                                          else f"`text[{S.pos}] = '{S.text[S.pos]}'` 不是实体开头 → 原样拷贝"),
        "text[pos + 1] == 'q'": lambda S, B, r: f"`&` 后第二个字符是 `{S.text[S.pos+1]}`" + (" → `q`：可能是 `&quot;`（长 6），第 6 位必须是 `;`" if S.text[S.pos+1] == 'q' else " ≠ `q` → 看下一个分支"),
        "text[pos + 2] == 'u'": '逐个核对 `u` `o` `t`，全对才是 `&quot;`',
        "res += '\"'": '识别出 `&quot;` → 追加 `"`，`res` = =={res}==',
        "res += '&'": '识别出 `&amp;` → 追加 `&`，`res` = =={res}==',
        "res += \"'\"": '识别出 `&apos;` → 追加 `\'`',
        "elif text[pos + 1] == 'a'": lambda S, B, r: (f"第二个字符是 `a`：可能是 `&amp;`（长 5）或 `&apos;`（长 6）" if S.text[S.pos+1] == 'a' else f"第二个字符 `{S.text[S.pos+1]}` ≠ `a` → 看下一个分支"),
        "(text[pos + 1] == 'g'": lambda S, B, r: (f"第二个字符是 `{S.text[S.pos+1]}`：可能是 `&gt;` / `&lt;`（长 4），第 4 位必须是 `;`" if S.text[S.pos+1] in 'gl' and S.text[S.pos+3:S.pos+4] == ';' else f"第二个字符 `{S.text[S.pos+1]}` 不满足 `g/l` + `;` → 看下一个分支"),
        "text[pos + 2] == 't'": '第三位是 `t` 才是 `&gt;` / `&lt;`',
        "res += '>'": '`&gt;` → 追加 `>`，`res` = =={res}==',
        "res += '<'": '`&lt;` → 追加 `<`',
        "pos = pos + 4": '`&gt;` 占 4 个字符 → `pos` 跳到 {pos}',
        "pos += 5": '`&amp;` 占 5 个字符 → `pos` 跳到 {pos}',
        "pos += 6": '实体占 6 个字符 → `pos` 跳到 {pos}',
        "pos += 7": '`&frasl;` 占 7 个字符 → `pos` 跳到 {pos}',
        "pos += 2": '不是合法实体：只拷贝 `&` 和下一个字符，`pos` → {pos}',
        "pos += 1": '拷贝一个普通字符，`res` = `{res}`，`pos` → {pos}',
        'return res': '扫描结束，返回 `{res}`',
    },
    cards=dict(
        one_liner='没有花哨算法：逐个字符扫描，遇到 & 就手工判断是哪种实体',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把字符串里的 HTML 实体换回对应字符：`&quot;`→`"`，`&apos;`→`\'`，`&amp;`→`&`，`&gt;`→`>`，`&lt;`→`<`，`&frasl;`→`/`',
                 '不是上述实体的原样保留',
                 '示例：`a&gt;b &amp; &quot;` → `a>b & "`'],
        quote='没有什么复杂算法，但是实现起来比较麻烦的题目。直接逐个字符扫描，判断各种转义的情况即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos` 逐个字符扫描，遇到 `&` 就看后面几个字符',
              '按第二个字符分支：`q` / `a` / `g l` / `f`，再核对剩余字母和结尾的 `;`',
              '匹配成功：追加替换字符，`pos` 跳过整个实体；失败：只拷贝一两个字符继续'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：每次读 `text[pos+k]` 前都要保证不越界（`pos + 3 < n` 等）',
                 '实体长度各不相同：`&gt;` 4、`&amp;` 5、`&quot;` 6、`&frasl;` 7，`pos` 要跳对',
                 '作者也提到：Python 里直接 `replace` 一行就能做（注意 `&amp;` 要最后替换）',
                 '原文已是 Python 3 可运行的写法，未做改动'],
    ),
)
