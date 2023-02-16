import random
from faker import Faker
from typing import Dict
import pprint


class IndividualReservations:

    def create(client,
               url: str,
               headers: Dict[str, str],
               proxies: Dict[str, str],
               name: str,
               timeout: int,
               config: Dict[str, list],
               profile: list,
               quota: dict,
               channel_code,
               market_segment,
               source_code,
               guarantee_code,
               guests,
               ):

        fake = Faker(random.choice(config["FAKER_LANG"]))

        arrival = fake.date_object()
        departure = fake.date_object()
        from_date = f"{str(fake.date_time_this_month()).split(' ')[0]}T{str(fake.date_time_this_month()).split(' ')[1]}"
        to_date = f"{str(fake.date_time_this_month()).split(' ')[0]}T{str(fake.date_time_this_month()).split(' ')[1]}"

        amount = quota["averageDailyPrice"]
        base_amount = quota["stayRateBasePriceType"]
        profile = profile.pop(0)
        data = {
            "_flowControl": {
                "validateProfiles": "true",
                "validatePrices": "true",
                "waitForInventoryAllocation": "true",
                "waitForAccountCreation": "true",
            },
            "guest": {"id": profile},
            "arrivalDate": from_date,
            "departureDate": to_date,
            "roomTypeId": quota["roomTypeId"],
            "roomId": None,
            "breakdown": [
                {
                    "fromDate": from_date,
                    "toDate": to_date,
                    "marketSegmentId": market_segment,
                    "ratePricingDetails": {
                        "promotionId": None,
                        "ratePlanId": quota["ratePlanId"],
                        "roomTypeToChargeId": quota["roomTypeId"],
                    },
                    "ratePricePerDay": {
                        "gross": amount["gross"],
                        "net": amount["net"],
                        "currency": quota["currency"]["code"],
                        "basePriceType": base_amount,
                    },
                    "pricePerDay": {
                        "gross": amount["gross"],
                        "net": amount["net"],
                        "currency": quota["currency"]["code"],
                        "basePriceType": base_amount,
                    },
                    "guests": guests,
                }
            ],
            "purchaseElements": [],
            "paymentMethods": [],
            "guaranteeTypeId": guarantee_code,
            "channelId": channel_code,
            "sourceId": source_code,
            "preferences": [],
            "billingInstructions": [],
            "accompanyingGuestProfileIds": [],
            "applicableMembershipIds": [],
            "customFields": [],
            "eta": None,
            "etd": None,
            "externalIds": [],
            "transportations": {},
            "noPost": False,
        }
        print(data)
        req = client.post(
            url=url,
            json=data,
            headers=headers,
            proxies=proxies,
            name=name,
            timeout=timeout
        )
