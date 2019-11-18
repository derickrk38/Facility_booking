import datetime
import csv
import sys

bookingConfig = {
    "facilities": {
        "Club House": {
            "type": "slot",
            "price": [100, 500],
            "slot_time_from": ["10:00", "16:00"],
            "slot_time_to": ["16:00", "22:00"],
        },
        "Tennis Court": {
            "type": "multiplier",
            "price": 50,
            "slot_time_from": "00:00",
            "slot_time_to": "00:00"
        }
    }
}


def check_availability(bf, bt, book_val):
    with open('booking_records.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # print(repr(row))

            if len(row) == 5 and row[0] == book_val["facility"] and row[1] == book_val["date"]:
                rf = datetime.datetime.strptime(row[2], "%H:%M")
                rt = datetime.datetime.strptime(row[3], "%H:%M")
                if not ((bf < rf and bt <= rf) or bf >= rt):
                    return False
    return True


def book(bf, bt, book_val, bookingConfig, bf_str, bt_str):
    facilty_name = book_val["facility"]
    # print(facilty_name)
    amount = 0
    if bookingConfig["facilities"][facilty_name]["type"] == "slot":

        st1 = bookingConfig["facilities"][facilty_name]["slot_time_to"][0]
        st_1 = datetime.datetime.strptime(st1, "%H:%M")

        if bf < st_1 and bt <= st_1:
            duration = (bt - bf).total_seconds() / 3600
            amount = bookingConfig["facilities"][facilty_name]["price"][0] * duration
        elif bf >= st_1 and bt > st_1:
            duration = (bt - bf).total_seconds() / 3600
            amount = bookingConfig["facilities"][facilty_name]["price"][1] * duration
        else:
            duration = (st_1 - bf).total_seconds() / 3600
            amount = duration * bookingConfig["facilities"][facilty_name]["price"][0]
            duration = (bt - st_1).total_seconds() / 3600
            amount = amount + duration * bookingConfig["facilities"][facilty_name]["price"][1]

    else:
        duration = (bt - bf).total_seconds() / 3600
        amount = duration * bookingConfig["facilities"][facilty_name]["price"]

    with open('booking_records.csv', mode='a', newline='') as record_file:
        record_writer = csv.writer(record_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        record_writer.writerow([book_val["facility"], book_val["date"], bf_str, bt_str, int(amount)])

    return amount


arr_val = sys.argv[1].split(",")
fromtime = arr_val[2].split(":")
from_hr = int(fromtime[0])
from_min = int(fromtime[1])
totime = arr_val[3].split(":")
to_hr = int(totime[0])
to_min = int(totime[1])

#  parsed according to given format
book_val = {
    "facility": arr_val[0].strip(),
    "date": arr_val[1].strip(),
    "from": {
        "hour": from_hr,
        "minute": from_min
    },
    "to": {
        "hour": to_hr,
        "minute": to_min
    }
}

# converting string to time

bf = datetime.datetime.strptime(arr_val[2], "%H:%M")  # bf --> From time given in booking
bt = datetime.datetime.strptime(arr_val[3], "%H:%M")  # bt --> To time given in booking
start = datetime.datetime.strptime("10:00", "%H:%M")  # start time available for booking
end = datetime.datetime.strptime("22:00", "%H:%M")  # end time available for booking

# validations
if bf >= bt or bf < start or bt < start or bf > end or bt > end:
    print("invalid timing")
    exit()

status = check_availability(bf, bt, book_val)  # check status for slot availability
if status:
    amt = int(book(bf, bt, book_val, bookingConfig, arr_val[2], arr_val[3]))
    print("Booked, Rs." + str(amt))
else:
    print("Booking Failed, Already Booked")
