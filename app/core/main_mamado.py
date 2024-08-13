from xml_parser import process_data
from models import model
from app.config.paths import XML_PATH
from app.config.variables import  CLASS_LABELS

def main():
    process_data(XML_PATH, model, CLASS_LABELS)

if __name__ == '__main__':
    main()