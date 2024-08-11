#from app.core.xml_parser_lite import process_data
from xml_parser import process_data
from models import model
from config import XML_PATH, CLASS_LABELS

def main():
    process_data(XML_PATH, model, CLASS_LABELS)

if __name__ == '__main__':
    main()