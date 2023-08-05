from business_days_australia import BusinessDays

if __name__ == "__main__":
    import sys
    state = None
    date_format = None
    # --f or --format > datetime format
    if 'f' in sys.argv[1] or 'format' in sys.argv[1]:
        date_format = r"%d/%m/%y"
    # --s or --state > state
    if 's' in sys.argv[1] or 'state' in sys.argv[1]:
        state = r"%d/%m/%y"
    # create business day object
    biz_day = BusinessDays(state=state, datetime_format=date_format)
    # --n or --next > get next bus day
    biz_day.get_next_business_day(sys.argv[1])
    # --p or --previous > get previous bus day
    biz_day.get_previous_business_day(sys.argv[1])
    # else
    biz_day.is_business_day(sys.argv[1])
    