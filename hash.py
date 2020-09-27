import hashlib

a={'name':'Danish', 'age':107}
b={'age':107, 'name':'Danish'}

print str(a)
print str (b)
print hashlib.sha1(str(a)).hexdigest()
print hashlib.sha1(str(b)).hexdigest()



a={'name':'Danish', 'age':107}
b={'age':107, 'name':'Danish'}


def get_id_for_dict(dict):
    unique_str = ''.join(["'%s':'%s';"%(key, val) for (key, val) in sorted(dict.items())])
    return hashlib.sha1(unique_str).hexdigest()

print get_id_for_dict(a)
print get_id_for_dict(b)


def function_G(initial_seed):
    binary_string = initial_seed
    result = ''
    for i in range(FUNCTION_L(SEED_SIZE)):
        first_half = binary_string[:len(binary_string)/2]
        second_half = binary_string[len(binary_string)/2:]
        binary_string = function_H(first_half, second_half)
        result += binary_string[-1]
        binary_string = binary_string[:-1]
    print result
    return result

function_G()
