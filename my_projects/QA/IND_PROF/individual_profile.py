"""
code to create Individual Profile class with random and fake python library
"""
import pprint
import random
from faker import Faker
import typing


class IndividualProfile:
    """
    A class to fake profile

    """

    def create(
            client,
            url: str,
            headers: typing.Dict[str, str],
            proxies: typing.Dict[str, str],
            name: str,
            timeout: int,
            config: typing.Dict[str, list],
            extended: bool = False
    ) -> dict:
        """
        Constructs all the necessary attributes for the IndividualProfile.

        ...
        Attributes
        ---------
        client <class 'object'>
            Instance of HttpSession that is created upon instantiation of Locust.
            The client supports cookies, and therefore keeps the session between HTTP requests.
        url: <class str>
            api-gateway for individual profiles
        headers: <class dict>
            Return property id
        proxies: <class dict>
            dict with proxies addresses
        name: <class str>
            Name shown in Locust
        timeout: <class int>
            Timeout response
        extended: <class bool>
            Is individual profile extended or not.
            Default False
        """

        fake = Faker(random.choice(config["FAKER_LANG"]))

        names = fake.name().split()
        address = fake.address().split()
        country_code = fake.current_country_code()
        lang_code = random.choice(config["lang"])
        address_code = random.choice(config["Address_Type_Code"])
        phone = fake.phone_number()
        mode_code_det = {"Phone": phone}
        mode_code = random.choice([key for key in mode_code_det.keys()])
        type_code = random.choice(config["append_str"]) + str(mode_code.upper())
        greeting = fake.sentence(nb_words=5)
        birthday = str(fake.date_object()).split("-")
        gender = random.choice(config["gender_code"])

        data = {
            "typeCode": "PIND",
            "details": {
                "firstName": names[0],
                "lastName": names[1],
            },
            "addresses": [
                {
                    "countryCode": country_code,
                    "isPrimary": "true",
                    "languageCode": lang_code,
                    "addressTypeCode": address_code,
                }
            ],
            "communicationChannels": [
                {
                    "typeCode": type_code,
                    "modeCode": mode_code,
                    "details": mode_code_det['Phone'],
                    "isPrimary": "true",
                }
            ],
            "propertyId": headers['AC-Property-ID']
        }
        if extended:
            data["details"].update({"preferredCommunicationLanguageCode": country_code,
                                    "greeting": greeting,
                                    "genderCode": gender,
                                    "birthdayAnniversaryDate": {
                                        "day": birthday[2],
                                        "month": birthday[1],
                                        "year": birthday[0],
                                    }})
            data["addresses"][0].update({"addressLine1": ' '.join(address[:-2]),
                                         "city": address[-1],
                                         "postalCode": address[-2],
                                         })

        req = client.post(
            url=url,
            json=data,
            headers=headers,
            proxies=proxies,
            name=name,
            timeout=timeout
        )

        return req.headers['Location'].split('/')[-1]




