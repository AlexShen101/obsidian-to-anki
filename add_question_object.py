import re
import global_data
import logging

# creates a question object based on given lines


def add_question_object(question, lines, i, file_name):
    front_item = "<div className=\"questions_container\">\n\t<p>" + \
        question + "</p>\n</div>"
    question = {'front': front_item, 'back': ''}
    answer = []
    indents = []

    # scan next lines till it reaches a question
    for j in range(i+1, len(lines)):

        answer_line = lines[j].replace(
            '[', '').replace(']', '').replace('!', '')
        stripped_answer_line = answer_line.strip()
        # logging.info(f'{stripped_answer_line}')

        # If detected block code, make a code block
        if '```' in stripped_answer_line:
            if global_data.current_answer_type == "code":
                answer.append("</code>")
                answer.append("</pre>")
                global_data.current_answer_type = ""
                continue
            else:
                answer.append("<pre>")
                answer.append('<code class="code code-block">')
                global_data.current_answer_type = "code"
                continue

        # don't want to mess with stuff in code blocks
        if global_data.current_answer_type == "code":
            code_line = lines[j]
            code_line = re.sub('\t', r'  ', code_line)
            answer.append(code_line)
            continue

        # detect block latex
        if stripped_answer_line == '$$':
            if global_data.current_answer_type == "latex":
                global_data.current_answer_type = ""
                answer.append('\\]')
                continue
            else:
                global_data.current_answer_type = "latex"
                answer.append('\\[')
                continue

        if global_data.current_answer_type == "latex":
            answer.append(stripped_answer_line)
            continue

        # logging.info(f'Answer: {answer_line}')

        if stripped_answer_line != '':
            # determine indentation of bullet points (has to be before answerLine is stripped of whitespace)
            current_indent = 0
            if answer_line.startswith('\t-'):
                current_indent = 1
            elif answer_line.startswith('\t\t-'):
                current_indent = 2
            indents.append(current_indent)

            # find if line has imgur link (for images)
            if re.findall(
                    '(http|https:\/\/)?(i\.)?imgur.com\/((?P<gallery>gallery\/)(?P<galleryid>\w+)|(?P<album>a\/)(?P<albumid>\w+)#?)?(?P<imgid>\w*)', stripped_answer_line) != []:
                stripped_answer_line = re.search(
                    '(http|https:\/\/)?(i\.)?imgur.com\/((?P<gallery>gallery\/)(?P<galleryid>\w+)|(?P<album>a\/)(?P<albumid>\w+)#?)?(?P<imgid>\w*)', stripped_answer_line)
                stripped_answer_line = stripped_answer_line.group() + '.png'
                stripped_answer_line = "<img class=\"display_image\" src=\"" + \
                    stripped_answer_line + "\" />"
                answer.append(stripped_answer_line)

            # stop at end part
            if stripped_answer_line == global_data.termination_line:
                break
            # stop at another question or header
            elif stripped_answer_line[0] == '#' or stripped_answer_line.endswith('?'):
                break

            # add answer line for points
            elif stripped_answer_line[0] == '-':
                # remove '- ' from answers because li has its own bullet point
                stripped_answer_line = stripped_answer_line[2:]

                # add inline code blocks
                stripped_answer_line = re.sub(
                    '`(.*?)`', r'<code class="code code-inline">\1</code>', stripped_answer_line)

                # Check for inline latex in question
                stripped_answer_line = re.sub(
                    '\$\$([^$]*)\$\$', '\\[\g<1>\\]', stripped_answer_line)
                stripped_answer_line = re.sub(
                    '\$(\S[^$]*\S)\$', '\\(\g<1>\\)', stripped_answer_line)

                try:
                    if indents != [] and current_indent == 0:
                        stripped_answer_line = "<li class=\"new_point indent_" + \
                            str(current_indent) + "\">\n\t" + \
                            stripped_answer_line + "\n</li>"
                    else:
                        stripped_answer_line = "<li class=\"indent_" + \
                            str(current_indent) + "\">\n\t" + \
                            stripped_answer_line + "\n</li>"
                    answer.append(stripped_answer_line)
                except:
                    logging.error('Error while trying to create answer bullet point. (Line 112)')
            else:
                continue

    global_data.current_answer_type = ""
    logging.info(f'creating answer item:')
    # create back object, which holds the answer
    back = "<div class=\"answer_container\">\n"
    for item in answer:
        back += "\t\n" + item
        logging.info(f'{item}')
    back += "\n</div>"
    question['back'] = back
    return question
