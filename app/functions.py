import uuid
import os
import base64
import re
import datetime


def dateTimeNow():
    return datetime.datetime.now()


def dateTimeIntNow():
    dt = datetime.datetime.now()
    seq = int(dt.strftime("%Y%m%d%H%M%S"))
    return seq


def number_format_comma(value):
    numbers = "{:,}".format(value)
    return numbers


def dmytoymd(date):
    # 2022-03-31
    x = date.split('/')
    day = x[0]
    month = x[1]
    year = x[2]
    format_data = year + '-' + month + '-' + day
    return format_data


def ymdtodmy(date):
    # 31/02/2022
    x = date.split('-')
    year = x[0]
    month = x[1]
    day = x[2]
    format_data = day + '/' + month + '/' + year
    return format_data


def ternaryZero(value):
    if value:
        if (int(value)):
            r = 0
        else:
            r = value
    else:
        r = 0
    return r


def generateId():
    generateId = uuid.uuid4().hex[:24]
    return generateId


# def generate_unique_name(path):
#     def wrapper(instance, filename):
#         extension = "." + filename.split('.')[-1]
#         filename = str(random.randint(10, 99)) + str(random.randint(10, 99)) + \
#             str(random.randint(10, 99)) + \
#             str(random.randint(10, 99)) + extension
#         return os.path.join(path, filename)
#     return wrapper

def generate_unique_name(path):
    return path


def base64_string_encode(val):
    sample_string = str(val)
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def base64_string_decode(val):
    base64_string = str(val)
    base64_bytes = base64_string.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string


def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    # s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r'\*(.*?)\*', '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s


def chek_image_from_request(requestFile):
    # extesion = os.path.splitext(str(request.FILES['mcf_path']))[1]
    extesion = os.path.splitext(str(requestFile))[1]
    t = extesion.split(".")[-1]  # get file type
    tlower = t.lower()
    if (tlower == "png" or tlower == "jpg" or tlower == "jpeg" or tlower == "gif"):
        return tlower
    return False


def month_fomat(value):
    month_set = int(value)
    if month_set == 1:
        f = "มกราคม"
    elif month_set == 2:
        f = "กุมภาพันธ์"
    elif month_set == 3:
        f = "มีนาคม"
    elif month_set == 4:
        f = "เมษายน"
    elif month_set == 5:
        f = "พฤษภาคม"
    elif month_set == 6:
        f = "มิถุนายน"
    elif month_set == 7:
        f = "กรกฎาคม"
    elif month_set == 8:
        f = "สิงหาคม"
    elif month_set == 9:
        f = "กันยายน"
    elif month_set == 10:
        f = "ตุลาคม"
    elif month_set == 11:
        f = "พฤศจิกายน"
    elif month_set == 12:
        f = "ธันวาคม"
    return f


def treeDigit(value):
    number = int(value)
    if number >= 100:
        r = value
    elif number <= 99 and number >= 10:
        r = "0" + str(value)
    elif number <= 9:
        r = "00" + str(value)
    else:
        r = "000"
    return str(r)
