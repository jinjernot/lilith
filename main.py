from app.core.xml_parser_lite import process_data
from app.config.paths import XML_PATH

def main():
    process_data(XML_PATH)

if __name__ == '__main__':
    main()  