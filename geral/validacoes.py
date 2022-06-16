import datetime

# ********* string_to_date_naive Início ********* 
def string_to_date_naive(string):
    '''
    Converte data em formato string para data:

    Uso:
    variavel = string_to_date_naive(string_data)
    '''
    inputDate = string
    try:
        if string:
            day, month, year = string.split('/')
            inputDate = datetime.date(int(year), int(month), int(day))
    except:
        inputDate = None
    
    return inputDate
# ********* string_to_date_naive Início ********* 