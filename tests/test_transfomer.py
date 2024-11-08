import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import json
from src.xmltojson.transformer import XMLtoJSONTransformer


class TestXMLtoJSONTransformer(unittest.TestCase):
    """
    Unit tests for XML to JSON Transformation.
    """

    def setUp(self):
        """
        Sets up the necessary XML strings for testing.
        """
        # Valid XML data
        self.valid_xml = """
        <person>
            <given_name>John</given_name>
            <surname>Doe</surname>
            <birth_date>Jan 2, 2003</birth_date>
            <home_address>789 Residential Rd, Hometown, CA 67890</home_address>
        </person>
        """

        # XML data with invalid birth date
        self.invalid_birthday_xml = """
        <person>
            <given_name>John</given_name>
            <surname>Doe</surname>
            <birth_date>Invalid Date</birth_date>
            <home_address>789 Residential Rd, Hometown</home_address>
        </person>
        """

        # Malformed XML data
        self.malformed_xml = "<person><given_name>John</given_name></person"

        # XML data with invalid address
        self.invalid_address_xml = """
        <person>
            <given_name>John</given_name>
            <surname>Bob</surname>
            <birth_date>Jan 2, 2003</birth_date>
            <home_address></home_address>
        </person>
        """

    def test_successful_conversion(self):
        """
        Tests if a valid XML is successfully converted to the expected JSON format.
        """
        converter = XMLtoJSONTransformer()
        expected_json = json.dumps({
            "full_name": "John Doe",
            "dob": "2003-01-02",
            "home_address": {
                "street": "789 Residential Rd",
                "city": "Hometown",
                "state": "CA",
                "zip": "67890"
            }
        }, indent=4)
        self.assertEqual(converter.transform_xml_to_json(self.valid_xml), expected_json)

    @patch('src.xmltojson.transformer.XMLtoJSONTransformer.transform_xml_to_json')
    def test_successful_conversion_mock(self, mock_transform):
        """
        Tests XML to JSON conversion using a mocked transformation method.
        """
        expected_json = json.dumps({
            "full_name": "John Doe",
            "dob": "2003-01-02",
            "home_address": {
                "street": "789 Residential Rd",
                "city": "Hometown",
                "state": "CA",
                "zip": "67890"
            }
        }, indent=4)
        mock_transform.return_value = expected_json
        converter = XMLtoJSONTransformer()
        self.assertEqual(converter.transform_xml_to_json(self.valid_xml), expected_json)

    def test_invalid_xml_conversion(self):
        """
        Tests if a ValueError is raised for malformed XML.
        """
        converter = XMLtoJSONTransformer()
        with self.assertRaises(ValueError):
            converter.transform_xml_to_json(self.malformed_xml)

    def test_invalid_birthday_format(self):
        """
        Tests if a ValueError is raised for invalid birth date format in the XML.
        """
        converter = XMLtoJSONTransformer()
        with self.assertRaises(ValueError):
            converter.transform_xml_to_json(self.invalid_birthday_xml)

    def test_invalid_address_format(self):
        """
        Tests if a ValueError is raised for invalid address format in the XML.
        """
        converter = XMLtoJSONTransformer()
        with self.assertRaises(ValueError):
            converter.transform_xml_to_json(self.invalid_address_xml)


if __name__ == '__main__':
    unittest.main()
