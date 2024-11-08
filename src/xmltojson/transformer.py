# Used Jetbrains AI assistant in Pycharm for code assist, logging and doc generation

# transformer.py

"""
transformer.py

This module contains classes and methods to transform XML data into JSON format.
"""
# Use ElementTree module for XML parsing
import xml.etree.ElementTree as ET
import json
import logging
from datetime import datetime

# Set up logging for this module
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class XMLtoJSONTransformer:
    """
    A class to transform XML data to JSON format.
    """

    def __init__(self):
        """
        Initializes the XMLtoJSONTransformer with default settings.
        """
        pass

    def transform_xml_to_json(self, xml_input_data: str) -> str:
        """
        Transforms XML input data to a JSON string.

        Args:
            xml_input_data (str): A string containing XML data of a person.

        Returns:
            str: A JSON string representation of the input XML data.

        Raises:
            ValueError: If the XML data is invalid or cannot be processed.
        """
        logging.debug("Starting conversion from XML to JSON")

        # Parse XML input data
        try:
            root = ET.fromstring(xml_input_data)  # Parse the XML data
            logging.debug("XML data parsed successfully")
        except ET.ParseError as e:
            # Handle XML parsing errors
            logging.error(f"Failed to parse XML data: {e}")
            raise ValueError("Invalid XML data")

        try:
            # Extract data from XML
            given_name = root.find('given_name').text if root.find('given_name') is not None else 'Unknown'
            surname = root.find('surname').text if root.find('surname') is not None else 'Unknown'
            birth_date = root.find('birth_date').text if root.find('birth_date') is not None else 'Unknown'
            home_address = root.find('home_address').text if root.find('home_address') is not None else 'Unknown'

            logging.debug(
                f"Extracted data - Given Name: {given_name}, Surname: {surname}, Birth Date: {birth_date}, Home Address: {home_address}")

            # Clean and process extracted data
            given_name = given_name.strip()
            surname = surname.strip()
            birth_date = birth_date.strip()
            home_address = home_address.strip() if home_address is not None else ''

            # Transform birth date to ISO format if possible
            try:
                dob = datetime.strptime(birth_date, '%b %d, %Y').strftime('%Y-%m-%d')
                logging.debug(f"Parsed birth date successfully: {dob}")
            except ValueError:
                dob = 'Invalid Date Format'
                logging.warning("Invalid birth date format")

            # Split home address into components
            address_parts = home_address.split(', ')
            if len(address_parts) < 3:
                logging.error("Home address format is incorrect")
                raise ValueError("Home address format is incorrect")
            street = address_parts[0]
            city = address_parts[1]
            state_zip = address_parts[2].split(' ')
            if len(state_zip) < 2:
                logging.error("State and zip code format is incorrect")
                raise ValueError("State and zip code format is incorrect")
            state = state_zip[0]
            zip_code = state_zip[1]

            # Construct the JSON object
            return self._construct_json(given_name, surname, dob, street, city, state, zip_code)

        except Exception as e:
            logging.error(f"Error during conversion: {e}")
            raise

    def _construct_json(self, given_name, surname, dob, street, city, state, zip_code):
        person_dict = {
            "full_name": f"{given_name} {surname}",
            "dob": dob,
            "home_address": {
                "street": street,
                "city": city,
                "state": state,
                "zip": zip_code
            }
        }
        logging.debug("JSON Conversion successful")
        return json.dumps(person_dict, indent=4)


if __name__ == '__main__':
    # Example usage of the transformer
    xml_data = """
    <person>
        <given_name>John</given_name>
        <surname>Doe</surname>
        <birth_date>Jan 2, 2003</birth_date>
        <home_address>789 Residential Rd, Hometown, CA 67890</home_address>
    </person>
    """

    try:
        converter = XMLtoJSONTransformer()
        json_data = converter.transform_xml_to_json(xml_data)
        print(json_data)
    except ValueError as e:
        logging.error(f"ValueError encountered: {e}")
    except Exception as e:
        logging.error(f"Unexpected error encountered: {e}")
