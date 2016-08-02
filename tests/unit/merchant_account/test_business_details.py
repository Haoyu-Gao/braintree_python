from tests.test_helper import *
from braintree.merchant_account.business_details import BusinessDetails

class TestBusinessDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = BusinessDetails({
            "dba_name": "Bar Suenami",
            "legal_name": "Suenami Restaurant Group",
            "tax_id": "123001234",
            "address": {
                "street_address": "123 First St",
                "region": "Las Vegas",
                "locality": "NV",
            }
        })

        regex = r"<BusinessDetails {dba_name: 'Bar Suenami', legal_name: 'Suenami Restaurant Group', tax_id: '123001234', address_details: <AddressDetails {street_address: '123 First St', locality: 'NV', region: 'Las Vegas'} at \w+>} at \w+>"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
