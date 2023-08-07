from .business_days_australia import BusinessDays


def main():
    """
    Initiate command line interface requests
    :return:
    """
    import argparse
    parser = argparse.ArgumentParser(prog="business_days_australia", description="Check if date is a valid business day in Australia or a specific state.")
    # print(parser)
    parser.add_argument("date", help="Date to be searched", type=str)
    parser.add_argument("-s", "--state", help="State to search", type=str)
    parser.add_argument("-f", "--format", help="String datetime format", type=str)
    parser.add_argument("-n", "--next", help="String datetime format", action='store_true')
    parser.add_argument("-p", "--previous", help="String datetime format", action='store_true')
    parser.add_argument("-d", "--details", help="Get details for public holiday on date", action='store_true')
    args = parser.parse_args()
    # create business day object
    if args.format is not None:
        biz_day = BusinessDays(state=args.state, datetime_format=args.format)
    else:
        biz_day = BusinessDays(state=args.state)
    # --n or --next > get next bus day
    if args.next:
        print(biz_day.get_next_business_day(args.date))
    # --p or --previous > get previous bus day
    elif args.previous:
        print(biz_day.get_previous_business_day(args.date))
    elif args.details:
        print(biz_day.get_public_holiday(args.date))
    # else
    else:
        print(biz_day.is_business_day(args.date))


if __name__ == '__main__':
    main()
