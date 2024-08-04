from app.core.models import model
from app.core.xml_parser import process_data
from config import XML_PATH

def main():
    process_data(XML_PATH, model)

if __name__ == '__main__':
    main()
