GST = 18


def get_rates():
    return {"ZERODHA": {"Brokerage": [40, 0, 40, 40],
                        "STT": [0.025, 0.1, 0.01, 0.05],
                        "ExchTrnChrg": [0.00345, 0.00345, 0.002, 0.053],
                        "ClearingChrg": [0, 0, 0, 0],
                        "SEBIChrg": [0.0001, 0.0001, 0.0001, 0.0001],
                        "StampDuty": [0.003, 0.015, 0.002, 0.003],
                        },
            "ANGLE": {"Brokerage": [40, 0, 40, 40],
                      "STT": [0.025, 0.1, 0.01, 0.05],
                      "ExchTrnChrg": [0.00345, 0.00345, 0.002, 0.053],
                      "ClearingChrg": [0, 0, 0, 0],
                      "SEBIChrg": [0.0001, 0.0001, 0.0001, 0.0001],
                      "StampDuty": [0.003, 0.015, 0.002, 0.003],
                      },
            "UPSTOX": {"Brokerage": [40, 0, 40, 40],
                       "STT": [0.025, 0.1, 0.01, 0.05],
                       "ExchTrnChrg": [0.00345, 0.00345, 0.002, 0.053],
                       "ClearingChrg": [0, 0, 0, 0],
                       "SEBIChrg": [0.00005, 0.00005, 0.00005, 0.00005],
                       "StampDuty": [0.003, 0.015, 0.002, 0.003],
                       },
            "TRADE+": {"Brokerage": [18, 0, 18, 0],
                       "STT": [0.025, 0.1, 0.1, 0.05],
                       "ExchTrnChrg": [0.00345, 0.00345, 0.002, 0.053],
                       "ClearingChrg": [0, 0, 0.016, 0.025],
                       "SEBIChrg": [0.0001, 0.0001, 0.0001, 0.0001],
                       "StampDuty": [0.003, 0.015, 0.002, 0.003],
                       },
            "PAYTM": {"Brokerage": [20, 0, 20, 20],
                      "STT": [0.025, 0.1, 0.01, 0.05],
                      "ExchTrnChrg": [0.00345, 0.00345, 0.002, 0.053],
                      "ClearingChrg": [0, 0, 0, 0],
                      "SEBIChrg": [0.00005, 0.00005, 0.00005, 0.00005],
                      "StampDuty": [0.003, 0.015, 0.002, 0.003],
                      }
            }


def calc_charges(broker, instrkey, buy, sell, qty):
    rates = get_rates()
    buyamt = buy * qty
    sellamt = sell * qty
    turnover = buyamt + sellamt

    if qty > 0 and (buy > 0 or sell > 0):
        if broker.upper() in ["ZERODHA", "PAYTM", "UPSTOX"] and instrkey != 1:
            brokeragerate = (rates[broker]["Brokerage"][instrkey]) / 2
            buybrokerage = buyamt / 100 * (0.03 if broker.upper() == "ZERODHA" else 0.05)
            buybrokerage = brokeragerate if buybrokerage > brokeragerate else buybrokerage
            sellbrokerage = sellamt / 100 * (0.03 if broker.upper() == "ZERODHA" else 0.05)
            sellbrokerage = brokeragerate if sellbrokerage > brokeragerate else sellbrokerage
            if instrkey == 3:
                brokerage = brokeragerate * 2
            else:
                brokerage = buybrokerage + sellbrokerage
        else:
            brokerage = rates[broker]["Brokerage"][instrkey]
    else:
        brokerage = 0
    brokerage = round(brokerage, 2)
    stt = round(rates[broker]["STT"][instrkey] * (turnover if instrkey == 1 else sellamt) / 100, 2)
    exchtrnchrg = round(rates[broker]["ExchTrnChrg"][instrkey] * turnover / 100, 2)
    clearingchrg = round(rates[broker]["ClearingChrg"][instrkey] * turnover / 100, 2)
    if qty > 0:
        gst = round((brokerage + exchtrnchrg + clearingchrg) * GST / 100, 2)
    else:
        gst = 0
    sebicharg = round(rates[broker]["SEBIChrg"][instrkey] * turnover / 100, 2)
    stampduty = round(rates[broker]["StampDuty"][instrkey] * buyamt / 100, 2)

    # totalcharges = brokerage+stt+exchtrnchrg+clearingchrg+gst+sebicharg+stampduty
    # pl = (sellamt-buyamt-totalcharges

    return [brokerage, stt, round(exchtrnchrg + clearingchrg, 2), gst, sebicharg, stampduty]


if __name__ == "__main__":
    print("Select instrument type...")
    print("0: for Intraday")
    print("1: for Delivery")
    print("2: for Futures")
    print("3: for Options")
    instKey = int(input("Enter your instrument choice....: "))
    if not instKey >= 0 and instKey <= 3:
        print("invalid instrument type.. press between 0-3")
        exit(-1)
    print("Type broker name any of this ZERODHA,ANGLE,UPSTOX,PAYTM")
    broker = input("Enter broker name as specify above: ")
    buy = float(input("Input Buy price: "))
    sell = float(input("Enter Sell Price: "))
    qty = float(input("Enter Quantity: "))
    charges = calc_charges(broker.upper(), instKey, buy, sell, qty)
    totcharges = round(sum(charges), 2)
    print("-" * 50)
    print("Total Charges:", totcharges)
    pl = round((sell - buy) * qty - totcharges, 2)
    print("P/L After Charges", pl)
