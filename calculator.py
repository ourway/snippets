def to_postfix(input):
    res = []
    op_stack = []
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
    operators = {'(':1, ')':1, '^':2, '*':3, '/':3, '+':4, '-':4}
    i = 0
    op_pos = -1
    for i in range(len(input)):
        str_num = ''
        while input[i] in nums:
            str_num = str_num + input[i]
            if len(input)-1 > i:
                i += 1
            else:
                break
        if str_num:
            if '.' in str_num:
                res.append(float(str_num))
            else:
                res.append(int(str_num))
        if input[i] in operators.keys():
            if input[i] == '(':
                op_stack.append(input[i])
            elif input[i] == ')':
                while op_stack[-1:] != ['(']:
                    res.append(op_stack.pop())
            else:

                #print(''.join(op_stack[op_pos]))
                if not op_stack:
                    op_stack.append(input[i])
                elif operators[''.join(op_stack[-1:])] > operators[''.join(input[i])]:
                    op_stack.append(input[i])
                else:
                    while op_stack and  operators[''.join(op_stack[-1:])] <= operators[''.join(input[i])]:
                        res.append(op_stack.pop())
    while len(op_stack):
        res.append(op_stack.pop())
    return res

print(to_postfix(input('Enter str: ')))
