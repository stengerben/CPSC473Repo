import cgi

def escape_html(s):
    return cgi.escape(s, quote = True)

months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'Septem    ber', 'October', 'November', 'December']

def valid_day(day):
    if(day and day.isdigit()):
        day=int(day)
    if(day < 32 and day > 0):
        return day

def valid_month(month):
    if(month):
        month = month.capitalize()
    if(month in months):
        return month

def valid_year(year):
    if(year and year.isdigit()):
        year = int(year)
    if(year < 2020 and year > 1880):
        return year

