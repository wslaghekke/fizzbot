# Interactive python client for fizzbot

import requests
import json

domain = 'https://api.noopschallenge.com'


def print_sep(): print('----------------------------------------------------------------------')


def generate_answer(question_data):
    if 'rules' in question_data:
        return generate_fizzbuzz_rules_answer(question_data)
    if 'exampleResponse' in question_data:
        return question_data['exampleResponse']['answer']


def generate_fizzbuzz_rules_answer(question_data):
    output = list(map(
        lambda x: generate_fizzbuzz_rules_answer_number(question_data['rules'], x),
        question_data['numbers']
    ))


    return ' '.join(output)

def generate_fizzbuzz_rules_answer_number(rules, number):
    output = ''
    for rule in rules:
        if number % rule['number'] == 0:
            output += rule['response']

    if output == '':
        output = str(number)
    return output

# print server response
def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')


# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({'answer': answer})
    print('*** POST %s %s' % (question_url, body))
    try:
        res = requests.post(domain + question_url, json={'answer': answer})
        # req = requests.get(domain + question_url, data=body.encode('utf8'),
        #                              headers={'Content-Type': 'application/json'})
        # res = urllib.request.urlopen(req)
        response = json.loads(res.content.decode('utf-8'))
        print_response(response)
        print_sep()
        return response

    except requests.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response


# keep trying answers until a correct one is given
def get_correct_answer(question_url, question_data):
    while True:
        answer = generate_answer(question_data)
        response = try_answer(question_url, answer)

        if response.get('result') == 'interview complete':
            print('congratulations!')
            exit()

        if response.get('result') == 'correct':
            return response.get('nextQuestion')

        if response.get('result') == 'incorrect':
            print('Answer failed, exiting...')
            exit()


# do the next question
def do_question(domain, question_url):
    print_sep()
    print('*** GET %s' % question_url)

    response = requests.get(domain + question_url)
    question_data = json.loads(response.content.decode('utf-8'))
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    if next_question: return next_question
    return get_correct_answer(question_url, question_data)


def main():
    question_url = '/fizzbot'
    while question_url:
        question_url = do_question(domain, question_url)


if __name__ == '__main__': main()
