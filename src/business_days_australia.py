class BusinessDays:
    def __init__(self, state=None, datetime_format="%Y%m%d"):
        from datetime import datetime
        self.id = '33673aca-0857-42e5-b8f0-9981b4755686'
        self.gov_entry_limit = 32000
        self.today = datetime.now().date()
        self.state = state
        self.datetime_format = datetime_format
        self.required_date_format = "%Y%m%d"
        self.public_holidays = self.get_public_holidays()
        return

    def convert_date_to_datetime(self, date, datetime_format=None):
        from datetime import datetime
        if datetime_format is None:
            datetime_format = self.datetime_format
        if type(date) == str:
            # Convert the date string to a datetime object
            return datetime.strptime(date, datetime_format)
        elif not isinstance(date, datetime):
            print(type(date))
            print(isinstance(date, datetime))
            raise TypeError
        return date

    def convert_date_to_string(self, date, datetime_format=None, output_datetime_format=None):
        from datetime import datetime
        if datetime_format is None:
            datetime_format = self.datetime_format
        if output_datetime_format is None:
            output_datetime_format = self.required_date_format
        if isinstance(date, datetime):
            return date.strftime(output_datetime_format)
        elif type(date) == str:
            # Convert the input date string to a datetime object
            date_obj = datetime.strptime(date, datetime_format)
            # Convert the datetime object to a string with the desired format
            return date_obj.strftime(output_datetime_format)
        else:
            raise TypeError
        return

    def get_public_holidays(self):
        """
        Get public holiday data from data.gov.au
        :return:
        """
        import requests
        import json
        response_data = requests.get(f'https://data.gov.au/data/api/3/action/datastore_search?resource_id={self.id}&limit={self.gov_entry_limit}').text
        response = json.loads(response_data)
        if response['result']['total'] > 0:
            return response['result']['records']
        raise ConnectionError

    def is_public_holiday(self, date, state=None, datetime_format=None) -> bool:
        """
        Determine if the date provided is a public holiday
        :param date: supports date as datetime object or string - string must be in the format yyyymmdd
        :param state: 3 letter abbreviation state code - If ommited or None - wil check if it is a national holiday. If state is provided - will check if public holiday for the specified state
        :return: bool - True > date is a pubic holiday; False > date is not a public holiday
        """
        if state is None:
            state = self.state
        date = self.convert_date_to_string(date, datetime_format)
        # check if it is a national public holiday
        if state is None and sum(1 for holiday in self.public_holidays if holiday.get('Date') == date) == 8:
            return True
        elif state is None:
            return False
        return any(holiday.get('Date') == date and holiday.get('Jurisdiction') == state.lower() for holiday in self.public_holidays)

    def is_week_day(self, date, datetime_format=None) -> bool:
        """
        Determine if the date provided is a week day
        :param date:
        :param datetime_format:
        :return: bool - True > date is a weekday; False > date is a weekend (not a weekday)
        """
        date = self.convert_date_to_datetime(date, datetime_format)
        # Get the day of the week (0 is Monday, 6 is Sunday)
        day_of_week = date.weekday()

        # Check if it's a working day (Monday to Friday)
        return 0 <= day_of_week <= 4

    def is_business_day(self, date, state=None, datetime_format=None):
        if self.is_week_day(date=date, datetime_format=datetime_format) and not self.is_public_holiday(date=date, state=state, datetime_format=datetime_format):
            return True
        return False

    def get_next_business_day(self, date, state=None, datetime_format=None, include_current_date=True, force_return_sting=False, force_return_datetime=False):
        from datetime import timedelta
        next_business_day = self.convert_date_to_datetime(date)
        if not include_current_date:
            next_business_day = next_business_day + timedelta(days=1)
        while self.is_business_day(next_business_day, state=state, datetime_format=datetime_format) is False:
            next_business_day = next_business_day + timedelta(days=1)
        if (type(date) == str and not force_return_datetime) or force_return_sting:
            return self.convert_date_to_string(next_business_day)
        else:
            return self.convert_date_to_datetime(next_business_day)

    def get_previous_business_day(self, date, state=None, datetime_format=None, include_current_date=True, force_return_sting=False, force_return_datetime=False):
        from datetime import timedelta
        next_business_day = self.convert_date_to_datetime(date)
        if not include_current_date:
            next_business_day = next_business_day - timedelta(days=1)
        while self.is_business_day(next_business_day, state=state, datetime_format=datetime_format) is False:
            next_business_day = next_business_day - timedelta(days=1)
        if (type(date) == str and not force_return_datetime) or force_return_sting:
            return self.convert_date_to_string(next_business_day, self.required_date_format, self.datetime_format)
        else:
            return self.convert_date_to_datetime(next_business_day)

