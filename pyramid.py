from bottle import request, route, response, run, post, static_file, template
from collections import Counter

'''
Pyramid Words necessarily have lengths
1,3,6,10,15,21,...
In the event that the word does not have
a valid length, we do not need to sort
and count character frequencies
'''

valid_lengths = []
i=1
n = i
while(i < 70):
    valid_lengths.append(n)
    i+=1
    n+=i


def pyramidify(word):
    '''This function sorts the word by character count
    and checks to see if the word follows the pyramid structure'''
    count = sorted(Counter(word).items() ,  key=lambda x: x[1])
    if(count[0][1] == 1 and (all(count[i][1] == count[i + 1][1]-1 for i in range(len(count)-1)))): 
        result = "This IS a pyramid word!\n"
        for freq in count:
            result += freq[0]*freq[1]+'\n'
        return result
    else:
        return "This is NOT a pyramid word!\n"

def scrub_input(word,include_numbers,include_upper,webpage=False):
    global i, n
    try:
        if len(word) in valid_lengths or len(word) > 2048:
            not_alpha = False
            for c in word:
                if not c.isalpha():
                    if include_numbers and c.isalnum():
                        continue
                    else:                
                        not_alpha = True
                        break                
            if not_alpha:
                response.status = 500
                return "Please try again with alpha characters only or specify 'num=True' to use numbers\n"
            if word == "":
                response.status = 500
                return "No word\n"
            else:
                if not include_upper:
                    result = pyramidify(word.upper())
                else:
                    result = pyramidify(word)
                if 'NOT' in result:
                    response.status = 404
                    return result
                else:
                    valid_lengths.append(len(word))
                    if webpage:
                        results = result.split('\n')
                        return template('pyramid',lines=results)
                    return result
        else:
            response.status = 500
            return "This is NOT a pyramid word! (invalid length)\n"
    except Exception as e:
        response.status = 500
        return e.message

@route('/')
def server_static(filepath="index.html"):
    return static_file(filepath, root='./public/')


@post('/doform')
def process():
    '''Function to retrieve user entry from form and return whether
    or not the provided word is a pyramid word'''
    word = request.forms.get('word')
    include_upper = True            #allow user to input upper and lower case characters
    include_numbers = True          #allow user to input numeric characters
    return scrub_input(word,include_numbers,include_upper,webpage=True)


@route('/isPyramid')
def index():
    word = request.query.word
    caps = request.query.caps
    numbers = request.query.num
    include_upper = False
    include_numbers = False
    if caps and caps.upper() == 'TRUE':
        include_upper = True
    if numbers and numbers.upper() == 'TRUE':
        include_numbers = True
    return scrub_input(word,include_numbers,include_upper)
    

if  __name__ == '__main__':
    run(port=8081)