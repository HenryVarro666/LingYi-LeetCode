CONFIG = dict(
    num=726, title='原子的数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从右往左扫描 + 栈',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def countOfAtoms(self, formula):

        stack = []
        now_multi = ''
        now_element = ''
        now_dict = {}

        for index in range(len(formula) - 1, -1, -1):
            if formula[index] >= '0' and formula[index] <= '9':
                now_multi = formula[index] + now_multi
            elif formula[index] == ')':
                if now_multi == '':
                    stack.append([1, now_dict])
                else:
                    stack.append([int(now_multi), now_dict])
                    now_multi = ''
                now_dict = {}
            elif formula[index] == '(':
                pre_multi, pre_dict = stack.pop()
                for key in now_dict:
                    now_dict[key] *= pre_multi
                for key in pre_dict:
                    now_dict[key] = now_dict.get(key, 0) + pre_dict[key]
            elif formula[index] >= 'a' and formula[index] <= 'z':
                now_element = formula[index] + now_element
            else:
                now_element = formula[index] + now_element
                if now_multi == '':
                    now_dict[now_element] = now_dict.get(now_element, 0) + 1
                else:
                    now_dict[now_element] = now_dict.get(now_element, 0) + int(now_multi)
                now_multi = ''
                now_element = ''

        res = ''
        for element, cnt in sorted(now_dict.items(), key=lambda d:d[0]):
            res += element
            if cnt > 1:
                res += str(cnt)

        return res
''',
    call='Solution().countOfAtoms("(NH4)2SO4")',
    expect='H8N2O4S',
    skip=[6, 7, 34],
    max_steps=100,
    views=[
        dict(type='text', fn=lambda S: (f"从右往左：系数 `now_multi` = `'{S['now_multi']}'`，元素 `now_element` = `'{S['now_element']}'`" if 'now_multi' in S else '系数在元素后面，所以从右往左扫，先读到系数再读到元素')),
        dict(type='string', var='formula', label='formula（从右往左扫）', pointers={'index': 'blue'}, h=200, cell=84),
        dict(type='map', var='now_dict', label='now_dict：当前这一层的元素数量', h=200),
        dict(type='stack', var='stack', label='stack：遇到 ) 压入 [系数, 之前的 dict]', h=220, fmt=lambda x: f'x{x[0]} {dict(x[1])}'),
    ],
    watch=[('index', 'index', 'blue'), ('now_multi', 'now_multi', 'orange'), ('now_element', 'now_element', 'pink'), ('res', 'res', 'green')],
    captions={
        'stack = []': '栈：保存括号外面已经统计好的内容',
        'for index in range': lambda S, B, r: ('全部字符扫完' if 'index' in B and B['index'] == S['index'] and S['index'] == 0 else f"从右往左取下一个字符：`index = {S['index']}`，字符 `{S['formula'][S['index']]}`"),
        "formula[index] >= '0'": lambda S, B, r: (f"`{S['formula'][S['index']]}` 是数字 → 并入系数" if '0' <= S['formula'][S['index']] <= '9' else f"`{S['formula'][S['index']]}` 不是数字，看看是什么字符"),
        'now_multi = formula[index] + now_multi': '数字放到系数字符串的==最前面==（因为是从右往左）：`now_multi = {now_multi}`',
        "== ')'": lambda S, B, r: (f"`)` → 括号里的内容在它左边，先把当前结果压栈" if S['formula'][S['index']] == ')' else f"`{S['formula'][S['index']]}` 不是右括号"),
        'stack.append([1': '系数 `1` 连同 `now_dict` 一起压栈',
        'stack.append([int': '系数 `{now_multi}` 连同 `now_dict` 一起压栈',
        5: '三个变量：`now_multi` 当前系数（字符串）、`now_element` 当前元素名、`now_dict` 当前层各元素数量',
        6: '`now_element`：当前拼到的元素名',
        7: '`now_dict`：当前这一层各元素的数量',
        17: '系数用完了，清空',
        18: '括号里的内容从一个空 dict 开始统计',
        "== '('": lambda S, B, r: (f"`(` → 括号里的内容统计完了，出栈合并" if S['formula'][S['index']] == '(' else f"`{S['formula'][S['index']]}` 不是左括号"),
        'pre_multi, pre_dict = stack.pop()': '出栈得到括号的系数 `{pre_multi}` 和括号外已统计的 `{pre_dict}`',
        'for key in now_dict': lambda S, B, r: ('括号里的元素都乘完了' if 'key' in B and B['key'] == S['key'] else f"括号里的每个元素都要乘以系数 `{S['pre_multi']}`"),
        'now_dict[key] *= pre_multi': '`{key}` 乘以 `{pre_multi}` → `{now_dict[key]}`',
        'for key in pre_dict': lambda S, B, r: ('括号外的统计也合并完了' if 'key' in B and B['key'] == S['key'] and S['key'] == list(S['pre_dict'])[-1] else f"再把括号外的统计 `{dict(S['pre_dict'])}` 合并进来"),
        'now_dict[key] = now_dict.get': '合并 `{key}`：现在是 `{now_dict[key]}`',
        "formula[index] >= 'a'": lambda S, B, r: (f"`{S['formula'][S['index']]}` 是小写字母 → 元素名的一部分" if 'a' <= S['formula'][S['index']] <= 'z' else f"`{S['formula'][S['index']]}` 是大写字母 → 元素名的开头"),
        'now_element = formula[index] + now_element': '字符放到元素名最前面：`now_element = {now_element}`',
        13: lambda S, B, r: '右括号后面没有系数 → 系数是 `1`' if S['now_multi'] == '' else '右括号后面有系数 `' + S['now_multi'] + '`',
        29: lambda S, B, r: (f"没有系数 → 这个元素加 `1` 个" if S['now_multi'] == '' else f"系数是 `{S['now_multi']}` → 这个元素加 `{S['now_multi']}` 个"),
        '+ 1': '`{now_element}` 数量 +1 → `{now_dict}`',
        '+ int(now_multi)': '`{now_element}` 数量 +`{now_multi}` → `{now_dict}`',
        33: '系数用完了，清空',
        34: '元素处理完，元素名清空',
        'res = \'\'': '扫完了，`now_dict` = `{now_dict}`，按字典序拼接结果',
        'res += element': '先写元素名：`res = {res}`',
        'if cnt > 1': '数量 `{cnt}`：只有大于 1 才写数字',
        'res += str(cnt)': '写上数量：`res = {res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='系数在元素后面，那就从右往左扫，括号用栈',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['化学式里原子 = 大写字母 + 小写字母，后面可跟数量；括号后可跟倍数',
                 '统计每种原子的数量，按字典序输出，数量为 1 不写',
                 '本视频：`(NH4)2SO4` → `H8N2O4S`'],
        quote='注意到这里的乘法操作，系数是在元素符号后面的，因此我们可以适当转换思路，从后往前进行扫描，遇到右括号时进行压栈操作，左括号则弹栈合并',
        quote_src='—— yiduobo 题解原文',
        idea=['当作「代数符号 + 加乘 + 括号」的表达式：碰到括号就压栈',
              '从右往左：先读到数字（系数字符串，往前拼），再读到元素名（小写、大写字母往前拼）',
              '`)` 压栈 `[系数, now_dict]` 并清空；`(` 弹栈，括号内每个数量乘系数，再合并括号外的'],
        summary=['时间 `O(n^2)`（嵌套括号的合并），空间 `O(n)`',
                 '系数用字符串拼接：从右往左读，新数字要放在最高位',
                 '易错：`)` 后没有数字时系数是 `1`；最后数量为 1 的元素不写数字',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动',
                 '对比灵神：灵神从左往右扫，遇 `(` 压栈、`)` 弹栈后读系数；这里反着扫，先读系数'],
    ),
)
