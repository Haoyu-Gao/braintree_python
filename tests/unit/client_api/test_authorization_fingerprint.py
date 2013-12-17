from tests.test_helper import *

class TestAuthorizationFingerprint(unittest.TestCase):
    def test_fingerprint_contains_required_data(self):
        fingerprint = AuthorizationFingerprint.generate()
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertTrue("merchant_id=%s" % Configuration.merchant_id in encoded_data)
        self.assertTrue("public_key=%s" % Configuration.public_key in encoded_data)
        self.assertTrue("created_at=" in encoded_data)

        base_url = "http://localhost:3000/merchants/%s" % Configuration.merchant_id
        self.assertTrue("base_url=%s" % base_url  in encoded_data)

    def test_fingerprint_optionally_contains_customer_id(self):
        fingerprint = AuthorizationFingerprint.generate({
            "customer_id": "1234"
        })
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertTrue("customer_id=1234" in encoded_data)

    def test_required_data_cannot_be_overridden(self):
        fingerprint = AuthorizationFingerprint.generate({
            "merchant_id": "1234"
        })
        signature, encoded_data = fingerprint.split("|")

        self.assertTrue(len(signature) > 1)
        self.assertFalse("merchant_id=1234" in encoded_data)

    def test_credit_card_options_require_customer_id(self):
        for option in ["verify_card", "make_default", "fail_on_duplicate_payment_method"]:
            try:
                fingerprint = AuthorizationFingerprint.generate({
                    option: True
                })
                self.assertTrue(False, "Should have raised an exception")
            except InvalidSignatureError, e:
                self.assertTrue(str(e).find(option))
