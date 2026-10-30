def _info(S):
    if 'now_multi' not in S:
        return '从右往左扫：数字攒成系数，`)` 压栈，`(` 弹栈合并'
    return f'系数串 `now_multi = "{S["now_multi"]}"`，元素名 `now_element = "{S["now_element"]}"`'


def _ch(S, i, v):
    return 'blue' if 'index' in S and i == S['index'] else None


CONFIG = dict(
    num=726, title='原子的数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从右往左扫描 + 栈保存外层',
    tags=['栈', '表达式解析'],
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
    call='Solution().countOfAtoms("Mg(OH)2")',
    expect='H2MgO2',
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='string', var='formula', label='formula（从右往左扫，蓝 = 当前字符）', pointers={'index': 'blue'}, cell=90, h=230, color=_ch),
        dict(type='stack', var='stack', label='stack（压入 [外层系数, 外层已统计的原子]）', h=170, font=26,
             fmt=lambda x: f'×{x[0]} {x[1]}'),
        dict(type='map', var='now_dict', label='now_dict（当前层各原子计数）', h=190, fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'blue'), ('now_multi', 'now_multi', 'pink'), ('now_element', 'now_element', 'purple'), ('now_dict', 'now_dict', 'green')],
    max_steps=80,
    captions={
        4: '栈用来存放括号外层的系数和已统计的结果',
        5: '`now_multi`：当前的系数（字符串，方便往高位拼）',
        6: '`now_element`：当前元素符号，从右往左拼',
        7: '`now_dict`：当前这一层各元素的出现次数',
        9: lambda S, B, ret: ('扫描完毕，`now_dict` 里就是最终计数' if 'index' in B and B.index == S.index and S.index == 0 else f"看 `formula[{S.index}] = '{S.formula[S.index]}'`"),
        10: lambda S, B, ret: (f"`'{S.formula[S.index]}'` 是数字 → 并入系数" if S.formula[S.index].isdigit() else f"`'{S.formula[S.index]}'` 不是数字 → 看下一类"),
        11: '数字拼到系数最高位：`now_multi = "{now_multi}"`（从右往左，所以加在前面）',
        12: lambda S, B, ret: ("`')'` 是右括号：从右往左先碰到它 → 进入一层括号，把外面的状态压栈" if S.formula[S.index] == ')' else f"`'{S.formula[S.index]}'` 不是右括号 → 看下一类"),
        13: lambda S, B, ret: ("`now_multi = ''`：括号后没写系数 → 当作 1" if S.now_multi == '' else f"`now_multi = '{S.now_multi}'`：括号后面有系数"),
        14: '压栈 `[1, now_dict]`：括号后系数为 1',
        16: '压栈 `[{stack[-1][0]}, now_dict]`：==括号右边的系数==和外层已统计的结果',
        17: '系数已经用掉，清空 `now_multi`',
        18: '括号里重新统计：`now_dict` 换成空字典',
        19: lambda S, B, ret: ("`'('` 是左括号：括号里的内容扫完了 → 弹栈合并" if S.formula[S.index] == '(' else f"`'{S.formula[S.index]}'` 不是左括号 → 看下一类"),
        20: '弹出外层：系数 `pre_multi = {pre_multi}`，外层结果 `{pre_dict}`',
        21: lambda S, B, ret: ('括号里的原子都乘完了' if 'key' in B and B.key == S.key else f'取括号里的原子 `{S.key}`'),
        22: '括号里的 `{key}` 乘以系数 `{pre_multi}` → =={now_dict[key]}==',
        23: lambda S, B, ret: ('外层的原子都合并完了' if 'key' in B and B.key == S.key else f'取外层已统计的原子 `{S.key}`'),
        24: '把外层的 `{key}` 合并进来：`{key}` = =={now_dict[key]}==',
        25: lambda S, B, ret: (f"`'{S.formula[S.index]}'` 是小写字母 → 属于元素名的一部分" if 'a' <= S.formula[S.index] <= 'z' else f"`'{S.formula[S.index]}'` 不是小写字母 → 只能是大写字母，元素名的开头"),
        26: '小写字母往前拼：`now_element = "{now_element}"`',
        28: '大写字母往前拼：`now_element = "{now_element}"` 成为完整元素名',
        29: lambda S, B, ret: ("`now_multi = ''`：元素后没写数字 → 数量按 1 计" if S.now_multi == '' else f"`now_multi = '{S.now_multi}'`：这个元素的数量是 {S.now_multi}"),
        30: '元素 `{now_element}` 加 1 次：`now_dict[{now_element!r}] = {now_dict[now_element]}`',
        32: '元素 `{now_element}` 加 `{now_multi}` 次：`now_dict[{now_element!r}] = {now_dict[now_element]}`',
        33: '系数用掉了，清空 `now_multi`',
        34: '元素已入账，清空 `now_element`',
        36: '扫描完成，开始按字典序拼接结果 `res`',
        37: lambda S, B, ret: ('所有元素处理完毕' if 'element' in B and B.element == S.element and B.cnt == S.cnt else f'按字典序取 `{S.element}`，数量 `{S.cnt}`'),
        38: '`res` 先写元素名：`"{res}"`',
        39: lambda S, B, ret: (f'`cnt = {S.cnt} > 1` → 要写数量' if S.cnt > 1 else f'`cnt = {S.cnt}`：只有 1 个，==不写数量=='),
        40: '写上数量：`res = "{res}"`',
        42: '返回 `"{ret}"`：原子数量 H=2, Mg=1, O=2',
    },
    cards=dict(
        one_liner='括号当栈：从右往左扫，系数先到，括号里的结果再乘上去',
        complexity='时间约 `O(n²)`（括号嵌套合并），空间 `O(n)`',
        problem=['化学式里：元素名 = 大写字母 + 小写字母，后面可跟数量，括号后也可跟系数',
                 '求每种原子的数量，按字典序输出，数量为 1 不写',
                 '示例：`"Mg(OH)2"` → `"H2MgO2"`'],
        quote='系数是在元素符号后面的，因此我们可以适当转换思路，从后往前进行扫描，遇到右括号时进行压栈操作，左括号则弹栈合并。',
        quote_src='—— yiduobo 题解原文',
        idea=['系数写在后面 → 从右往左扫，先拿到系数再遇到元素/括号',
              '数字拼进 `now_multi`；小写、大写字母往前拼 `now_element`，碰到大写字母就入账',
              '`)` 压栈 `[系数, now_dict]` 并清空；`(` 弹栈，括号里每个数量 ×系数，再合并外层'],
        summary=['时间约 `O(n²)`，空间 `O(n)`',
                 '易错：系数用字符串拼，才能把多位数字按从右往左拼回来',
                 '易错：大写字母才结束一个元素名；数量为 1 的元素输出时不写数字',
                 '原文本身可直接在 Python 3 运行，没有改动',
                 '同类题：基本计算器、字符串解码（括号 + 栈）'],
    ),
)
